# pip install beautifulsoup4
# pip install requests
import os
from urllib import request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests
import time
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

def downloadGithub(accesUrl, headers, fname, path):
    try:   
        req2 = requests.get(accesUrl, headers=headers)
        soup2 = BeautifulSoup(req2.text, 'html.parser')    
        time.sleep(5)
        print('GitHub 접속')
        # download zip 버튼 클릭
        codeUrl = soup2.find_all('a', class_='d-flex flex-items-center color-fg-default text-bold no-underline')[-1]['href']
        zipUrl = 'https://github.com' + codeUrl
        print('code zip file url: '+ zipUrl)
        request.urlretrieve(zipUrl, path + '/' + fname + '.zip')
        time.sleep(5)
        print('코드 다운로드 완료\n')
    except Exception as e:
        print('Error:', e)
        pass


url = 'https://github.com/'
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}
path = '/home/gpuadmin/youngmi/youngmi/opensourcedata/github/'
heads = pd.read_csv('./muhayu/heads.csv', names=['sha','repository'])
new_heads = heads.iloc[10600:]
for head in new_heads['repository']:
    accessUrl = url + head
    fname = head.split('/')[-1]
    savepath = path + head

    req2 = requests.get(accessUrl, headers=headers)
    soup2 = BeautifulSoup(req2.text, 'html.parser')
    print('github url: '+ accessUrl)

    createFolder(savepath)
    downloadGithub(accessUrl, headers, fname, savepath)
