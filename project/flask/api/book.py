# -*- coding: utf-8 -*-
import sys
import json
sys.path.append("./project/flask/")
sys.path.append("./project/flask/api")
from api.db_model.mysql import conn_mysqldb
from api.utils.ColumnsFromDB import ColumnsFromDB

class BookInfo:
    def get_title_to_info(title):
        """
        도서 제목을 검색하면 db에서 해당 도서의 정보를 조회
        :param title: 도서 제목
        :return: 도서 정보 딕셔너리
        """
        data = ColumnsFromDB.get_db_data("*", "Book", "title", title)
        return json.dumps(data, indent=2, default=str, ensure_ascii=False)

    def get_title_to_info_style(title):
        data = ColumnsFromDB.get_db_data(db_col="*", table_name="Book", col="title", param=title)
        
        responseBody = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "itemCard": {
                            "imageTitle": {
                                "title": data['title'],
                                "description": data['description']
                            },
                            "title": "",
                            "description": "",
                            "thumbnail": {
                                "imageUrl": data['cover'],
                                "width": 800,
                                "height": 800
                            },
                            '''
                            "profile": {
                                "title": "AA Airline",
                                "imageUrl": "https://t1.kakaocdn.net/openbuilder/docs_image/aaairline.jpg"
                            },
                            '''
                            "itemList": [
                                {
                                    "title": "ISBN13",
                                    "description": data['isbn13']
                                },
                                {
                                    "title": "작가",
                                    "description": data['author']
                                },
                                {
                                    "title": "출판사",
                                    "description": data['publisher']
                                },
                                {
                                    "title": "가격",
                                    "description": data['priceStandard']
                                },
                                {
                                    "title": "평점",
                                    "description": data['customerReviewRank']
                                }
                            ],
                            '''
                            "itemListAlignment" : "right",
                            "itemListSummary": {
                                "title": "Total",
                                "description": "$4,032.54"
                            },
                            '''
                            "buttons": [
                                {
                                    "label": "상세보기",
                                    "action": "webLink",
                                    "webLinkUrl": data['link']
                                }
                            ],
                            "buttonLayout" : "vertical"
                        }
                    }
                ]
            }
        }
        return responseBody


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
    # res = BookInfo.get_isbn_to_info("9791165341909")
    # res = BookInfo.get_title_to_review('달러구트 꿈 백화점')
    # print(res)
    # print(len(res))

    res = BookInfo.get_title_to_info_style('부자들의 생각법')
    print(res)