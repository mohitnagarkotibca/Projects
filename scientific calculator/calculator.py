import numpy as np
from tkinter import *
import math

root= Tk()
root.configure(bg='#39434d',bd=10)
root.title('casio')

text_displayed = ""
input_provided = StringVar()

class functions:
    def button_click(char):
        global text_displayed
        text_displayed += str(char)
        input_provided.set(text_displayed)

    def square_root():
        global text_displayed
        if int(text_displayed)>=0:
            temp = str(eval(text_displayed+'**(1/2)'))
            text_displayed = temp
        else:
            temp = "ERROR"
        input_provided.set(temp)

    def third_root():
        global text_displayed
        if int(text_displayed)>=0:
            temp = str(eval(text_displayed+'**(1/3)'))
            text_displayed = temp
        else:
            temp = "ERROR"
        input_provided.set(temp)

    def button_clear_all():
        global text_displayed
        text_displayed = ""
        input_provided.set("")

    def button_delete():
        global text_displayed
        text = text_displayed[:-1]
        text_displayed = text
        input_provided.set(text)

    def factorial(self,n):
        if n==0 or n==1:
            return 1
        else:
            return n*self.factorial(n-1)

    def fact_func(self):
        global text_displayed
        result = str(self.factorial(int(text_displayed)))
        text_displayed = result
        input_provided.set(result)

    def trig_sin():
        global text_displayed
        result = str(math.sin(math.radians(int(text_displayed))))
        text_displayed = result
        input_provided.set(result)

    def trig_cos():
        global text_displayed
        result = str(math.cos(math.radians(int(text_displayed))))
        text_displayed = result
        input_provided.set(result)

    def trig_tan():
        global text_displayed
        result = str(math.tan(math.radians(int(text_displayed))))
        text_displayed = result
        input_provided.set(result)

    def trig_cot():
        global text_displayed
        result = str(1/math.tan(math.radians(int(text_displayed))))
        text_displayed = result
        input_provided.set(result)


    def sign_change():
        global text_displayed
        if text_displayed[0]=='-':
            temp = text_displayed[1:]
        else:
            temp = '-'+text_displayed
        text_displayed = temp
        input_provided.set(temp)    

    def percent():
        global text_displayed
        temp = str(eval(text_displayed+'/100'))
        text_displayed = temp
        input_provided.set(temp)


    def button_equal():
        global text_displayed
        temp_op = str(eval(text_displayed))
        input_provided.set(temp_op)
        text_displayed = temp_op
    



text_display = Entry(root, font=('Candara', 20, 'bold'), textvariable=input_provided,
                     bd=5, insertwidth = 5, bg='#BBB', justify='left').grid(row=0,columnspan=5, padx = 10, pady = 15)

button_params = {'bd':5, 'fg':'#BBB', 'bg':'#3C3636', 'font':('Candara', 10, 'bold')}
button_params_main = {'bd':5, 'fg':'#000', 'bg':'#BBB', 'font':('Candara', 10, 'bold')}
square_root = Button(root, button_params, text='\u00B2\u221A',
                     command=functions.square_root).grid(row=1, column=0, sticky="nsew")

third_root = Button(root, button_params, text='\u00B3\u221A',
                    command=functions.third_root).grid(row=1, column=1, sticky="nsew")
nth_root = Button(root, button_params, text='\u221A',
                  command=lambda:functions.button_click('**(1/')).grid(row=1, column=2, sticky="nsew")

log_base10 = Button(root, button_params, text='log\u2081\u2080', font=('Candara', 10, 'bold'),
                   command=lambda:functions.button_click('log(')).grid(row=1, column=3, sticky="nsew")

log_basee = Button(root, button_params, text='ln',
                   command=lambda:functions.button_click('ln(')).grid(row=1, column=4, sticky="nsew")

abs_value= Button(root,button_params,text='abs',
command= lambda: functions.button_click('abs')
).grid(row=2,column=0,sticky='nsew')


button_7 = Button(root, button_params_main, text='7',
                  command=lambda:functions.button_click('7')).grid(row=6, column=0, sticky="nsew")
button_8 = Button(root, button_params_main, text='8',
                  command=lambda:functions.button_click('8')).grid(row=6, column=1, sticky="nsew")
button_9 = Button(root, button_params_main, text='9',
                  command=lambda:functions.button_click('9')).grid(row=6, column=2, sticky="nsew")

modulo = Button(root, button_params, text='mod',
                command=lambda:functions.button_click('%')).grid(row=2, column=1, sticky="nsew")

int_div = Button(root, button_params, text='div',
                 command=lambda:functions.button_click('//')).grid(row=2, column=2, sticky="nsew")
f= functions()
factorial_button = Button(root, button_params, text='x!',
                   command=f.fact_func).grid(row=2, column=3, sticky="nsew")

