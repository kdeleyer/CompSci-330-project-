import numpy as np
import pandas as pd
from pathlib import Path
import os

# Global dictionaries to track grades per student across sections
student_a_grades = {}
student_a_minus_grades = {}
student_d_grades = {}
student_d_minus_grades = {}
student_f_grades = {}

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
    global student_a_grades, student_a_minus_grades, student_d_grades, student_d_minus_grades, student_f_grades
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
            grade_dict = {
                "A": student_a_grades,
                "A-": student_a_minus_grades,
                "D": student_d_grades,
                "D-": student_d_minus_grades,
                "F": student_f_grades
            }.get(grade)

            if grade_dict is not None:
                if name not in grade_dict:
                    grade_dict[name] = {}
                if sectionName not in grade_dict[name]:
                    grade_dict[name][sectionName] = 0
                grade_dict[name][sectionName] += 1

            if convert_grade(grade) is not None:
                gradeArray = np.append(gradeArray, convert_grade(grade))

    sectionGPA = round(gradeArray.sum() / len(gradeArray), 2) if gradeArray.size > 0 else 0
    return [sectionName, sectionGPA, sectionCredits]

def readGroup(fileName, result_file_path):
    path_of_files = Path(fileName)
    parent_folder = path_of_files.parent
    sectionNameArray, sectionGradeArray, sectionCreditsArray = np.array([]), np.array([]), np.array([])

    try:
        with open(fileName, 'r') as file:
            lines = file.readlines()
            if not lines:
                print("File is empty")
                return None

        for line in lines[1:]:
            sectionDetails = readSection(parent_folder / line.strip())
            if sectionDetails:
                sectionNameArray = np.append(sectionNameArray, sectionDetails[0])
                sectionGradeArray = np.append(sectionGradeArray, sectionDetails[1])
                sectionCreditsArray = np.append(sectionCreditsArray, float(sectionDetails[2]))

        if sectionCreditsArray.sum() > 0:
            groupGPA = np.dot(sectionGradeArray, sectionCreditsArray) / sectionCreditsArray.sum()
        else:
            groupGPA = 0

        groupStd = np.std(sectionGradeArray)
        with open(result_file_path, "a") as result:
            result.write(f"Group: {lines[0].strip()}\nGroup GPA: {groupGPA:.2f}\n")
            for i in range(len(sectionNameArray)):
                result.write(f"Section Name: {sectionNameArray[i]}, GPA: {sectionGradeArray[i]}, Credits: {sectionCreditsArray[i]}\n")
            z = calculate_z(sectionGradeArray, groupGPA, groupStd)
            for i, value in enumerate(z):
                if abs(value) >= 2:
                    result.write(f"Section {sectionNameArray[i]}'s GPA {sectionGradeArray[i]} is statistically different from the group's GPA {groupGPA:.2f} with a z-score of {value:.2f}\n")
            result.write("\n")
    except Exception as e:
        print(f"An error occurred: {e}")
        return "", 0  # Return default values in case of error

    return lines[0].strip(), groupGPA

def readRun(fileName, result_file_path):
    path_of_files = Path(fileName)
    parent_folder = path_of_files.parent
    groupNames = []
    groupGPA = np.array([])
    with open(fileName, 'r') as file:
        lines = file.readlines()

    with open(result_file_path, "w") as result:
        result.write(f"Run Name: {lines[0].strip()}\n")
    for line in lines[1:]:
        name, GPA = readGroup(parent_folder / line.strip(), result_file_path)
        groupNames.append(name)
        groupGPA = np.append(groupGPA, GPA)

    runGPA = groupGPA.sum() / len(groupGPA) if len(groupGPA) > 0 else 0
    if len(groupNames) > 1:
        with open(result_file_path, "a") as result:
            z = calculate_z(groupGPA, runGPA, np.std(groupGPA))
            for i, name in enumerate(groupNames):
                if abs(z[i]) >= 2:
                    result.write(f"{name}'s GPA {groupGPA[i]:.2f} is statistically different from the Run's GPA {runGPA:.2f} with a z-score of {z[i]:.2f}\n")
            result.write("\n")

def analyze_a_grades(result_file_path):
    with open(result_file_path, "a") as result_file:
        result_file.write("Students with 'A' grade in at least 2 different sections:\n")
        for student, classes in student_a_grades.items():
            if len(classes) >= 2:
                class_details = ', '.join(f"{cls} ({count} times)" for cls, count in classes.items())
                result_file.write(f"{student} received 'A' in: {class_details}\n")

def analyze_a_minus_grades(result_file_path):
    with open(result_file_path, "a") as result_file:
        result_file.write("Students with 'A-' grade in at least 2 different sections:\n")
        for student, classes in student_a_minus_grades.items():
            if len(classes) >= 2:
                class_details = ', '.join(f"{cls} ({count} times)" for cls, count in classes.items())
                result_file.write(f"{student} received 'A-' in: {class_details}\n")

def analyze_d_grades(result_file_path):
    with open(result_file_path, "a") as result_file:
        result_file.write("Students with 'D' grade in at least 2 different sections:\n")
        for student, classes in student_d_grades.items():
            if len(classes) >= 2:
                class_details = ', '.join(f"{cls} ({count} times)" for cls, count in classes.items())
                result_file.write(f"{student} received 'D' in: {class_details}\n")

def analyze_d_minus_grades(result_file_path):
    with open(result_file_path, "a") as result_file:
        result_file.write("Students with 'D-' grade in at least 2 different sections:\n")
        for student, classes in student_d_minus_grades.items():
            if len(classes) >= 2:
                class_details = ', '.join(f"{cls} ({count} times)" for cls, count in classes.items())
                result_file.write(f"{student} received 'D-' in: {class_details}\n")

def analyze_f_grades(result_file_path):
    with open(result_file_path, "a") as result_file:
        result_file.write("Students with 'F' grade in at least 2 different sections:\n")
        for student, classes in student_f_grades.items():
            if len(classes) >= 2:
                class_details = ', '.join(f"{cls} ({count} times)" for cls, count in classes.items())
                result_file.write(f"{student} received 'F' in: {class_details}\n")

def main():
    pass
    # Tk().withdraw()
    # fileName = filedialog.askopenfilename()
    # readRun(fileName)
    # path_of_files=Path(fileName)
    # parent_folder=path_of_files.parent
    # analyze_a_grades(parent_folder)
if __name__ == "__main__":
    (main)
