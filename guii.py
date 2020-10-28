from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
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


######### 숨겨진 HTML 호출을 위한 추가 (앞부분)
import os
# from selenium.webdriver.support.relative_locator import with_tag_name

chromedriver = "chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument("lang=ko_KR") # 한국어!
#driver = webdriver.Chrome(chromedriver, chrome_options = options)
driver = webdriver.Chrome('C:\\Users\\quarkmos\\Desktop\\pyc\\chromedriver.exe', options = options)


def expand_shadow_element(element):
  shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
  return shadow_root
############ 추가 끝

data_set = pd.read_csv('rottenscore.csv', encoding='utf8', header=None) #크롤링한 데이터 저장한 엑셀파일

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

author_title = []
author_score = []
movieurl = []


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

#실행시 가장 먼저 출력할 메인화면
class UIWindow(QWidget):

    #호출시 자동 실행되는 생성자
    def __init__(self, parent=None):


        super(UIWindow, self).__init__(parent)
#        QWidget.__init__(self, parent)

        self.resize(1400, 800)
        #화면 중앙에 윈도우가 위치하게 하는 함수 실행. 근데 고장남
        self.center()

        self.inputimg()

        #유저에게 입력받을 새 윈도우에 영화 레이블 8개
        self.nextbtn = QPushButton(self)
        self.nextbtn.setText(' 다 음 ')

        #입력받은 데이터를 바탕으로 유사도 계산 후 영화 추천할 것
        self.donebtn = QPushButton(self)
        self.donebtn.setText(' 완 료 ')

        #클릭시 영화점수 입력할 수 있는 기능 필요
        self.label1 = QLabel(self)
        #sorted_counttitle[0][0]을 로튼토마토에 검색해서 첫번쨰 이미지 크롤링 해야 함
        pixmap = QPixmap('C:\\Users\\quarkmos\\Desktop\\pyc\\poster\\poster1.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label1.setPixmap(QPixmap(pixmap))

        self.label2 = QLabel(self)
        pixmap = QPixmap('C:\\Users\\quarkmos\\Desktop\\pyc\\poster\\poster2.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.label2.setPixmap(QPixmap(pixmap))

        self.label3 = QLabel(self)
        pixmap = QPixmap('C:\\Users\\quarkmos\\Desktop\\pyc\\poster\\poster3.jpg')
        pixmap = pixmap.scaled(250, 250)
        self.label3.setPixmap(QPixmap(pixmap))

        self.label4 = QLabel(self)
        pixmap = QPixmap('C:\\Users\\quarkmos\\Desktop\\pyc\\poster\\poster4.jpg')
        pixmap = pixmap.scaled(250, 250)
        self.label4.setPixmap(QPixmap(pixmap))

        self.label5 = QLabel(self)
        pixmap = QPixmap('C:\\Users\\quarkmos\\Desktop\\pyc\\poster\\poster5.jpg')
        pixmap = pixmap.scaled(250, 250)
        self.label5.setPixmap(QPixmap(pixmap))

        self.label6 = QLabel(self)
        pixmap = QPixmap('C:\\Users\\quarkmos\\Desktop\\pyc\\poster\\poster6.jpg')
        pixmap = pixmap.scaled(250, 250)
        self.label6.setPixmap(QPixmap(pixmap))

        self.label7 = QLabel(self)
        pixmap = QPixmap('C:\\Users\\quarkmos\\Desktop\\pyc\\poster\\poster7.jpg')
        pixmap = pixmap.scaled(250, 250)
        self.label7.setPixmap(QPixmap(pixmap))

        self.label8 = QLabel(self)
        pixmap = QPixmap('C:\\Users\\quarkmos\\Desktop\\pyc\\poster\\poster8.jpg')
        pixmap = pixmap.scaled(250, 250)
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

    def inputimg(self):

        base_url = 'https://www.rottentomatoes.com/search?search='

        n = 1
        for i in range(len(sorted_counttitle)):
            if n == 8:
                break

            key_url = sorted_counttitle[i][0]
            url = base_url + quote_plus(key_url)

            driver.get(url)
            root1 = driver.find_element_by_tag_name('search-result-container')
            shadow_root1 = expand_shadow_element(root1)

            root2 = shadow_root1.find_element_by_css_selector('search-result + *')
            shadow_root2 = expand_shadow_element(root2)

            root3 = shadow_root2.find_element_by_css_selector('media-row')
            shadow_root3 = expand_shadow_element(root3)

            imgurl = shadow_root3.find_element_by_css_selector('img').get_attribute('src')

            #이미지 리사이즈 크기 변경 > 화질개선
            imgurl = imgurl.replace('80x126', '320x512')

            urllib.request.urlretrieve(imgurl, './poster/poster' + str(n) + '.jpg')
            n = n + 1



#done버튼 누르면 출력되는 화면 // 영화 추천 결과 출력
class recWindow(QWidget):

    def __init__(self, parent=None):

        super(recWindow, self).__init__(parent)

        self.resize(1400, 800)

        #새로운 윈도우 출력 할 것, 추천할 영화 9~16순위
        self.recnextbtn = QPushButton(self)
        self.recnextbtn.setText(' 다 음 ')

        #이전 화면 출력
        self.recexbtn = QPushButton(self)
        self.recexbtn.setText(' 이 전 ')

        self.imgsaver()

        #첫번째 추천 영화
        self.reclabel1 = QLabel(self)
        #sorted_rank_dict[0][0]로튼토마토에 검색 후 첫번째 포스터
        pixmap = QPixmap('C:\\Users\\quarkmos\\Desktop\\pyc\\images\\img1.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel1.setPixmap(QPixmap(pixmap))

        self.reclabel2 = QLabel(self)
        pixmap = QPixmap('C:\\Users\\quarkmos\\Desktop\\pyc\\images\\img2.jpg')
        pixmap = pixmap.scaled(205, 305)
        self.reclabel2.setPixmap(QPixmap(pixmap))

        self.reclabel3 = QLabel(self)
        pixmap = QPixmap('C:\\Users\\quarkmos\\Desktop\\pyc\\images\\img3.jpg')
        pixmap = pixmap.scaled(250, 250)
        self.reclabel3.setPixmap(QPixmap(pixmap))

        self.reclabel4 = QLabel(self)
        pixmap = QPixmap('C:\\Users\\quarkmos\\Desktop\\pyc\\images\\img4.jpg')
        pixmap = pixmap.scaled(250, 250)
        self.reclabel4.setPixmap(QPixmap(pixmap))

        self.reclabel5 = QLabel(self)
        pixmap = QPixmap('C:\\Users\\quarkmos\\Desktop\\pyc\\images\\img5.jpg')
        pixmap = pixmap.scaled(250, 250)
        self.reclabel5.setPixmap(QPixmap(pixmap))

        self.reclabel6 = QLabel(self)
        pixmap = QPixmap('C:\\Users\\quarkmos\\Desktop\\pyc\\images\\img6.jpg')
        pixmap = pixmap.scaled(250, 250)
        self.reclabel6.setPixmap(QPixmap(pixmap))

        self.reclabel7 = QLabel(self)
        pixmap = QPixmap('C:\\Users\\quarkmos\\Desktop\\pyc\\images\\img7.jpg')
        pixmap = pixmap.scaled(250, 250)
        self.reclabel7.setPixmap(QPixmap(pixmap))

        self.reclabel8 = QLabel(self)
        pixmap = QPixmap('C:\\Users\\quarkmos\\Desktop\\pyc\\images\\img8.jpg')
        pixmap = pixmap.scaled(250, 250)
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
        reclayout.addWidget(self.recexbtn, 2, 1)
        reclayout.addWidget(self.recnextbtn, 2, 2)

        clickable(self.reclabel1).connect(self.linkurl1)
        clickable(self.reclabel2).connect(self.linkurl2)
        clickable(self.reclabel3).connect(self.linkurl3)
        clickable(self.reclabel4).connect(self.linkurl4)
        clickable(self.reclabel5).connect(self.linkurl5)
        clickable(self.reclabel6).connect(self.linkurl6)
        clickable(self.reclabel7).connect(self.linkurl7)
        clickable(self.reclabel8).connect(self.linkurl8)


    def linkurl1(self):
        url = movieurl[0]
        webbrowser.open(url)

    def linkurl2(self):
        url = movieurl[1]
        webbrowser.open(url)

    def linkurl3(self):
        url = movieurl[2]
        webbrowser.open(url)

    def linkurl4(self):
        url = movieurl[3]
        webbrowser.open(url)

    def linkurl5(self):
        url = movieurl[4]
        webbrowser.open(url)

    def linkurl6(self):
        url = movieurl[5]
        webbrowser.open(url)

    def linkurl7(self):
        url = movieurl[6]
        webbrowser.open(url)

    def linkurl8(self):
        url = movieurl[7]
        webbrowser.open(url)

    #유사도 가장 높은 3명의 영화 포스터 이미지 크롤링, 점수 높은 순으로 미구현
    def imgsaver(self):
        global  rank_dict, author_title, author_score, movieurl
        rank_dict = dict()
        for item in rank_df:
            for title in item['Title']:
                author_title.append(title)
            for score in item['Score']:
                author_score.append(score)
        for i in range(len(author_title)):
            rank_dict[author_title[i]] = int(author_score[i])

        sorted_rank_dict = sorted(rank_dict.items(), key=operator.itemgetter(1), reverse=True)

        base_url = 'https://www.rottentomatoes.com/search?search='

        n = 1
        for i in range(len(sorted_rank_dict)):
            if n == 8:
                break

            key_url = sorted_rank_dict[i][0]
            url = base_url + quote_plus(key_url)

            driver.get(url)
            root1 = driver.find_element_by_tag_name('search-result-container')
            shadow_root1 = expand_shadow_element(root1)

            root2 = shadow_root1.find_element_by_css_selector('search-result + *')
            shadow_root2 = expand_shadow_element(root2)

            root3 = shadow_root2.find_element_by_css_selector('media-row')
            shadow_root3 = expand_shadow_element(root3)

            movielink = shadow_root3.find_element_by_css_selector('a').get_attribute('href')
            imgurl = shadow_root3.find_element_by_css_selector('img').get_attribute('src')

            #이미지 리사이즈 크기 변경 > 화질개선
            imgurl = imgurl.replace('80x126', '320x512')

            urllib.request.urlretrieve(imgurl, './images/img' + str(n) + '.jpg')
            movieurl.append(movielink)
#            print(movielink)

            n = n + 1

        return rank_dict, author_title, author_score, movieurl


#테스트용
class UIToolTab(QWidget):
    def __init__(self, parent=None):
        super(UIToolTab, self).__init__(parent)
        self.CPSBTN = QPushButton("text2", self)
        self.CPSBTN.move(100, 350)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(50, 50, 400, 450)
        self.setFixedSize(1200, 800)
        self.startUIWindow()

    #테스트용
    def gopage2(self):
        self.ToolTab = UIToolTab(self)
        self.setWindowTitle("UIToolTab")
        self.setCentralWidget(self.ToolTab)
        self.ToolTab.CPSBTN.clicked.connect(self.startUIWindow)
        self.show()

    def showresult(self):
        self.Window = recWindow(self)
        self.setWindowTitle('result')
        self.setCentralWidget(self.Window)
        self.show()

    def startUIWindow(self):
        self.Window = UIWindow(self)
        self.setWindowTitle("UIWindow")
        self.setCentralWidget(self.Window)
        self.Window.nextbtn.clicked.connect(self.gopage2)
        self.Window.donebtn.clicked.connect(self.simrank)
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
        print(temp)

        return rank_name, rank_temp, rank_df

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())