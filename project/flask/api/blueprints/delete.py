from api.user import *
from flask import Blueprint, request

delete_bp = Blueprint('delete', __name__, url_prefix='/delete')

# @delete_bp.route('/bookRead/')
# def delete_book_read(name):
#     return UserRead.delete_read_book(name)

# @delete_bp.route('/bookWant/')
# def delete_book_want(name):
#     return UserWish.delete_book_want(name)
    
# @delete_bp.route('/interestAuthor/')
# def delete_interest_author(name):
#     return UserAuthor.delete_interest_author(name)

# @delete_bp.route('/interestGenre/')
# def delete_interest_genre(name):
#     return UserGenre.delete_interest_genre(name)

# @delete_bp.route('/')