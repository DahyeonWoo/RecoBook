#from flask import request
import json.decoder
import pymysql
from decouple import config
from db_model import mysql
import csv

import os
from urllib.request import urlopen
import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains

class Review:
    
    @staticmethod
    def get_bookISBN():
        searchList=[]
        db = mysql.conn_mysqldb()
        cursor = db.cursor()
        sql = "SELECT isbn13 FROM Book"
        cursor.execute(sql)
        isbnNumbers = cursor.fetchall()
        for isbn in isbnNumbers:
            searchList.append(isbn[0])
        
        return searchList

    @staticmethod
    #리뷰페이지 한 쪽에서 리뷰 1개 가져오는 함수
    def oneReview(driver):
        #reviews = ''
        'review 블럭 찾기'
        reviewBlock = driver.find_element_by_id('infoset_reviewContentList')
        if reviewBlock:
            print('reviewBlock found')


        childNum = 3
        eachReview = reviewBlock.find_element_by_css_selector(f'div:nth-child({childNum}) > div.reviewInfoBot.crop > a')
        print('each review found')

        #더보기 누르고
        btnClick = ActionChains(driver).move_to_element(eachReview).click()
        btnClick.perform()
        print('successfully clicked btn')
        time.sleep(2)

        #내용가져오고
        reviewTxt = reviewBlock.find_element_by_css_selector(f'div:nth-child({childNum}) > div.reviewInfoBot.origin > div.review_cont')
        reviews = reviewTxt.text

        return reviews

    #여기까지

    @staticmethod
    def crawlReview(driver):
        reviewTemp = ''
        try:
            reviewPageNum = 4
            for i in range(4):
                print('review {} page'.format(i+1))
                reviewTemp = reviewTemp + Review.fiveReview(driver)
                nextReview = driver.find_element_by_css_selector(f'#infoset_reviewContentList > div.review_sort.sortBot > div.review_sortLft > div > a:nth-child({reviewPageNum})')
                if nextReview:
                    nextReviewClick = ActionChains(driver).move_to_element(nextReview).click()
                    nextReviewClick.perform()
                    time.sleep(10)
                    print('successfully clicked next page')
                    reviewPageNum = reviewPageNum + 1
            
            print("final reviews for one book:", reviewTemp)
    #         house.append([isbnNum,star,corpus])
    #         return house
            return reviewTemp
        
        except Exception as e:
            print(e)

    @staticmethod
    def reviewTable_to_db():
        db = pymysql.connect(host=config('host'),port=3306,user=config('user'),passwd=config('passwd'),db=config('db'),charset='utf8mb4')
        cur = db.cursor()
        
        bList = Review.get_bookISBN()

        chromedriver = '/Users/zogak/Downloads/chromedriver'
        driver = webdriver.Chrome(chromedriver)

        driver.get('http://www.yes24.com/main/default.aspx')

        howMany = len(bList)

        #values = list()
        star = 0

        for i in range(2300,2401):
            isbn13 = bList[i]
            print(isbn13)
            #검색창
            elem = driver.find_element_by_css_selector("#query")
            elem.clear()
            elem.send_keys("{}".format(isbn13))

            #검색창 클릭
            elem = driver.find_element_by_css_selector("#yesSForm > fieldset > span.schBtn > button")
            elem.send_keys(Keys.RETURN)
            time.sleep(1)
            
            #첫번재 책 클릭
            try:
                firstBook = driver.find_element_by_css_selector('#schMid_wrap > div:nth-child(4) > div.goodsList.goodsList_list > table > tbody > tr:nth-child(1) > td.goods_infogrp > div.goods_rating > span.gd_reviewCount > a > em')
                if firstBook:
                    print('book found')
                    
                    
                    starBlock = driver.find_element_by_css_selector('#schMid_wrap > div:nth-child(4) > div.goodsList.goodsList_list > table > tbody > tr:nth-child(1) > td.goods_infogrp > div.goods_rating > span.gd_rating > em')
                    star = starBlock.text
                    print(star)
                    
                    firstBookClick = driver.find_element_by_css_selector('#schMid_wrap > div:nth-child(4) > div.goodsList.goodsList_list > table > tbody > tr:nth-child(1) > td.goods_infogrp > div.goods_rating > span.gd_reviewCount > a')
                    firstBookClick.send_keys(Keys.ENTER)
                    time.sleep(2)
                    
                    reviewCorpus = Review.oneReview(driver)
                    print("finished {}".format(isbn13))
                    #values.append([isbn13, star, reviewCorpus])
                    
                    
                    sqlSentence = "INSERT INTO Review (isbn13, rating, review) values (%s,%s,%s)"
                    cur.execute(sqlSentence, (isbn13, star, reviewCorpus))
                    db.commit()
                    #driver.back()
                    

            except Exception as e:
                print('현재 i :', i)
                print(e)
        
    @staticmethod
    def get_reviews():
        mysql_db = mysql.conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT isbn13 FROM Review WHERE idx >5"
        db_cursor.execute(sql)
        reviews = db_cursor.fetchall()
        if not reviews:
            return None
        return reviews

if __name__ == '__main__':
    #Review().reviewTable_to_db()
    #res = Review().get_reviews()
    #print(res)
    #print(Review.get_bookISBN())
    #searchList = Review.get_bookISBN()
    #print(searchList)
    Review.reviewTable_to_db()