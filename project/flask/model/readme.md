# MODEL 폴더 활용법

## 1. DB에서 정보 추출하기
- utils/extract_features.py에서 extract_book_info() 함수 사용

## 2. 추출한 정보를 embedding 하기
- model/refine_description.ipynb를 사용해서 description의 특수문자 제거
- model/adding_embedding.ipynb를 사용해 dataframe에 embedding 컬럼 추가 후 저장 

## 3. embedding한 정보를 통해 유사도 추출하기
- model/cosine_similarity.ipynb를 사용해 책들의 코사인 유사도 계산

## 4. DB에 저장하기
- dataframe을 DB에 올리기위해서는 pymysql이 아닌 SQLAlchemy가 필요함
- db_model/mysql.py를 노션 -> ignore 파일 관리에 있는 최신화된 mysql.py로 바꾸자. (`conn_sadb()`가 있으면 정답)
- model/connect_db.py를 사용해 DB에 올린다
    - `df.to_sql(name='Score', con=db, index=False, if_exists='replace')`
- DB에 Score라는 테이블이 새로 생겼음을 알 수 있다.
- 매일 조인해서 쓰는 건 귀찮으니 view table을 만들어주자.

```mysql
CREATE VIEW Score AS 
SELECT a.idcategory, a.name, b.main_menu, b.grade, a.avg_grade 
FROM category AS a 
INNER JOIN customer AS b 
ON a.idcategory = b.category 
WHERE a.idcategory = 105
```
