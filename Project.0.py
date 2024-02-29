## Kyle Deleyer
## Programing for 330 project
## this is ment for code segments, like a bank

import numpy as np
import pandas as pd
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
file1 = askopenfilename() # show an "Open" dialog box and return the path to the selected file
##file2 - askopenfilename()
with open(file1, 'r') as file1:
    # Read the contents of the file
    file_content = file1.read()
    # Print the contents
    print(file_content)


import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def convert_grade(grade):
    # Implement a function to convert letter grades to a GPA value if needed
    pass

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
            # Process each line
            for line in lines:
                # Remove quotes and then split the line into parts
                cleaned_line = line.strip().replace('\"', '')
                parts = cleaned_line.split(',')

                # If there are enough parts to process
                if len(parts) >= 3:
                    # Extract the name, ID number, and grade
                    # Assuming the first two parts are the last and first names
                    name = f"{parts[0]}, {parts[1]}"
                    id_number = parts[2]
                    grade = parts[3]  # Assuming grade is the fourth part

                    # Print the extracted information
                    print("Name:", name)
                    print("ID Number:", id_number)
                    print("Grade:", grade)
                    print()  # Print an empty line between each student's information
                else:
                    print("Line does not have enough parts:", line)

except FileNotFoundError:
    print("File not found. Please check the file path.")
except Exception as e:
    print("An error occurred:", e)


