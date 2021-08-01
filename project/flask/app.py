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


@app.route('/bookList', methods=['POST'])
def post_now_showing():
    Book = Aladin().get_book()
    return jsonify({'result': 'success'})

@app.route('/bookList', methods=['GET'])
def get_now_showing():
    Book = User().get_user()

@app.route('/author/<name>', methods=['GET'])
def post_author(name):
    author_name = Author().get_author(name)
    return author_name

@app.route('/genre', methods=['POST'])
def post_genre():
    pass    

if __name__ == '__main__':
    app.run(debug=True)
        # print(res.read().d

    