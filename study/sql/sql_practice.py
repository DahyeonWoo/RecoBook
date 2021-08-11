import sys
sys.path.insert(1, 'project/flask/api/db_model')
from mysql import conn_mysqldb
import pymysql


db = conn_mysqldb()
db_cursor = db.cursor() # cursor 오브젝트 가져오기

sql = """SELECT author FROM Book""" # 쿼리문
db_cursor.execute(sql) # sql 실행
result = db_cursor.fetchall() # mysql 서버로부터 데이터 가져오기
print(result)