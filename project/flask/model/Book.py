import sys
import json
sys.path.insert(1, 'project/flask/api/db_model')
from mysql import conn_mysqldb

class Book:
    """
    1. 도서 정보 조회
    2. 도서 검색
        - 제목, 작가 등을 검색하면 결과 반환
    3. 도서 리뷰 조회
    4. 도서 작가 조회
    """
    @staticmethod
    def get_book_info(db, book_id):
        """
        도서 정보 조회
        :param db: 데이터베이스 연결 객체
        :param book_id: 도서 고유번호
        :return: 도서 정보 딕셔너리
        """
        db = conn_mysqldb()
        cursor = db.cursor()
        sql = "SELECT * FROM book WHERE book_id = %s"
        row = db.executeAll(sql, book_id)
        return row[0]


class Author:

    @staticmethod
    def get_author(name):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM Book WHERE author LIKE %s" 
        db_cursor.execute(sql, f"%{name}%")
        author = db_cursor.fetchall()
        if not author:
            return None
        return json.dump(author)

if __name__ == '__main__':
    res = Author.get_author('이지은')
    print(res)