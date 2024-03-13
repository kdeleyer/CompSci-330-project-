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
            return 4.00
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
        case _:
            return None

Tk().withdraw() 
file1 = askopenfilename()  


def readSection(fileName):
    # Open the file in read mode
    with open(fileName, 'r', encoding="utf-8-sig") as file:
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
                    grade = parts[3] # Assuming grade is the fourth part
                    
                    if (convert_grade(grade)!=None): #These letter grades dont affect the GPA
                        gradeArray = np.append(gradeArray, convert_grade(grade))

                else:
                    print("Line does not have enough parts:", line)
            return [sectionName, round(gradeArray.sum()/len(gradeArray), 2), sectionCredits] #returns section GPA


def readGroup(fileName):
    with open(fileName, 'r') as file:
        lines = file.readlines()
        if not lines:
            print("File is empty")
        else:
            sectionNameArray = np.array([], dtype=str) # Array where section names will be held
            sectionGradeArray = np.array([], dtype=float) # Array where section grades will be held
            sectionCreditsArray = np.array([], dtype=float) # Array where section credits will be held

            print(lines[0].strip().split()[0]) 
            for line in lines[1:]:
                cleaned_line = line.strip()
                section = readSection(cleaned_line) #read each section in the group
                sectionNameArray=np.append(sectionNameArray,section[0])
                sectionGradeArray=np.append(sectionGradeArray,section[1])
                sectionCreditsArray=np.append(sectionCreditsArray, float(section[2]))


    with open("results.txt", "a") as result:
        result.writelines(["Group: ", lines[0].strip().split()[0], "\nGroup GPA: ", str(np.dot(sectionGradeArray, sectionCreditsArray)/sectionCreditsArray.sum())]) #writes name of the group and group gpa
        result.write(f"\nSections in {lines[0].strip().split()[0]}\n")
        for i in range(len(sectionNameArray)):
            result.writelines(["Section Name: ", sectionNameArray[i], " GPA: ", str(sectionGradeArray[i]), " Credits: ", str(sectionCreditsArray[i]),"\n"])
        result.write("\n")


def readRun(fileName):
    with open(fileName, 'r') as file: 
        lines = file.readlines()
        runName = lines[0]
        with open("results.txt", "w") as result:
            result.writelines(["Run Name: ",runName,"\n"])
        for line in lines[1:]:
            readGroup(line.strip())

            

readRun(file1)
