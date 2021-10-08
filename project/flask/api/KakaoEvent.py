# -*- coding: utf-8 -*-
from api.book import BookInfo


class KakaoEvent:
    def __init__(self):
        # 템플릿 버전
        self.version = "2.0"

    # 단순 텍스트 출력 요소
    def simpleTextComponent(self, text):
        return {
            "simpleText": {"text": text}
        }

    # 단순 이미지 출력 요소
    def simpleImageComponent(self, imageUrl, altText):
        return {
            "simpleImage": {"imageUrl": imageUrl, "altText": altText}
        }

    # 사용자에게 응답 스킬 전송
    def send_response(self, bot_resp):
        responseBody = {
            "version": self.version,
            "template": {
                "outputs": []
            }
        }

        # 이미지 답변이 텍스트 답변보다 먼저 출력 됨
        # 이미지 답변이 있는 경우
        if bot_resp['AnswerImageUrl'] is not None:
            responseBody['template']['outputs'].append(self.simpleImageComponent(bot_resp['AnswerImageUrl'], ''))

        # 텍스트 답변이 있는 경우
        if bot_resp['Answer'] is not None:
            responseBody['template']['outputs'].append(self.simpleTextComponent(bot_resp['Answer']))

        return responseBody

    # 리스트카드(5개)
    def listCardTemplate(self, title, topFive):
        first = topFive[0]
        second = topFive[1]
        third = topFive[2]
        fourth = topFive[3]
        fifth = topFive[4]

        responseBody = {
            "version": self.version,
            "template": {
                "outputs": [
                {
                    "listCard": {
                    "header": {
                        "title": title
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



if __name__ == '__main__':
    KakaoEvent().send_response({"AnswerImageUrl":"image","Answer":"고양이"})