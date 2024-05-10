import numpy as np
import pandas as pd
from tkinter import Tk, filedialog
from pathlib import Path
import os

# Global dictionaries to track grades per student across sections, storing section names
student_good_grades = {}
student_bad_grades = {}
# student_d_grades = {}
# student_d_minus_grades = {}
# student_f_grades = {}

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

def calculate_z(sectionGPA, groupGPA, groupStd):
    return (sectionGPA - groupGPA) / groupStd

calculate_z = np.vectorize(calculate_z)

def readSection(fileName):
    global student_good_grades, student_bad_grades
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
            name = f"{cleaned_line[1]} {cleaned_line[0]}"
            grade = cleaned_line[3]
            student_grades = {
                "good": student_good_grades,
                "bad": student_bad_grades
            }
            if grade in ["A","A-"]:
                if name not in student_grades["good"]:
                    student_grades["good"][name] = []
                if not (sectionName in student_grades["good"][name]):
                    student_grades["good"][name].append(sectionName)

            elif grade in ["D", "D-", "F"]:
                if name not in student_grades["bad"]:
                    student_grades["bad"][name] = []
                if not (sectionName in student_grades["bad"][name]):
                    student_grades["bad"][name].append(sectionName)
                    
            
            if convert_grade(grade) is not None:
                gradeArray = np.append(gradeArray, convert_grade(grade))

    sectionGPA = round(gradeArray.sum() / len(gradeArray), 2) if gradeArray.size > 0 else 0
    return [sectionName, sectionGPA, sectionCredits]


def readGroup(fileName, result_file_path):
    path_of_files = Path(fileName)
    parent_folder = path_of_files.parent
    with open(fileName, 'r') as file:
        lines = file.readlines()

    if not lines:
        print("File is empty")
        return "", 0.0  # Return a default tuple if the file is empty

    sectionNameArray, sectionGradeArray, sectionCreditsArray = np.array([]), np.array([]), np.array([])
    for line in lines[1:]:
        sectionDetails = readSection(parent_folder / line.strip())
        if sectionDetails:
            sectionNameArray = np.append(sectionNameArray, sectionDetails[0])
            sectionGradeArray = np.append(sectionGradeArray, sectionDetails[1])
            sectionCreditsArray = np.append(sectionCreditsArray, float(sectionDetails[2]))
        else:
            print(f"Failed to process section from file: {line.strip()}")  # Log the failure

    if sectionCreditsArray.sum() > 0:
        groupGPA = np.dot(sectionGradeArray, sectionCreditsArray) / sectionCreditsArray.sum()
    else:
        groupGPA = 0.0  # Default GPA if no credits or sections processed

    groupStd = np.std(sectionGradeArray) if sectionGradeArray.size > 0 else 0

    with open(result_file_path, "a") as result:
        groupName = lines[0].strip()
        result.write(f"Group: {groupName}\nGroup GPA: {groupGPA:.2f}\n")
        for i in range(len(sectionNameArray)):
            result.write(
                f"Section Name: {sectionNameArray[i]}, GPA: {sectionGradeArray[i]}, Credits: {sectionCreditsArray[i]}\n")
        result.write("\n")
        z = calculate_z(sectionGradeArray, groupGPA, groupStd)
        for i in range(len(sectionGradeArray)):
            if z[i] >= 2 or z[i] <= -2:
                result.write(
                    f"Section {sectionNameArray[i]}'s GPA {sectionGradeArray[i]} is statistically different than the group's GPA {groupGPA:.2f} with z-score {z[i]:.2f}")
        result.write("\n")

    return groupName, groupGPA

def readRun(fileName, result_file_path):
    path_of_files = Path(fileName)
    parent_folder = path_of_files.parent
    groupNames = []
    groupGPA = np.array([])
    with open(fileName, 'r') as file:
        lines = file.readlines()

    with open(result_file_path, "w") as result:
        result.write(f"Run Name: {lines[0]}\n")
    for line in lines[1:]:
        name, GPA = readGroup(parent_folder / line.strip(), result_file_path)
        groupNames.append(name)
        groupGPA = np.append(groupGPA, GPA)

    runGPA = groupGPA.sum() / len(groupGPA)
    if len(groupNames) > 1:
        with open(result_file_path, "a") as result:
            z = calculate_z(groupGPA, runGPA, groupGPA.std())
            for i in range(len(groupGPA)):
                if (z[i] >= 2 or z[i] <= -2):
                    result.write(f"{groupNames[i]}\'s GPA {groupGPA[i]:.2f} is statistically different than the run's GPA {runGPA:.2f} with z-score {z[i]:.2f}\n")
            result.write("\n")

def analyze_good_grades(result_file_path):
    with open(result_file_path, "a") as result_file:
        flag = 0
        previous_position = result_file.tell()

        result_file.write("Students with good grades (A, A-) in at least 2 different sections:\n")
        for student, sections in sorted(student_good_grades.items()):
            if len(sections) >= 2:
                flag = 1
                result_file.write(f"{student} - {', '.join(sections)}\n")

        if flag == 0:
            result_file.truncate(previous_position)

def analyze_bad_grades(result_file_path):
    with open(result_file_path, "a") as result_file:
        flag = 0
        previous_position = result_file.tell()

        result_file.write("\nStudents with bad grades (D, D-, F) in at least 2 different sections:\n")
        for student, sections in sorted(student_bad_grades.items()):
            if len(sections) >= 2:
                flag = 1
                result_file.write(f"{student} - {', '.join(sections)}\n")

        if flag == 0:
            result_file.truncate(previous_position)

# def analyze_d_grades(result_file_path):
#     with open(result_file_path, "a") as result_file:
#         flag = 0
#         previous_position = result_file.tell()

#         result_file.write("\nStudents with 'D' grade in at least 2 different sections:\n")
#         for student, sections in sorted(student_d_grades.items()):
#             if len(sections) >= 2:
#                 flag = 1
#                 result_file.write(f"{student} - {', '.join(sections)}\n")

#         if flag == 0:
#             result_file.truncate(previous_position)

# def analyze_d_minus_grades(result_file_path):
#     with open(result_file_path, "a") as result_file:
#         flag = 0
#         previous_position = result_file.tell()

#         result_file.write("\nStudents with 'D-' grade in at least 2 different sections:\n")
#         for student, sections in sorted(student_d_minus_grades.items()):
#             if len(sections) >= 2:
#                 flag = 1
#                 result_file.write(f"{student} - {', '.join(sections)}\n")

#         if flag == 0:
#             result_file.truncate(previous_position)

# def analyze_f_grades(result_file_path):
#     with open(result_file_path, "a") as result_file:
#         flag = 0
#         previous_position = result_file.tell()

#         result_file.write("\nStudents with 'F' grade in at least 2 different sections:\n")
#         for student, sections in sorted(student_f_grades.items()):
#             if len(sections) >= 2:
#                 flag = 1
#                 result_file.write(f"{student} - {', '.join(sections)}\n")

#         if flag == 0:
#             result_file.truncate(previous_position)

def main():
    pass
    # Tk().withdraw()
    # fileName = filedialog.askopenfilename()
    # readRun(fileName)
    # path_of_files=Path(fileName)
    # parent_folder=path_of_files.parent
    # analyze_a_grades(parent_folder)

if __name__ == "__main__":
    main()
