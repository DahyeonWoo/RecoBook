# -*- coding: utf-8 -*-
import sys

sys.path.append("./project/flask/")
sys.path.append("./project/flask/api/")
import json

from api.db_model.mysql import conn_mysqldb
from api.utils.ColumnsFromDB import ColumnsFromDB


class UserInfo:
    @staticmethod
    def post_user(
        name,
        birthday,
        age,
        gender,
        bookRead,
        bookWant,
        interestBook,
        interestAuthor,
        interestCategory,
    ):
        """
        유저 정보를 업데이트 하는 함수
        """
        db = conn_mysqldb()
        db_cursor = db.cursor()
        sql = """INSERT INTO User(name, birthday, age, gender, bookRead, bookWant, interestBook, interestAuthor,interestCategory) 
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
        db_cursor.execute(
            sql,
            (
                name,
                birthday,
                age,
                gender,
                bookRead,
                bookWant,
                interestBook,
                interestAuthor,
                interestCategory,
            ),
        )
        db.commit()
        db_cursor.close()

    @staticmethod
    def get_user(name: str):
        """
        유저 정보를 가져오는 함수
        :params name: 유저의 이름
        :return: 유저 정보
        """
        user = ColumnsFromDB.get_db_data("*", "User", "name", name)
        return json.dumps(user, indent=2, default=str, ensure_ascii=False)


class UserRead:
    @staticmethod
    def get_read_book(user_name):
        """
        읽은 책 리스트를 가져오는 함수
        :params user_name: 유저의 이름 
        :return: 읽은 책 리스트
        """
        user = ColumnsFromDB.get_db_data("bookRead", "User", "name", user_name)
        return json.dumps(user, indent=2, default=str, ensure_ascii=False)

    @staticmethod
    def insert_read_book(user_name, title):
        """
        읽은 책을 추가하는 함수
        :params name: 사용자의 이름
        :params title: 추가할 책 이름
        """
        ColumnsFromDB.insert_db_data("User", "bookRead", "name", user_name, title)

    @staticmethod
    def delete_read_book(user_name, title):
        """
        읽은 책 삭제하는 함수
        :params name: 사용자의 이름
        :params book: 삭제할 책 이름
        """
        ColumnsFromDB.delete_db_data("User", "bookRead", "name", user_name, title)


class UserWish:
    @staticmethod
    def get_book_want(user_name):
        """
        위시 리스트를 가져오는 함수
        :params user_name: 유저의 이름 
        :return: 위시 리스트
        """
        book_want = ColumnsFromDB.get_db_data("bookWant", "User", "name", user_name)
        return json.dumps(book_want, indent=2, default=str, ensure_ascii=False)

    @staticmethod
    def insert_book_want(user_name, title):
        """
        위시 리스트를 추가하는 함수
        :params user_name: 사용자의 이름
        :params title: 추가할 책 이름
        """
        ColumnsFromDB.insert_db_data("User", "bookWant", "name", user_name, title)

    @staticmethod
    def delete_book_want(user_name, title):
        """
        위시 리스트를 삭제하는 함수
        :params user_name: 사용자의 이름
        :params title: 삭제할 책 이름
        """
        ColumnsFromDB.delete_db_data("User", "bookWant", "name", user_name, title)


class UserAuthor:
    @staticmethod
    def get_interest_author(user_name):
        """
        선호 작가 목록을 가져오는 함수
        :params user_name: 유저의 이름
        :return: 선호 작가 목록
        """
        author_list = ColumnsFromDB.get_db_data(
            "InterestAuthor", "User", "name", user_name
        )
        return json.dumps(author_list, indent=2, default=str, ensure_ascii=False)

    @staticmethod
    def insert_interest_author(user_name, author_name):
        """
        선호 작가를 추가하는 함수
        :params user_name: 유저의 이름
        :params author_name: 추가할 작가의 이름
        """
        ColumnsFromDB.insert_db_data(
            "User", "interestAuthor", "name", user_name, author_name
        )

    @staticmethod
    def delete_interest_author(user_name, author_name):
        """
        선호 작가를 삭제하는 함수
        :params user_name: 유저의 이름
        :params author_name: 삭제할 작가의 이름
        """
        ColumnsFromDB.delete_db_data(
            "User", "interestAuthor", "name", user_name, author_name
        )


class UserGenre:
    @staticmethod
    def get_interest_genre(user_name):
        """
        선호 장르 목록을 가져오는 함수
        :params user_name: 유저의 이름
        :return: 선호 장르 목록
        """
        genre_list = ColumnsFromDB.get_db_data(
            "interestCategory", "User", "name", user_name
        )
        return json.dumps(genre_list, indent=2, default=str, ensure_ascii=False)

    @staticmethod
    def insert_interest_genre(user_name, genre):
        """
        선호 장르를 추가하는 함수
        :params user_name: 유저의 이름
        :params genre: 추가할 장르
        """
        ColumnsFromDB.insert_db_data(
            "User", "interestCategory", "name", user_name, genre
        )

    @staticmethod
    def delete_interest_genre(user_name, genre):
        """
        선호 장르를 삭제하는 함수
        :params user_name: 유저의 이름
        :params genre: 삭제할 장르
        """
        ColumnsFromDB.delete_db_data(
            "User", "interestCategory", "name", user_name, genre
        )


if __name__ == "__main__":
    # post_user('이독자','2000-07-07',22, 'M','밤의 여행자들','밝은 밤','이웃집 밤','이지은','소설')
    # res = UserRead.get_read_book('이현준') # 읽은 책 가져오기
    # print(list(res.values())[0])
    res = UserRead.insert_read_book("이현준", "아몬드")  # 읽은 책 추가
    # res = UserRead.delete_read_book('김민준', '아몬드') # 읽은 책 삭제
    # res = UserWish.insert_book_want('김민준', '아몬드')
    # res = UserWish.delete_book_want('김민준', '아몬드')
    # res = UserWish.get_book_want('김민준')
    # res = UserAuthor.insert_interest_author('김민준', '김영하')
    # res = UserAuthor.delete_interest_author('김민준', '김영하')
    # res = UserAuthor.get_interest_author('김민준')
    # res = UserGenre.insert_interest_genre('박지훈', '로맨스')
    # res = UserGenre.delete_interest_genre('박지훈', '로맨스')
    # res = UserGenre.get_interest_genre("박지훈")
    # res = UserRead.get_db_data("이현준", "*")

    print(res)
