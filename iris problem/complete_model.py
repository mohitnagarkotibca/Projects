from sklearn import datasets    
import numpy as np         
import pandas as pd
import matplotlib.pyplot as plt  
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
iris = datasets.load_iris()      
data = iris.data                 
target = iris.target             

shape = data.shape             


data = np.array(data).reshape(shape[0],shape[1])
target = np.array(target).reshape(shape[0],1)

#print('dataset has {} examples each containing {} features'.format(data.shape[0],data.shape[1]))

#print('Number of target values: ', target.shape[0])

#checking wether the dataset is balanced or not
#display(pd.Series(np.squeeze(target)).value_counts().plot(kind='bar',title= 'Data distribution of target values'))


# Defining parameters and Hyperparameters
# number of of hidden layers: 1
# number of intital units in hidden layer: 8
# number of output units: 3
# number of input units: 4

# Dimesions of Parameters

# Shape of W0 (Wxh) = (4,8)
# Shape of layer1_biasess (Bh) = (8,1)
# Shape of W1 (Why) = (8,3)
# Shape of layer2_biasess (By) = (3,1) 

class Iris_solve:
    num_classes = len(np.unique(target))

    # number of features
    input_units  = 4   

    # number of units in hidden layer
    hidden_units = 8  

    #number of outputs in last layer
    output_units = 3   

    #define hyper-parameters
    learning_rate = 0.03

    #regularization parameter in case overfitting
    beta = 0.00001

    #num of iterations
    iters = 4001

    def initialize_parameters(self,train_dataset):
        input_units= train_dataset.shape[1]
        mean = 0       
        std = 0.03      
        
        W0 = np.random.normal(mean,std,(input_units,self.hidden_units))          
        layer1_biases = np.ones((self.hidden_units,1))                                       
        W1 = np.random.normal(mean,std,(self.hidden_units,self.output_units))
        layer2_biases = np.ones((self.output_units,1))
        
        parameters = dict()
        parameters['W0'] = W0
        parameters['layer1_biases'] = layer1_biases
        parameters['W1'] = W1
        parameters['layer2_biases'] = layer2_biases
        
        return parameters

    def sigmoid(self,X):
        return 1/(1+np.exp((-1)*X))

    def softmax(self,X):
        exp_X = np.exp(X)
        exp_X_sum = np.sum(exp_X,axis=1).reshape(-1,1)
        exp_X = (exp_X/exp_X_sum)
        return exp_X

    def forward_propagation(self,train_dataset,parameters):
        cache = dict()          
        m = len(train_dataset)    
        W0 = parameters['W0']
        layer1_biases = parameters['layer1_biases']
        W1 = parameters['W1']
        layer2_biases = parameters['layer2_biases']
        #forward prop
        Z1 = np.matmul(train_dataset,W0) + layer1_biases.T
        A1 = np.array(self.sigmoid(Z1)).reshape(m,self.hidden_units)
        A2 = np.array(np.matmul(A1,W1) + layer2_biases.T).reshape(m,self.output_units)
        output = np.array(self.softmax(A2)).reshape(m,self.num_classes)
        #fill in the cache
        cache['output'] = output
        cache['A1'] = A1

        return cache,output
        
    #backward propagation
    def backward_propagation(self,train_dataset,train_labels,parameters,cache):
        derivatives = dict()         #to store the derivatives
        #get stuff from cache
        output = cache['output']
        A1 = cache['A1']
        #get parameters
        W0 = parameters['W0']
        W1 = parameters['W1']

        #calculate errors
        error_output = output - train_labels
        error_A1 = np.matmul(error_output,W1.T)
        error_A1 = np.multiply(error_A1,A1)
        error_A1 = np.multiply(error_A1,1-A1)


        #calculate partial derivatives
        partial_derivatives2 = np.matmul(A1.T,error_output)/len(train_dataset)
        partial_derivatives1 = np.matmul(train_dataset.T,error_A1)/len(train_dataset)
        #store the derivatives
        derivatives['partial_derivatives1'] = partial_derivatives1
        derivatives['partial_derivatives2'] = partial_derivatives2

        return derivatives


    #update the parameters
    def update_parameters(self,derivatives,parameters):
        #get the parameters
        W0 = parameters['W0']
        W1 = parameters['W1']

        #get the derivatives
        partial_derivatives1 = derivatives['partial_derivatives1']
        partial_derivatives2 = derivatives['partial_derivatives2']

        #update the derivatives
        W0 -= (self.learning_rate*(partial_derivatives1 + self.beta*W0))
        W1 -= (self.learning_rate*(partial_derivatives2 + self.beta*W1))

        #update the dict
        parameters['W0'] = W0
        parameters['W1'] = W1

        return parameters

    #calculate the loss and accuracy
    def cal_loss_accuray(self,train_dataset,train_labels,predictions,parameters):
        #get the parameters
        W0 = parameters['W0']
        W1 = parameters['W1']

        #cal loss and accuracy
        loss = -1*np.sum(np.multiply(np.log(predictions),train_labels) + np.multiply(np.log(1-predictions),(1-train_labels)))/len(W0) + np.sum(W0**2)*self.beta/len(train_labels) + np.sum(W1**2)*self.beta/len(train_labels)
        accuracy = np.sum(np.argmax(train_labels,axis=1)==np.argmax(predictions,axis=1))
        
        accuracy /= len(train_dataset)
        accuracy = np.sum(np.argmax(train_labels,axis=1)==np.argmax(predictions,axis=1))
        accuracy /= len(train_dataset)
        

        return loss,accuracy
        
    def train(self,train_dataset,train_labels,iters=2):
        LOSS = []
        Acc=[]
        global W0
        global layer1_biases
        global W1
        global layer2_biases


        parameters = self.initialize_parameters(train_dataset)
        W0 = parameters['W0']
        layer1_biases = parameters['layer1_biases']
        W1 = parameters['W1']
        layer2_biases = parameters['layer2_biases']

        final_output = []

        for j in range(iters):

            cache,output = self.forward_propagation(train_dataset,parameters)

            derivatives = self.backward_propagation(train_dataset,train_labels,parameters,cache)
    

            loss,accuracy = self.cal_loss_accuray(train_dataset,train_labels,output,parameters)

            parameters = self.update_parameters(derivatives,parameters)
            
            LOSS.append(loss)
            Acc.append(accuracy)
            final_output = output
            