eulers_num = Button(root, button_params, text='e',
                    command=lambda:functions.button_click(str(math.exp(1)))).grid(row=2, column=4, sticky="nsew")


sine = Button(root, button_params, text='sin',
             command=functions.trig_sin).grid(row=3, column=0, sticky="nsew")

cosine = Button(root, button_params, text='cos',
             command=functions.trig_cos).grid(row=3, column=1, sticky="nsew")

tangent = Button(root, button_params, text='tan',
             command=functions.trig_tan).grid(row=3, column=2, sticky="nsew")

cotangent = Button(root, button_params, text='cot',
             command=functions.trig_cot).grid(row=3, column=3, sticky="nsew")

pi_num = Button(root, button_params, text='π',
                command=lambda:functions.button_click(str(math.pi))).grid(row=3, column=4, sticky="nsew")

second_power = Button(root, button_params, text='x\u00B2',
             command=lambda:functions.button_click('**2')).grid(row=4, column=0, sticky="nsew")

third_power = Button(root, button_params, text='x\u00B3',
             command=lambda:functions.button_click('**3')).grid(row=4, column=1, sticky="nsew")

nth_power = Button(root, button_params, text='x^n',
             command=lambda:functions.button_click('**')).grid(row=4, column=2, sticky="nsew")

inv_power = Button(root, button_params, text='x\u207b\xb9',
             command=lambda:functions.button_click('**(-1)')).grid(row=4, column=3, sticky="nsew")

tens_powers = Button(root, button_params, text='x^10', font=('Candara', 10, 'bold'),
                     command=lambda:functions.button_click('10**')).grid(row=4, column=4, sticky="nsew")


left_par = Button(root, button_params, text='(',
                  command=lambda:functions.button_click('(')).grid(row=5, column=0, sticky="nsew")

right_par = Button(root, button_params, text=')',
                   command=lambda:functions.button_click(')')).grid(row=5, column=1, sticky="nsew")   

signs = Button(root, button_params, text='\u00B1',
               command=functions.sign_change).grid(row=5, column=2, sticky="nsew")

percentage = Button(root, button_params, text='%',
               command=functions.percent).grid(row=5, column=3, sticky="nsew")

ex = Button(root, button_params, text='e^x',
               command=lambda:functions.button_click('e(')).grid(row=5, column=4, sticky="nsew")


delete_one = Button(root, bd=5, fg='#000', font=('Candara', 10, 'bold'),
              text='DEL', command=functions.button_delete, bg='#db701f').grid(row=6, column=3, sticky="nsew")
delete_all = Button(root, bd=5, fg='#000', font=('Candara', 10, 'bold'),
              text='AC', command=functions.button_clear_all, bg='#db701f').grid(row=6, column=4, sticky="nsew")

button_4 = Button(root, button_params_main, text='4',
                  command=lambda:functions.button_click('4')).grid(row=7, column=0, sticky="nsew")
button_5 = Button(root, button_params_main, text='5',
                  command=lambda:functions.button_click('5')).grid(row=7, column=1, sticky="nsew")
button_6 = Button(root, button_params_main, text='6',
                  command=lambda:functions.button_click('6')).grid(row=7, column=2, sticky="nsew")
mul = Button(root, button_params_main, text='*',
             command=lambda:functions.button_click('*')).grid(row=7, column=4, sticky="nsew")
div = Button(root, button_params_main, text='/',
             command=lambda:functions.button_click('/')).grid(row=7, column=3, sticky="nsew")

button_1 = Button(root, button_params_main, text='1',
                  command=lambda:functions.button_click('1')).grid(row=8, column=0, sticky="nsew")
button_2 = Button(root, button_params_main, text='2',
                  command=lambda:functions.button_click('2')).grid(row=8, column=1, sticky="nsew")
button_3 = Button(root, button_params_main, text='3',
                  command=lambda:functions.button_click('3')).grid(row=8, column=2, sticky="nsew")
add = Button(root, button_params_main, text='+',
             command=lambda:functions.button_click('+')).grid(row=8, column=4, sticky="nsew")
sub = Button(root, button_params_main, text='-',
             command=lambda:functions.button_click('-')).grid(row=8, column=3, sticky="nsew")

button_0 = Button(root, button_params_main, text='0',
                  command=lambda:functions.button_click('0')).grid(row=9, column=0, sticky="nsew")
point = Button(root, button_params_main, text='.',
               command=lambda:functions.button_click('.')).grid(row=9, column=2, sticky="nsew")
exp = Button(root, button_params_main, text='EXP', font=('Candara', 10, 'bold'),
             command=lambda:functions.button_click(E)).grid(row=9, column=1, sticky="nsew")
equal = Button(root, button_params_main, text='=',
               command=functions.button_equal).grid(row=9, columnspan=2, column=3, sticky="nsew")

root.mainloop()
