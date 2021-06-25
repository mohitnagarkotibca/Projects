
from tkinter import *
from PIL import ImageTk,Image
root= Tk()
root.geometry("390x290+700+200")


frame= LabelFrame(root, text='my frame')
frame.pack(fill="both",expand=True,padx=10,pady=10)

class emotions:
    mood= None
    def after_click(self,x):
        
        if x=='b1':
            mood='Happy'
            self.b1.config(background='#eaf320')
            self.b2.config(background='SystemButtonFace')
            self.b3.config(background='SystemButtonFace')
            self.b4.config(background='SystemButtonFace')
            self.b5.config(background='SystemButtonFace')

        elif x=='b2':
            mood='Sad'
            self.b2.config(background='#676f59')
            self.b1.config(background='SystemButtonFace')
            self.b3.config(background='SystemButtonFace')
            self.b4.config(background='SystemButtonFace')
            self.b5.config(background='SystemButtonFace')


        elif x=='b3':
            mood='meh'
            self.b3.config(background='#6320b8')
            self.b2.config(background='SystemButtonFace')
            self.b1.config(background='SystemButtonFace')
            self.b4.config(background='SystemButtonFace')
            self.b5.config(background='SystemButtonFace')


        elif x=='b4':
            mood='Sleepy'
            self.b4.config(background='#31d8a8')
            self.b2.config(background='SystemButtonFace')
            self.b3.config(background='SystemButtonFace')
            self.b1.config(background='SystemButtonFace')
            self.b5.config(background='SystemButtonFace')

        elif x=='b5':
            mood='ill'
            self.b5.config(background='#23c009')
            self.b2.config(background='SystemButtonFace')
            self.b3.config(background='SystemButtonFace')
            self.b1.config(background='SystemButtonFace')
            self.b4.config(background='SystemButtonFace')
        self.mood= mood

    def load_images(self):    
        self.happy= ImageTk.PhotoImage(Image.open("emoticon/smile.png").resize((30,30)))
        self.sad= ImageTk.PhotoImage(Image.open("emoticon/sad.png").resize((30,30)))
        self.meh= ImageTk.PhotoImage(Image.open("emoticon/meh.png").resize((30,30)))
        self.yawn= ImageTk.PhotoImage(Image.open("emoticon/yawn.png").resize((30,30)))
        self.ill= ImageTk.PhotoImage(Image.open("emoticon/ill.png").resize((30,30)))

    def load_buttons(self):    
        def on_enter(t):
            if t == 'happy':    
                self.l1.config(text='happy')
            if t == 'sad':    
                self.l2.config(text='sad')
            if t == 'meh':    
                self.l3.config(text='meh')
            if t == 'yawn':    
                self.l4.config(text='yawn')
            if t == 'ill':    
                self.l5.config(text='ill')

        def on_leave(a):
            self.l1.configure(text="")
            self.l2.configure(text="")
            self.l3.configure(text="")
            self.l4.configure(text="")
            self.l5.configure(text="")
            
        self.b1 = Button(frame,image= self.happy,command=lambda:self.after_click('b1'))
        self.b1.grid(row=2,column=1)
        self.b1.bind("<Enter>",lambda event ,t='happy':on_enter(t))
        self.b1.bind("<Leave>", on_leave)

        self.b2 = Button(frame,image= self.sad,command=lambda:self.after_click('b2'))
        self.b2.grid(row=2,column=2)
        self.b2.bind("<Enter>",lambda event ,t='sad':on_enter(t))
        self.b2.bind("<Leave>", on_leave)

        self.b3 = Button(frame,image= self.meh,command=lambda:self.after_click('b3'))
        self.b3.grid(row=2,column=3)
        self.b3.bind("<Enter>",lambda event ,t='meh':on_enter(t))
        self.b3.bind("<Leave>", on_leave)

        self.b4 = Button(frame,image= self.yawn,command=lambda:self.after_click('b4'))
        self.b4.grid(row=2,column=4)
        self.b4.bind("<Enter>",lambda event ,t='yawn':on_enter(t))
        self.b4.bind("<Leave>", on_leave)
        
        self.b5 = Button(frame,image= self.ill,command=lambda:self.after_click('b5'))
        self.b5.grid(row=2,column=5)
        self.b5.bind("<Enter>",lambda event ,t='ill':on_enter(t))
        self.b5.bind("<Leave>", on_leave)

        self.l1= Label(frame,text='')
        self.l1.grid(row=3,column=1)

        self.l2= Label(frame,text='')
        self.l2.grid(row=3,column=2)

        self.l3= Label(frame,text='')
        self.l3.grid(row=3,column=3)

        self.l4= Label(frame,text='')
        self.l4.grid(row=3,column=4)

        self.l5= Label(frame,text='')
        self.l5.grid(row=3,column=5)

        def retreat(self):
            print('your mood is : ',self.mood)
            root.quit()
            
        main_button= Button(frame, text= 'submit',command=lambda:retreat(self))
        main_button.grid(row=4,column=5)

    def run(self):
        self.load_images()
        self.load_buttons()

E= emotions()
E.run()
root.mainloop()
print(E.mood)
