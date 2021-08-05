import requests
import json
from db_model import mysql
import pymysql
from decouple import config

import os
from urllib.request import urlopen
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains

class Writer:

    @staticmethod
    def post_writer():
        db = pymysql.connect(host=config('host'),port=3306,user=config('user'),passwd=config('passwd'),db=config('db'),charset='utf8mb4')
        db_cursor = db.cursor()

        #crawling
        options = Options()
        options.add_argument('start-maximized')
        options.add_argument('disable-infobars')
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches",["enable-automation"])
        driver = webdriver.Chrome(options=options, executable_path='/Users/zogak/chromedriver')

        try:
            pageNum = 41
            i=1
            while(True):
                if pageNum == 51:
                    break
                url = f'http://www.yes24.com/24/AuthorFile/AuthorGroup/001?SortGb=01&domainGb=01&fieldGb=01&Type=EX&PageNumber={pageNum}'
                driver.get(url)
            
                nameNum = 2*i
                each = driver.find_element_by_css_selector(f'#wrapperContent > table > tbody > tr > td > table > tbody > tr > td:nth-child(2) > table:nth-child(5) > tbody > tr:nth-child({nameNum}) > td.txt10p > a:nth-child(1)')
                actions = ActionChains(driver).move_to_element(each).click()
                actions.perform()
                
                writerName = driver.find_element_by_css_selector('#wrapperContent > table > tbody > tr > td > table > tbody > tr > td:nth-child(2) > table:nth-child(3) > tbody > tr:nth-child(1) > td > table > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(1) > td > span:nth-child(1)')
                author = writerName.text
                #print(author)
                writerInfo = driver.find_element_by_class_name('txt150')
                authorInfo = writerInfo.text
                #print(authorInfo)

                db_cursor.execute("INSERT INTO Author (name, description) VALUES (%s,%s)", (author, authorInfo))

                i = i+1
                if i>20:
                    i=1
                    pageNum = pageNum + 1
                driver.back()
        
        except Exception as e:
            print(e)

        db.commit()
        db_cursor.close()


    @staticmethod
    def get_writer():
        mysql_db = mysql.conn_mysqldb()
        db_cursor = mysql_db.cursor()
        #sql = "SELECT * FROM Author LIMIT 3"
        sql = "SELECT COUNT(*) FROM Author"
        db_cursor.execute(sql)
        authors = db_cursor.fetchall()
        if not authors:
            return None
        return authors

if __name__ == '__main__':

    #Writer().post_writer()
    res = Writer().get_writer()
    print(res)

    #8/5 국내문학작가 825명