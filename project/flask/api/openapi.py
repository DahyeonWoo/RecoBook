#-*- coding:utf-8 -*-
import requests
import json
from db_model.mysql import conn_mysqldb
import pymysql
from decouple import config

class Aladin:

    @staticmethod
    def post_book():
        db = pymysql.connect(host=config('host'),port=3306,user=config('user'),passwd=config('passwd'),db=config('db'),charset='utf8mb4')
        db_cursor = db.cursor()
        ttbkey = config('TTBKEY')
        url = f"http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey="+str(ttbkey)+"&QueryType=Bestseller&MaxResults=50" \
        "&start=1&SearchTarget=Book&output=js&Version=20131101&CategoryId=0"
        
        bookList = requests.get(url).json()
        
        for i in range(len(bookList['item'])): #range(len(bookList['item']))
            isbn13 = bookList['item'][i]['isbn13'] #str
            title = bookList['item'][i]['title'] #str
            link = bookList['item'][i]['link'] #str
            author = bookList['item'][i]['author'] #str
            publishDate = bookList['item'][i]['pubDate'] #str
            description = bookList['item'][i]['description'] #str
            publisher = bookList['item'][i]['publisher'] #str
            priceStandard = bookList['item'][i]['priceStandard'] #int
            stockStatus = bookList['item'][i]['stockStatus'] #str
            cover = bookList['item'][i]['cover'] #str
            salesPoint = bookList['item'][i]['salesPoint'] #int
            adult = bookList['item'][i]['adult'] #bool
            customerReviewRank = bookList['item'][i]['customerReviewRank'] #int
            category = bookList['item'][i]['categoryName'] #str
            bestRank = bookList['item'][i]['bestRank'] #int

            # print(isbn13,title,link,author,publishDate,description,publisher,priceStandard,stockStatus,cover,salesPoint,adult,customerReviewRank,category,bestRank)
            # sql = """INSERT INTO Book(isbn13,title,link,author,publishDate,description,publisher,priceStandard,stockStatus,cover,salesPoint,adult,customerReviewRank,category,bestRank) values(${isbn13},${title},${link},${author},${publishDate},${description},${publisher},${priceStandard},${stockStatus},${cover},${salesPoint},${adult},${customerReviewRank},${category},${bestRank})"""
            # """ % (isbn13,title,link,author,publishDate,description,publisher,priceStandard,stockStatus,cover,salesPoint,adult,customerReviewRank,category,bestRank)
            # sql = "INSERT INTO Book(isbn13,title,link,author,publishDate,description,publisher,priceStandard,stockStatus,cover,salesPoint,adult,customerReviewRank,category,bestRank) values("+isbn13+","+title+","+link+","+author+","+publishDate+","+description+","+publisher+","+priceStandard+","+stockStatus+","+cover+","+salesPoint+","+adult+","+customerReviewRank+","+category+","+bestRank+")"
            sql = """INSERT INTO Book(isbn13,title,link,author,publishDate,description,publisher,priceStandard,stockStatus,cover,salesPoint,adult,customerReviewRank,category,bestRank) 
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            db_cursor.execute(sql,(isbn13,title,link,author,publishDate,description,publisher,priceStandard,stockStatus,cover,salesPoint,adult,customerReviewRank,category,bestRank))

            db.commit()
            
        db_cursor.close()
        
    @staticmethod
    def get_book():
        mysql_db = conn_mysqldb()
        db_cursor = db.cursor()
        sql = "SELECT * FROM Book LIMIT 3"
        db_cursor.execute(sql)
        books = db_cursor.fetchall()
        if not books:
            return None
        return books

if __name__ == '__main__':

    Aladin().post_book()
    # res = Aladin().get_book()
    # print(res)