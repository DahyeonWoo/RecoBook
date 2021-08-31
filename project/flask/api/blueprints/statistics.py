from api import statistics
from flask import Blueprint
"""
statistics.py
읽은 책/위시리스트/선호작가/선호장르 topn 반환
"""
statistics_bp = Blueprint("statistics", __name__, url_prefix="/statistics")

n = 3

# 읽은 책
@statistics_bp.route("/bookRead/")
def get_book_read():
    return statistics.get_topn_bookRead(n)

# 위시리스트
@statistics_bp.route("/bookWant/")
def get_book_want():
    return statistics.get_topn_bookWant(n)

# 선호작가
@statistics_bp.route("/interestAuthor/")
def get_interest_author():
    return statistics.get_topn_interestAuthor(n)

# 선호장르
@statistics_bp.route("/interestGenre/")
def get_interest_genre():
    return statistics.get_topn_interestGenre(n)



