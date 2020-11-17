from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import parmap
from multiprocessing import cpu_count, freeze_support
from urllib.parse import quote_plus
import pandas as pd
import glob
import os

chromedriver = "chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument("lang=ko_KR") # 한국어!

alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z']
url = []
num_cores = cpu_count()

class crawling_score():

    def __init__(self):
        self.mapper()
        glober()

    def mapper(self):

        baseurl = 'https://www.rottentomatoes.com/critics/authors?letter='
        for i in range(len(alpha)):
            realurl = baseurl + quote_plus(alpha[i])
            url.append(realurl)
        parmap.map(self.crawler, url, pm_pbar=True, pm_processes=num_cores)

    def crawler(self, url):

        driver = webdriver.Chrome('./chromedriver.exe', options=options)
        driver.get(url)
        alphabet = url[-1:]
        xl = open('./csvfiles/critic_' + alphabet + '.csv', 'w', -1, 'utf-8', newline='')
        wr = csv.writer(xl)
        try:

            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            info = soup.find_all('li', {'class': 'critics__list-item'})  # 저자의 정보

            for item in info:
                url = item.find('a')  # 저자의 이름과 url을 가지고있음
                href = url.get('href')  # href에 있는 url만 가져옴
                name = href.strip('/critic/')
                name = name.strip()
                driver.get('https://www.rottentomatoes.com' + '{0}'.format(href))  # 저자의 url을 통해 드라이버에 저장

                author = driver.page_source
                soup = BeautifulSoup(author, 'html.parser')
                movieinfo = soup.find('tbody', {'id': 'review-table-body'}).find_all('tr')

                for tomato in movieinfo:
                    titletag = tomato.find('a')
                    title = titletag.text
                    if title == None:
                        title = 'NULLTITLE(NULL)'
                    titlei = title.find('(')
                    title = title[:titlei].strip()
                    score = tomato.find('td').text.strip()
                    rep_score = tomato.find('span', {'class': 'tMeterScore'})

                    if rep_score == None:
                        rep_score = '0'
                    else:
                        rep_score = rep_score.text.strip().replace('%', '')

                    if score == '':  # text로 받아왔기때문에 None이아님
                        score = rep_score

                    elif score == '0/4':
                        score = '0'
                    elif score == '0.5/4':
                        score = '13'
                    elif score == '1/4':
                        score = '25'
                    elif score == '1.5/4':
                        score = '38'
                    elif score == '2/4':
                        score = '50'
                    elif score == '2.5/4':
                        score = '63'
                    elif score == '3/4':
                        score = '75'
                    elif score == '3.5/4':
                        score = '88'
                    elif score == '4/4':
                        score = '100'
                    ############################################
                    elif score == '0/5':
                        score = '0'
                    elif score == '0.5/5':
                        score = '10'
                    elif score == '1/5':
                        score = '20'
                    elif score == '1.5/5':
                        score = '30'
                    elif score == '2/5':
                        score = '40'
                    elif score == '2.5/5':
                        score = '50'
                    elif score == '3/5':
                        score = '60'
                    elif score == '3.5/5':
                        score = '70'
                    elif score == '4/5':
                        score = '80'
                    elif score == '4.5/5':
                        score = '90'
                    elif score == '5/5':
                        score = '100'
                    ############################################
                    elif score == '0/10':
                        score = '0'
                    elif score == '0.5/10':
                        score = '5'
                    elif score == '1/10':
                        score = '10'
                    elif score == '1.5/10':
                        score = '15'
                    elif score == '2/10':
                        score = '20'
                    elif score == '3/10':
                        score = '30'
                    elif score == '3.5/10':
                        score = '35'
                    elif score == '4/10':
                        score = '40'
                    elif score == '4.5/10':
                        score = '45'
                    elif score == '5/10':
                        score = '50'
                    elif score == '5.5/10':
                        score = '55'
                    elif score == '6/10':
                        score = '60'
                    elif score == '6.5/10':
                        score = '65'
                    elif score == '7/10':
                        score = '70'
                    elif score == '7.5/10':
                        score = '75'
                    elif score == '8/10':
                        score = '80'
                    elif score == '8.5/10':
                        score = '85'
                    elif score == '9/10':
                        score = '90'
                    elif score == '9.5/10':
                        score = '95'
                    elif score == '10/10':
                        score = '100'
                        ############################################
                    elif score == 'F':
                        score = '0'
                    elif score == 'D-':
                        score = '16'
                    elif score == 'D':
                        score = '24'
                    elif score == 'D+':
                        score = '32'
                    elif score == 'C-':
                        score = '40'
                    elif score == 'C':
                        score = '48'
                    elif score == 'C+':
                        score = '56'
                    elif score == 'B-':
                        score = '63'
                    elif score == 'B':
                        score = '71'
                    elif score == 'B+':
                        score = '79'
                    elif score == 'A-':
                        score = '86'
                    elif score == 'A':
                        score = '93'
                    elif score == 'A+':
                        score = '100'
                    else:
                        score = '0'
                    ############################################

                    print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
                    wr.writerow([name, title, score])

        finally:
            print("############end############")
            driver.close()
            xl.close()

def glober():
    input_file = r'./csvfiles/'  # csv파일들이 있는 디렉토리 위치
    output_file = r'./csvfiles/rottenscore.csv'  # 병합하고 저장하려는 파일명

    allFile_list = glob.glob(os.path.join(input_file, 'critic_*'))  # glob함수로 sales_로 시작하는 파일들을 모은다
    allData = []  # 읽어 들인 csv파일 내용을 저장할 빈 리스트를 하나 만든다
    for file in allFile_list:
        df = pd.read_csv(file, encoding='utf8', header=None)  # for구문으로 csv파일들을 읽어 들인다
        allData.append(df)  # 빈 리스트에 읽어 들인 내용을 추가한다

    dataCombine = pd.concat(allData, axis=0, ignore_index=True)  # concat함수를 이용해서 리스트의 내용을 병합
    # axis=0은 수직으로 병합함. axis=1은 수평. ignore_index=True는 인데스 값이 기존 순서를 무시하고 순서대로 정렬되도록 한다.
    dataCombine.to_csv(output_file, index=False)  # to_csv함수로 저장한다. 인데스를 빼려면 False로 설정

def run():
    freeze_support()
    crawling_score()

if __name__ == '__main__':
    run()