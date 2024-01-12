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

class Namu:
    def __init__(self, save_path):
        self.url = 'https://namu.wiki/w/%EB%A7%88%EB%A3%A8%EB%8A%94%20%EA%B0%95%EC%A5%90/%EB%93%B1%EC%9E%A5%EC%9D%B8%EB%AC%BC'
        self.save_path = save_path
    
    def __wait_until_find(self, driver, xpath):
        WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.XPATH, xpath)))
        element = driver.find_element(By.XPATH, xpath)
        return element
            
    def __wait_and_click(self, driver, xpath):
        WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        button = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", button)

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
    
    def get_info(self):
        ## Selenium
        driver = webdriver.Chrome(service=Service(), options=options)
        driver.get(self.url)
        
        ## BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        print(soup.get_text())
        
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
    
    save_path = 'data/namu/data.csv'
    
    crawler = Namu(save_path)
    # crawler.get_bestreply()
    crawler.get_info()