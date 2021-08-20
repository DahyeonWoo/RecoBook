# -*- coding: utf-8 -*-
import sys
import json

sys.path.append("./project/flask/api")
from api.db_model.mysql import conn_mysqldb
from api.utils.CreateDict import create_dict
from api.utils.ColumnsFromDB import ColumnsFromDB


def get_title_to_info(title):
    """
    도서 제목을 검색하면 db에서 해당 도서의 정보를 조회
    :param title: 도서 제목
    :return: 도서 정보 딕셔너리
    """
    data = ColumnsFromDB.get_db_data("*", "Book", "title", title)
    return json.dumps(data, indent=2, default=str, ensure_ascii=False)


def get_isbn_to_info(isbn13):
    """
    도서 ISBN13을 검색하면 db에서 해당 도서의 정보를 조회
    :param isbn13: 도서 ISBN13
    :return: 도서 정보 딕셔너리
    """
    data = ColumnsFromDB.get_db_data("*", "Book", "isbn13", isbn13)
    return json.dumps(data, indent=2, default=str, ensure_ascii=False)


def get_author_to_info(name):
    """
    도서 작가를 검색하면 db에서 해당 도서의 정보를 조회
    :param name: 도서 작가
    :return: 도서 정보 딕셔너리
    """
    data = ColumnsFromDB.get_db_data("*", "Book", "author", name)
    return json.dumps(data, indent=2, default=str, ensure_ascii=False)


def get_title_to_review(title):
    """
    도서 제목을 검색하면 db에서 해당 도서의 리뷰를 조회
    :param title: 도서 제목
    :return: 도서 리뷰 딕셔너리
    """
    db = conn_mysqldb()
    cursor = db.cursor()
    sql = """
    SELECT Review.review 
    FROM Review 
    INNER JOIN Book 
    ON Review.isbn13 = Book.isbn13
    WHERE title 
    LIKE %s
    """
    cursor.execute(sql, f"%{title}%")
    book_info = cursor.fetchone()
    if not book_info:
        return None
    else:
        return json.dumps(book_info, indent=2, default=str, ensure_ascii=False)


if __name__ == "__main__":
    # res = Book.get_title_to_review('달러구트')
    # res = get_title_to_info('금각사')
    # res = get_title_to_info2('금각 사')
    # res = get_author_to_info('이미예')
    res = get_isbn_to_info("9791165341909")
    print(res)
    print(len(res))
