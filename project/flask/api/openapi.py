#-*- coding:utf-8 -*-
import requests
import json
from api.db_model.mysql import conn_mysqldb
from decouple import config

class Aladin:

    @staticmethod
    def post_book():
        db = conn_mysqldb()
        db_cursor = db.cursor()

        ttbkey = config("TTBKEY")
        url = f"http://www.aladin.co.kr/ttb/api/ItemList.aspx?ttbkey="+str(ttbkey)+"&QueryType=Bestseller&MaxResults=100" \
        "&start=1&SearchTarget=Book&output=js&Version=20131101&CategoryId=0"
        
        bookList = requests.get(url).json()
        
        for i in range(2):#range(len(bookList['item'])): #range(len(bookList['item']))
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

            print(stockStatus)
            #isbn13 = int(isbn13)

            #print(isbn13,title,link,author,publishDate,description,publisher,priceStandard,stockStatus,cover,salesPoint,adult,customerReviewRank,category,bestRank)
            #sql = """INSERT INTO Book(isbn13,title,link,author,publishDate,description,publisher,priceStandard,stockStatus,cover,salesPoint,adult,customerReviewRank,category,bestRank) values(${isbn13},${title},${link},${author},${publishDate},${description},${publisher},${priceStandard},${stockStatus},${cover},${salesPoint},${adult},${customerReviewRank},${category},${bestRank})"""
            sql = """INSERT INTO Book(isbn13,title,link,author,publishDate,description,publisher,priceStandard,stockStatus,cover,salesPoint,adult,customerReviewRank,category,bestRank) 
            values (%d,%s,%s,%s,%s,%s,%s,%d,%s,%s,%d,%s,%d,%s,%d)
            """ % (isbn13,title,link,author,publishDate,description,publisher,priceStandard,stockStatus,cover,salesPoint,adult,customerReviewRank,category,bestRank)
            #sql = "INSERT INTO Book(isbn13,title,link,author,publishDate,description,publisher,priceStandard,stockStatus,cover,salesPoint,adult,customerReviewRank,category,bestRank) values("+isbn13+","+title+","+link+","+author+","+publishDate+","+description+","+publisher+","+priceStandard+","+stockStatus+","+cover+","+salesPoint+","+adult+","+customerReviewRank+","+category+","+bestRank+")"
            # sql = """INSERT INTO Book(isbn13,title,author,description,publisher) 
            # values (%s,%s,%s,%s,%s)
            # """
            # db_cursor.execute(sql,(isbn13,title,author,description,publisher))
        
        books = db_cursor.fetchall()
        if not books:
            return None
        return books
        
    @staticmethod
    def get_book():
        all_books = list(db.movies.find({}, {'_id': 0}))
        return jsonify({'result': 'success', 'info': all_books})


if __name__ == '__main__':

    res = Aladin().post_book()
    #res = BookDB().get_book()
    print(res.status_code)

    if(res.status_code == 200):
        print(res.text)
        #print(res.read().decode("UTF-8"))