import sys
import json
sys.path.insert(1, 'project/flask/model')
from db_model.mysql import conn_mysqldb
from CreateDict import create_dict

class Book:
    """
    1. 도서 정보 조회
        - 제목, 작가, isbn13으로 책 정보 조회
    2. 도서 리뷰 조회
    """
    @staticmethod
    def get_title_to_info(title):
        """
        도서 제목을 검색하면 db에서 해당 도서의 정보를 조회
        :param title: 도서 제목
        :return: 도서 정보 딕셔너리
        """

        dict = create_dict()
        db = conn_mysqldb()
        cursor = db.cursor()
        sql = "SELECT * FROM Book WHERE title LIKE %s"
        cursor.execute(sql, f"%{title}%")
        book_info = cursor.fetchall()
        if not book_info:
            return None
        else:
            for row in book_info:
                dict.add(row[0], {'title': row[1], 'url': row[2], 'author': row[3], 'datetime': row[4],
                 'description': row[5], 'publisher': row[6], 'price': row[7], 'status': row[8], 'img': row[9], 'salesPoint': row[10], 'adult': row[11], 'reviewRank': row[12], 'category': row[13], 'bestRank': row[14],})
            return json.dumps(dict, indent=2, default=str, ensure_ascii=False)

    @staticmethod
    def get_isbn_to_info(isbn13):
        """
        도서 ISBN13을 검색하면 db에서 해당 도서의 정보를 조회
        :param isbn13: 도서 ISBN13
        :return: 도서 정보 딕셔너리
        """
        dict = create_dict()
        db = conn_mysqldb()
        cursor = db.cursor()
        sql = "SELECT * FROM Book WHERE isbn13 = %s"
        cursor.execute(sql, f"{isbn13}")
        book_info = cursor.fetchone()
        if not book_info:
            return None
        else:
            dict.add(book_info[0],{'title': book_info[1], 'url': book_info[2], 'author': book_info[3], 'datetime': book_info[4],
                 'description': book_info[5], 'publisher': book_info[6], 'price': book_info[7], 'status': book_info[8], 'img': book_info[9], 'salesPoint': book_info[10], 'adult': book_info[11], 'reviewRank': book_info[12], 'category': book_info[13], 'bestRank': book_info[14],})
            return json.dumps(dict, indent=2, default=str, ensure_ascii=False)

    @staticmethod
    def get_author_to_info(name):
        """
        도서 작가를 검색하면 db에서 해당 도서의 정보를 조회
        :param name: 도서 작가
        :return: 도서 정보 딕셔너리
        """
        dict = create_dict()
        db = conn_mysqldb()
        cursor = db.cursor()
        sql = "SELECT * FROM Book WHERE author LIKE %s"
        cursor.execute(sql, f"%{name}%")
        book_info = cursor.fetchall()
        if not book_info:
            return None
        else:
            for row in book_info:
                dict.add(row[0], {'title': row[1], 'url': row[2], 'author': row[3], 'datetime': row[4],
                 'description': row[5], 'publisher': row[6], 'price': row[7], 'status': row[8], 'img': row[9], 'salesPoint': row[10], 'adult': row[11], 'reviewRank': row[12], 'category': row[13], 'bestRank': row[14],})
            return json.dumps(dict, indent=2, default=str, ensure_ascii=False)

    @staticmethod
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

if __name__ == '__main__':
    # res = Book.get_title_to_review('달러구트')
    # res = Book.get_title_to_info('달러구트')
    # res = Book.get_author_to_info('이미예')
    res = Book.get_isbn_to_info('9791165341909')
    print(res)
    print(len(res))
    