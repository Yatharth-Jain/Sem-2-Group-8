import pandas as pd
import os

os.chdir(os.path.dirname(__file__))

data=pd.read_excel('Marks-sheet.xlsx','CS (4 sem)')
data.columns=data[1]
print(data.columns)
