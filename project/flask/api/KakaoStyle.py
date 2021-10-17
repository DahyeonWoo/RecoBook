# -*- coding: utf-8 -*-
import sys
sys.path.append("./project/flask/api")
import json
from api.author import Author
from api.utils.ColumnsFromDB import ColumnsFromDB
from api.book import BookInfo


class KakaoStyle:

    # get info - title / isbn
    @staticmethod
    def Style1(title, cover, description, author, publisher, priceStandard, link):
        responseBody = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "itemCard": {
                            "imageTitle": {
                                "title": title,
                                "description": description
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
                                {
                                    "title": "출판사",
                                    "description": publisher
                                },
                                {
                                    "title": "가격",
                                    "description": priceStandard
                                },
                                {
                                    "title": "출판사",
                                    "description": publisher
                                }
                            ],

                            "buttons": [
                                {
                                    "label": "상세보기",
                                    "action": "webLink",
                                    "webLinkUrl": link
                                }
                            ],
                            "buttonLayout": "vertical"
                        }
                    }
                ]
            }
        }
        return responseBody

    # 리스트카드 (책 제목과 유사한 책)
    @staticmethod
    def Style2(title, topFive, review=False):
        """
        params: title: 스타일 제목
        params: topFive: 5개 제목이 담긴 리스트
        params: review: Review 테이블 사용 여부
        """
        first = topFive[0]
        second = topFive[1]
        third = topFive[2]
        fourth = topFive[3]
        fifth = topFive[4]

        # for i in topFive:
        title_text = title + ' 유사한 책'
        responseBody = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "listCard": {
                            "header": {
                                "title": title_text
                            },
                            "items": [
                                {
                                    "title": first,
                                    # author
                                    "description": BookInfo.get_title_to_info(first)['author'],
                                    "imageUrl": BookInfo.get_title_to_info(first)['resizedCover'],
                                    "link": {
                                        "web": BookInfo.get_title_to_info(first)['link']
                                    }
                                },
                                {
                                    "title": second,
                                    # author
                                    "description": BookInfo.get_title_to_info(second)['author'],
                                    "imageUrl": BookInfo.get_title_to_info(second)['resizedCover'],
                                    "link": {
                                        "web": BookInfo.get_title_to_info(second)['link']
                                    }
                                },
                                {
                                    "title": third,
                                    # author
                                    "description": BookInfo.get_title_to_info(third)['author'],
                                    "imageUrl": BookInfo.get_title_to_info(third)['resizedCover'],
                                    "link": {
                                        "web": BookInfo.get_title_to_info(third)['link']
                                    }
                                },
                                {
                                    "title": fourth,
                                    # author
                                    "description": BookInfo.get_title_to_info(fourth)['author'],
                                    "imageUrl": BookInfo.get_title_to_info(fourth)['resizedCover'],
                                    "link": {
                                        "web": BookInfo.get_title_to_info(fourth)['link']
                                    }
                                },
                                {
                                    "title": fifth,
                                    # author
                                    "description": BookInfo.get_title_to_info(fifth)['author'],
                                    "imageUrl": BookInfo.get_title_to_info(fifth)['resizedCover'],
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

    # 리스트카드 (작가와 유사한 작가)
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
                                "title": author + " 작가와 유사한 작가"
                            },
                            "items": [
                                {
                                    "title": first,
                                    # author
                                    "description": BookInfo.get_author_info(first)
                                },
                                {
                                    "title": second,
                                    # author
                                    "description": BookInfo.get_title_to_info(second)
                                },
                                {
                                    "title": third,
                                    # author
                                    "description": BookInfo.get_title_to_info(third)
                                },
                                {
                                    "title": fourth,
                                    # author
                                    "description": BookInfo.get_title_to_info(fourth)
                                },
                                {
                                    "title": fifth,
                                    # author
                                    "description": BookInfo.get_title_to_info(fifth)
                                }
                            ]
                        }
                    }
                ]
            }

        }
        return responseBody

    # 캐로셀 (basicCard)
    @staticmethod
    def Carousel(title, topFive):
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
                        "simpleText": {
                            "text": title + " 유사한 책을 추천드려요."
                        }
                    },
                    {
                        "carousel": {
                            "type": "basicCard",
                            "items": [
                                {
                                    "title": BookInfo.get_title_to_info(first)['title'],
                                    "description": BookInfo.get_title_to_info(first)['author'],
                                    "thumbnail": {
                                        "imageUrl": BookInfo.get_title_to_info(first)['resizedCover']
                                    },
                                    "buttons": [
                                        {
                                            "action": "webLink",
                                            "label": "상세보기",
                                            "webLinkUrl": BookInfo.get_title_to_info(first)['link']
                                        }
                                    ]
                                },
                                {
                                    "title": BookInfo.get_title_to_info(second)['title'],
                                    "description": BookInfo.get_title_to_info(second)['author'],
                                    "thumbnail": {
                                        "imageUrl": BookInfo.get_title_to_info(second)['resizedCover']
                                    },
                                    "buttons": [
                                        {
                                            "action": "webLink",
                                            "label": "상세보기",
                                            "webLinkUrl": BookInfo.get_title_to_info(second)['link']
                                        }
                                    ]
                                },
                                {
                                    "title": BookInfo.get_title_to_info(third)['title'],
                                    "description": BookInfo.get_title_to_info(third)['author'],
                                    "thumbnail": {
                                        "imageUrl": BookInfo.get_title_to_info(third)['resizedCover']
                                    },
                                    "buttons": [
                                        {
                                            "action": "webLink",
                                            "label": "상세보기",
                                            "webLinkUrl": BookInfo.get_title_to_info(third)['link']
                                        }
                                    ]
                                },

                                {
                                    "title": BookInfo.get_title_to_info(fourth)['title'],
                                    "description": BookInfo.get_title_to_info(fourth)['author'],
                                    "thumbnail": {
                                        "imageUrl": BookInfo.get_title_to_info(fourth)['resizedCover']
                                    },
                                    "buttons": [
                                        {
                                            "action": "webLink",
                                            "label": "상세보기",
                                            "webLinkUrl": BookInfo.get_title_to_info(fourth)['link']
                                        }
                                    ]
                                },

                                {
                                    "title": BookInfo.get_title_to_info(fifth)['title'],
                                    "description": BookInfo.get_title_to_info(fifth)['author'],
                                    "thumbnail": {
                                        "imageUrl": BookInfo.get_title_to_info(fifth)['resizedCover']
                                    },
                                    "buttons": [
                                        {
                                            "action": "webLink",
                                            "label": "상세보기",
                                            "webLinkUrl": BookInfo.get_title_to_info(fifth)['link']
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                ]
            }
        }

    # 캐로셀 (유저 기반 책 추천)
    @staticmethod
    def Carousel2(topFive, keyword=''):

        first = json.loads(BookInfo.get_isbn_to_info(topFive[0]))
        print(first)
        second = json.loads(BookInfo.get_isbn_to_info(topFive[1]))
        third = json.loads(BookInfo.get_isbn_to_info(topFive[2]))
        fourth = json.loads(BookInfo.get_isbn_to_info(topFive[3]))
        fifth = json.loads(BookInfo.get_isbn_to_info(topFive[4]))

        responseBody = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": keyword + " 좋아할만한 책"
                        }
                    },
                    {
                        "carousel": {
                            "type": "basicCard",
                            "items": [
                                {
                                    "title": first['title'],
                                    "description": first['author'],
                                    "thumbnail": {
                                        "imageUrl": first['resizedCover']
                                    },
                                    "buttons": [
                                        {
                                            "action": "webLink",
                                            "label": "상세보기",
                                            "webLinkUrl": first['link']
                                        }
                                    ]
                                },
                                {
                                    "title": second['title'],
                                    "description": second['author'],
                                    "thumbnail": {
                                        "imageUrl": second['resizedCover']
                                    },
                                    "buttons": [
                                        {
                                            "action": "webLink",
                                            "label": "상세보기",
                                            "webLinkUrl": second['link']
                                        }
                                    ]
                                },
                                {
                                    "title": third['title'],
                                    "description": third['author'],
                                    "thumbnail": {
                                        "imageUrl": third['resizedCover']
                                    },
                                    "buttons": [
                                        {
                                            "action": "webLink",
                                            "label": "상세보기",
                                            "webLinkUrl": third['link']
                                        }
                                    ]
                                },

                                {
                                    "title": fourth['title'],
                                    "description": fourth['author'],
                                    "thumbnail": {
                                        "imageUrl": fourth['resizedCover']
                                    },
                                    "buttons": [
                                        {
                                            "action": "webLink",
                                            "label": "상세보기",
                                            "webLinkUrl": fourth['link']
                                        }
                                    ]
                                },

                                {
                                    "title": fifth['title'],
                                    "description": fifth['author'],
                                    "thumbnail": {
                                        "imageUrl": fifth['resizedCover']
                                    },
                                    "buttons": [
                                        {
                                            "action": "webLink",
                                            "label": "상세보기",
                                            "webLinkUrl": fifth['link']
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                ]
            }
        }
        return responseBody

    @staticmethod
    def Carousel3(topFive, keyword=''):
        """
        작가 추천 캐로셀
        """
        first = json.loads(Author.get_author_info(topFive[0]))
        print(first)
        second = json.loads(Author.get_author_info(topFive[1]))
        third = json.loads(Author.get_author_info(topFive[2]))
        fourth = json.loads(Author.get_author_info(topFive[3]))
        fifth = json.loads(Author.get_author_info(topFive[4]))

        responseBody = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": keyword + " 유사한 작가"
                        }
                    },
                    {
                        "carousel": {
                            "type": "basicCard",
                            "items": [
                                {
                                    "name": first['author'],
                                    "description": first['info'],
                                },
                                {
                                    "name": second['author'],
                                    "description": second['info'],
                                },
                                {
                                    "name": third['author'],
                                    "description": third['info'],
                                },
                                {
                                    "name": fourth['author'],
                                    "description": fourth['info'],
                                },
                                {
                                    "name": fifth['author'],
                                    "description": fifth['info'],
                                },
                            ]
                        }
                    }
                ]
            }
        }
                    
        return responseBody

    def oneItem_title(title):
        print(title)
        responseBody = {
            "title": BookInfo.get_title_to_info(title)['title'],
            "description": BookInfo.get_title_to_info(title)['author'],
            "thumbnail": {
                "imageUrl": BookInfo.get_title_to_info(title)['resizedCover']
            },
            "buttons": [
                {
                    #"action": "webLink",
                    "action":"message",
                    "label": "내 코멘트 보기",
                    #"webLinkUrl": BookInfo.get_title_to_info(title)['link']
                    "messageText": "너무너무 재밌었어. 인생소설..! 재탕 300번 해야지"
                }
            ]
        }
        return responseBody

    def oneItem_title_stats(title, howManyRead, verb):
        responseBody = {
            "title": BookInfo.get_title_to_info(title)['title'],
            "description": str(howManyRead) + " 명 " + verb,
            "thumbnail": {
                "imageUrl": BookInfo.get_title_to_info(title)['resizedCover']
            },
            "buttons": [
                {
                    "action": "webLink",
                    "label": "상세보기",
                    "webLinkUrl": BookInfo.get_title_to_info(title)['link']
                }
            ]
        }
        return responseBody

    def oneItem_author(author):
        responseBody = {
            "title": BookInfo.get_author_to_author_info(author)["name"],
            "description": BookInfo.get_author_to_author_info(author)["description"],
        }
        return responseBody

    # basic card carousel
    @staticmethod
    def ElasticBasicCard(reqinfo,param):

        paramList = param.split(';')
        print(paramList)
        number = len(paramList)
        for i in range(number):
            print(paramList[i])

        frame = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "carousel": {
                            "type": "basicCard",
                            "items": [

                            ]
                        }
                    }
                ]
            }
        }

        itemSection = frame['template']['outputs'][0]['carousel']['items']
        for i in range(number):
            if reqinfo == "interestAuthor":
                itemSection.append(KakaoStyle.oneItem_author(paramList[i]))
            else:
                itemSection.append(KakaoStyle.oneItem_title(paramList[i]))
        return frame

    # list card carousel
    @staticmethod
    def ElasticBasicList(answer, param):
        paramList = param.split(';')
        print(paramList)
        number = len(paramList)
        for i in range(number):
            print(paramList[i])

        frame = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "listCard": {
                            "header": {
                                "title": answer
                            },
                            "items": [

                            ]
                        }
                    }
                ]
            }
        }
        itemSection = frame['template']['outputs'][0]['carousel']['items']
        for i in range(number):
            itemSection.append(KakaoStyle.oneItem_title(paramList[i]))
        return frame

    @staticmethod
    def ElasticBasicListTop(subject, data, count, verb):
        '''
        data는 책(top읽은 책, top위시리트스, top관심 책)목록이 dictionary 형태로 주어진다. 최대 5개
        '''

        print(subject, data, count, verb)


        # 책 제목
        paramList = ['first', 'second', 'third', 'fourth', 'fifth']
        # 읽은 사람 수
        paramList_count = ['first_c', 'second_c', 'third_c', 'fourth_c', 'fifth_c']

        for i in range(count):
            paramList[i] = data[i + 1]["name"]
            paramList_count[i] = data[i + 1]["count"]

            print(paramList[i])

        frame = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "listCard": {
                            "header": {
                                "title": subject + " 목록"
                            },
                            "items": [

                            ]
                        }
                    }
                ]
            }
        }
        itemSection = frame['template']['outputs'][0]['listCard']['items']
        for i in range(count):
            itemSection.append(KakaoStyle.oneItem_title_stats(paramList[i], paramList_count[i], verb))
        return frame

if __name__ == '__main__':
    res = KakaoStyle.Style1('a', 'b', 'c', 'd', 'e', 'f', 'g')
    list = ['부자들의 생각법', '구운몽', '종의 기원', '종의 기원', '종의 기원']
    # res = KakaoStyle.Style2('부자들의 생각법', list)
    data = {1: {'name': '불안한 사람들', 'count': 18}, 2: {'name': '7년의 밤', 'count': 9}, 3: {'name': '종의 기원', 'count': 7}}
    # res = KakaoStyle.ElasticCarousel('읽은 책', list)

    # res = KakaoStyle.ElasticCarousel2('읽은 책', data, 3, '읽음')
    print(res)