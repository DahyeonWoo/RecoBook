# -*- coding: utf-8 -*-
from flask import Flask, request
app = Flask(__name__)

from utils.ColumnsFromDB import ColumnsFromDB

# 카카오톡 텍스트형 응답
@app.route('/api/sayHello', methods=['POST'])
def sayHello():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "안녕 hello I'm Ryan"
                    }
                }
            ]
        }
    }

    return responseBody


# 카카오톡 이미지형 응답
@app.route('/api/showHello', methods=['POST'])
def showHello():
    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleImage": {
                        "imageUrl": "https://t1.daumcdn.net/friends/prod/category/M001_friends_ryan2.jpg",
                        "altText": "hello I'm Ryan"
                    }
                }
            ]
        }
    }

    return responseBody

#카카오톡 도서 검색(제목)
@app.route('/api/bookInfo/title', methods=['POST'])
def get_title_to_info_style():
    body = request.get_json()
    title = body["action"]["detailParams"]["title"]["value"]
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)