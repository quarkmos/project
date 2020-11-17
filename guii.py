from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.request import urlopen
import urllib.request
from urllib.parse import quote_plus
import pandas as pd
import numpy as np
import operator
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import webbrowser
import parmap
from multiprocessing import Manager, cpu_count, freeze_support
import os

chromedriver = "chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument("lang=ko_KR") # 한국어!

data_set = pd.read_csv('./csvfiles/rottenscore.csv', encoding='utf8', header=None) #크롤링한 데이터 저장한 엑셀파일

name = data_set[0].tolist() #평론가 이름
title = data_set[1].tolist() #영화 제목
score = data_set[2].tolist() #영화 평점

user_name = list()
user_title = list()
user_score = list()

data = [] # 저장 공간
saver = name[0] # 현재 A컬럼의 이름을 기억할 변수
dicter = {} # 임시 저장공간

rank_temp = []
rank_name = []
rank_df = []
rank_score = []
rank_dict = dict()
sorted_rank_dict = dict()

author_title = []
author_score = []

urldata =[]
urlidx = []

re_urldata = []
re_urlidx = []

num_cores = cpu_count()
urllist = []

for i in range(len(name)): #평론가 이름 {'영화제목': '영화 평점' }
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

def com_title(final_df, final_dfpt, p1, p2): #p1, p2의 인덱스로 피어슨 유사도를 구하는 함수

    # 같이 평가한 영화 저장할 dict
    si = dict()

    # 인덱스 받아서 해당 평론가가 가진 영화 제목 저장
    titlep1 = final_df[final_df['Name'] == final_dfpt.index[p1]]['Title']
    titlep2 = final_df[final_df['Name'] == final_dfpt.index[p2]]['Title']

    for item in titlep1.values: #공통으로 평가한 영화 제목 추려냄
        if item in titlep2.values:
            si[item] = 1

    # 공통 항목 개수
    n = len(si)

    # 공통 항목 없을 경우 유사도는 0
    if n == 0:
        return 0


    sscore1 = []
    ssscore1 = [] #1의 합
    ssqcore1 = []
    sssqcore1 = [] #1의 제곱의 합

    sscore2 = []
    ssscore2 = [] #2의 합
    ssqcore2 = []
    sssqcore2 = [] #2의 제곱의 합

    sumpow1 = []
    sumpow2 = []
    ssumpow1 = []
    ssumpow2 = []

    psum = []
    ppsum = [] #1*2의 합

    cname1 = final_df['Name'] == final_dfpt.index[p1] # 다중 조건을 위한 평론가 이름 Boolean형태로 출력
    cname2 = final_df['Name'] == final_dfpt.index[p2]

    for it in si:
        ctitle1 = final_df['Title'] == it # 다중 조건을 위한 공통항목 내 영화 점수
        cscore1 = final_df[cname1 & ctitle1]['Score'].values # df 내 두 조건을 만족하는 항목의 점수
        cscore1 = cscore1.astype(np.int)
        sscore1.append(cscore1)
        ssscore1 = sum(sscore1)

        ctitle2 = final_df['Title'] == it
        cscore2 = final_df[cname2 & ctitle2]['Score'].values
        cscore2 = cscore2.astype(np.int)
        sscore2.append(cscore2)
        ssscore2 = sum(sscore2)

        qscore1 = cscore1 ** 2
        ssqcore1.append(qscore1)
        sssqcore1 = sum(ssqcore1)

        qscore2 = (cscore2) ** 2
        ssqcore2.append(qscore2)
        sssqcore2 = sum(ssqcore2)

        sumpow1 = pow(cscore1, 2)
        ssumpow1 = sum(sumpow1)

        sumpow2 = pow(cscore2, 2)
        ssumpow2 = sum(sumpow2)

        pscore = cscore1 * cscore2
        psum.append(pscore)
        ppsum = sum(psum)

    num = ppsum - (ssscore1 * ssscore2 / n)

#    den = np.sqrt((sssqcore1 - pow(ssscore1, 2) / n) * (sssqcore2 - pow(ssscore2, 2) / n))

    pow_val = (ssumpow1 - pow(ssscore1, 2) / n) * (ssumpow2 - pow(ssscore2, 2) / n)

    # 음수 나올경우 에러남
    if (sum(pow_val) < 0):
        den = 0
    # 0을 루트씌우면 에러남
    elif (sum(pow_val) != 0):
        den = np.sqrt(pow_val)
        den = den.tolist()
    else:
        den = 0

    if den == 0:
        return 0

    # -1 ~ +1 마이너스 선형상관계수를 가지면 상이한 개체
    r = num / den

    return r

