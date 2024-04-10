# run from here please

import os

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

import Project01

# button behaviours

def on_fileBtn_pressed():
    global filePath
    filePath = filedialog.askopenfilename(title="Select a file.")
    print(filePath)

def on_goBtn_pressed():
    print(filePath)
    
    if os.path.exists(filePath):
        print("file exists")
        Project01.readRun(filePath)
        Project01.analyze_a_grades()
    else:
        print("file not found")

# initialize window
window = Tk()
# set window name
window.title("GPA Calculator")
# set window size
window.geometry('600x400')
# scale window items up
window.tk.call('tk', 'scaling', 2.0)

# widgets

# grid() determines where the label will be displayed on the screen
# 3x3 grid
lbl = Label(window, text="GPA Calculator")
lbl.grid(column=1, row=0)

gradeLbl = Label(window, text="(Please submit a .RUN file.)")
gradeLbl.grid(column=0, row=1)

fileBtn = Button(window, text="Select File", command=on_fileBtn_pressed)
fileBtn.grid(column=1, row=1)

goBtn = Button(window, text="GO", command=on_goBtn_pressed)
goBtn.grid(column=1, row=2)

# runs the window
window.mainloop()