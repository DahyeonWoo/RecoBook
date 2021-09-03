# -*- coding: utf-8 -*-
import sys

sys.path.append("./project/flask/api")
import json
from flask import Flask, request, jsonify, abort
from api.KakaoEvent import KakaoEvent
from api.KakaoText import KakaoText
from api import book, create_app
from api.recommendations import recommend_by_title, recommend_by_author
from api.user import *

# Flask 어플리케이션
app = create_app()


# 유저 정보 조회
@app.route("/userinfo/<idx>/", methods=["POST"])
def get_user_info_all(idx):
    return UserInfo.get_user(idx)

# 유저 정보 조회
@app.route("/<bot_type>/user/get/<reqinfo>", methods=["POST"])
def get_user_info(bot_type,reqinfo):
    body = request.get_json()
    try:
        if bot_type == "kakao":
            # utterance = body["userRequest"]["utterance"]
            # ret = get_answer_from_engine(bottype=bot_type, query=utterance)
            idx = body["userRequest"]["user"]["id"]

            userinfo = UserInfo.get_user_info(idx)
            result = json.loads(userinfo)

            name = result["name"]
            bookRead = result["bookRead"]
            bookWant = result['bookWant']
            interestBook = result["interestBook"]
            interestAuthor = result["interestAuthor"]
            interestCategory = result["interestCategory"]

            if reqinfo == "bookRead":
                if bookRead != None and len(bookRead) != 0:
                    answer = name+", 지금까지 <"+bookRead+">를 읽었네. 좋아!"
                else:
                    answer = "우선 읽은 책을 등록해줘"
            elif reqinfo == "bookWant":
                if bookWant != None and len(bookWant) != 0:
                    answer = name+", 읽고 싶은 책이 <"+bookWant+">야."
                else:
                    answer = "우선 읽고 싶은 책을 등록해줘"
            elif reqinfo == "interestBook":
                if interestBook != None and len(interestBook) != 0:
                    answer = name+", <"+interestBook+"> 책을 좋아해."
                else:
                    answer = "우선 관심 책을 등록해줘"
            elif reqinfo == "interestAuthor":
                if interestAuthor != None and len(interestAuthor) != 0:
                    answer = name+", <"+interestAuthor+"> 작가를 좋아해."
                else:
                    answer = "우선 관심 작가를 등록해줘"
            elif reqinfo == "interestCategory":
                if interestCategory != None and len(interestCategory) != 0:
                    answer = name+", <"+interestCategory+"> 장르를 좋아해."
                else:
                    answer = "우선 관심 분야를 등록해줘"
            else:
                answer = "레꼬북에 없는 기능이야. 계속 개발중이니까, 더 많은 기능을 기대해줘!"
            return KakaoText().send_response({"Answer": answer})
        elif bot_type == "naver":
            return json.dumps({}), 200
        else:
            abort(404)
    except Exception as ex:
        abort(500)
        print(Exception)

# 유저 정보 수정
@app.route("/<bot_type>/user/insert/<reqinfo>", methods=["POST"])
def insert_user_info(bot_type,reqinfo):
    body = request.get_json()
    try:
        if bot_type == "kakao":
            # utterance = body["userRequest"]["utterance"]
            # ret = get_answer_from_engine(bottype=bot_type, query=utterance)
            idx = body["userRequest"]["user"]["id"]

            if reqinfo == "bookRead":
                title = body["action"]["detailParams"]["title"]["value"]
                result = UserInfo.insert_user_info(idx, reqinfo, title)
                print(result)
                if result == 1:
                    answer = "읽은 책으로 <"+title+">가 등록됐어."
                elif result == 2:
                    answer = "이미 읽은 책으로 등록한 도서야"
            elif reqinfo == "bookWant":
                title = body["action"]["detailParams"]["title"]["value"]
                result = UserInfo.insert_user_info(idx, reqinfo, title)
                if result == 1:
                    answer = "위시리스트에 <"+title+">가 등록됐어"
                elif result == 2:
                    answer = "이미 위시리스트에 등록한 도서야."
            elif reqinfo == "interestBook":
                title = body["action"]["detailParams"]["title"]["value"]
                result = UserInfo.insert_user_info(idx, reqinfo, title)
                if result == 1:
                    answer = "관심 도서에 <"+title+">가 등록됐어"
                elif result == 2:
                    answer = "이미 등록한 관심 도서야."
            elif reqinfo == "interestAuthor":
                author = body["action"]["detailParams"]["author"]["value"]
                result = UserInfo.insert_user_info(idx, reqinfo, author)
                if result == 1:
                    answer = "관심 작가에 <"+author+">가 등록됐어"
                elif result == 2:
                    answer = "이미 등록한 관심 작가야"
            elif reqinfo == "interestCategory":
                genre = body["action"]["detailParams"]["genre"]["value"]
                result = UserInfo.insert_user_info(idx, reqinfo, genre)
                if result == 1:
                    answer = "관심 장르에 <"+genre+">가 등록됐어"
                elif result == 2:
                    answer = "이미 등록한 관심 장르야"
            else:
                answer = "레꼬북에 없는 기능이야. 계속 개발중이니까, 더 많은 기능을 기대해줘!"
            return KakaoText().send_response({"Answer": answer})
        elif bot_type == "naver":
            return json.dumps({}), 200
        else:
            abort(404)
    except Exception as ex:
        abort(500)
        print(Exception)


