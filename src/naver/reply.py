
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
options.add_argument("headless") ## 크롤링 창 보이게 하려면 주석 처리
options.add_argument('--window-size=1920, 1080')
options.add_argument('--no-sandbox')
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--start-maximized') 
options.add_argument('--start-fullscreen') ## 전체 화면 없애려면 주석 처리
options.add_argument('--disable-blink-features=AutomationControlled')

class Reply:
    def __init__(self, save_path, week, no, titleId):
        self.url = f'https://comic.naver.com/webtoon/detail?titleId={titleId}&no={no}&week={week}'
        self.save_path = save_path + f'{titleId}/{no}/'

    # def get_bestreply(self):
    #     driver = webdriver.Chrome(service=Service(), options=options)
    #     driver.get(self.url)
    
    #     bestreply_list = []
        
    #     for i in range(1, 16):
    #         xpath = f'//*[@id="cbox_module_wai_u_cbox_content_wrap_tabpanel"]/ul/li[{i}]/div[1]/div/div[2]/span[2]'
    #         element = self.__wait_until_find(driver, xpath)
    #         print(element.text)
            
    #         bestreply_list.append(element.text)
            
    #     self.save_csv(bestreply_list)
    #     driver.quit()
    
    def get_reply(self):
        ## Selenium
        driver = webdriver.Chrome(service=Service(), options=options)
        driver.get(self.url)
        
        ## BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        ## BEST 댓글 저장
        content_list = soup.find_all('span', attrs={'class': "u_cbox_contents"})
        self.save_csv("bestreply.csv", content_list)
        
        ## 전체댓글 클릭
        action = ActionChains(driver)
        element = self.__wait_until_find(driver, '//*[@id="cbox_module_wai_u_cbox_content_wrap_tabpanel"]')
        action.move_to_element(element).click().perform()
        self.__wait_and_click(driver, '//*[@id="cbox_module_wai_u_cbox_sort_option_tab2"]/span[2]')
        
        time.sleep(0.1)
        
        ## BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        ## 전체 댓글 수
        entire_reply_num = int(soup.find('span', attrs={'class': 'u_cbox_count'}).string.replace(',', ''))
        
        while True:
            try:
                ## 더보기 클릭
                element = self.__wait_until_find(driver, '//*[@id="cbox_module"]/div/div[7]/a/span/span/span[1]')
                action.move_to_element(element).click().perform()
                self.__wait_and_click(driver, '//*[@id="cbox_module"]/div/div[7]/a/span/span/span[1]')
                time.sleep(0.1)
            except:
                soup = BeautifulSoup(driver.page_source, 'lxml')
                break
        
        ## 댓글 크롤링
        content_list = soup.find_all('span', attrs={'class': "u_cbox_contents"})
        print(len(content_list))
        
        ## csv 저장
        self.save_csv("allreply.csv", content_list)
        
        driver.quit()

        
    def save_csv(self, filename, reply_list):
        if not os.path.exists(os.path.dirname(self.save_path + filename)):
            os.makedirs(os.path.dirname(self.save_path + filename))
    
        with open(self.save_path+filename, 'w', newline='') as f:
            wr = csv.writer(f)
            wr.writerow(['reply'])
            for reply in reply_list:
                wr.writerow([reply.string])  
    
if __name__ == '__main__':
    reply = Reply('data/reply/', 'fri', '1', '651673')
    reply.get_reply()