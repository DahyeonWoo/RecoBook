
from utils.ColumnsFromDB import ColumnsFromDB

from book import BookInfo

class KakaoStyle:

    # get info - title / isbn
    @staticmethod
    def Style1(title, cover, author, link):
        responseBody = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "itemCard": {
                            "imageTitle": {
                                "title": title,
                                "description": ""
                            },
                            "title": "",
                            "description": "",
                            "thumbnail": {
                                "imageUrl": cover,
                                "width": 800,
                                "height": 800
                            },
                            
                            "itemList": [
                                {
                                    "title": "작가",
                                    "description": author
                                },
                            ],
                            
                            "buttons": [
                                {
                                    "label": "상세보기",
                                    "action": "webLink",
                                    "webLinkUrl": link
                                }
                            ],
                            "buttonLayout" : "vertical"
                        }
                    }
                ]
            }
        }
        return responseBody

    # 리스트카드 (책 제목과 유사한 책)
    @staticmethod
    def Style2(title, topFive):
        first = topFive[0]
        second = topFive[1]
        third = topFive[2]
        fourth = topFive[3]
        fifth = topFive[4]

        responseBody = {
            "version": "2.0",
            "template": {
                "outputs": [
                {
                    "listCard": {
                    "header": {
                        "title": title + " 유사한 책"
                    },
                    "items": [
                        {
                        "title": first,
                        #author
                        "description": BookInfo.get_title_to_info(first)['author'],
                        "imageUrl": BookInfo.get_title_to_info(first)['cover'],
                        "link": {
                            "web": BookInfo.get_title_to_info(first)['link']
                            }
                        },
                        {
                        "title": second,
                        #author
                        "description": BookInfo.get_title_to_info(second)['author'],
                        "imageUrl": BookInfo.get_title_to_info(second)['cover'],
                        "link": {
                            "web": BookInfo.get_title_to_info(second)['link']
                            }
                        },
                        {
                        "title": third,
                        #author
                        "description": BookInfo.get_title_to_info(third)['author'],
                        "imageUrl": BookInfo.get_title_to_info(third)['cover'],
                        "link": {
                            "web": BookInfo.get_title_to_info(third)['link']
                            }
                        },
                        {
                        "title": fourth,
                        #author
                        "description": BookInfo.get_title_to_info(fourth)['author'],
                        "imageUrl": BookInfo.get_title_to_info(fourth)['cover'],
                        "link": {
                            "web": BookInfo.get_title_to_info(fourth)['link']
                            }
                        },
                        {
                        "title": fifth,
                        #author
                        "description": BookInfo.get_title_to_info(fifth)['author'],
                        "imageUrl": BookInfo.get_title_to_info(fifth)['cover'],
                        "link": {
                            "web": BookInfo.get_title_to_info(fifth)['link']
                            }
                        }
                    ]
                    }
                }
                ]
            }

        }
        return responseBody
        
    # 리스트카드 (작가와 유사한 책)
    @staticmethod
    def Style3(author, topFive):
        first = topFive[0]
        second = topFive[1]
        third = topFive[2]
        fourth = topFive[3]
        fifth = topFive[4]

        responseBody = {
            "version": "2.0",
            "template": {
                "outputs": [
                {
                    "listCard": {
                    "header": {
                        "title": author + " 작가가 쓴 책과 유사한 책"
                    },
                    "items": [
                        {
                        "title": first,
                        #author
                        "description": BookInfo.get_title_to_info(first)['author'],
                        "imageUrl": BookInfo.get_title_to_info(first)['cover'],
                        "link": {
                            "web": BookInfo.get_title_to_info(first)['link']
                            }
                        },
                        {
                        "title": second,
                        #author
                        "description": BookInfo.get_title_to_info(second)['author'],
                        "imageUrl": BookInfo.get_title_to_info(second)['cover'],
                        "link": {
                            "web": BookInfo.get_title_to_info(second)['link']
                            }
                        },
                        {
                        "title": third,
                        #author
                        "description": BookInfo.get_title_to_info(third)['author'],
                        "imageUrl": BookInfo.get_title_to_info(third)['cover'],
                        "link": {
                            "web": BookInfo.get_title_to_info(third)['link']
                            }
                        },
                        {
                        "title": fourth,
                        #author
                        "description": BookInfo.get_title_to_info(fourth)['author'],
                        "imageUrl": BookInfo.get_title_to_info(fourth)['cover'],
                        "link": {
                            "web": BookInfo.get_title_to_info(fourth)['link']
                            }
                        },
                        {
                        "title": fifth,
                        #author
                        "description": BookInfo.get_title_to_info(fifth)['author'],
                        "imageUrl": BookInfo.get_title_to_info(fifth)['cover'],
                        "link": {
                            "web": BookInfo.get_title_to_info(fifth)['link']
                            }
                        }
                    ]
                    }
                }
                ]
            }

        }
        return responseBody

if __name__=='__main__':
    #res = KakaoStyle.Style1('a','b','c','d')
    list = ['부자들의 생각법', '구운몽', '종의 기원', '종의 기원', '종의 기원']
    res = KakaoStyle.Style2('부자들의 생각법', list)
    print(res)
    

