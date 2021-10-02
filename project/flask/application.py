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


# naver entity 전역변수 설정

naver_example_entity = "29ce5a43db2849249a9d3c8e94dcd766"
naver_title_entity = "f76d07044c714ebabcc710620a8e05a3"
naver_author_entity = "330cbe05bc954ee68b82022b73fd4a68"
naver_genre_entity = "fb93fe2f70964641ae5a5e11fa74324c"



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
        elif bot_type == "naver":
            idx = body["userInfo"]["id"]
        else:
            abort(404)

        isUser = UserInfo.get_is_user(idx)

        if isUser != None:
            userinfo = UserInfo.get_user_info(idx)
            result = json.loads(userinfo)
            # name = result["name"]
            bookRead = result["bookRead"]
            bookWant = result['bookWant']
            interestBook = result["interestBook"]
            interestAuthor = result["interestAuthor"]
            interestCategory = result["interestCategory"]

            if reqinfo == "bookRead":
                if bookRead != None and len(bookRead) != 0:
                    answer = "지금까지 <"+bookRead+">를 읽었네. 좋아!"
                else:
                    answer = "우선 읽은 책을 등록해줘"
            elif reqinfo == "bookWant":
                if bookWant != None and len(bookWant) != 0:
                    answer = "읽고 싶은 책들은 <"+bookWant+">야."
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
        else:
            UserInfo.insert_user_idx(idx)
            answer = "확장 기능을 사용하려면 유저 등록을 해야해. 유저 등록이 완료됐으니 기능을 다시 실행해줄래? 민감한 개인정보는 사용하지 않으니 걱정마!"

        if bot_type == "kakao":
            return KakaoText().send_response({"Answer": answer})
        elif bot_type == "naver":
            data = "GET"+reqinfo
            responseBody = {
                data: [
                    {
                        "name": "answer",
                        "value": answer
                    }
                ]
            }
            return responseBody

        else:
            abort(404)
    except Exception as ex:
        abort(500)
        print(Exception)