#레이블을 클릭해서 유저데이터를 입력한 후 유저 인덱스를 찾기위한 함수
def finduser_index(final_dfpt, len_index):
    for i in range(0, len_index):
        if final_dfpt.index[i] == 'user':
            return i

#평론가들이 중복적으로 평가한 영화
counttitle={} #dict
for i in title:
    try: counttitle[i] += 1
    except: counttitle[i]=1
#가장 많이 평가된 영화순으로 정렬 > 유저에게 순서대로 평가를 제안
sorted_counttitle = sorted(counttitle.items(), key = operator.itemgetter(1), reverse = True) #tuple

#QLabel은 원래 clicked()가 불가능한데 가능하게 해주는 함수
def clickable(widget):
    class Filter(QObject):

        clicked = pyqtSignal()

        def eventFilter(self, obj, event):

            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        # The developer can opt for .emit(obj) to get the object within the slot.
                        return True

            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked


#movielink = shadow_root3.find_element_by_css_selector('a').get_attribute('href')  # 영화url
class main_poster_crawler():

    def __init__(self):

        self.maincrawler()

    def openbrowser(self, value, urldict):

        self.idx = int()
        for key, val in urldict.items():
            if val == str(value):
                self.idx = int(key)
                break
            else:
                continue


        driver = webdriver.Chrome('./chromedriver.exe', options=options) #, options=options
        driver.get(value)

        def expand_shadow_element(element):
            shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
            return shadow_root

        try:

            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "search-result-container")))

            root1 = driver.find_element_by_tag_name('search-result-container')
            shadow_root1 = expand_shadow_element(root1)

            root2 = shadow_root1.find_element_by_css_selector('search-result + *')
            shadow_root2 = expand_shadow_element(root2)

            root3 = shadow_root2.find_element_by_css_selector('media-row')
            shadow_root3 = expand_shadow_element(root3)

            imgurl = shadow_root3.find_element_by_css_selector('img').get_attribute('src')

            # 이미지 리사이즈 크기 변경 > 화질개선
            imgurl = imgurl.replace('80x126', '320x512')

            urllib.request.urlretrieve(imgurl, './poster/poster' + str(self.idx) + '.jpg')

        finally:
            driver.quit()


    def maincrawler(self):

        base_url = 'https://www.rottentomatoes.com/search?search='
        for i in range(len(sorted_counttitle)):
            if i == 24:
                break
            key_url = sorted_counttitle[i][0]
            url = base_url + quote_plus(key_url)

            urldata.append(url)
            urlidx.append(i)

        for i in range(len(urldata)):
            urldict[urlidx[i]] = urldata[i]

        parmap.map(self.openbrowser, urldict.values(), urldict, pm_pbar=True, pm_processes=num_cores)

class result_poster_crawler():

    def __init__(self):

        self.resultcrawler()

    def openbrowser(self, value, rec_shared_dict, re_urldict):

        self.idxx = int()
        for key, val in re_urldict.items():
            if val == str(value):
                self.idxx = int(key)
                break
            else:
                continue

        driver = webdriver.Chrome('./chromedriver.exe', options=options) #, options=options
        driver.get(value)

        def expand_shadow_element(element):
            shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
            return shadow_root

        try:

            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "search-result-container")))

            root1 = driver.find_element_by_tag_name('search-result-container')
            shadow_root1 = expand_shadow_element(root1)

            root2 = shadow_root1.find_element_by_css_selector('search-result + *')
            shadow_root2 = expand_shadow_element(root2)

            root3 = shadow_root2.find_element_by_css_selector('media-row')
            shadow_root3 = expand_shadow_element(root3)

            imgurl = shadow_root3.find_element_by_css_selector('img').get_attribute('src')
            movielink = shadow_root3.find_element_by_css_selector('a').get_attribute('href')  # 영화url

            # 이미지 리사이즈 크기 변경 > 화질개선
            imgurl = imgurl.replace('80x126', '320x512')

            urllib.request.urlretrieve(imgurl, './resultposter/resultposter' + str(self.idxx) + '.jpg')
            rec_shared_dict[self.idxx] = movielink


        finally:
            driver.quit()


    def resultcrawler(self):

        base_url = 'https://www.rottentomatoes.com/search?search='
        for i in range(len(sorted_rank_dict)):
            if i == 24:
                break
            key_url = sorted_rank_dict[i][0]
            url = base_url + quote_plus(key_url)

            re_urldata.append(url)
            re_urlidx.append(i)

        for i in range(len(re_urldata)):
            re_urldict[re_urlidx[i]] = re_urldata[i]

        parmap.map(self.openbrowser, re_urldict.values(), rec_shared_dict, re_urldict, pm_pbar=True, pm_processes=num_cores)

