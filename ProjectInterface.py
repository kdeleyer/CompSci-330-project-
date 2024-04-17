# run from here please

import os

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from pathlib import Path
import Project_stats2



# initialize window
window = Tk()
# set window name
window.title("GPA Calculator")
# set window size
window.geometry('600x400')
# scale window items up
window.tk.call('tk', 'scaling', 2.0)

donelbl = Label(window, text="")
# donelbl.grid(column=1, row=3, pady=(100,0))
donelbl.place(relx=0.5, rely=0.5, anchor="center")
# button behaviours

def on_fileBtn_pressed():
    global filePath
    filePath = filedialog.askopenfilename(title="Select a file.")
    print(filePath)

def on_goBtn_pressed():
    if filePath == None:
        donelbl.config(text="No file path is chosen, please choose a file path")
    else:
        print(filePath)
        path_of_files = Path(filePath)
        parent_folder = path_of_files.parent
        
        if os.path.basename(filePath).endswith(".run"):
            Project_stats2.student_a_grades= {}
            Project_stats2.student_a_minus_grades= {}
            Project_stats2.student_d_grades= {}
            Project_stats2.student_d_minus_grades= {}
            Project_stats2.student_f_grades= {}
            print("file exists")
            result_file_path= parent_folder/f"{os.path.basename(filePath).rstrip('.run')}results.txt"
            # if os.path.exists(result_file_path):
            #     i = 2
            #     result_file_path= parent_folder/f"results{i}.txt"
            #     while os.path.exists(parent_folder/f"results{i}.txt"):
            #        i += 1
            #        result_file_path = parent_folder/f"results{i}.txt"

            Project_stats2.readRun(filePath, result_file_path)
            Project_stats2.analyze_a_grades(result_file_path)
            Project_stats2.analyze_a_minus_grades(result_file_path)
            Project_stats2.analyze_d_grades(result_file_path)
            Project_stats2.analyze_d_minus_grades(result_file_path)
            Project_stats2.analyze_f_grades(result_file_path)
            donelbl.config(text=f"Successful")
            ## opening results in window
            os.system(f'start notepad {result_file_path}')
        else:
            donelbl.config(text="Not a .run file, please choose a .run file")

# widgets

# grid() determines where the label will be displayed on the screen
# 3x3 grid
lbl = Label(window, text="GPA Calculator", font=("Arial", 13))
lbl.grid(column=1, row=0)

gradeLbl = Label(window, text="(Please submit a .run file.)")
gradeLbl.grid(column=0, row=1)

fileBtn = Button(window, text="Select File", command=on_fileBtn_pressed)
fileBtn.grid(column=1, row=1)

goBtn = Button(window, text="GO", command=on_goBtn_pressed)
goBtn.grid(column=1, row=2)

# runs the window
window.mainloop()