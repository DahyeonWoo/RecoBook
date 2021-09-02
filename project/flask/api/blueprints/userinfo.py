from flask.helpers import url_for
from werkzeug.utils import redirect
from api.user import *
from flask import Blueprint, request

userinfo_bp = Blueprint("userinfo", __name__, url_prefix="/userinfo/<name>")


@userinfo_bp.route("/")
def get_user_info(name):
    return UserInfo.get_user(name)


# 읽은 책
@userinfo_bp.route("/bookRead/")  # 조회
def get_book_read(name):
    return UserRead.get_read_book(name)


@userinfo_bp.route("/bookRead/delete")  # 삭제
def delete_book_read(name):
    title = request.args.get("title")
    UserRead.delete_read_book(name, title)
    return redirect(url_for("userinfo.get_book_read", name=name))


@userinfo_bp.route("/bookRead/insert")  # 추가
def insert_book_read(name):
    title = request.args.get("title")
    UserRead.insert_read_book(name, title)
    return redirect(url_for("userinfo.get_book_read", name=name))


# 위시리스트
@userinfo_bp.route("/bookWant/")  # 조회
def get_book_want(name):
    return UserWish.get_book_want(name)


@userinfo_bp.route("/bookWant/delete")  # 삭제
def delete_book_want(name):
    title = request.args.get("title")
    UserWish.delete_book_want(name, title)
    return redirect(url_for("userinfo.get_book_want", name=name))


@userinfo_bp.route("/bookWant/insert")  # 추가
def insert_book_want(name):
    title = request.args.get("title")
    UserWish.insert_book_want(name, title)
    return redirect(url_for("userinfo.get_book_want", name=name))


# 선호작가
@userinfo_bp.route("/interestAuthor/")  # 조회
def get_interest_author(name):
    return UserAuthor.get_interest_author(name)


@userinfo_bp.route("/interestAuthor/delete")  # 삭제
def delete_interest_author(name):
    author = request.args.get("author")
    UserAuthor.delete_interest_author(name, author)
    return redirect(url_for("userinfo.get_interest_author", name=name))


@userinfo_bp.route("/interestAuthor/insert")  # 추가
def insert_interest_author(name):
    author = request.args.get("author")
    UserAuthor.insert_interest_author(name, author)
    return redirect(url_for("userinfo.get_interest_author", name=name))


# 선호장르
@userinfo_bp.route("/interestGenre/")  # 조회
def get_interest_genre(name):
    return UserGenre.get_interest_genre(name)


@userinfo_bp.route("/interestGenre/delete")  # 삭제
def delete_interest_genre(name):
    genre = request.args.get("genre")
    UserGenre.delete_interest_genre(name, genre)
    return redirect(url_for("userinfo.get_interest_genre", name=name))


@userinfo_bp.route("/interestGenre/insert")  # 추가
def insert_interest_genre(name):
    genre = request.args.get("genre")
    UserGenre.insert_interest_genre(name, genre)
    return redirect(url_for("userinfo.get_interest_genre", name=name))
