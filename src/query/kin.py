from bs4 import BeautifulSoup
import lxml
import os
import warnings
from tqdm import tqdm
import time
import csv
from csv import writer
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains

warnings.filterwarnings('ignore')
options = Options()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
## for background
# options.add_argument("headless") ## 크롤링 창 보이게 하려면 주석 처리
options.add_argument('--window-size=1920, 1080')
options.add_argument('--no-sandbox')
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--start-maximized') 
options.add_argument('--start-fullscreen') ## 전체 화면 없애려면 주석 처리
options.add_argument('--disable-blink-features=AutomationControlled')

class Kin:
    def __init__(self, save_path):
        self.search_url = 'https://kin.naver.com/search/list.nhn?sort=none&section=kin&query=%EC%9B%B9%ED%88%B0%20%EC%B0%BE%EC%95%84&period=all&page='
        self.save_path = save_path
    
    def __wait_until_find(self, driver, xpath):
        WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.XPATH, xpath)))
        element = driver.find_element(By.XPATH, xpath)
        return element
            
    def __wait_and_click(self, driver, xpath):
        WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        button = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", button)
    
    def get_kin(self):
        ## Selenium
        driver = webdriver.Chrome(service=Service(), options=options)
        driver.get(self.search_url + '1')
        time.sleep(0.2)
        
        ## BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        ## csv 해더 생성
        if not os.path.exists(os.path.dirname(self.save_path + "kin_old2.csv")):
            os.makedirs(os.path.dirname(self.save_path + "kin_old2.csv"))
    
        with open(self.save_path+"kin_old2.csv", 'w', newline='') as f:
            wr = csv.writer(f)
            wr.writerow(['title', 'content', 'answer', 'link'])
        
            ## 전체 데이터 수
            entire_num = int(soup.select_one('#s_content > div.section > h2 > span > em').string.split('/')[1].replace(',', ''))
            
            ## 전체 페이지 수
            entire_page = entire_num // 10 + 1
            
            ## 제목, 링크 크롤링
            # for i in tqdm(range(1, entire_page+1), desc='search page'):
            
            ## 최대 100까지만 됨..ㅜㅠ
            for i in tqdm(range(1, 101), desc='search page'):
                driver.get(self.search_url + str(i))
                time.sleep(0.2)
                soup = BeautifulSoup(driver.page_source, 'lxml')
                
                title_list = soup.find_all('a', attrs={'class': "_nclicks:kin.txt _searchListTitleAnchor"})
                # print(len(title_list))
                ## csv 저장
                for title in title_list:
                    # print(title.get_text())
                    wr.writerow([title.get_text(), '', '', title['href']])
            
        with open(self.save_path+"kin_old2.csv", 'r', newline='') as f:
            rdr = csv.reader(f)
            
            ## csv 해더 생성
            if not os.path.exists(os.path.dirname(self.save_path + "kin2.csv")):
                os.makedirs(os.path.dirname(self.save_path + "kin2.csv"))
            
            with open(self.save_path+"kin2.csv", 'w', newline='') as f2:
                wr = csv.writer(f2)
                wr.writerow(['title', 'content', 'answer', 'link'])
                ## 내용, 답변 크롤링
                for line in tqdm(rdr, desc='detail page'):
                    if line[3] == 'link':
                        continue
                    driver.get(line[3])
                    time.sleep(0.2)
                    soup = BeautifulSoup(driver.page_source, 'lxml')
                    
                    title = soup.find('div', attrs={'class': 'c-heading__title'})
                    content = soup.find('div', attrs={'class': 'c-heading__content'})
                    answer = soup.find('div', attrs={'class': 'c-heading-answer__content-user'})

                    #content > div.question-content > div > div.c-heading._questionContentsArea.c-heading--default-old > div.c-heading__title
                    
                    title = title.get_text().replace("\n", "").replace("\t", "") if title else ''
                    content = content.get_text().replace("\n", "").replace("\t", "") if content else ''
                    answer = answer.get_text().replace("\n", "").replace("\t", "") if answer else ''
                    
                    wr.writerow([title, content, answer, line[3]])
                
    
if __name__ == '__main__':
    
    save_path = 'data/query/'
    
    kin = Kin(save_path)
    kin.get_kin()
    
    