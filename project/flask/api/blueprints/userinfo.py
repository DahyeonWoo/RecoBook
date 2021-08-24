from api.user import *
from flask import Blueprint, request

bp = Blueprint('userinfo', __name__, url_prefix='/userinfo')

@bp.route('/<name>/')
def get_user_info(name):
    return UserInfo.get_user(name)

@bp.route('/<name>/bookRead/')
def get_book_read(name):
    return UserRead.get_read_book(name)

@bp.route('/<name>/bookWant/')
def get_book_want(name):
    return UserWish.get_book_want(name)
    
@bp.route('/<name>/interestAuthor/')
def get_interest_author(name):
    return UserAuthor.get_interest_author(name)

@bp.route('/<name>/interestGenre/')
def get_interest_genre(name):
    return UserGenre.get_interest_genre(name)