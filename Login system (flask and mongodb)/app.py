from flask import Flask,render_template,request
import pymongo
class Routes:
    def __init__(self):
        self.fullname=None
        self.email= None
        self.password= None
        self.app=None
        client = pymongo.MongoClient()
        self.db=client['db_1']
    def create_app(self):
        app= Flask(__name__)
        self.app=app
    def login(self):    
        @self.app.route('/',methods=['GET','POST'])
        def login():
            if request.method=='GET':    
                return render_template('login.html')
            else:
                email= request.form.get('email')
                password= request.form.get('password')
                print(email)
                print(password)
                x= self.db.login.find({'email':str(email),'password':str(password)})
                print(x.retrieved)
                if x.retrieved == 1:    
                    return "submission done !"
                else:
                    return 'error !'
    def register(self):
        @self.app.route('/register',methods=['GET','POST'])
        def register():
            if request.method=='GET':
                print('inside get')
                return render_template('register.html')
            if request.method=='POST':
                print('inside post')
                self.fullname= request.form.get('fullname')
                self.email= request.form.get('email')
                self.password= request.form.get('password')
                self.upload_to_mongo()
                return render_template('register.html')      
    def upload_to_mongo(self):
        name= self.fullname
        email= self.email
        password= self.password
        x= self.db.login.find({
            'full_name':name,
            'email':email
        })
        if x.retrieved ==1:
            print('User already exits')
        self.db.login.insert_one(
            {
                'full_name':name,
                'email':email,
                'password':password
            }
        )
    def Run(self):
        self.create_app()
        self.login()
        self.register()
        self.app.run()


r= Routes()
r.Run()