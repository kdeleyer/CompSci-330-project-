import numpy as np
import pandas as pd
from tkinter import Tk, filedialog

# Global dictionary to track 'A' grades per student across sections
student_a_grades = {}

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

def readSection(fileName):
    global student_a_grades
    with open(fileName, 'r', encoding="utf-8-sig") as file:
        lines = file.readlines()

    if not lines:
        print("File is empty")
        return None

    parts = lines[0].split()
    if len(parts) < 2:
        print(f"Unexpected format in {fileName}")
        return None

    sectionName = parts[0]
    sectionCredits = parts[1]
    gradeArray = np.array([])

    for line in lines[1:]:
        cleaned_line = line.strip().replace('\"', '').split(',')
        if len(cleaned_line) >= 4:
            name = f"{cleaned_line[0]} {cleaned_line[1]}"
            grade = cleaned_line[3]
            if grade == "A":
                student_a_grades[name] = student_a_grades.get(name, 0) + 1
            if convert_grade(grade) is not None:
                gradeArray = np.append(gradeArray, convert_grade(grade))

    sectionGPA = round(gradeArray.sum() / len(gradeArray), 2) if gradeArray.size > 0 else 0
    return [sectionName, sectionGPA, sectionCredits]

def readGroup(fileName):
    with open(fileName, 'r') as file:
        lines = file.readlines()
        if not lines:
            print("File is empty")
            return

    sectionNameArray, sectionGradeArray, sectionCreditsArray = np.array([]), np.array([]), np.array([])
    for line in lines[1:]:
        sectionDetails = readSection(line.strip())
        if sectionDetails:
            sectionNameArray = np.append(sectionNameArray, sectionDetails[0])
            sectionGradeArray = np.append(sectionGradeArray, sectionDetails[1])
            sectionCreditsArray = np.append(sectionCreditsArray, float(sectionDetails[2]))

    groupGPA = np.dot(sectionGradeArray, sectionCreditsArray) / sectionCreditsArray.sum() if sectionCreditsArray.sum() > 0 else 0
    with open("results.txt", "a") as result:
        result.write(f"Group: {lines[0].strip()}\nGroup GPA: {groupGPA:.2f}\n")
        for i in range(len(sectionNameArray)):
            result.write(f"Section Name: {sectionNameArray[i]}, GPA: {sectionGradeArray[i]}, Credits: {sectionCreditsArray[i]}\n")
        result.write("\n")

def readRun(fileName):
    with open(fileName, 'r') as file:
        lines = file.readlines()

    with open("results.txt", "w") as result:
        result.write(f"Run Name: {lines[0]}\n")
    for line in lines[1:]:
        readGroup(line.strip())

def analyze_a_grades():
    with open("results.txt", "a") as result_file:
        result_file.write("\nStudents with 'A' grade in at least 2 different sections:\n")
        for student, count in student_a_grades.items():
            if count >= 2:
                result_file.write(f"{student} has received an 'A' grade in at least 2 different sections.\n")

def main():
    pass
    #Tk().withdraw()
    #fileName = filedialog.askopenfilename()
    #readRun(fileName)
    #analyze_a_grades()

if __name__ == "__main__":
    main()