# 유저 정보 추가
@app.route("/<bot_type>/user/insert/<reqinfo>", methods=["POST"])
def insert_user_info(bot_type,reqinfo):
    body = request.get_json()
    idx = body["userInfo"]["id"]

    try:
        if bot_type == "kakao":
            idx = body["userRequest"]["user"]["id"]
        elif bot_type == "naver":
            idx = body["userInfo"]["id"]
        else:
            abort(404)

        isUser = UserInfo.get_is_user(idx)
        if isUser != None:
            if reqinfo == "bookRead":
                if bot_type == "kakao":
                    title = body["action"]["detailParams"]["title"]["value"]
                elif bot_type == "naver":
                    title = body["userInfo"]["entities"][naver_title_entity]
                result = UserInfo.insert_user_info(idx, reqinfo, title)
                print(result)
                if result == 1:
                    answer = "읽은 책으로 <"+title+">가 등록됐어."
                elif result == 2:
                    answer = "이미 읽은 책으로 등록한 도서야"
            elif reqinfo == "bookWant":
                if bot_type == "kakao":
                    title = body["action"]["detailParams"]["title"]["value"]
                elif bot_type == "naver":
                    title = body["userInfo"]["entities"][naver_title_entity]
                result = UserInfo.insert_user_info(idx, reqinfo, title)
                if result == 1:
                    answer = "위시리스트에 <"+title+">가 등록됐어"
                elif result == 2:
                    answer = "이미 위시리스트에 등록한 도서야."
            elif reqinfo == "interestBook":
                if bot_type == "kakao":
                    title = body["action"]["detailParams"]["title"]["value"]
                elif bot_type == "naver":
                    title = body["userInfo"]["entities"][naver_title_entity]
                result = UserInfo.insert_user_info(idx, reqinfo, title)
                if result == 1:
                    answer = "관심 도서에 <"+title+">가 등록됐어"
                elif result == 2:
                    answer = "이미 등록한 관심 도서야."
            elif reqinfo == "interestAuthor":
                if bot_type == "kakao":
                    author = body["action"]["detailParams"]["author"]["value"]
                elif bot_type == "naver":
                    author = body["userInfo"]["entities"][naver_author_entity]
                result = UserInfo.insert_user_info(idx, reqinfo, author)
                if result == 1:
                    answer = "관심 작가에 <"+author+">가 등록됐어"
                elif result == 2:
                    answer = "이미 등록한 관심 작가야"
            elif reqinfo == "interestCategory":
                if bot_type == "kakao":
                    genre = body["action"]["detailParams"]["genre"]["value"]
                elif bot_type == "naver":
                    genre = body["userInfo"]["entities"][naver_genre_entity]
                result = UserInfo.insert_user_info(idx, reqinfo, genre)
                if result == 1:
                    answer = "관심 장르에 <"+genre+">가 등록됐어"
                elif result == 2:
                    answer = "이미 등록한 관심 장르야"
            else:
                answer = "레꼬북에 없는 기능이야. 계속 개발중이니까, 더 많은 기능을 기대해줘!"
        else:
            UserInfo.insert_user_idx(idx)
            answer = "확장 기능을 사용하려면 유저 등록을 해야해. 유저 등록이 완료됐으니 기능을 다시 실행해줄래? 민감한 개인정보는 사용하지 않으니 걱정마!"

        if bot_type == "kakao":
            return KakaoText().send_response({"Answer": answer})
        elif bot_type == "naver":
            data = "INSERT" + reqinfo
            responseBody = {
                data: [
                    {
                        "name": "answer",
                        "value": answer
                    }
                ]
            }
            return responseBody
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
        elif bot_type == "naver":
            idx = body["userInfo"]["id"]
        else:
            abort(404)

        isUser = UserInfo.get_is_user(idx)
        if isUser != None:
            if reqinfo == "bookRead":
                if bot_type == "kakao":
                    title = body["action"]["detailParams"]["title"]["value"]
                elif bot_type == "naver":
                    title = body["userInfo"]["entities"][naver_title_entity]
                result = UserInfo.update_user_info(idx, reqinfo, title)
                if result == 1:
                    answer = "읽은 책 목록에서 <"+title+">를 삭제했어"
                elif result == 2:
                    answer = "등록하지 않은 책은 삭제할 수 없어"
            elif reqinfo == "bookWant":
                if bot_type == "kakao":
                    title = body["action"]["detailParams"]["title"]["value"]
                elif bot_type == "naver":
                    title = body["userInfo"]["entities"][naver_title_entity]
                result = UserInfo.update_user_info(idx, reqinfo, title)
                if result == 1:
                    answer = "위시리스트에서 <"+title+">를 삭제했어"
                elif result == 2:
                    answer = "등록하지 않은 책은 삭제할 수 없어"
            elif reqinfo == "interestBook":
                if bot_type == "kakao":
                    title = body["action"]["detailParams"]["title"]["value"]
                elif bot_type == "naver":
                    title = body["userInfo"]["entities"][naver_title_entity]
                result = UserInfo.update_user_info(idx, reqinfo, title)
                if result == 1:
                    answer = "관심 책 목록에서 <"+title+">를 삭제했어"
                elif result == 2:
                    answer = "등록하지 않은 책은 삭제할 수 없어"
            elif reqinfo == "interestAuthor":
                if bot_type == "kakao":
                    author = body["action"]["detailParams"]["author"]["value"]
                elif bot_type == "naver":
                    author = body["userInfo"]["entities"][naver_author_entity]
                result = UserInfo.update_user_info(idx, reqinfo, author)
                if result == 1:
                    answer = "관심 작가 목록에서 <"+author+">를 삭제했어"
                elif result == 2:
                    answer = "등록하지 않은 작가는 삭제할 수 없어"
            elif reqinfo == "interestCategory":
                if bot_type == "kakao":
                    genre = body["action"]["detailParams"]["genre"]["value"]
                elif bot_type == "naver":
                    genre = body["userInfo"]["entities"][naver_genre_entity]
                result = UserInfo.update_user_info(idx, reqinfo, genre)
                if result == 1:
                    answer = "관심 장르 목록에서 <"+genre+">를 삭제했어"
                elif result == 2:
                    answer = "등록하지 않은 장르는 삭제할 수 없어"
            else:
                answer = "레꼬북에 없는 기능이야. 계속 개발중이니까, 더 많은 기능을 기대해줘!"
                return KakaoText().send_response({"Answer": answer})
        else:
            UserInfo.insert_user_idx(idx)
            answer = "확장 기능을 사용하려면 유저 등록을 해야해. 유저 등록이 완료됐으니 기능을 다시 실행해줄래? 민감한 개인정보는 사용하지 않으니 걱정마!"

        if bot_type == "kakao":
            return KakaoText().send_response({"Answer": answer})
        elif bot_type == "naver":
            data = "DELETE" + reqinfo
            responseBody = {
                data: [
                    {
                        "name": "answer",
                        "value": answer
                    }
                ]
            }
            return responseBody
        else:
            abort(404)

    except Exception as ex:
        abort(500)
        print(Exception)

