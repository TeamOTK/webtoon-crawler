from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
import requests
import csv
import os
import logging
import time
from dataclass_csv import DataclassWriter
from model.reply import Reply
from model.webtoon import Webtoon
class Driver:
    def __init__(self):
        pass

    def wait_until_find_xpath(self, driver, xpath):
        WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.XPATH, xpath)))
        element = driver.find_element(By.XPATH, xpath)
        return element
    
    def wait_until_find_classname(self, driver, classname):
        WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.CLASS_NAME, classname)))
        element = driver.find_element(By.CLASS_NAME, classname)
        return element
        
    def wait_and_click_xpath(self, driver, xpath):
        WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        button = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", button)
        
    def wait_and_click_classname(self, driver, classname):
        WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.CLASS_NAME, classname)))
        button = driver.find_element(By.CLASS_NAME, classname)
        driver.execute_script("arguments[0].click();", button)
        
    def click_escape_key(self, driver):
        try:
            action = ActionChains(driver)
            action.send_keys(Keys.ESCAPE).perform()
        except:
            print("Click Error")
    
    def save_webtoon_csv(self, webtoon, f):
        w = DataclassWriter(f, webtoon, Webtoon)
        w.write(skip_header=True)
        
    def save_reply_csv(self, reply, f):
        w = DataclassWriter(f, reply, Reply)
        w.write(skip_header=True)
        

    def open_file(self, save_dir, file_name, columns):
        if not os.path.exists(os.path.dirname(save_dir + file_name)):
            os.makedirs(os.path.dirname(save_dir + file_name))
        # ex) save_dir="data/webtoon"  file_name="info.csv"
        f = open(save_dir+file_name, 'w', encoding='utf-8', newline='') 
        writer = csv.writer(f)
        writer.writerow(columns)
        return f
    
    def set_driver(self, options):
        driver = webdriver.Chrome(service=Service(), options=options)
        return driver
    
    def set_log(self, site_name):
        dir_path='../log/'+site_name
        datetime=time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime())
        if not os.path.isdir(dir_path): 
            os.makedirs(dir_path)
            
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(dir_path+datetime+'.log')
        logger.addHandler(file_handler)