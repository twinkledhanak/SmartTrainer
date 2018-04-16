import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
import sys
import os
from tkinter import ttk
import threading
from tkinter import *


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack( side="right",fill="both", expand=True) #side="top",
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(50, weight=1) # instead of weight = 1

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree , PageFour , PageFive ,ProgressPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")# nsew
            frame.configure(background="RoyalBlue1")
            #frame.place(relx=0.5, rely=0.5, anchor=CENTER)
            

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
   

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Smart-Trainer", font=("Arial Bold", 30))
        label.grid(column=500,row=10)
        label.configure(background="RoyalBlue1")

        #self.grid_rowconfigure(1, weight=1)
        #self.grid_columnconfigure(1, weight=1)

        lbl = tk.Label(self, text="A virtual trainer for physical exercises" , font=("Arial Bold", 15)) # to set font properties
        lbl.grid(column=500, row=100) # to position
        lbl.configure(background="RoyalBlue1")

        lbl = tk.Label(self, text="Username" , font=("Arial Bold", 10) , padx = 5, pady = 5) # to set font properties
        lbl.grid(column=500, row=280) # to position
        lbl.configure(background="RoyalBlue1")

        txt1 = tk.Entry(self, width=30)
        txt1.grid(column=500, row=282)
        txt1.focus()

        lbl = tk.Label(self, text="Password" , font=("Arial Bold", 10)) # to set font properties
        lbl.grid(column=500, row=320) # to position
        lbl.configure(background="RoyalBlue1")

        txt2 = tk.Entry(self, width=30)
        txt2.grid(column=500, row=322)
        txt2.focus()

        Username = tk.StringVar()
        Username = txt1.get() + txt2.get()

        button1 = tk.Button(self, text="Login",
                           command=lambda: controller.show_frame("PageOne"))
        button1.grid(column = 500,row = 350)
        button1.configure(background="white")        
        #button2 = tk.Button(self, text="Go to Page Two",
          #                  command=lambda: controller.show_frame("PageTwo"))
        #button1.pack()
        #button2.pack()

        #window = Tk()
     
        #window.title("Welcome to Smart-Trainer!")
        #window.geometry('700x400') # initial window size

       

