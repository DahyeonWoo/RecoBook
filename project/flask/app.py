from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from api.chatbot import ChatbotMessageSender as CM

app = Flask(__name__)
app.config['SQLALCHEMY_CATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bookcode')
def start():
    ChatBot = CM().req_message_send()
    return render_template('bookcode.html')
if __name__ == '__main__':
    app.run(debug=True)