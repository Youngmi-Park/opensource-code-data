# pip install beautifulsoup4
# pip install requests
import os
from urllib import request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests
import time
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def createFolder(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print('Error: Creating directory. ' + path)
        return

def downloadPaper(soup, fname, path):
    try:
        pdfUrl = soup.find_all('a', class_='badge badge-light')[0]['href']
        print('pdf url: '+ pdfUrl)
        request.urlretrieve(pdfUrl, path + '/' + fname + '.pdf')
        print('논문 다운로드 완료\n')
    except Exception as e:
        print('Error:', e)
        pass

def downloadGithub(soup, headers, fname, path, writer):
    try:   
        gitUrl = soup.find_all('a', class_='code-table-link')[0]['href']
        print('github url: ' + gitUrl)
        user = gitUrl.split('/')[-2]
        project = gitUrl.split('/')[-1]
        newpath = f"{path}{user}/{project}"
        print(newpath)

        req2 = requests.get(gitUrl, headers=headers)
        soup2 = BeautifulSoup(req2.text, 'html.parser')    
        time.sleep(5)
        print('GitHub 접속')
        # download zip 버튼 클릭
        codeUrl = soup2.find_all('a', class_='d-flex flex-items-center color-fg-default text-bold no-underline')[-1]['href']
        zipUrl = 'https://github.com' + codeUrl
        print('code zip file url: '+ zipUrl)
        createFolder(newpath)
        savepath = f"{newpath}/{project}.zip"
        request.urlretrieve(zipUrl, savepath)
        time.sleep(5)
        print('코드 다운로드 완료\n')
        writer.writerow([user, project]) # csv 파일에 데이터 추가
        downloadPaper(soup, fname, newpath)
    except Exception as e:
        print('Error:', e)
        pass

url = 'https://paperswithcode.com' 
url2_list = ['https://paperswithcode.com', 'https://paperswithcode.com/top-social?num_days=30', 'https://paperswithcode.com/top-social?num_days=1']
#url2_list = ['https://paperswithcode.com/greatest', 'https://paperswithcode.com/latest', 'https://paperswithcode.com/top-social']

with open("/home/gpuadmin/youngmi/youngmi/opensourcedata/paperwithcode/github_urls.csv", "a", encoding='utf-8') as f:
    writer = csv.writer(f)
 #   writer.writerow(["user","project"])

    for url2 in url2_list:
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}
        path = '/home/gpuadmin/youngmi/youngmi/opensourcedata/paperwithcode/'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--single-process")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome('./chromedriver', options=chrome_options)
        driver.get(url2)
        prev_height = driver.execute_script("return document.body.scrollHeight")

# 웹페이지 맨 아래까지 무한 스크롤
        while True:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")     # 스크롤을 화면 가장 아래로 내린다
            time.sleep(3)    # 페이지 로딩 대기
            curr_height = driver.execute_script("return document.body.scrollHeight")    # 현재 문서 높이를 가져와서 저장

            if(curr_height == prev_height):
                break
            else:
                prev_height = driver.execute_script("return document.body.scrollHeight")


        html = driver.page_source #URL에 해당하는 페이지의 HTML를 가져옴
        soup1 = BeautifulSoup(html, 'html.parser')
        papers = soup1.find_all('a', class_='badge badge-light') # 모든 paper 버튼의 정보
        print(len(papers)) # 기본 열개, 스크롤내려서 추가로 목록이 display

        for h in papers:
            accesUrl = url + h['href'] # paper 버튼을 눌렀을 때 나오는 페이지 주소
            fname = h['href'].split('/')[-1]
            req2 = requests.get(accesUrl, headers=headers)
            soup2 = BeautifulSoup(req2.text, 'html.parser')
            print('access url: '+ accesUrl)

            downloadGithub(soup2, headers, fname, path, writer)
