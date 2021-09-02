# -*- coding: utf-8 -*-
import sys

sys.path.append("./project/flask/api")
import json
from flask import Flask, request, jsonify, abort
from api.KakaoEvent import KakaoEvent
from api.KakaoText import KakaoText
from api import book, create_app
from api.recommendations import recommend_by_title, recommend_by_author

# Flask 어플리케이션
app = create_app()


@app.route("/", methods=["GET"])
def index():
    # return 'hello', 200
    return "hello"


# 챗봇 엔진 query 전송 API
@app.route("/query/<bot_type>", methods=["POST"])
def query(bot_type):
    body = request.get_json()

    try:
        if bot_type == "kakao":
            # 카카오톡 스킬 처리
            body = request.get_json()
            utterance = body["userRequest"]["utterance"]
            # ret = get_answer_from_engine(bottype=bot_type, query=utterance)

            skillTemplate = KakaoEvent()
            return skillTemplate.send_response(
                {"AnswerImageUrl": "image", "Answer": "고양이"}
            )

        elif bot_type == "naver":
            # 네이버톡톡 이벤트 처리
            body = request.get_json()
            user_key = body["user"]
            event = body["event"]

            from NaverEvent import NaverEvent

            authorization_key = "<보내기 API 인증키>"
            naverEvent = NaverEvent(authorization_key)

            if event == "open":
                # 사용자가 채팅방 들어왔을 때 처리
                print("채팅방에 유저가 들어왔습니다.")
                return json.dumps({}), 200

            elif event == "leave":
                # 사용자가 채팅방 나갔을 때 처리
                print("채팅방에 유저가 나갔습니다.")
                return json.dumps({}), 200

            elif event == "send":
                # 사용자가 챗봇에게 send 이벤트를 전송했을 때
                user_text = body["textContent"]["text"]
                ret = get_answer_from_engine(bottype=bot_type, query=user_text)
                return naverEvent.send_response(user_key, ret)

            return json.dumps({}), 200

        else:
            # 정의되지 않은 bot type인 경우 404 오류
            abort(404)

    except Exception as ex:
        # 오류 발생시 500 오류
        abort(500)
        print(Exception)


# 카카오톡 텍스트형 응답
@app.route("/kakao/sayHello", methods=["POST"])
def sayHello():
    body = request.get_json()
    print(body["userRequest"]["utterance"])

    responseBody = {
        "version": "2.0",
        "template": {"outputs": [{"simpleText": {"text": "안녕 hello I'm Ryan"}}]},
    }

    return responseBody


# 카카오톡 이미지형 응답
@app.route("/kakao/showHello", methods=["POST"])
def showHello():
    body = request.get_json()
    print(body["userRequest"]["utterance"])

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleImage": {
                        "imageUrl": "https://t1.daumcdn.net/friends/prod/category/M001_friends_ryan2.jpg",
                        "altText": "hello I'm Ryan",
                    }
                }
            ]
        },
    }

    return responseBody


# 아이디 확인하기 (임의의 API)
@app.route("/<bot_type>/userID", methods=["POST"])
def get_userID(bot_type):
    body = request.get_json()

    if bot_type == "kakao":
        body = request.get_json()
        user_id = body["userRequest"]["user"]["id"]

        return KakaoText().send_response({"Answer": user_id})


# 책장 보기
@app.route("/<bot_type>/bookList", methods=["POST"])
def get_bookList(bot_type):
    body = request.get_json()

    if bot_type == "kakao":
        # Book = Aladin().get_book()
        # print(Book.json())
        return KakaoText().send_response({"Answer": Book.json()})


@app.route("/bookinfo", methods=["GET"])
def get_bookinfo():
    title = request.args.get("title")
    author = request.args.get("author")
    isbn = request.args.get("isbn13")
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


@app.route('/title', methods=['POST'])
def recommendation_title():
    req = request.get_json()
    print(req)

    title = req["action"]["detailParams"]["title"]["value"]
    answer = recommend_by_title(title)

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer
                    }
                }
            ]
        }
    }
    return jsonify(res)


@app.route('/author', methods=['POST'])
def recommendation_author():
    req = request.get_json()

    author = req["action"]["detailParams"]["author"]["value"]
    answer = recommend_by_author(author)

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer
                    }
                }
            ]
        }
    }
    return jsonify(res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
