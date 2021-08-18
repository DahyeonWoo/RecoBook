# -*- coding: utf-8 -*-
import sys
sys.path.append('./project/flask/api')
from flask import Flask, render_template, request, redirect, jsonify

from api.user import UserInfo, UserAuthor, UserGenre, UserRead, UserWish
from api.openapi import Aladin
from api import book

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bookList', methods=['GET'])
def post_now_showing():
    Book = Aladin().get_book()
    return Book.json()

@app.route('/user', methods=['GET'])
def get_now_showing():
    user = request.args.get('name')
    user_info = UserInfo().get_user(user)
    return user_info

@app.route('/bookinfo', methods=['GET'])
def get_bookinfo():
    title = request.args.get('title')
    author = request.args.get('author')
    isbn = request.args.get('isbn13')
    if isbn:
        book_info = book.get_isbn_to_info(isbn)
    elif title:
        book_info = book.get_title_to_info(title)
    elif author:
        book_info = book.get_author_to_info(author)
    return book_info


@app.route('/genre', methods=['POST'])
def post_genre():
    pass    

if __name__ == '__main__':
    app.run(debug=True)
    # print(res.read().d