# for user input details
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Welcome!", font=controller.title_font)
        label.grid(column=550, row=80)
        label.configure(background="RoyalBlue1")

        label = tk.Label(self, text="Please fill your details :", font=controller.title_font)
        label.grid(column=550, row=100)
        label.configure(background="RoyalBlue1")


        lbl = tk.Label(self, text="Height (in cms)" , font=("Arial Bold", 10) , padx = 5, pady = 5) # to set font properties
        lbl.grid(column=550, row=280) # to position
        lbl.configure(background="RoyalBlue1")
       
        height = tk.Entry(self, width=30)
        height.grid(column=550, row=282)
        height.focus()

        lbl = tk.Label(self, text="Weight (in kgs)" , font=("Arial Bold", 10) , padx = 5, pady = 5) # to set font properties
        lbl.grid(column=550, row=290) # to position
        lbl.configure(background="RoyalBlue1")
       
        weight = tk.Entry(self, width=30)
        weight.grid(column=550, row=292)
        weight.focus()

        # BMI IS TO BE CALCULATED IN BACKGROUND

        diabetes = IntVar()
        hypertension = IntVar()
        smoker = IntVar()
        exsmoker = IntVar()
        obesity = IntVar()
        thyroid = IntVar()
        chestpain = IntVar()
        physicalactivity = IntVar()
        h = IntVar()
        w = IntVar()
        h2 = IntVar()
        bmi = IntVar()
                

        lbl = tk.Label(self, text="Do you have Diabetes?" , font=("Arial Bold", 10) , padx = 5, pady = 5) # to set font properties
        lbl.grid(column=550, row=320) # to position
        lbl.configure(background="RoyalBlue1")
        rad1 = Radiobutton(self,text='Yes', value=1 , variable=diabetes)
        rad1.grid(column=600,row = 320)
        rad1.configure(background="RoyalBlue1")
        rad2 = Radiobutton(self,text='No', value=2 ,variable=diabetes)
        rad2.grid(column=700,row = 320)
        rad2.configure(background="RoyalBlue1")
        rad2.place()

            

        lbl = tk.Label(self, text="Do you have HyperTension?" , font=("Arial Bold", 10) , padx = 5, pady = 5) # to set font properties
        lbl.grid(column=550, row=410) # to position
        lbl.configure(background="RoyalBlue1")
        rad3 = Radiobutton(self,text='Yes', value=3 ,variable=hypertension)
        rad3.grid(column=600,row = 410)
        rad3.configure(background="RoyalBlue1")
        rad4 = Radiobutton(self,text='No', value=4 , variable=hypertension)
        rad4.grid(column=700,row = 410)
        rad4.configure(background="RoyalBlue1")

        lbl = tk.Label(self, text="Are you currently a smoker?" , font=("Arial Bold", 10) , padx = 5, pady = 5) # to set font properties
        lbl.grid(column=550, row=510) # to position
        lbl.configure(background="RoyalBlue1")
        rad5 = Radiobutton(self,text='Yes', value=5 ,variable=smoker)
        rad5.grid(column=600,row = 510)
        rad5.configure(background="RoyalBlue1")
        rad6 = Radiobutton(self,text='No', value=6 , variable=smoker)
        rad6.grid(column=700,row = 510)
        rad6.configure(background="RoyalBlue1")

        lbl = tk.Label(self, text="Are you an ex-smoker?" , font=("Arial Bold", 10) , padx = 5, pady = 5) # to set font properties
        lbl.grid(column=550, row=610) # to position
        lbl.configure(background="RoyalBlue1")
        rad7 = Radiobutton(self,text='Yes', value=7, variable=exsmoker)
        rad7.grid(column=600,row = 610)
        rad7.configure(background="RoyalBlue1")
        rad8 = Radiobutton(self,text='No', value=8, variable=exsmoker)
        rad8.grid(column=700,row = 610)
        rad8.configure(background="RoyalBlue1")

        lbl = tk.Label(self, text="Do you have Obesity?" , font=("Arial Bold", 10) , padx = 5, pady = 5) # to set font properties
        lbl.grid(column=550, row=710) # to position
        lbl.configure(background="RoyalBlue1")
        rad9 = Radiobutton(self,text='Yes', value=9, variable=obesity)
        rad9.grid(column=600,row = 710)
        rad9.configure(background="RoyalBlue1")
        rad10 = Radiobutton(self,text='No', value=10, variable=obesity)
        rad10.grid(column=700,row = 710)
        rad10.configure(background="RoyalBlue1")

        lbl = tk.Label(self, text="Do you have Thyroid?" , font=("Arial Bold", 10) , padx = 5, pady = 5) # to set font properties
        lbl.grid(column=550, row=810) # to position
        lbl.configure(background="RoyalBlue1")
        rad11 = Radiobutton(self,text='Yes', value=11, variable=thyroid)
        rad11.grid(column=600,row = 810)
        rad11.configure(background="RoyalBlue1")
        rad12 = Radiobutton(self,text='No', value=12, variable=thyroid)
        rad12.grid(column=700,row = 810)
        rad12.configure(background="RoyalBlue1")

        lbl = tk.Label(self, text="Do you have Chest pain?" , font=("Arial Bold", 10) , padx = 5, pady = 5) # to set font properties
        lbl.grid(column=550, row=910) # to position
        lbl.configure(background="RoyalBlue1")
        rad13 = Radiobutton(self,text='Yes', value=13, variable=chestpain)
        rad13.grid(column=600,row = 910)
        rad13.configure(background="RoyalBlue1")
        rad14 = Radiobutton(self,text='No', value=14, variable=chestpain)
        rad14.grid(column=700,row = 910)
        rad14.configure(background="RoyalBlue1")

        lbl = tk.Label(self, text="Do you perform any physical activity?" , font=("Arial Bold", 10) , padx = 5, pady = 5) # to set font properties
        lbl.grid(column=550, row=1010) # to position
        lbl.configure(background="RoyalBlue1")
        rad15 = Radiobutton(self,text='Yes', value=15 , variable=physicalactivity)
        rad15.grid(column=600,row = 1010)
        rad15.configure(background="RoyalBlue1")
        rad16 = Radiobutton(self,text='No', value=16, variable=physicalactivity)
        rad16.grid(column=700,row = 1010)
        rad16.configure(background="RoyalBlue1")


        lbl = tk.Label(self, text="Daily exercise time (in min)" , font=("Arial Bold", 10) , padx = 5, pady = 5) # to set font properties
        lbl.grid(column=550, row=1210) # to position
        lbl.configure(background="RoyalBlue1")
       
        exercise = tk.Entry(self, width=30)
        exercise.grid(column=550, row=1212)
        exercise.focus()

        def submitdetails():
            # get details for height and weight to calculate bmi 
            print(height.get())
            print(weight.get())
            print(exercise.get())   

            h = int(height.get())
            w = int(weight.get())
            h = (h / 100)
            h2 = h * h
            bmi = (w / h2)
            print(bmi)

            print(diabetes.get()) 
            print(hypertension.get())
            print(smoker.get())
            print(exsmoker.get())
            print(obesity.get())
            print(thyroid.get())
            print(chestpain.get())
            print(physicalactivity.get()) 

        button2 = tk.Button(self, text="Submit Details",
                           command=submitdetails)
        button2.grid(column = 550, row =1280)
        button2.configure(background="white") 
           
        
        button2 = tk.Button(self, text="Done",
                           command=lambda: controller.show_frame("PageTwo"))
        button2.grid(column = 550, row = 1310)
        button2.configure(background="white")



        button1 = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button1.grid(column = 550, row = 1350)
        button1.configure(background="white")

        