# 유저 정보 삭제
@app.route("/<bot_type>/user/delete/<reqinfo>", methods=["POST"])
def update_user_info(bot_type,reqinfo):
    body = request.get_json()
    try:
        if bot_type == "kakao":
            # utterance = body["userRequest"]["utterance"]
            # ret = get_answer_from_engine(bottype=bot_type, query=utterance)
            idx = body["userRequest"]["user"]["id"]

            if reqinfo == "bookRead":
                title = body["action"]["detailParams"]["title"]["value"]
                result = UserInfo.update_user_info(idx, reqinfo, title)
                if result == 1:
                    answer = "읽은 책 목록에서 <"+title+">를 삭제했어"
                elif result == 2:
                    answer = "등록하지 않은 책은 삭제할 수 없어"
            elif reqinfo == "bookWant":
                title = body["action"]["detailParams"]["title"]["value"]
                result = UserInfo.update_user_info(idx, reqinfo, title)
                if result == 1:
                    answer = "위시리스트에서 <"+title+">를 삭제했어"
                elif result == 2:
                    answer = "등록하지 않은 책은 삭제할 수 없어"
            elif reqinfo == "interestBook":
                title = body["action"]["detailParams"]["title"]["value"]
                result = UserInfo.update_user_info(idx, reqinfo, title)
                if result == 1:
                    answer = "관심 책 목록에서 <"+title+">를 삭제했어"
                elif result == 2:
                    answer = "등록하지 않은 책은 삭제할 수 없어"
            elif reqinfo == "interestAuthor":
                author = body["action"]["detailParams"]["author"]["value"]
                result = UserInfo.update_user_info(idx, reqinfo, author)
                if result == 1:
                    answer = "관심 작가 목록에서 <"+author+">를 삭제했어"
                elif result == 2:
                    answer = "등록하지 않은 작가는 삭제할 수 없어"
            elif reqinfo == "interestCategory":
                genre = body["action"]["detailParams"]["genre"]["value"]
                result = UserInfo.update_user_info(idx, reqinfo, genre)
                if result == 1:
                    answer = "관심 장르 목록에서 <"+genre+">를 삭제했어"
                elif result == 2:
                    answer = "등록하지 않은 장르는 삭제할 수 없어"
            else:
                answer = "레꼬북에 없는 기능이야. 계속 개발중이니까, 더 많은 기능을 기대해줘!"
            return KakaoText().send_response({"Answer": answer})
        elif bot_type == "naver":
            return json.dumps({}), 200
        else:
            abort(404)
    except Exception as ex:
        abort(500)
        print(Exception)

# 제목 기반 추천
@app.route('/title', methods=['POST'])
def recommendation_title():
    req = request.get_json()

    title = req["action"]["detailParams"]["title"]["value"]
    answer = recommend_by_title(title)

    return KakaoText().send_response({"Answer": "너에게 딱 맞는 추천 목록이야\n" + answer})

# 작가 기반 추천
@app.route('/author', methods=['POST'])
def recommendation_author():
    req = request.get_json()

    author = req["action"]["detailParams"]["author"]["value"]
    answer = recommend_by_author(author)

    return KakaoText().send_response({"Answer": "너에게 딱 맞는 추천 목록이야\n" + answer})


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

# 책 정보 조회
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)