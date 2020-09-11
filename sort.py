import pandas as pd
import csv
import numpy as np

critc_data = pd.read_csv('rottenscore.csv', encoding = 'utf8', header = None)
critc_sort = critc_data.pivot_table(values = 2, index = 1, columns = 0, aggfunc='first').fillna(0) #index 0 = author, index 1 = title, index 2 = score
print(critc_sort.columns)

