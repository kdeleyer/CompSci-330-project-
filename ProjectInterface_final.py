import os
import subprocess
from tkinter import Tk, Label, Button
from tkinter import filedialog
from pathlib import Path
import Project_stats_final

# Initialize window
window = Tk()
window.title("GPA Calculator")
window.geometry('600x400')
window.tk.call('tk', 'scaling', 2.0)

# Default filePath
filePath = None

donelbl = Label(window, text="")
donelbl.place(relx=0.5, rely=0.5, anchor="center")


def on_fileBtn_pressed():
    global filePath
    filePath = filedialog.askopenfilename(title="Select a file.", filetypes=[("Run files", "*.run")])
    if not filePath:
        donelbl.config(text="File selection cancelled.")
    else:
        print(filePath)


def on_goBtn_pressed():
    global filePath
    if not filePath:
        donelbl.config(text="No file path is chosen, please choose a file path")
        return

    path_of_files = Path(filePath)
    parent_folder = path_of_files.parent

    if filePath.endswith(".run"):
        Project_stats_final.student_good_grades = {}
        Project_stats_final.student_bad_grades = {}
        result_file_path = parent_folder / f"{os.path.basename(filePath).rstrip('.run')}results.txt"

        Project_stats_final.readRun(filePath, result_file_path)
        Project_stats_final.analyze_good_grades(result_file_path)
        Project_stats_final.analyze_bad_grades(result_file_path)

        donelbl.config(text="Processing complete. Opening results...")

        # Open Notepad with the results and wait for it to close
        process = subprocess.Popen(['notepad', str(result_file_path)], close_fds=True)
        process.wait()  # Wait for the Notepad process to close
        donelbl.config(text="Notepad closed. You may continue using the application.")
    else:
        donelbl.config(text="Not a .run file, please choose a .run file")


# Widgets
lbl = Label(window, text="GPA Calculator", font=("Arial", 13))
lbl.grid(column=1, row=0)

gradeLbl = Label(window, text="(Please submit a .run file.)")
gradeLbl.grid(column=0, row=1)

fileBtn = Button(window, text="Select File", command=on_fileBtn_pressed)
fileBtn.grid(column=1, row=1)

goBtn = Button(window, text="GO", command=on_goBtn_pressed)
goBtn.grid(column=1, row=2)

# Run the window
window.mainloop()
