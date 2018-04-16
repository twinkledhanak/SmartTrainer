# code for PanedWIndow
from tkinter import *
import os

p1 = PanedWindow()
p1.pack(fill=BOTH, expand=1)

m1 = PanedWindow(p1,orient=VERTICAL)
m1.pack(fill=BOTH, expand=1)
left = Label(m1, text="left pane") # left label inside m1
m1.add(left)
os.system('python tadasana.py')


m2 = PanedWindow(p1,orient=VERTICAL)
m2.pack(fill=BOTH, expand = 1)
right = Label(m2, text = "right pane") # right label inside m2
m2.add(right)
os.system('python tadasana.py')

p1.add(m1)
p1.add(m2)
mainloop()
#m2 = PanedWindow(m1, orient=VERTICAL)
#m1.add(m2)

