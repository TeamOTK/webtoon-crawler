
from bs4 import BeautifulSoup
import os
import warnings
from tqdm import tqdm
import time
import csv
from csv import writer

from common.driver import Driver
from model.webtoon import Webtoon


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