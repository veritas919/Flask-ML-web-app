# run "python data_gatherer.py"
# run with an excel sheet, such as Data_3.xlsx, as the input to the read_excel invocation 


import pandas as pd

read_file = pd.read_excel (r'Data_3.xlsx')
read_file.to_csv (r'Data_saved_3.csv', index = None, header=True)