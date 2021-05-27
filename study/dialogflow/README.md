# Dialogflow Study

![다운로드](https://user-images.githubusercontent.com/68543150/114038996-52c7d180-98bd-11eb-8794-ef977d70e1c1.png)

- Contributor: 유재성, 장윤아

## 1. Intent Matching

### **사용자가 무엇을 원하는지 인식하는 것**

- 시작하려면 몇 가지 예만 있으면 된다.

  예를 들어 자전거 수리점에서 dialogflow를 이용하고 싶다면

  - 자전거를 고치고 싶어.
  - 내 자전거가 고장났어.
  - 이번 주에 자전거를 고칠 수 있을까?

- 이를 통해 dialogflow는 기계 학습을 진행해서, 비슷한  예시(ex. 자전거 수리 예약해줘, 브레이크가 고장났어 등)에 대해서도 응답할 수 있게 만듦.

- 따라서 사용자가 말하는 **의도(Intent)를 파악**하여 앱이 어떻게 반응할 지 정해줘야 한다!

## 2. Intent Examples

다음과 같은 Intent Matching의 사례를 살펴보겠다.

1. 가격확인
   - 가장 잘 팔리는 모델이 얼마야?
   - 튜닝 비용이 어떻게 돼?
   - 수리 비용이 어떻게 돼?
2. 수리예약
   - 자전거를 고치고 싶어
   - 자전거가 망가졌어
   - 이번 주에 자전거 수리 가능할까?
3. 영업시간
   - 영업시간이 어떻게 돼?
   - 언제 열어?
   - 언제 닫아?

위와 같이 자전거 수리점에서 Intent(1,2,3)와 각각에 맞는 예시를 설정해 놨다면 다음과 같은 질문을 받았을 때,

> 개장 시간이 언제야?

- 10시 부터 5시까지 영업합니다

라는 답변을 사용자가 받을 수 있다.



# Bookcode Chatbot

참고

[간단 챗봇 만들기](https://medium.com/@jwlee98/gcp-dialogflow-%EB%A5%BC-%EC%9D%B4%EC%9A%A9%ED%95%9C-%EA%B0%84%EB%8B%A8-%EC%B1%97%EB%B4%87-%EB%A7%8C%EB%93%A4%EA%B8%B0-514ea25e4961)

[도서검색 API 리스트](https://steemit.com/kr/@anpigon/open-api)

[Mysql과 Dialogflow 연결하기](https://www.youtube.com/watch?v=v7k5vckSzNo)

[멜론 노래추천 dialogflow](http://www.kwangsiklee.com/2018/01/%EA%B5%AC%EA%B8%80-ai-%ED%94%8C%EB%9E%AB%ED%8F%BC-dialogflow-%EB%88%88%EC%9C%BC%EB%A1%9C-%EB%94%B0%EB%9D%BC%ED%95%98%EB%A9%B0-%EB%B0%B0%EC%9A%B0%EA%B8%B0/)

## 1. Intent

어떤 인텐트를 넣을까?

### Welcome

챗봇 처음 시작 시 안내되는 문구

- Input
  - 안녕
  - 하이
  - 반가워
  - .
- Output
  - 안녕하세요. 도서 추천 기능을 제공하는 챗봇 '북코드'입니다 :) 원하시는 작가/도서/장르에 대해 말씀해주시면 이를 기반으로 유사한 도서를 추천해드릴게요! 

### Recommendation

#### 1. 작가

#### 2. 도서

#### 3. 장르

### 미흡한 점 (+ 보충할 점)

- DB연결을 어떻게 할 것인가?
  - ex) "A책과 비슷한 책을 추천해줘''
    - A 책을 찾기위해 dialogflow와 DB를 어떻게 연결할 것인지
    - 크롤링을 통한 DB 구축보다는 API 활용하는게 쉬워보임
- 두 가지 이상의 키워드를 동시에 물어볼 경우 어떻게 할 것인가?
  - ex) "B 작가의 C 책과 비슷한 책을 추천해줘"
    - 두 가지 인텐트가 동시에 존재할 때 어떻게 처리할 것인가?
      - [컨텍스트](https://cloud.google.com/dialogflow/es/docs/contexts-input-output) 활용
- 예외항이 존재할 경우?
  - ex) "B 작가의 책을 추천해줘, 대신 D 책은 말고"
    - D 책에 대한 예외처리를 어떻게 할 것인가?

- 커스텀 엔터티 만들기

  - ex) "C 작가의 책을 추천해줘"

    - 작가 이름은 다양한데, dialogflow가 이름을 이름으로 인식할 수 있는 엔터티 작성 필요

      작가 이름 뿐만 아니라 도서 이름, 장르도 해당

- 사용자가 잘못 입력한 경우
  - ex) "북코드 작가의 책을 추천해줘" 대신 "붘코드 작가의 책을 추천해줘"라고 입력한 경우
    - 검색 결과가 없다고 응답할 것인지? 북코드 작가로 인식해서 출력할 것인지?
      - [퍼지 일치 사용?](https://cloud.google.com/dialogflow/es/docs/entities-fuzzy)
- 엔터티 리스트
  - 방대한 도서/ 작가/ 장르를 하나하나 엔터티 항목에 채우기란 불가능
    - [엔터티 내보내기 및 가져오기](https://cloud.google.com/dialogflow/es/docs/entities-export) 