from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import sys
import csv

driver = webdriver.Chrome('C:\\Users\\quarkmos\\Desktop\\pyc\\chromedriver.exe')  # chrome 85버전
xl = open('rottenscore.csv', 'w', -1, 'utf-8', newline='')
wr = csv.writer(xl)

# driver.get('https://www.rottentomatoes.com/critics/authors?letter=x')

#평론가마다 점수제 방식이 들락날락해서 만든 것
def convertscore(score):

    if score == '0/4':
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

    return score


try:

    #알파펫 순서로 한번에 크롤링 하고 싶었는데 잘안됨
    #어차피 크롤링 시간이 너무 오래걸려서 이건 크롤링한 후 엑셀파일만 따로 넣어야 할 것 같음
    author_alpha = 'a'

    #평론가 이름, 영화 제목, 영화 점수 크롤링
    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])

    author_alpha = 'b'

    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])

    author_alpha = 'c'

    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])

    author_alpha = 'd'

    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])

    author_alpha = 'e'

    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])

    author_alpha = 'f'

    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])

    author_alpha = 'g'

    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])

    author_alpha = 'h'

    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])

    author_alpha = 'i'

    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])

    author_alpha = 'j'

    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])

    author_alpha = 'k'

    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])

    author_alpha = 'l'

    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])

    author_alpha = 'm'

    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])

    author_alpha = 'n'

    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])

    author_alpha = 'o'

    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])

    author_alpha = 'p'

    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])

    author_alpha = 'q'

    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])

    author_alpha = 'r'

    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])

    author_alpha = 's'

    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])

    author_alpha = 't'

    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])

    author_alpha = 'u'

    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])

    author_alpha = 'v'

    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])

    author_alpha = 'w'

    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])

    author_alpha = 'x'

    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])

    author_alpha = 'y'

    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])

    author_alpha = 'z'

    for index in author_alpha:
        driver.get('https://www.rottentomatoes.com/critics/authors?letter={0}'.format(author_alpha))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "critics__list-item")))
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
            else:
                score = convertscore(score)


            ############################################

            print('Author : {:15}'.format(name) + 'Title : {:50}'.format(title) + 'Score : {:15}'.format(score))
            wr.writerow([name, title, score])


finally:
    print("############end############")


driver.close()
xl.close()




































