from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain
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
    
    def get_csv(self):
        reply = ""
        for crawl in self.crawl_list:
            week = crawl['week']
            no = crawl['no']
            titleId = crawl['titleId']
            
            path = f'data/{week}/{no}/{titleId}.csv'
            
            with open(path, 'r', newline='') as f:
                csv_reader = csv.reader(f)
            
                header = next(csv_reader)
                # print(f'헤더: {header}')
                # 나머지 행은 데이터
                for row in csv_reader:
                    reply += row[0] + "\n"
                    
        return reply
    
    class CommaSeparatedListOutputParser(BaseOutputParser):
        """LLM 아웃풋에 있는 ','를 분리해서 리턴하는 파서."""
        def parse(self, text: str):
            return text.strip().split(", ")

    def parse(self, text: str):
        return text.strip().split(", ")
            
    def run(self):
        template = """
        너는 웹툰 작가에게 전달하기 위해 독자들의 댓글을 요약해주는 AI야
        너는 <{reply}> 를 요약해서 키워드 5개 나열해야 해.
        이때 각 키워드는 반드시 comma(,)로 분리해서 대답해주고, 이외의 말은 하지 마.
        질문:"""
        
        system_message_prompt = SystemMessagePromptTemplate.from_template(
            template)
        human_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        
        chain = LLMChain(
            llm=ChatOpenAI(openai_api_key = OPENAI_API_KEY),
            prompt=chat_prompt,
            output_parser=self.CommaSeparatedListOutputParser()
        )
        chain.run()
    
if __name__ == '__main__':
    
    crawl_list = [
        {
            'week': 'sun',
            'no': 202,
            'titleId': 703844
        }
    ]
    
    chat = Chat(crawl_list)
    chat.run()  