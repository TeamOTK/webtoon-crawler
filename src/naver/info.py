
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import re

from common.driver import Driver
from model.webtoon import Webtoon

class Info:
    def __init__(self, driver, save_dir, file_name):
        self.save_dir = save_dir
        self.file_name = file_name
        self.url = f'https://comic.naver.com'
        self.driver = driver
        self.f = Driver().open_file(save_dir=save_dir, file_name="old_" + file_name, columns=['id', 'link', 'title', 'author', 'genre', 'description'])

    def get_webtoon_list(self):
        ## Selenium
        self.driver.get(self.url + '/webtoon')
        time.sleep(1)
        
        ## BeautifulSoup
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        
        ## 웹툰 리스트
        webtoon_list = soup.find_all('li', attrs={'class': 'DailyListItem__item--LP6_T'})
        
        webtoon_model = []
        
        ## title, href
        for webtoon in webtoon_list:
            title = webtoon.find('span', attrs={'class': 'ContentTitle__title--e3qXt'}).get_text()
            link = webtoon.find('a', attrs={'class': 'Poster__link--sopnC'})['href']
            id = re.sub(r'[^0-9]', '', link)
            
            # print(id, title, link)
            
            webtoon_model.append(Webtoon(
                id=id,
                link=link,
                title=title
            ))
            
            ## 중복 제거
            webtoon_model = list(set(webtoon_model))
        ## csv 저장
        Driver().save_webtoon_csv(webtoon_model, self.f)
        return webtoon_model
        
    def get_webtoon_info(self):
        
        webtoon_model = self.get_webtoon_list()
        update_webtoon_model = []
        
        for webtoon in tqdm(webtoon_model, desc='webtoon info'):
            ## Selenium
            self.driver.get(self.url + webtoon.link)
            time.sleep(1)
            
            ## BeautifulSoup
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            
            try:
                ## 작가
                author_list = soup.find_all('a', attrs={'class': 'ContentMetaInfo__link--xTtO6'})
                author = ""
                for a in author_list:
                    author += a.get_text() + ','
                author = author[:-1]
                ## 장르
                genre_list = soup.find_all('a', attrs={'class': 'TagGroup__tag--xu0OH'})
                genre = ""
                for g in genre_list:
                    genre += g.get_text().replace('#', '') + ','
                genre = genre[:-1]
                ## 설명
                description = soup.find('p', attrs={'class': 'EpisodeListInfo__summary--Jd1WG'}).get_text()
                
                webtoon.author = author
                webtoon.genre = genre
                webtoon.description = description
                
                # print(webtoon)
                
                update_webtoon_model.append(webtoon)
            except:
                print("Error")
                continue
        
        ## csv 저장
        # print(len(webtoon_model))
        # print(len(update_webtoon_model))
        self.f = Driver().open_file(save_dir=self.save_dir, file_name=self.file_name, columns=['id', 'link', 'title', 'author', 'genre', 'description'])
        Driver().save_webtoon_csv(update_webtoon_model, self.f)
        self.driver.quit()
    
if __name__ == '__main__':
    info = Info('data/webtoon/', 'info.csv')
    info.get_webtoon_info()
    