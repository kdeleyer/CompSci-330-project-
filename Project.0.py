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


