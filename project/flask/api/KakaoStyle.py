
from utils.ColumnsFromDB import ColumnsFromDB

from book import BookInfo

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
                                    "title" : "출판사",
                                    "description": publisher
                                },
                                {
                                    "title" : "가격",
                                    "description": priceStandard
                                },
                                {
                                    "title" : "출판사",
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
                        #author
                        "description": BookInfo.get_author_info(first)
                        },
                        {
                        "title": second,
                        #author
                        "description": BookInfo.get_title_to_info(second)
                        },
                        {
                        "title": third,
                        #author
                        "description": BookInfo.get_title_to_info(third)
                        },
                        {
                        "title": fourth,
                        #author
                        "description": BookInfo.get_title_to_info(fourth)
                        },
                        {
                        "title": fifth,
                        #author
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
                            "imageUrl": BookInfo.get_title_to_info(first)['cover']
                        },
                        "buttons": [
                            {
                            "action":  "webLink",
                            "label": "상세보기",
                            "webLinkUrl": BookInfo.get_title_to_info(first)['link']
                            }
                        ]
                        },
                        {
                        "title": BookInfo.get_title_to_info(second)['title'],
                        "description": BookInfo.get_title_to_info(second)['author'],
                        "thumbnail": {
                            "imageUrl": BookInfo.get_title_to_info(second)['cover']
                        },
                        "buttons": [
                            {
                            "action":  "webLink",
                            "label": "상세보기",
                            "webLinkUrl": BookInfo.get_title_to_info(second)['link']
                            }
                        ]
                        },
                        {
                        "title": BookInfo.get_title_to_info(third)['title'],
                        "description": BookInfo.get_title_to_info(third)['author'],
                        "thumbnail": {
                            "imageUrl": BookInfo.get_title_to_info(third)['cover']
                        },
                        "buttons": [
                            {
                            "action":  "webLink",
                            "label": "상세보기",
                            "webLinkUrl": BookInfo.get_title_to_info(third)['link']
                            }
                        ]
                        },

                        {
                        "title": BookInfo.get_title_to_info(fourth)['title'],
                        "description": BookInfo.get_title_to_info(fourth)['author'],
                        "thumbnail": {
                            "imageUrl": BookInfo.get_title_to_info(fourth)['cover']
                        },
                        "buttons": [
                            {
                            "action":  "webLink",
                            "label": "상세보기",
                            "webLinkUrl": BookInfo.get_title_to_info(fourth)['link']
                            }
                        ]
                        },

                        {
                        "title": BookInfo.get_title_to_info(fifth)['title'],
                        "description": BookInfo.get_title_to_info(fifth)['author'],
                        "thumbnail": {
                            "imageUrl": BookInfo.get_title_to_info(fifth)['cover']
                        },
                        "buttons": [
                            {
                            "action":  "webLink",
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

    def oneItem_title(title):
        responseBody = {
            "title": BookInfo.get_title_to_info(title)['title'],
            "description": BookInfo.get_title_to_info(title)['author'],
            "thumbnail": {
                "imageUrl": BookInfo.get_title_to_info(title)['cover']
            },
            "buttons": [
                {
                "action":  "webLink",
                "label": "상세보기",
                "webLinkUrl": BookInfo.get_title_to_info(title)['link']
                }
            ]
        }
        return responseBody

    def oneItem_title_stats(title, howManyRead, verb):
        responseBody = {
            "title": BookInfo.get_title_to_info(title)['title'],
            "description": str(howManyRead) + " 명 " + verb,
            "thumbnail": {
                "imageUrl": BookInfo.get_title_to_info(title)['cover']
            },
            "buttons": [
                {
                "action":  "webLink",
                "label": "상세보기",
                "webLinkUrl": BookInfo.get_title_to_info(title)['link']
                }
            ]
        }
        return responseBody

    def oneItem_author(author):
        responseBody = {
            "title": BookInfo.get_author_info(author)['name'],
            "description": BookInfo.get_author_info(author)['description'],
        }
        return responseBody

    # 개수에 따라 변하는 케로셀
    @staticmethod
    def ElasticCarousel(subject, topFive):
        '''
        topFive는 책(읽은 책, 위시리스트, 관심 책)목록이 리스트 형태로 주어진다. 최대 5개
        '''
        howMany = len(topFive)
        paramList = ['first', 'second', 'third', 'fourth', 'fifth']

        for i in range(howMany):
            paramList[i] = topFive[i]

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
        for i in range(howMany):
            itemSection.append(KakaoStyle.oneItem_title(paramList[i]))
        return frame

    @staticmethod
    def ElasticCarousel2(subject, data, count, verb):
        '''
        data는 책(top읽은 책, top위시리트스, top관심 책)목록이 dictionary 형태로 주어진다. 최대 5개
        '''
        #책 제목
        paramList = ['first', 'second', 'third', 'fourth', 'fifth']
        #읽은 사람 수
        paramList_count = ['first_c', 'second_c', 'third_c', 'fourth_c', 'fifth_c']

        for i in range(count):
            paramList[i] = data[i+1]["name"]
            paramList_count[i] = data[i+1]["count"]

        print(paramList)
        print(paramList_count)

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

    # 개수에 따라 변하는 리스트
    def ElasticList(subject, topFive):
        howMany = len(topFive)
        paramList = ['first', 'second', 'third', 'fourth', 'fifth']

        for i in range(howMany):
            paramList[i] = topFive[i]

        frame = {
            "version": "2.0",
            "template": {
                "outputs": [
                {
                    "listCard": {
                    "header": {
                        "title": subject + "목록"
                    },
                    "items": [
                        
                    ]
                    }
                }
                ]
            }
        }
        itemSection = frame['template']['outputs'][0]['listCard']['items']
        for i in range(howMany):
            itemSection.append(KakaoStyle.oneItem_author(paramList[i]))
        return frame

if __name__=='__main__':
    res = KakaoStyle.Style1('a','b','c','d','e', 'f', 'g')
    list = ['부자들의 생각법', '구운몽', '종의 기원', '종의 기원', '종의 기원']
    # res = KakaoStyle.Style2('부자들의 생각법', list)
    data = {1: {'name': '불안한 사람들', 'count': 18}, 2: {'name': '7년의 밤', 'count': 9}, 3: {'name': '종의 기원', 'count': 7}}
    #res = KakaoStyle.ElasticCarousel('읽은 책', list)
    
    #res = KakaoStyle.ElasticCarousel2('읽은 책', data, 3, '읽음')
    print(res)
    

