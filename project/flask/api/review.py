#from flask import request
import json.decoder
import pymysql
from decouple import config
from db_model import mysql
import csv

class Review:
        
    @staticmethod
    def reviewTable_to_db():
        db = pymysql.connect(host=config('host'),port=3306,user=config('user'),passwd=config('passwd'),db=config('db'),charset='utf8mb4')
        cur = db.cursor()
        #files = request.files['/Users/zogak/hanium/yes24Review_aladin_1.csv']
        with open('yes24Review_aladin_1.csv', 'rt') as f:
            reader = csv.DictReader(f)
        
            data = [row for row in reader]
            for row in data:
                #print(row['\ufeffisbn13'])
                isbn13 = row['\ufeffisbn13']
                rating = row['rating']
                review = row['review']
                cur.execute("INSERT INTO Review (isbn13, rating, review) VALUES (%s,%s,%s)", (isbn13, rating, review))
        db.commit()
        cur.close()
    
    @staticmethod
    def get_reviews():
        mysql_db = mysql.conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM Review LIMIT 3"
        db_cursor.execute(sql)
        reviews = db_cursor.fetchall()
        if not reviews:
            return None
        return reviews

if __name__ == '__main__':
    #Review().reviewTable_to_db()
    res = Review().get_reviews()
    print(res)