# 책 정보 조회
@app.route("/<bot_type>/book/get/<reqinfo>", methods=["POST"])
def get_book_info(bot_type,reqinfo):
    body = request.get_json()
    try:
        if reqinfo == "title-info":
            if bot_type == "kakao":
                title = body["action"]["detailParams"]["title"]["value"]
            elif bot_type == "naver":
                title = body["userInfo"]["entities"][naver_title_entity]
            result = BookInfo.get_title_to_info(title)
            answer = "책 제목으로 검색했을 때의 결과야.\n" + result
        elif reqinfo == "isbn13-info":
            if bot_type == "kakao":
                isbn = body["action"]["detailParams"]["isbn13"]["value"]
            elif bot_type == "naver":
                isbn = body["userInfo"]["entities"][naver_example_entity]
            result = BookInfo.get_isbn_to_info(isbn)
            answer = "책 isbn13으로 검색했을 때의 결과야.\n" + result
        elif reqinfo == "author":
            if bot_type == "kakao":
                author = body["action"]["detailParams"]["author"]["value"]
            elif bot_type == "naver":
                author = body["userInfo"]["entities"][naver_author_entity]
            result = BookInfo.get_author_to_info(author)
            answer = "작가 정보로 검색했을 때의 결과야.\n" + result
        elif reqinfo == "title-review":
            if bot_type == "kakao":
                title = body["action"]["detailParams"]["title"]["value"]
            elif bot_type == "naver":
                title = body["userInfo"]["entities"][naver_title_entity]
            result = BookInfo.get_title_to_review(title)
            answer = "제목으로 검색했을 때의 결과야.\n" + result
        else:
            answer = "레꼬북에 없는 기능이야. 계속 개발중이니까, 더 많은 기능을 기대해줘!"

        if bot_type == "kakao":
            return KakaoText().send_response({"Answer": answer})
        elif bot_type == "naver":
            data = "GET" + reqinfo
            responseBody = {
                data: [
                    {
                        "name": "answer",
                        "value": answer
                    }
                ]
            }
            return responseBody
        else:
            abort(404)
    except Exception as ex:
        abort(500)
        print(Exception)