#             if(j%1000==0):
#                 print('epoch :', j ,' W0 mean:',np.round(parameters['W0'].mean(),5),' W1 mean:',np.round(parameters['W1'].mean(),7))

#                 print('Iteration :',j, 'Accuracy :',accuracy*100, 'with loss :',loss)
            fit_p= {'W1':W0,'B1':layer1_biases}
        print('Accuracy achieved :',np.round(accuracy*100,2), '% with loss :',np.round(loss,4),' %')        
        return Acc,LOSS,final_output,parameters

    def make_dataset(self,data,target):    
        z = list(zip(data,target))
        np.random.shuffle(z)
        data,target = zip(*z)
        train_dataset = np.array(data).reshape(-1,4)
        train_labels = np.zeros([train_dataset.shape[0],self.num_classes])
        #one-hot encoding
        for i,label in enumerate(target):
            train_labels[i,label] = 1

        for i in range(self.input_units):    
            mean = train_dataset[:,i].mean()
            std = train_dataset[:,i].std()
            train_dataset[:,i] = (train_dataset[:,i]-mean)/std
        return train_dataset, train_labels
        
    def make_split(self,train_dataset,train_labels):
        train_x,val_x,train_y1,val_y1= train_test_split(train_dataset, train_labels)
        train_y= np.array([z for z in train_y1])
        val_y= np.array([v for v in val_y1])
        return train_x,val_x,train_y,val_y

    def predict(self,train_dataset,parameters):
        cache,output = self.forward_propagation(train_dataset,parameters)
#[list(x).index(max(x)) for x in output]
        return output

    def draw_conclusion(self,actual,Ot):    
        cm = confusion_matrix(actual, Ot)
        
        FP = cm.sum(axis=0) - np.diag(cm)
        FN = cm.sum(axis=1) - np.diag(cm)
        TP = np.diag(cm)
        TN = cm.sum() - (FP + FN + TP)
        print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in cm]))
        #confusionmatrix = np.matrix(cm)
        FP = cm.sum(axis=0) - np.diag(cm)
        FN = cm.sum(axis=1) - np.diag(cm)
        TP = np.diag(cm)
        TN = cm.sum() - (FP + FN + TP)
#         print('False Positives: {}'.format(FP))
#         print('False Negetives: {}'.format(FN))
#         print('True Positives: {}'.format(TP))
#         print('True Negetives: {}'.format(TN))
#         TPR = TP/(TP+FN)
#         print('Sensitivity: {}'.format(TPR))
#         TNR = TN/(TN+FP)
#         print('Specificity: {}'.format(TNR))
        Precision = TP/(TP+FP)
        print('Precision: {}'.format(Precision))
        Recall = TP/(TP+FN)
        print('Recall: {}'.format(Recall))
        Acc = (TP+TN)/(TP+TN+FP+FN)
        print('Áccuracy: {}'.format(Acc))
        Fscore = 2*(Precision*Recall)/(Precision+Recall)
        print('FScore: {}'.format(Fscore))



    def fit(self,train_x,train_y):
        acc,LOSS,output,parameters= self.train(train_x,train_y,iters=4001)
        dataset={}
        dataset['train_x']= train_x
        dataset['train_y']= train_y
        dataset['val_x']= val_x
        dataset['val_y']= val_y
        dataset['training_output']= output
        
        return acc,LOSS,parameters,dataset
#     def function_plot(train_y,,)

IS= Iris_solve()
train_dataset,train_labels= IS.make_dataset(data,target)
train_x,val_x,train_y,val_y= IS.make_split(train_dataset,train_labels)

#fit
accuracy, LOSS, parameters,dataset= IS.fit(train_x,train_y)

#train vs test loss
train_answer= IS.predict(train_x,parameters)
train_loss, train_accuracy= IS.cal_loss_accuray(train_x,train_y,train_answer,parameters)

val_answer= IS.predict(val_x,parameters)
val_loss, val_accuracy= IS.cal_loss_accuray(val_x,val_y,val_answer,parameters)
print()
print()
print()
print('Train loss :', train_loss,'\nTest loss :', val_loss)
print()
print()
print()
print('Train accuracy :', train_accuracy*100,'\nTest acccuracy :', val_accuracy)


train_y_1d= [list(x).index(max(x)) for x in train_y]
train_answer_1d= [list(x).index(max(x)) for x in train_answer]
print(classification_report(train_y_1d,train_answer_1d,target_names=['setosa','versicolor','virginica']))
# IS.draw_conclusion(train_y_1d,train_answer_1d)

plt.plot(LOSS)
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title(' Loss function vs epochs')