from flask import Flask, render_template, request, redirect, jsonify
import requests
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from api.chatbot import ChatbotMessageSender as CM
from api.user import User
from api.openapi import Aladin
from model import Author, Book, Genre
import urllib
#from api.user import User

app = Flask(__name__)
# app.config['SQLALCHEMY_CATABASE_URI'] = 'sqlite:///posts.db'
# db = SQLAlchemy(app)

# @app.route('/', methods=['POST', 'GET'])
# def welcome():
    
#     return
    
# def index():
#     return render_template('index.html')

# @app.route('/bookcode')
# def start():
    
#     return render_template('bookcode.html')


@app.route('/bookcode')
def start():
    ChatBot = CM().req_message_send()
    return render_template('bookcode.html')

@app.route('/bookList', methods=['POST'])
def post_now_showing():
    Book = Aladin().get_book()
    return jsonify({'result': 'success'})

@app.route('/bookList', methods=['GET'])
def get_now_showing():
    Book = User().get_user()

@app.route('/author/<name>', methods=['POST'])
def post_author(name):
    author_name = Author().get_author(name)
    return author_name

@app.route('/genre', methods=['POST'])
def post_genre():
    pass    

if __name__ == '__main__':
    res = CM().req_message_send()
    print(res.status_code)
    if(res.status_code == 200):
        print(res.text)
    app.run(debug=True)
        # print(res.read().d

    