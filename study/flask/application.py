import requests
import json
from flask import Flask,request, make_response, jsonify

ERROR_MESSAGE = '네트워크 접속에 문제가 발생하였습니다. 잠시 후 다시 시도해주세요.' 
URL_OPEN_TIME_OUT = 10

app = Flask(__name__)

def process_book_info(book_name):
    if book_name == u'로맨스':
        answer = '고양이'
        answer += '역시 로맨스는 고양이지'

@app.route('/',methods=['POST'])
def webhook():

    # 액션 구함
    req = request.get_json(force=True)
    action = req['result']['action']

    # 액션 처리
    if action == 'book_info':
        book_name = req['request']['parameters']['pizza_type']
        answer = proccess_book_info(book_name)
    else:
        answer = 'error'
    
    res = {'speech':answer}
    return jsonify(res)

# 카카오톡
@app.route("/keyboard")
def keyboard():
    res = {
        "type":"buttons",
        "buttons": ["대화하기"]
    }

    return jsonify(res)

@app.route('/message',methods=['POST'])
def message():

    #메시지 받기
    req = request.get_json()
    user_key = req['user_key']
    content = req['content']

    if len(user_key) <= 0 or len(content) <= 0:
        answer = ERROR_MESSAGE
    
    # 답변 구함
    answer = get_answer(content,user_key)

    #메시지 설정
    res = {
        'message': {'text': answer}
    }

    return jsonify(res)

def get_answer(text,user_key):

    #dialogflow에 요청
    data_send = {
        'lang': 'ko',
        'query': text,
        'sessionId': user_key,
        'timezone': 'Asia/Seoul'
    }

    data_header = {
        'Content-Type': 'application/json; charset=utf8',
        'Authorization': 'Bearer adfb4242e4' #client access token
    }

    dialogflow_url = 'https://api.dialogflow.com/v1/query?v=20150910'

    # 대답 처리
    if res.status_code != requests.codes.ok:
        return ERROR_MESSAGE
    
    data_receive = res.json()
    answer = data_receive['result']['fulfillment']['speech']

    return answer

@app.route('/message',methods=['POST'])
def message():
    # 메뉴 구함
    answer, menu = get_menu(answer)

    # 메뉴 버튼 설정
    menu_button = get_menu_button(menu)

    if menu_button != None:
        res['keyboard'] = menu_button

    # 사진 처리
    answer,photo = get_photo(answer)
    photo_width, photo_height  = get_photo_size(photo)

    if photo != '' and photo_width > 0 and photo_height > 0:
        res['message']['photo'] = {
            'url': photo,
            'width': photo_width,
            'height': photo_height
        }
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5110, threaded=True)
