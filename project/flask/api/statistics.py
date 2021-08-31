import sys

sys.path.append("./project/flask/")
sys.path.append("./project/flask/api/")
from api.utils.ColumnsFromDB import ColumnsFromDB
from api.utils.Agg import get_topn

"""
top n 개의 통계량을 반환
"""


def get_topn_bookRead(n):
    return get_topn("bookRead", "User", n)


def get_topn_bookWant(n):
    return get_topn("bookWant", "User", n)


def get_topn_interestAuthor(n):
    return get_topn("interestAuthor", "User", n)


def get_topn_interestGenre(n):
    return get_topn("interestCategory", "User", n)


if __name__ == "__main__":
    n=3
    print(get_topn_bookRead(n))
    print(get_topn_bookWant(n))
    print(get_topn_interestAuthor(n))
    print(get_topn_interestGenre(n))
