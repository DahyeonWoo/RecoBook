# -*- encoding: utf-8 -*-
import requests
import json
from flask import Flask, request, jsonify

def get_answer(text, user_key):    
    data_send = { 
        'query': text,
        'sessionId': user_key,
        'lang': 'ko',
    }    
    data_header = {
        'Authorization': 'Bearer CLIENT ACCESS TOKEN',
        'Content-Type': 'application/json; charset=utf-8'
    }    
    dialogflow_url = 'https://api.dialogflow.com/v1/query?v=20150910'    
    res = requests.post(dialogflow_url, data=json.dumps(data_send), headers=data_header)

    if res.status_code != requests.codes.ok:
        return '오류가 발생했습니다.'    
        
    data_receive = res.json()
    answer = data_receive['result']['fulfillment']['speech']     

    return answer

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
@app.route('/', methods=['POST', 'GET'])

def webhook():
    content = request.args.get('content')
    userid = request.args.get('userid')
    return get_answer(content, userid)

if __name__ == '__main__':
    app.run(host='0.0.0.0')    