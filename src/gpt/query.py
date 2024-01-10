from langchain.chat_models import ChatOpenAI
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
import pandas as pd

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class Query:
    
    def __init__(self):
        pass
    
    def get_csv(self):
        with_kw_path = 'data/query/with_kw.csv'
        query_list = []
        
        cnt = 0
        
        with open(with_kw_path, 'r', newline='') as f:
            csv_reader = csv.reader(f)
            header = next(csv_reader)
            
            for row in csv_reader:
                # print(row)
                query_list.append([row[0].replace(" ", ""), row[1].replace(" ", ""), row[2].replace(" ", ""), row[4]])
                cnt += 1
                
                if cnt == 25:
                    break
        
        return query_list
    
    def run(self):
        template = """
        웹툰을 찾는 질문과 답변을 통해 웹툰 독자들이 웹툰을 찾기 위해 무슨 질문을 많이 하는 지 분석해줘.
        데이터는 2차원 배열로 제공되고, 질문 제목, 질문 내용, 대답, 키워드 순서로 있어. 
        데이터를 바탕으로 웹툰을 찾기 위해 챗봇과 대화하는 사용자의 질문을 예상해서 뽑아줘.
        예를 들어, 흑발 남주가 여행을 갔다가 여주에게 반하는 내용의 웹툰 찾아줘. 이런 식으로.
        질문:{question} 데이터:{data}"""
        
        prompt = PromptTemplate.from_template(template)
        chat_model = ChatOpenAI(
            # model="gpt-3.5-turbo-1106",
            model="gpt-3.5-turbo-16k-0613",
            temperature=1,
            openai_api_key=OPENAI_API_KEY)
        
        message = chat_model.predict(prompt.format(
            question="웹툰을 찾는 질문을 분석해줘.",
            data=self.get_csv()))
        print(message)
        
    
if __name__ == '__main__':
    
    query = Query()
    query.run()  