#실행시 가장 먼저 출력할 메인화면
class page1(QWidget):

    #호출시 자동 실행되는 생성자
    def __init__(self, parent=None):

        super(page1, self).__init__(parent)

        self.resize(1400, 800)
        self.center()

        self.prevbtn = QPushButton(self)
        self.prevbtn.setText(' 이 전 ')

        #유저에게 입력받을 새 윈도우에 영화 레이블 8개
        self.nextbtn = QPushButton(self)
        self.nextbtn.setText(' 다 음 ')

        #입력받은 데이터를 바탕으로 유사도 계산 후 영화 추천할 것
        self.donebtn = QPushButton(self)
        self.donebtn.setText(' 완 료 ')

        #클릭시 영화점수 입력할 수 있는 기능 필요
        self.label1 = QLabel(self)
        #sorted_counttitle[0][0]을 로튼토마토에 검색해서 첫번쨰 이미지 크롤링 해야 함
        pixmap = QPixmap('./poster/poster0.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label1.setPixmap(QPixmap(pixmap))

        self.label2 = QLabel(self)
        pixmap = QPixmap('./poster/poster1.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label2.setPixmap(QPixmap(pixmap))

        self.label3 = QLabel(self)
        pixmap = QPixmap('./poster/poster2.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label3.setPixmap(QPixmap(pixmap))

        self.label4 = QLabel(self)
        pixmap = QPixmap('./poster/poster3.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label4.setPixmap(QPixmap(pixmap))

        self.label5 = QLabel(self)
        pixmap = QPixmap('./poster/poster4.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label5.setPixmap(QPixmap(pixmap))

        self.label6 = QLabel(self)
        pixmap = QPixmap('./poster/poster5.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label6.setPixmap(QPixmap(pixmap))

        self.label7 = QLabel(self)
        pixmap = QPixmap('./poster/poster6.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label7.setPixmap(QPixmap(pixmap))

        self.label8 = QLabel(self)
        pixmap = QPixmap('./poster/poster7.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label8.setPixmap(QPixmap(pixmap))

        #그리드 레이아웃
        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(self.label1, 0, 0)
        layout.addWidget(self.label2, 0, 1)
        layout.addWidget(self.label3, 0, 2)
        layout.addWidget(self.label4, 0, 3)
        layout.addWidget(self.label5, 1, 0)
        layout.addWidget(self.label6, 1, 1)
        layout.addWidget(self.label7, 1, 2)
        layout.addWidget(self.label8, 1, 3)
        layout.addWidget(self.prevbtn, 2, 0)
        layout.addWidget(self.nextbtn, 2, 1)
        layout.addWidget(self.donebtn, 2, 2)

        #레이블 클릭할 수 있게 만들어줌
        clickable(self.label1).connect(self.checklbl0)
        clickable(self.label2).connect(self.checklbl1)
        clickable(self.label3).connect(self.checklbl2)
        clickable(self.label4).connect(self.checklbl3)
        clickable(self.label5).connect(self.checklbl4)
        clickable(self.label6).connect(self.checklbl5)
        clickable(self.label7).connect(self.checklbl6)
        clickable(self.label8).connect(self.checklbl7)

    #레이블 클릭시 실행되는 것
    def checklbl0(self):
        user_name.append('user')
        user_title.append(sorted_counttitle[0][0])
        #유저 점수 따로 입력받고 싶음
        user_score.append('89')

    def checklbl1(self):
        user_name.append('user')
        user_title.append(sorted_counttitle[1][0])
        user_score.append('90')

    def checklbl2(self):
        user_name.append('user')
        user_title.append(sorted_counttitle[2][0])
        user_score.append('89')

    def checklbl3(self):
        user_name.append('user')
        user_title.append(sorted_counttitle[3][0])
        user_score.append('90')

    def checklbl4(self):
        user_name.append('user')
        user_title.append(sorted_counttitle[4][0])
        user_score.append('89')

    def checklbl5(self):
        user_name.append('user')
        user_title.append(sorted_counttitle[5][0])
        user_score.append('90')

    def checklbl6(self):
        user_name.append('user')
        user_title.append(sorted_counttitle[6][0])
        user_score.append('89')

    def checklbl7(self):
        user_name.append('user')
        user_title.append(sorted_counttitle[7][0])
        user_score.append('90')

    #화면 중앙 출력
    def center(self):
        frame_info = self.frameGeometry()
        display_center = QDesktopWidget().availableGeometry().center()
        frame_info.moveCenter(display_center)
        self.move(frame_info.topLeft())


#done버튼 누르면 출력되는 화면 // 영화 추천 결과 출력
class recWindow(QWidget):

    def __init__(self, parent=None):

        super(recWindow, self).__init__(parent)

        self.resize(1400, 800)
        self.linker()

        #이전 화면 출력
        self.prevbtn = QPushButton(self)
        self.prevbtn.setText(' 이 전 ')

        #새로운 윈도우 출력 할 것, 추천할 영화 9~16순위
        self.nextbtn = QPushButton(self)
        self.nextbtn.setText(' 다 음 ')

        #첫번째 추천 영화
        #sorted_rank_dict[0][0]로튼토마토에 검색 후 첫번째 포스터
        self.reclabel1 = QLabel(self)
        pixmap = QPixmap('./resultposter/resultposter0.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel1.setPixmap(QPixmap(pixmap))

        self.reclabel2 = QLabel(self)
        pixmap = QPixmap('./resultposter/resultposter1.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel2.setPixmap(QPixmap(pixmap))

        self.reclabel3 = QLabel(self)
        pixmap = QPixmap('./resultposter/resultposter2.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel3.setPixmap(QPixmap(pixmap))

        self.reclabel4 = QLabel(self)
        pixmap = QPixmap('./resultposter/resultposter3.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel4.setPixmap(QPixmap(pixmap))

        self.reclabel5 = QLabel(self)
        pixmap = QPixmap('./resultposter/resultposter4.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel5.setPixmap(QPixmap(pixmap))

        self.reclabel6 = QLabel(self)
        pixmap = QPixmap('./resultposter/resultposter5.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel6.setPixmap(QPixmap(pixmap))

        self.reclabel7 = QLabel(self)
        pixmap = QPixmap('./resultposter/resultposter6.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel7.setPixmap(QPixmap(pixmap))

        self.reclabel8 = QLabel(self)
        pixmap = QPixmap('./resultposter/resultposter7.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel8.setPixmap(QPixmap(pixmap))

        reclayout = QGridLayout()
        self.setLayout(reclayout)
        reclayout.addWidget(self.reclabel1, 0, 0)
        reclayout.addWidget(self.reclabel2, 0, 1)
        reclayout.addWidget(self.reclabel3, 0, 2)
        reclayout.addWidget(self.reclabel4, 0, 3)
        reclayout.addWidget(self.reclabel5, 1, 0)
        reclayout.addWidget(self.reclabel6, 1, 1)
        reclayout.addWidget(self.reclabel7, 1, 2)
        reclayout.addWidget(self.reclabel8, 1, 3)
        reclayout.addWidget(self.prevbtn, 2, 1)
        reclayout.addWidget(self.nextbtn, 2, 2)

        clickable(self.reclabel1).connect(self.linkurl1)
        clickable(self.reclabel2).connect(self.linkurl2)
        clickable(self.reclabel3).connect(self.linkurl3)
        clickable(self.reclabel4).connect(self.linkurl4)
        clickable(self.reclabel5).connect(self.linkurl5)
        clickable(self.reclabel6).connect(self.linkurl6)
        clickable(self.reclabel7).connect(self.linkurl7)
        clickable(self.reclabel8).connect(self.linkurl8)


    def linkurl1(self):
        url = urllist[0]
        webbrowser.open(url)

    def linkurl2(self):
        url = urllist[1]
        webbrowser.open(url)

    def linkurl3(self):
        url = urllist[2]
        webbrowser.open(url)

    def linkurl4(self):
        url = urllist[3]
        webbrowser.open(url)

    def linkurl5(self):
        url = urllist[4]
        webbrowser.open(url)

    def linkurl6(self):
        url = urllist[5]
        webbrowser.open(url)

    def linkurl7(self):
        url = urllist[6]
        webbrowser.open(url)

    def linkurl8(self):
        url = urllist[7]
        webbrowser.open(url)


    def linker(self):
        for i in range(len(rec_shared_dict)):
            urllist.append(rec_shared_dict[i])

class recpage2(QWidget):

    def __init__(self, parent=None):

        super(recpage2, self).__init__(parent)

        self.resize(1400, 800)

        #이전 화면 출력
        self.prevbtn = QPushButton(self)
        self.prevbtn.setText(' 이 전 ')

        #새로운 윈도우 출력 할 것, 추천할 영화 9~16순위
        self.nextbtn = QPushButton(self)
        self.nextbtn.setText(' 다 음 ')

        #첫번째 추천 영화
        #sorted_rank_dict[0][0]로튼토마토에 검색 후 첫번째 포스터
        self.reclabel9 = QLabel(self)
        pixmap = QPixmap('./resultposter/resultposter8.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel9.setPixmap(QPixmap(pixmap))

        self.reclabel10 = QLabel(self)
        pixmap = QPixmap('./resultposter/resultposter9.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel10.setPixmap(QPixmap(pixmap))

        self.reclabel11 = QLabel(self)
        pixmap = QPixmap('./resultposter/resultposter10.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel11.setPixmap(QPixmap(pixmap))

        self.reclabel12 = QLabel(self)
        pixmap = QPixmap('./resultposter/resultposter11.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel12.setPixmap(QPixmap(pixmap))

        self.reclabel13 = QLabel(self)
        pixmap = QPixmap('./resultposter/resultposter12.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel13.setPixmap(QPixmap(pixmap))

        self.reclabel14 = QLabel(self)
        pixmap = QPixmap('./resultposter/resultposter13.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel14.setPixmap(QPixmap(pixmap))

        self.reclabel15 = QLabel(self)
        pixmap = QPixmap('./resultposter/resultposter14.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel15.setPixmap(QPixmap(pixmap))

        self.reclabel16 = QLabel(self)
        pixmap = QPixmap('./resultposter/resultposter15.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel16.setPixmap(QPixmap(pixmap))

        reclayout = QGridLayout()
        self.setLayout(reclayout)
        reclayout.addWidget(self.reclabel9, 0, 0)
        reclayout.addWidget(self.reclabel10, 0, 1)
        reclayout.addWidget(self.reclabel11, 0, 2)
        reclayout.addWidget(self.reclabel12, 0, 3)
        reclayout.addWidget(self.reclabel13, 1, 0)
        reclayout.addWidget(self.reclabel14, 1, 1)
        reclayout.addWidget(self.reclabel15, 1, 2)
        reclayout.addWidget(self.reclabel16, 1, 3)
        reclayout.addWidget(self.prevbtn, 2, 1)
        reclayout.addWidget(self.nextbtn, 2, 2)

        clickable(self.reclabel9).connect(self.linkurl9)
        clickable(self.reclabel10).connect(self.linkurl10)
        clickable(self.reclabel11).connect(self.linkurl11)
        clickable(self.reclabel12).connect(self.linkurl12)
        clickable(self.reclabel13).connect(self.linkurl13)
        clickable(self.reclabel14).connect(self.linkurl14)
        clickable(self.reclabel15).connect(self.linkurl15)
        clickable(self.reclabel16).connect(self.linkurl16)

    def linkurl9(self):
        url = urllist[8]
        webbrowser.open(url)

    def linkurl10(self):
        url = urllist[9]
        webbrowser.open(url)

    def linkurl11(self):
        url = urllist[10]
        webbrowser.open(url)

    def linkurl12(self):
        url = urllist[11]
        webbrowser.open(url)

    def linkurl13(self):
        url = urllist[12]
        webbrowser.open(url)

    def linkurl14(self):
        url = urllist[13]
        webbrowser.open(url)

    def linkurl15(self):
        url = urllist[14]
        webbrowser.open(url)

    def linkurl16(self):
        url = urllist[15]
        webbrowser.open(url)


class recpage3(QWidget):

    def __init__(self, parent=None):

        super(recpage3, self).__init__(parent)

        self.resize(1400, 800)

        #이전 화면 출력
        self.prevbtn = QPushButton(self)
        self.prevbtn.setText(' 이 전 ')

        #새로운 윈도우 출력 할 것, 추천할 영화 9~16순위
        self.nextbtn = QPushButton(self)
        self.nextbtn.setText(' 다 음 ')

        #첫번째 추천 영화
        #sorted_rank_dict[0][0]로튼토마토에 검색 후 첫번째 포스터
        self.reclabel17 = QLabel(self)
        pixmap = QPixmap('./resultposter/resultposter16.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel17.setPixmap(QPixmap(pixmap))

        self.reclabel18 = QLabel(self)
        pixmap = QPixmap('./resultposter/resultposter17.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel18.setPixmap(QPixmap(pixmap))

        self.reclabel19 = QLabel(self)
        pixmap = QPixmap('./resultposter/resultposter18.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel19.setPixmap(QPixmap(pixmap))

        self.reclabel20 = QLabel(self)
        pixmap = QPixmap('./resultposter/resultposter19.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel20.setPixmap(QPixmap(pixmap))

        self.reclabel21 = QLabel(self)
        pixmap = QPixmap('./resultposter/resultposter20.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel21.setPixmap(QPixmap(pixmap))

        self.reclabel22 = QLabel(self)
        pixmap = QPixmap('./resultposter/resultposter21.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel22.setPixmap(QPixmap(pixmap))

        self.reclabel23 = QLabel(self)
        pixmap = QPixmap('./resultposter/resultposter22.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel23.setPixmap(QPixmap(pixmap))

        self.reclabel24 = QLabel(self)
        pixmap = QPixmap('./resultposter/resultposter23.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel24.setPixmap(QPixmap(pixmap))

        reclayout = QGridLayout()
        self.setLayout(reclayout)
        reclayout.addWidget(self.reclabel17, 0, 0)
        reclayout.addWidget(self.reclabel18, 0, 1)
        reclayout.addWidget(self.reclabel19, 0, 2)
        reclayout.addWidget(self.reclabel20, 0, 3)
        reclayout.addWidget(self.reclabel21, 1, 0)
        reclayout.addWidget(self.reclabel22, 1, 1)
        reclayout.addWidget(self.reclabel23, 1, 2)
        reclayout.addWidget(self.reclabel24, 1, 3)
        reclayout.addWidget(self.prevbtn, 2, 1)
        reclayout.addWidget(self.nextbtn, 2, 2)

        clickable(self.reclabel17).connect(self.linkurl17)
        clickable(self.reclabel18).connect(self.linkurl18)
        clickable(self.reclabel19).connect(self.linkurl19)
        clickable(self.reclabel20).connect(self.linkurl20)
        clickable(self.reclabel21).connect(self.linkurl21)
        clickable(self.reclabel22).connect(self.linkurl22)
        clickable(self.reclabel23).connect(self.linkurl23)
        clickable(self.reclabel24).connect(self.linkurl24)


    def linkurl17(self):
        url = urllist[16]
        webbrowser.open(url)

    def linkurl18(self):
        url = urllist[17]
        webbrowser.open(url)

    def linkurl19(self):
        url = urllist[18]
        webbrowser.open(url)

    def linkurl20(self):
        url = urllist[19]
        webbrowser.open(url)

    def linkurl21(self):
        url = urllist[20]
        webbrowser.open(url)

    def linkurl22(self):
        url = urllist[21]
        webbrowser.open(url)

    def linkurl23(self):
        url = urllist[22]
        webbrowser.open(url)

    def linkurl24(self):
        url = urllist[23]
        webbrowser.open(url)


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(50, 50, 400, 450)
        self.setFixedSize(1200, 800)
        self.startdownload()
        self.startUIWindow()

    def startdownload(self):
        main_poster_crawler()

    def recstartdownload(self):
        result_poster_crawler()

    def showresult(self):
        self.Window = recWindow(self)
        self.setWindowTitle('result')
        self.setCentralWidget(self.Window)
        self.Window.nextbtn.clicked.connect(self.resultpage2)
        self.show()

    def resultpage2(self):
        self.Window = recpage2(self)
        self.setWindowTitle('recpage2')
        self.setCentralWidget(self.Window)
        self.Window.prevbtn.clicked.connect(self.showresult)
        self.Window.nextbtn.clicked.connect(self.resultpage3)
        self.show()

    def resultpage3(self):
        self.Window = recpage3(self)
        self.setWindowTitle('recpage3')
        self.setCentralWidget(self.Window)
        self.Window.prevbtn.clicked.connect(self.resultpage2)
        self.show()

    def startUIWindow(self):
        self.Window = page1(self)
        self.setWindowTitle("Page1")
        self.setCentralWidget(self.Window)
        self.Window.nextbtn.clicked.connect(self.gopage2)
        self.Window.donebtn.clicked.connect(self.simrank)
        self.Window.donebtn.clicked.connect(self.resultrank)
        self.Window.donebtn.clicked.connect(self.recstartdownload)
        self.Window.donebtn.clicked.connect(self.showresult)
        self.show()

    def gopage2(self):
        self.Window = Page2(self)
        self.setWindowTitle("Page2")
        self.setCentralWidget(self.Window)
        self.Window.nextbtn.clicked.connect(self.gopage3)
        self.Window.prevbtn.clicked.connect(self.startUIWindow)
        self.Window.donebtn.clicked.connect(self.simrank)
        self.Window.donebtn.clicked.connect(self.resultrank)
        self.Window.donebtn.clicked.connect(self.recstartdownload)
        self.Window.donebtn.clicked.connect(self.showresult)
        self.show()

    def gopage3(self):
        self.Window = Page3(self)
        self.setWindowTitle("Page3")
        self.setCentralWidget(self.Window)
        self.Window.prevbtn.clicked.connect(self.gopage2)
        self.Window.donebtn.clicked.connect(self.simrank)
        self.Window.donebtn.clicked.connect(self.resultrank)
        self.Window.donebtn.clicked.connect(self.recstartdownload)
        self.Window.donebtn.clicked.connect(self.showresult)
        self.show()

    #유사도 계산하는 함수
    def simrank(self):
        #엑셀에서 만들어진 데이터 프레임
        df = pd.DataFrame({'Name': name, 'Title': title, 'Score': score}, columns=['Name', 'Title', 'Score'])

        #유저가 클릭한 레이블로 만들어진 데이터 프레임
        user_df = pd.DataFrame({'Name': user_name, 'Title': user_title, 'Score': user_score}, columns=['Name', 'Title', 'Score'])

        #데이터 프레임 합침
        final_df = df.append(user_df, ignore_index=True)
        final_dfpt = final_df.pivot_table(index='Name', columns='Title', values='Score', aggfunc='first').fillna(0)  # index 0 = name, index 1 = title, index 2 = score

        len_index = len(final_dfpt.index)
        #유저인덱스 찾기
        user_index = finduser_index(final_dfpt, len_index)

        #평론가 별 유사도 저장한 것 temp에 저장
        temp = dict()
        for item in range(0, len_index-1):
            temp[item] = com_title(final_df, final_dfpt, item, user_index)

        #유사도 순위 계산 후 저장
        global rank_temp # index, sim
        rank_temp = sorted(temp.items(), key=operator.itemgetter(1), reverse=True)# tuple

        #유사도 가장 높은 3명 이름
        global rank_name
        for index in range(1, 5):
            rank_name.append(final_dfpt.index[rank_temp[index][0]])

        #유사도 가장 높은 3명만 df에 저장
        global rank_df
        for item in rank_name:
            rank_df.append(final_df[final_df['Name'] == item])

        return rank_name, rank_temp, rank_df

    def resultrank(self):
        global  rank_dict, author_title, author_score, sorted_rank_dict
        rank_dict = dict()
        for item in rank_df:
            for title in item['Title']:
                author_title.append(title)
            for score in item['Score']:
                author_score.append(score)
        for i in range(len(author_title)):
            rank_dict[author_title[i]] = int(author_score[i])

        sorted_rank_dict = sorted(rank_dict.items(), key=operator.itemgetter(1), reverse=True)


class Page2(QWidget):

    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)

        self.resize(1400, 800)

        self.prevbtn = QPushButton(self)
        self.prevbtn.setText(' 이 전 ')

        self.nextbtn = QPushButton(self)
        self.nextbtn.setText(' 다 음 ')

        self.donebtn = QPushButton(self)
        self.donebtn.setText(' 완 료 ')

        self.label9 = QLabel(self)
        pixmap = QPixmap('./poster/poster8.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label9.setPixmap(QPixmap(pixmap))

        self.label10 = QLabel(self)
        pixmap = QPixmap('./poster/poster9.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label10.setPixmap(QPixmap(pixmap))

        self.label11 = QLabel(self)
        pixmap = QPixmap('./poster/poster10.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label11.setPixmap(QPixmap(pixmap))

        self.label12 = QLabel(self)
        pixmap = QPixmap('./poster/poster11.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label12.setPixmap(QPixmap(pixmap))

        self.label13 = QLabel(self)
        pixmap = QPixmap('./poster/poster12.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label13.setPixmap(QPixmap(pixmap))

        self.label14 = QLabel(self)
        pixmap = QPixmap('./poster/poster13.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label14.setPixmap(QPixmap(pixmap))

        self.label15 = QLabel(self)
        pixmap = QPixmap('./poster/poster14.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label15.setPixmap(QPixmap(pixmap))

        self.label16 = QLabel(self)
        pixmap = QPixmap('./poster/poster15.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label16.setPixmap(QPixmap(pixmap))

        # 그리드 레이아웃
        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(self.label9, 0, 0)
        layout.addWidget(self.label10, 0, 1)
        layout.addWidget(self.label11, 0, 2)
        layout.addWidget(self.label12, 0, 3)
        layout.addWidget(self.label13, 1, 0)
        layout.addWidget(self.label14, 1, 1)
        layout.addWidget(self.label15, 1, 2)
        layout.addWidget(self.label16, 1, 3)
        layout.addWidget(self.prevbtn, 2, 0)
        layout.addWidget(self.nextbtn, 2, 1)
        layout.addWidget(self.donebtn, 2, 2)

        # 레이블 클릭할 수 있게 만들어줌
        clickable(self.label9).connect(self.checklbl8)
        clickable(self.label10).connect(self.checklbl9)
        clickable(self.label11).connect(self.checklbl10)
        clickable(self.label12).connect(self.checklbl11)
        clickable(self.label13).connect(self.checklbl12)
        clickable(self.label14).connect(self.checklbl13)
        clickable(self.label15).connect(self.checklbl14)
        clickable(self.label16).connect(self.checklbl15)

    # 레이블 클릭시 실행되는 것
    def checklbl8(self):
        user_name.append('user')
        user_title.append(sorted_counttitle[8][0])
        # 유저 점수 따로 입력받고 싶음
        user_score.append('89')

    def checklbl9(self):
        user_name.append('user')
        user_title.append(sorted_counttitle[9][0])
        user_score.append('90')

    def checklbl10(self):
        user_name.append('user')
        user_title.append(sorted_counttitle[10][0])
        user_score.append('89')

    def checklbl11(self):
        user_name.append('user')
        user_title.append(sorted_counttitle[11][0])
        user_score.append('90')

    def checklbl12(self):
        user_name.append('user')
        user_title.append(sorted_counttitle[12][0])
        user_score.append('89')

    def checklbl13(self):
        user_name.append('user')
        user_title.append(sorted_counttitle[13][0])
        user_score.append('90')

    def checklbl14(self):
        user_name.append('user')
        user_title.append(sorted_counttitle[14][0])
        user_score.append('89')

    def checklbl15(self):
        user_name.append('user')
        user_title.append(sorted_counttitle[15][0])
        user_score.append('90')

class Page3(QWidget):

    def __init__(self, parent=None):
        super(Page3, self).__init__(parent)

        self.resize(1400, 800)

        self.prevbtn = QPushButton(self)
        self.prevbtn.setText(' 이 전 ')

        self.nextbtn = QPushButton(self)
        self.nextbtn.setText(' 다 음 ')

        self.donebtn = QPushButton(self)
        self.donebtn.setText(' 완 료 ')

        self.label17 = QLabel(self)
        pixmap = QPixmap('./poster/poster16.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label17.setPixmap(QPixmap(pixmap))

        self.label18 = QLabel(self)
        pixmap = QPixmap('./poster/poster17.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label18.setPixmap(QPixmap(pixmap))

        self.label19 = QLabel(self)
        pixmap = QPixmap('./poster/poster18.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label19.setPixmap(QPixmap(pixmap))

        self.label20 = QLabel(self)
        pixmap = QPixmap('./poster/poster19.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label20.setPixmap(QPixmap(pixmap))

        self.label21 = QLabel(self)
        pixmap = QPixmap('./poster/poster20.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label21.setPixmap(QPixmap(pixmap))

        self.label22 = QLabel(self)
        pixmap = QPixmap('./poster/poster21.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label22.setPixmap(QPixmap(pixmap))

        self.label23 = QLabel(self)
        pixmap = QPixmap('./poster/poster22.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label23.setPixmap(QPixmap(pixmap))

        self.label24 = QLabel(self)
        pixmap = QPixmap('./poster/poster23.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label24.setPixmap(QPixmap(pixmap))

        # 그리드 레이아웃
        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(self.label17, 0, 0)
        layout.addWidget(self.label18, 0, 1)
        layout.addWidget(self.label19, 0, 2)
        layout.addWidget(self.label20, 0, 3)
        layout.addWidget(self.label21, 1, 0)
        layout.addWidget(self.label22, 1, 1)
        layout.addWidget(self.label23, 1, 2)
        layout.addWidget(self.label24, 1, 3)
        layout.addWidget(self.prevbtn, 2, 0)
        layout.addWidget(self.nextbtn, 2, 1)
        layout.addWidget(self.donebtn, 2, 2)

        # 레이블 클릭할 수 있게 만들어줌
        clickable(self.label17).connect(self.checklbl16)
        clickable(self.label18).connect(self.checklbl17)
        clickable(self.label19).connect(self.checklbl18)
        clickable(self.label20).connect(self.checklbl19)
        clickable(self.label21).connect(self.checklbl20)
        clickable(self.label22).connect(self.checklbl21)
        clickable(self.label23).connect(self.checklbl22)
        clickable(self.label24).connect(self.checklbl23)

    # 레이블 클릭시 실행되는 것
    def checklbl16(self):
        user_name.append('user')
        user_title.append(sorted_counttitle[16][0])
        # 유저 점수 따로 입력받고 싶음
        user_score.append('89')

    def checklbl17(self):
        user_name.append('user')
        user_title.append(sorted_counttitle[17][0])
        user_score.append('90')

    def checklbl18(self):
        user_name.append('user')
        user_title.append(sorted_counttitle[18][0])
        user_score.append('89')

    def checklbl19(self):
        user_name.append('user')
        user_title.append(sorted_counttitle[19][0])
        user_score.append('90')

    def checklbl20(self):
        user_name.append('user')
        user_title.append(sorted_counttitle[20][0])
        user_score.append('89')

    def checklbl21(self):
        user_name.append('user')
        user_title.append(sorted_counttitle[21][0])
        user_score.append('90')

    def checklbl22(self):
        user_name.append('user')
        user_title.append(sorted_counttitle[22][0])
        user_score.append('89')

    def checklbl23(self):
        user_name.append('user')
        user_title.append(sorted_counttitle[23][0])
        user_score.append('90')

def run():
    global  urldict, rec_shared_dict, re_urldict
    freeze_support()
    manager = Manager()
    urldict = manager.dict()
    rec_shared_dict = manager.dict()
    re_urldict = manager.dict()
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()