# for  choosing the exercise:, eg , Tadasana , mountain-pose , etc
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="You are at Beginner level!", font=controller.title_font)
        label.grid(column = 550 , row = 10)
        label.configure(background="RoyalBlue1")

        lbl = tk.Label(self, text="Choose from list of exercises: " , font=("Arial Bold", 10) , padx = 5, pady = 5) # to set font properties
        lbl.grid(column=550, row=280) # to position
        lbl.configure(background="RoyalBlue1")

        lbl = tk.Label(self, text="Beginner Level " , font=("Arial Bold", 10) , padx = 5, pady = 5) # to set font properties
        lbl.grid(column=550, row=300) # to position
        lbl.configure(background="RoyalBlue1")

        button2 = tk.Button(self, text="Mountain Pose",
                   command=lambda: controller.show_frame("PageThree"))
        button2.grid(column = 550, row = 335)  
        button2.configure(background="white")

        lbl = tk.Label(self, text="Intermediate level" , font=("Arial Bold", 10) , padx = 5, pady = 5) # to set font properties
        lbl.grid(column=550, row=350) # to position
        lbl.configure(background="RoyalBlue1")

        button3 = tk.Button(self, text="Warrior Pose",
                           command=lambda: controller.show_frame("PageFour"))
        button3.grid(column = 550, row = 385) 
        button3.configure(background="white")

        lbl = tk.Label(self, text="Advanced level" , font=("Arial Bold", 10) , padx = 5, pady = 5) # to set font properties
        lbl.grid(column=550, row=400) # to position
        lbl.configure(background="RoyalBlue1")
        button3 = tk.Button(self, text="Tree Pose",
                           command=lambda: controller.show_frame("PageFive"))
        button3.grid(column = 550, row = 415) 
        button3.configure(background="white")

        def checkProgress():
            # left to define
           button.grid(column = 550 , row = 500)     

        button2 = tk.Button(self, text="Check your overall progress",
                           command=checkProgress)
        button2.grid(column = 550, row = 495) 
        button2.configure(background="white")


        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(column = 550 , row = 510)
        button.configure(background="white")


# for  Tadasana details and links
class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Mountain Pose (Tadasana)", font=controller.title_font)
        label.grid(column = 0 , row = 10)
        label.configure(background="RoyalBlue1")

        lbl = tk.Label(self, text="Tadasana teaches you proper standing posture needed for all other exercises " 
        , font=("Arial Bold", 10) , padx = 5, pady = 5) # to set font properties
        lbl.configure(background="RoyalBlue1")
        lbl.grid(column=0, row=280) # to position

        lbl = tk.Label(self,
         text="About BANDS: "+
         "one GREEN band for  hip, one BLUE band for right hand , one BLUE band for"+
         "  left hand. Wear bands and stand with right side facing webcam." 
        , font=("Arial Bold", 10) , padx = 5, pady = 5) # to set font properties
        lbl.grid(column=0, row=320) # to position
        lbl.configure(background="RoyalBlue1")

        def playTrainerVideo():
            os.system('python tadasana.py') # play trainer video
            
       
        button2 = tk.Button(self, text="Show trainer video",
                           command=playTrainerVideo)
        button2.grid(column = 0, row = 385)   
        button2.configure(background="white")

        def startExercise():
            os.system('python tadasana.py') # start taking users video

        def calculation():
            playTrainerVideo()    
            
        button2 = tk.Button(self, text="I am ready to exercise!",
                           command=startExercise)
        button2.grid(column = 0, row = 395) 
        button2.configure(background="white")

        button2 = tk.Button(self, text="Show my progress!",
                           command=lambda: controller.show_frame("ProgressPage"))
        button2.grid(column = 0, row = 415) 
        button2.configure(background="white")


        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(column = 0 , row = 500)
        button.configure(background="white")


