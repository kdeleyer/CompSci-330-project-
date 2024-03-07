## Kyle Deleyer
## Programing for 330 project
## this is ment for code segments, like a bank

import numpy as np
import pandas as pd
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

"""
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
file1 = askopenfilename() # show an "Open" dialog box and return the path to the selected file
##file2 - askopenfilename()
with open(file1, 'r') as file1:
    # Read the contents of the file
    file_content = file1.read()
    # Print the contents
    print(file_content)
"""

import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Converts letter grade to grade points
def convert_grade(grade):
    match grade:
        case "A":
            return 4.0
        case "A-":
            return 3.67
        case "B+":
            return 3.33
        case "B":
            return 3.00
        case "B-":
            return 2.67
        case "C+":
            return 2.33
        case "C":
            return 2.00
        case "C-":
            return 1.67
        case "D+":
            return 1.33
        case "D":
            return 1.00
        case "D-":
            return 0.67
        case "F":
            return 0.00

Tk().withdraw() 
file1 = askopenfilename()  

try:
    # Open the file in read mode
    with open(file1, 'r') as file:
        # Read the contents of the file
        lines = file.readlines()

        if not lines:
            print("File is empty")
        else:
            gradeArray = np.array([])


            parts = lines[0].split()
            sectionName=parts[0]
            sectionCredits=parts[1]

            # Process each line after the first line
            for line in lines[1:]:
                # Remove quotes and then split the line into parts
                cleaned_line = line.strip().replace('\"', '')
                parts = cleaned_line.split(',')

                if len(parts) >= 3: # If there are enough parts to process
                    # Extract the name, ID number, and grade
                    # Assuming the first two parts are the last and first names
                    name = f"{parts[0]}, {parts[1]}"
                    id_number = parts[2]
                    grade = parts[3]  # Assuming grade is the fourth part

                    # Print the extracted information
                   # print("Name:", name)
                    print("Grade:", grade)
                   # print()  # Print an empty line between each student's information
                    
                    if (grade !="I") & (grade !="W") & (grade !="P") & (grade !="NP") & (convert_grade(grade)!=None): #These letter grades dont affect the GPA
                        gradeArray = np.append(gradeArray, convert_grade(grade))

                else:
                    print("Line does not have enough parts:", line)
            
            print(round(gradeArray.sum()/len(gradeArray), 2)) #prints section GPA

except FileNotFoundError:
    print("File not found. Please check the file path.")
except Exception as e:
    print("An error occurred:", e)


