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

#dfpt.index는 이름을 가지고 있음 이름을 순차적으로 item에 대입
#내가 필요한건 해당이름에 있는 영화목록 df[df['Name'] == item]['Title']
#다른 이름의 영화목록과 비교해서 공통 영화목록을 뽑아내는 것
#공통 영화목록의 점수가 필요함 



def com_title(df, dfpt, p1, p2): 
    
    si = dict() #같이 평가한 영화 저장

    titlep1 = df[df['Name']==dfpt.index[p1]]['Title']
    titlep2 = df[df['Name']==dfpt.index[p2]]['Title']
    for item in titlep1.values: 
        if item in titlep2.values:
            si[item] = 1
 
    # 공통 항목 개수
    n = len(si)
    if n==0:
        return 0

    sscore1 = [] #sum
    ssqcore1 = [] #**2sum
    sscore2 = []
    ssqcore2 = []
    psum = []
    
    cname1 = df['Name']==dfpt.index[p1]
    cname2 = df['Name']==dfpt.index[p2]

    for it in si:
        ctitle1 = df['Title']==it
        cscore1 = df[cname1 & ctitle1]['Score'].values
        sscore1.append(cscore1)
        ssscore1 = sum(sscore1)
        
        ctitle2 = df['Title']==it
        cscore2 = df[cname2 & ctitle2]['Score'].values
        sscore2.append(cscore2)
        ssscore2 = sum(sscore2)
    
        qscore1 = (df[cname1 & ctitle1]['Score'].values)**2
        ssqcore1.append(qscore1)
        sssqcore1 = sum(ssqcore1)
    
        qscore2 = (df[cname2 & ctitle2]['Score'].values)**2
        ssqcore2.append(qscore2)
        sssqcore2 = sum(ssqcore2)

        pscore = cscore1 * cscore2
        psum.append(pscore)
        ppsum = sum(psum)
       

    num = ppsum - (ssscore1*ssscore2/n)
    den = math.sqrt((sssqcore1-pow(ssscore1,2)/n) * (sssqcore2-pow(ssscore2,2)/n))
    if den==0:
        return 0

    r = num/den # -1 ~ +1 마이너스 선형상관계수를 가지면 상이한 개체 

    return r 

print (dfpt)