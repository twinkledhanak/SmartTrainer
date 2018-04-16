from tkinter import *
 
window = Tk()
 
window.title("Welcome to Smart-Trainer!")
window.geometry('700x400') # initial window size

lbl = Label(window, text="Smart-Trainer" , font=("Arial Bold", 30)) # to set font properties
lbl.grid(column=550, row=10) # to position

lbl = Label(window, text="A virtual trainer for physical exercises" , font=("Arial Bold", 15)) # to set font properties
lbl.grid(column=550, row=100) # to position

lbl = Label(window, text="Username" , font=("Arial Bold", 10) , padx = 5, pady = 5) # to set font properties
lbl.grid(column=550, row=280) # to position
txt = Entry(window, width=30)
txt.grid(column=550, row=282)
txt.focus()

lbl = Label(window, text="Password" , font=("Arial Bold", 10)) # to set font properties
lbl.grid(column=550, row=320) # to position
txt = Entry(window, width=30)
txt.grid(column=550, row=322)
txt.focus()

def clicked(): 
    lbl.configure(text="Button was clicked !!")
    # DO SOME ACTION HERE

 
#btn = Button(window, text="Login", command=clicked)
#btn.grid(column=550, row=350)
button1 = Button(window, text="Login",
        command=lambda: self.show_frame("PageOne"))
button1.grid(column=550,row=350)


window.mainloop() # important , else user wont be able to see anything



lbl = tk.Label(self, text="Weight (in kgs)" , font=("Arial Bold", 10) , padx = 5, pady = 5) # to set font properties
        #lbl.grid(column=550, row=280) # to position
        lbl.pack(side="top", fill="x", pady=10)
        txt = tk.Entry(self, width=30)
        #txt.grid(column=550, row=282)
        txt.pack()
        txt.focus()

        lbl = tk.Label(self, text="Daily Excercise time (in hrs)" ,
         font=("Arial Bold", 10) , padx = 5, pady = 5) # to set font properties
        lbl.pack(side="top", fill="x", pady=10)
        #lbl.grid(column=550, row=280) # to position
        txt = tk.Entry(self, width=30)
        #txt.grid(column=550, row=282)
        txt.pack()
        txt.focus()
