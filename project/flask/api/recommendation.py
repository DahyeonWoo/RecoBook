#-*- coding:utf-8 -*-
import requests
import json
from db_model.mysql import conn_mysqldb
from decouple import config
import sys


class Recommend:

    # 별점 높은 순 추천
    @staticmethod
    def get_recommend_desc():
        db = conn_mysqldb()
        db_cursor = db.cursor()
        sql = "SELECT ReviewRate FROM Book WHERE name = '" + str(name) + "'" + "DESC"
        db_cursor.execute(sql)
        books = db_cursor.fetchone()
        # 답변
        return "book"
    
    # 키워드 추출 추천
    def get_recommend_desc():
        # 추천 함수 호출
        keyword = recommend_keyword()
        # 답변
        return "저희가 추천하는 책은"+str(keyword)+"입니다."
    

def recommend_keyword():
    return keyword


if __name__ == '__main__':
    res = Recommend.get_recommend()
    print(res)