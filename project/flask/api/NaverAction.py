# -*- coding: utf-8 -*-
class NaverAction:
    def __init__(self):
        # 템플릿 버전
        self.name = "recobook"

    # 사용자에게 응답 스킬 전송
    def example(self):
        responseBodyExample = {
        "data": [
            {
              "variableName": "변수명에 해당하는 부분입니다",
              "value": "variableName에 해당하는 변수를 어떤 값으로 치환할지를 결정합니다"
            }
        ],
        "userVariable": [
            {
              "name": "사용자 변수 이름입니다",
              "value": "사용자 변수에 저장할 값입니다",
              "type": "사용자 변수의 타입입니다",
              "action": "동작을 지정합니다",
              "valueType": "저장할 값의 타입입니다"
            },
            {
            "name": "text",
            "value": "olive",
            "type": "TEXT",
            "action": "EQ",
            "valueType": "TEXT"
           },
          {
            "name": "number",
            "value": 10,
            "type": "NUMBER",
            "action": "ADD",
            "valueType": "NUMBER"
          },
          {
            "name": "date.year",
            "value": 2020,
            "type": "JSON",
            "action": "EQ",
            "valueType": "NUMBER"
          },
          {
            "name": "date.month",
            "value": 6,
            "type": "JSON",
            "action": "EQ",
            "valueType": "NUMBER"
          }
        ]
        }

        responseBody = {
            "membership": [
                {
                    "name": "name",
                    "value": "홍길동"
                },
                {
                    "name": "point",
                    "value": "10000"
                }
            ]
        }


if __name__ == '__main__':
    NaverAction().send_response()
