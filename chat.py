from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import BaseOutputParser
import os
from dotenv import load_dotenv
import csv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class Chat:
    
    def __init__(self, crawl_list):
        self.crawl_list = crawl_list
        
    def titleId_to_title(self, titleId):
        if titleId == 703844:
            return '가비지타임'
        elif titleId == 735661:
            return '재혼 황후'
        elif titleId == 769209:
            return '화산귀환'
    
    def get_csv(self):
        reply = {
            '가비지타임': {},
            '재혼 황후': {},
            '화산귀환': {}
        }
        for crawl in self.crawl_list:
            week = crawl['week']
            no = crawl['no']
            titleId = crawl['titleId']
            
            allreply_path = f'data/{titleId}/{no}/allreply.csv'
            bestreply_path = f'data/{titleId}/{no}/bestreply.csv'
            
            reply[self.titleId_to_title(titleId)][no] = ''
            
            with open(bestreply_path, 'r', newline='') as f:
                csv_reader = csv.reader(f)
                header = next(csv_reader)
                for row in csv_reader:
                    reply[self.titleId_to_title(titleId)][no] += row[0]
            
            # cnt = 0
            # with open(allreply_path, 'r', newline='') as f:
            #     csv_reader = csv.reader(f)
            #     header = next(csv_reader)
            #     for row in csv_reader:
            #         reply[self.titleId_to_title(titleId)][no] += row[0]
            #         cnt += 1
            #         if cnt == 3:
            #             break
        # print(reply)         
        return reply
            
    def run(self):
        template = """
        사용자가 웹툰 내용에 대한 질문을 하면, 무슨 회차인지 사용자에게 설명해줘.
        데이터는 중첩 딕셔너리로 제공되고, 웹툰의 제목이 키, 그 안의 딕셔너리의 키는 웹툰 회차, 값은 웹툰 회차에 대한 내용이 있어. 
        내용을 바탕으로 해당 웹툰의 회차를 찾아서 사용자에게 알려줘
        질문:{question} 데이터:{data}"""
        
        prompt = PromptTemplate.from_template(template)
        chat_model = ChatOpenAI(
            # model="gpt-3.5-turbo-1106",
            model="gpt-3.5-turbo-16k-0613",
            temperature=0,
            openai_api_key=OPENAI_API_KEY)
        
        message = chat_model.predict(prompt.format(
            question="청명이가 싸우는 회차가 뭐지?",
            data=self.get_csv()))
        print(message)
        
    
if __name__ == '__main__':
    
    crawl_list = [
        # 가비지타입 최근 5화
        # {
        #     'week': 'sun',
        #     'no': 202,
        #     'titleId': 703844
        # },
        # {
        #     'week': 'sun',
        #     'no': 201,
        #     'titleId': 703844
        # },
        # {
        #     'week': 'sun',
        #     'no': 200,
        #     'titleId': 703844
        # },
        {
            'week': 'sun',
            'no': 199,
            'titleId': 703844
        },
        {
            'week': 'sun',
            'no': 198,
            'titleId': 703844
        },
        {
            'week': 'sun',
            'no': 197,
            'titleId': 703844
        },
        # {
        #     'week': 'sun',
        #     'no': 196,
        #     'titleId': 703844
        # },
        # {
        #     'week': 'sun',
        #     'no': 195,
        #     'titleId': 703844
        # },
        # {
        #     'week': 'sun',
        #     'no': 194,
        #     'titleId': 703844
        # },
        # {
        #     'week': 'sun',
        #     'no': 193,
        #     'titleId': 703844
        # },
        # 재혼 황후 최근 5화
        # {
        #     'week': 'fri',
        #     'no': 167,
        #     'titleId': 735661
        # },
        # {
        #     'week': 'fri',
        #     'no': 166,
        #     'titleId': 735661
        # },
        {
            'week': 'fri',
            'no': 165,
            'titleId': 735661
        },
        {
            'week': 'fri',
            'no': 164,
            'titleId': 735661
        },
        {
            'week': 'fri',
            'no': 163,
            'titleId': 735661
        },
        # {
        #     'week': 'fri',
        #     'no': 162,
        #     'titleId': 735661
        # },
        # {
        #     'week': 'fri',
        #     'no': 161,
        #     'titleId': 735661
        # },
        # {
        #     'week': 'fri',
        #     'no': 160,
        #     'titleId': 735661
        # },
        # {
        #     'week': 'fri',
        #     'no': 159,
        #     'titleId': 735661
        # },
        # {
        #     'week': 'fri',
        #     'no': 158,
        #     'titleId': 735661
        # },
        # 화산 귀환 최근 5화
        {
            'week': 'wed',
            'no': 102,
            'titleId': 769209
        },
        {
            'week': 'wed',
            'no': 101,
            'titleId': 769209
        },
        {
            'week': 'wed',
            'no': 100,
            'titleId': 769209
        },
        {
            'week': 'wed',
            'no': 99,
            'titleId': 769209
        },
        {
            'week': 'wed',
            'no': 98,
            'titleId': 769209
        },
        # {
        #     'week': 'wed',
        #     'no': 97,
        #     'titleId': 769209
        # },
        # {
        #     'week': 'wed',
        #     'no': 96,
        #     'titleId': 769209
        # },
        # {
        #     'week': 'wed',
        #     'no': 95,
        #     'titleId': 769209
        # },
        # {
        #     'week': 'wed',
        #     'no': 94,
        #     'titleId': 769209
        # },
        # {
        #     'week': 'wed',
        #     'no': 93,
        #     'titleId': 769209
        # },
    ]
    chat = Chat(crawl_list)
    chat.run()  