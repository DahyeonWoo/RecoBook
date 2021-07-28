import request
import json.decoder
import pymysql
from decouple import config
import csv

# from flask import Flask, render_template, url_for, request, redirect
# from flask_wtf import FlaskForm, Form
# from wtforms import StringField, SubmitField
# import csv
# from flask_mysqldb import MYSQL

class Review:
        
    @staticmethod
    def reviewTable_to_db():
        db = pymysql.connect(host=config('host'),port=3306,user=config('user'),passwd=config('passwd'),db=config('db'),charset='utf8mb4')
        cur = db.cursor()
        files = request.files['csv file name']
        reader = csv.DictReader(files)
        data = [row for row in reader]
        for row in data:
            isbn13 = row['isbn13']
            rating = row['rating']
            review = row['review']
            cur.execute("INSERT INTO Review(isbn13, rating, review)"
            "VALUES('%s','%s','%s')", isbn13, rating, review)
        db.commit()
        cur.close()

if __name__ == '__main__':

    Review().reviewTable_to_db()