# exercise details for Downward facing dog (Intermediate)
class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Warrior Pose (Virbhadrasana)", font=controller.title_font)
        label.grid(column = 0 , row = 10)
        label.configure(background="RoyalBlue1")

        lbl = tk.Label(self, text="Warrior pose improves strength , energy , focus and balance." 
        , font=("Arial Bold", 10) , padx = 5, pady = 5) # to set font properties
        lbl.grid(column=0, row=280) # to position
        lbl.configure(background="RoyalBlue1")

        lbl = tk.Label(self,
         text="About BANDS: "+
         
         "one GREEN band for left leg , one GREEN band for right leg , one BLUE band for"+
         "  right hand. Wear bands and stand in front of laptop with right side facing webcam." 
        , font=("Arial Bold", 10) , padx = 5, pady = 5) # to set font properties
        lbl.grid(column=0, row=320) # to position
        lbl.configure(background="RoyalBlue1")

        def playTrainerVideo():
            os.system('python warrior.py') # play trainer video
            
       
        button2 = tk.Button(self, text="Show trainer video",
                           command=playTrainerVideo)
        button2.grid(column = 0, row = 385)   
        button2.configure(background="white")

        def startExercise():
            os.system('python warrior.py') # start taking users video

        button2 = tk.Button(self, text="I am ready to exercise!",
                           command=startExercise)
        button2.grid(column = 0, row = 395) 
        button2.configure(background="white")

        button2 = tk.Button(self, text="Show my progress!",
                           command=lambda: controller.show_frame("ProgressPage"))
        button2.grid(column = 0, row = 415) 
        button2.configure(background="white")


        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(column = 0 , row = 500)
        button.configure(background="white")


# exercise details for Tree pose (Advanced)
class PageFive(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Tree pose (Vrksasana)", font=controller.title_font)
        label.grid(column = 550 , row = 10)
        label.configure(background="RoyalBlue1")


        lbl = tk.Label(self, text="Tree pose helps improve mental and physical steadiness and poise." 
        , font=("Arial Bold", 10) , padx = 5, pady = 5) # to set font properties
        lbl.grid(column=550, row=280) # to position
        lbl.configure(background="RoyalBlue1")

        lbl = tk.Label(self,
         text="About BANDS: "+
         
         "two GREEN bands for left and right hand each, "+
        " one BLUE band for  left leg , one BLUE band for"+
         " right leg . Wear bands and stand in front of laptop facing webcam." 
        , font=("Arial Bold", 10) , padx = 5, pady = 5) # to set font properties
        lbl.grid(column=550, row=320) # to position
        lbl.configure(background="RoyalBlue1")

        def playTrainerVideo():
            os.system('python treepose.py') # play trainer video
            
       
        button2 = tk.Button(self, text="Show trainer video",
                           command=playTrainerVideo)
        button2.grid(column = 550, row = 385)   
        button2.configure(background="white")

        def startExercise():
            os.system('python treepose.py') # start taking users video

        button2 = tk.Button(self, text="I am ready to exercise!",
                           command=startExercise)
        button2.grid(column = 550, row = 395) 
        button2.configure(background="white")


        button2 = tk.Button(self, text="Show my progress!",
                           command=lambda: controller.show_frame("ProgressPage"))
        button2.grid(column =550, row = 415) 
        button2.configure(background="white")


        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(column = 550 , row = 500)
        button.configure(background="white")



# exercise details for Tree pose (Advanced)
class ProgressPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Your Progress!", font=controller.title_font)
        label.grid(column = 550 , row = 10)
        label.configure(background="RoyalBlue1")

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(column = 550 , row = 500)
        button.configure(background="white")





if __name__ == "__main__":
    app = SampleApp()
    app.configure(background="RoyalBlue1")
    
    app.mainloop()