# 통계 분석
@app.route("/<bot_type>/book/get/top/<reqinfo>", methods=["POST"])
def get_book_info_top(bot_type,reqinfo):
    top_n = 5
    try:
        if reqinfo == "bookRead":
            data = Top.get_topn_bookRead(top_n)
            result = Top.accessing_dict_info(data)
            answer = "현재까지 사람들이 많이 읽은 책 목록이야.\n" + result
        elif reqinfo == "bookWant":
            data = Top.get_topn_bookWant(top_n)
            result = Top.accessing_dict_info(data)
            answer = "현재 인기 있는 위시리스트 도서 목록이야.\n" + result
        elif reqinfo == "interestBook":
            data = Top.get_topn_interestBook(top_n)
            result = Top.accessing_dict_info(data)
            answer = "현재 인기 있는 관심 도서 목록이야.\n" + result
        elif reqinfo == "interestAuthor":
            data =Top.get_topn_interestAuthor(top_n)
            result = Top.accessing_dict_info(data)
            answer = "현재 인기 있는 관심 작가 목록이야.\n" + result
        elif reqinfo == "interestCategory":
            data =Top.get_topn_interestCategory(top_n)
            result = Top.accessing_dict_info(data)
            answer = "현재 인기 있는 관심 장르 목록이야.\n" + result
        else:
            answer = "레꼬북에 없는 기능이야. 계속 개발중이니까, 더 많은 기능을 기대해줘!"
            # return result
            return KakaoText().send_response({"Answer": answer})

        if bot_type == "kakao":
            return KakaoText().send_response({"Answer": answer})
        elif bot_type == "naver":
            data = "GETtop" + reqinfo
            responseBody = {
                data: [
                    {
                        "name": "answer",
                        "value": answer
                    }
                ]
            }
            return responseBody
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
        if reqinfo == "title":
            if bot_type == "kakao":
                title = body["action"]["detailParams"]["title"]["value"]
            elif bot_type == "naver":
                title = body["userInfo"]["entities"][naver_title_entity]
            answer = recommend_by_title(title)
        elif reqinfo == "author":
            if bot_type == "kakao":
                author = body["action"]["detailParams"]["author"]["value"]
            elif bot_type == "naver":
                author = body["userInfo"]["entities"][naver_author_entity]
            answer = recommend_by_author(author)

        if bot_type == "kakao":
            return KakaoText().send_response({"Answer": answer})
        elif bot_type == "naver":
            data = "RECOMMENDsimilar-" + reqinfo
            responseBody = {
                data: [
                    {
                        "name": "answer",
                        "value": answer
                    }
                ]
            }
            return responseBody
        else:
            abort(404)
    except Exception as ex:
        abort(500)
        print(Exception)

# 벡터 평균값 추천, 유저 기반 도서/작가
@app.route("/<bot_type>/recommend/<reqinfo>/user", methods=['POST'])
def recommend_user(bot_type,reqinfo):
    body = request.get_json()
    try:
        if bot_type == "kakao":
            idx = body["userRequest"]["user"]["id"]
        elif bot_type == "naver":
            idx = body["userInfo"]["id"]
        else:
            abort(404)

        isUser = UserInfo.get_is_user(idx)
        if isUser != None:
            if reqinfo == "title":
                if bot_type == "kakao":
                    title = body["action"]["detailParams"]["title"]["value"]
                elif bot_type == "naver":
                    title = body["userInfo"]["entities"][naver_title_entity]
                answer = recommend_user_by_title(idx, title)
            elif reqinfo == "author":
                if bot_type == "kakao":
                    author = body["action"]["detailParams"]["author"]["value"]
                elif bot_type == "naver":
                    author = body["userInfo"]["entities"][naver_author_entity]
                answer = recommend_user_by_author(idx, author)
        else:
            UserInfo.insert_user_idx(idx)
            answer = "확장 기능을 사용하려면 유저 등록을 해야해. 유저 등록이 완료됐으니 기능을 다시 실행해줄래? 민감한 개인정보는 사용하지 않으니 걱정마!"

        if bot_type == "kakao":
            return KakaoText().send_response({"Answer": answer})
        elif bot_type == "naver":
            data = "RECOMMENDsimilar-" + reqinfo
            responseBody = {
                data: [
                    {
                        "name": "answer",
                        "value": answer
                    }
                ]
            }
            return responseBody
        else:
            abort(404)
    except Exception as ex:
        abort(500)
        print(Exception)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)