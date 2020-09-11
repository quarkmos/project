import pandas as pd
import numpy as np
import csv
import math

data_set = pd.read_csv('rottenscore.csv', encoding = 'utf8', header = None)

name = data_set[0].tolist()

title = data_set[1].tolist()

score = data_set[2].tolist()


data = [] # 저장 공간

saver = name[0] # 현재 A컬럼의 이름을 기억할 변수

dicter = {} # 임시 저장공간


for i in range(len(name)):
    if saver == name[i]:
        if score[i] == 'None score':
            dicter[title[i]] = '0' #none score
        elif score[i] != 'None score':
            dicter[title[i]] = int(score[i])
            saver = name[i]
    elif saver != name[i]:
        data.append(dicter)
        dicter = {}
        if score[i] == 'None score':
            dicter[title[i]] = '0' #none score
        elif score[i] != 'None score':
            dicter[title[i]] = int(score[i])
            saver = name[i]
            if i == len(name) - 1:
                data.append(dicter)


# data 안에 값이 다 있음
# sorted(name)해서 name[0]에 해당하는 값이 data[0]의 값임


df = pd.DataFrame({'Name' : name, 'Title' : title, 'Score' : score}, columns = ['Name', 'Title', 'Score']) 

#df = df.sort_values('Title')

dfpt = df.pivot_table( index = 'Name', columns = 'Title', values = 'Score', aggfunc='first').fillna(0) #index 0 = name, index 1 = title, index 2 = score

count = dict()

for i in title:
    try: count[i] += 1
    except: count[i] = 1
print (sorted(count.values(), reverse=True))
print (type(count))

