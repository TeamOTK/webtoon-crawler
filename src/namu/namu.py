from bs4 import BeautifulSoup
import os
from tqdm import tqdm
import time
import csv
from csv import writer
import pandas as pd

from common.driver import Driver
from model.namu import Namu

class NamuCrawler:
    def __init__(self, driver, save_dir, file_name):
        self.namu_url = 'https://namu.wiki'
        self.driver = driver
        self.save_dir = save_dir
        self.file_name = file_name
        self.f = Driver().open_file(save_dir=save_dir, file_name=file_name, columns=['id', 'link', 'title', 'author', 'genre', 'description', 'status', 'character', 'setting', 'evaluation'])
    
    def get_namu(self, url):
        ## Selenium
        self.driver.get(url)
        time.sleep(0.5)
        
        ## BeautifulSoup
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        time.sleep(0.5)
        
        url_dic = {}
        namu_dic = {'개요': '', '줄거리': '', '장르': '', '연재 현황': '', '등장인물': '', '설정': '', '평가': ''}
        
        ## 목차
        content_list = soup.find_all('span', attrs={'class': 'li7j6V-c'})
        for index, content in enumerate(content_list):
            if "개요" in content.get_text():
                url_dic['개요'] = {
                    "index": index,
                    "link": self.find_linking(content)
                }
                    
            elif "줄거리" in content.get_text():
                url_dic['줄거리'] = {
                    "index": index,
                    "link": self.find_linking(content)
                }
            
            elif "연재 현황" in content.get_text():
                url_dic['연재 현황'] = {
                    "index": index,
                    "link": self.find_linking(content)
                }
                
            elif "등장인물" in content.get_text():
                url_dic['등장인물'] ={
                    "index": index,
                    "link": self.find_linking(content)
                }
            
            elif "설정" in content.get_text():
                url_dic['설정'] = {
                    "index": index,
                    "link": self.find_linking(content)
                }
            
            elif "평가" or "비판" in content.get_text():
                url_dic['평가'] = {
                    "index": index,
                    "link": self.find_linking(content)
                }
                
        ## 장르
        namu_dic["장르"] = soup.find_all('div', attrs={'class': '_1TSYs3S7'})[12].get_text().replace(" ", "")
        
        ## 데이터 크롤링 
        for content in url_dic:
            print(content)
            if url_dic[content]['link'] == "":
                self.driver.get(url)
                time.sleep(1)
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                time.sleep(0.5)
                ## 특정 부분만 가져오기
                namu_dic[content] = soup.find_all('div', attrs={'class': 'p+q8IHhu'})[url_dic[content]['index']].get_text()
                
            else:
                self.driver.get(self.namu_url + url_dic[content]['link'])
                time.sleep(1)
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                time.sleep(0.5)
                ## 다 가져오기
                namu_dic[content] = soup.find('div', attrs={'class': 'pneixiEB'}).get_text()
            # print(namu_dic[content])
        
        # print(namu_dic)       
        return namu_dic
                
        
        
    def find_webtoon(self, title):
        info = pd.read_csv('data/webtoon/info.csv', encoding='utf-8')
        webtoon = info[info['title'] == title]
        return webtoon
    
    def find_linking(self, content):
        if content.find('a', attrs={'class': 'o4Hi0yj0'}) is None:
            return ""
        else:
            return content.find('a', attrs={'class': 'o4Hi0yj0'})['href']
        
    def save_csv(self, title_list, url_list):
        
        namu_model = []
        
        for title, url in tqdm(zip(title_list, url_list)):
            print(title, url)
            webtoon = self.find_webtoon(title)
            namu = self.get_namu(url)
            namu_model.append(Namu(
                id=int(webtoon['id'].to_string(index=False)),
                link=webtoon['link'].to_string(index=False),
                title=webtoon['title'].to_string(index=False),
                author=webtoon['author'].to_string(index=False),
                genre=webtoon['genre'].to_string(index=False) + "," + namu["장르"],
                description=webtoon['description'].to_string(index=False) + "\n" + namu["개요"] + "\n" + namu["줄거리"],
                status=namu["연재 현황"],
                character=namu["등장인물"],
                setting=namu["설정"],
                evaluation=namu["평가"]
            ))
        
        Driver().save_namu_csv(namu_model, self.f)
        self.driver.quit()
        
        
    
if __name__ == '__main__':
    ## 화산귀환, 신의탑, 외모지상주의, 나이트런, 전지적 독자 시점, 재혼황후, 가비지타임, 내일, 삼국지톡, 놓지마 정신줄
    namu = Namu(Driver().set_driver(), 'data/webtoon/', 'namu.csv')