import mysql

db = None

try:
    db = pymysql.connect(
        host = '127.0.0.1',
        user = 'homestead',
        passwd = 'secret',
        db = 'homestead',
        charset = 'utf8'
    )
    print("DB 연결 성공")
except Exception as e:
    print(e) #db 연결 실패 시 오류 내용 출력
finally:
    if db is not None: # db가 연결된 경우에 만 접속 닫기 시도
        db.close()
        print("DB 연결 닫기 성공")