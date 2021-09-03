# -*- coding: utf-8 -*-
import sys

sys.path.append("./project/flask/api")
import json
from flask import Flask, request, jsonify, abort
from api import create_app

from api.user import *
from api.book import *
from api.recommendations import recommend_by_title, recommend_by_author
from api.statistics import *

from api.KakaoEvent import KakaoEvent
from api.KakaoText import KakaoText

# Flask 어플리케이션
app = create_app()
#app = Flask(__name__)

# 첫 화면
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# 유저 정보 전체 조회
@app.route("/userinfo/<idx>/", methods=["POST"])
def get_user_info_all(idx):
    return UserInfo.get_user_info(idx)

# 유저 정보 조회
@app.route("/<bot_type>/user/get/<reqinfo>", methods=["POST"])
def get_user_info(bot_type,reqinfo):
    body = request.get_json()
    try:
        if bot_type == "kakao":
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

# 책 정보 조회
@app.route("/<bot_type>/book/get/<reqinfo>", methods=["POST"])
def get_book_info(bot_type,reqinfo):
    try:
        if bot_type == "kakao":
            if reqinfo == "title-info":
                result = BookInfo.get_title_to_info(title)
                answer = "책 제목으로 검색했을 때의 결과야.\n" + result
            elif reqinfo == "isbn13-info":
                result = BookInfo.get_isbn_to_info(isbn13)
                answer = "책 isbn13으로 검색했을 때의 결과야.\n" + result
            elif reqinfo == "author-info":
                result = BookInfo.get_author_to_info(name)
                answer = "작가 정보로 검색했을 때의 결과야.\n" + result
            elif reqinfo == "title-review":
                result = BookInfo.get_title_to_review(title)
                answer = "제목으로 검색했을 때의 결과야.\n" + result
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

# 통계 분석
@app.route("/<bot_type>/book/get/top/<reqinfo>", methods=["POST"])
def get_book_info_top(bot_type,reqinfo):
    body = request.get_json()
    try:
        if bot_type == "kakao":
            if reqinfo == "bookRead":
                result = Top.get_topn_bookRead(10)
                # answer = "현재까지 사람들이 많이 읽은 책 목록이야.\n" + result
            elif reqinfo == "bookWant":
                result = Top.get_topn_bookWant(10)
                # answer = "현재 인기 있는 위시리스트 도서 목록이야.\n" + result
            elif reqinfo == "interestBook":
                result = Top.get_topn_interestBook(10)
                # answer = "현재 인기 있는 관심 도서 목록이야.\n" + result
            elif reqinfo == "interestAuthor":
                result =Top.get_topn_interestAuthor(10)
                # answer = "현재 인기 있는 관심 작가 목록이야.\n" + result
            elif reqinfo == "interestCategory":
                result =Top.get_topn_interestCategory(10)
                # answer = "현재 인기 있는 관심 장르 목록이야.\n" + result
            else:
                answer = "레꼬북에 없는 기능이야. 계속 개발중이니까, 더 많은 기능을 기대해줘!"
            return result
            # return KakaoText().send_response({"Answer": answer})
        elif bot_type == "naver":
            return json.dumps({}), 200
        else:
            abort(404)
    except Exception as ex:
        abort(500)
        print(Exception)

# 벡터 평균값 추천, 비슷한 도서/작가
@app.route("/<bot_type>/recommend/<reqinfo>/similar", methods=['POST'])
def recommend_similar(bot_type,reqinfo):
    body = request.get_json()
    try:
        if bot_type == "kakao":
            if reqinfo == "title":
                title = body["action"]["detailParams"]["title"]["value"]
                answer = recommend_by_title(title)
                return KakaoText().send_response({"Answer": "너에게 딱 맞는 추천 목록이야\n" + answer})
            elif reqinfo == "author":
                author = body["action"]["detailParams"]["author"]["value"]
                answer = recommend_by_author(author)
                return KakaoText().send_response({"Answer": "너에게 딱 맞는 추천 목록이야\n" + answer})
        elif bot_type == "naver":
            return json.dumps({}), 200
        else:
            abort(404)
    except Exception as ex:
        abort(500)
        print(Exception)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)