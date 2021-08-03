from db_model.mysql import conn_mysqldb

class User():

    @staticmethod
    def __init__(self, name):
        self.name = name

    @staticmethod
    def post_user(name, birthday, age, gender, bookRead, bookWant, interestBook, interestAuthor,interestCategory):
        """
        유저 정보를 업데이트 하는 함수
        """
        db = conn_mysqldb()
        db_cursor = db.cursor()
        sql = """INSERT INTO User(name, birthday, age, gender, bookRead, bookWant, interestBook, interestAuthor,interestCategory) 
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
        db_cursor.execute(sql,(name, birthday, age, gender, bookRead, bookWant, interestBook, interestAuthor,interestCategory))
        db.commit()
        db_cursor.close()

    @staticmethod
    def get_user(name):
        """
        유저 정보를 가져오는 함수
        :params name: 유저의 이름
        :return: 유저 정보
        """
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM User WHERE name = '" + str(name) + "'"
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        return user

    @staticmethod
    def get_db_data(name, db_col):
        """
        읽은 책을 불러오는 함수
        :params name: 사용자의 이름
        :return: 읽은 책의 정보
        """
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT %s FROM User WHERE name = %s"
        db_cursor.execute(sql, (name, db_col))
        read_book = db_cursor.fetchone()
        return read_book[0]

    @staticmethod
    def insert_read_book(user_name, title):
        """
        읽은 책을 추가하는 함수
        :params name: 사용자의 이름
        :params book: 추가할 책 이름
        """
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        read_book = User.get_db_data(user_name, 'bookRead')
        read_book =  read_book.split(',') # 해당 사용자의 읽은 책들을 리스트로 변환
        if title not in read_book: # 읽은 책이 이미 리스트에 있는지 확인
            read_book.append(title) # 리스트에 없는 경우 읽은 책 추가
            sep_read_book = ','.join(set(read_book)) # 리스트를 ,구분 문자열로 변환
            sql = "UPDATE User SET bookRead = %s WHERE name = %s" # 해당 사용자의 읽은 책 리스트를 업데이트할 쿼리문
            db_cursor.execute(sql, (sep_read_book, user_name)) # 해당 사용자의 읽은 책 리스트를 업데이트
            mysql_db.commit() # 트랜잭션 저장
            db_cursor.close() # 커서 닫기
            print('읽은 책 추가 완료')
        else:# 해당 사용자의 읽은 책 리스트에 추가할 책이 있을 경우
            print('추가할 책이 이미 존재합니다.')

    @staticmethod
    def delete_read_book(user_name, title):
        """
        읽은 책 삭제하는 함수
        :params name: 사용자의 이름
        :params book: 삭제할 책 이름
        """
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        read_book = User.get_db_data(user_name, 'bookRead')
        read_book = read_book.split(',') # 튜플로 받은 읽은 책 문자열을 리스트로 변환
        try: # 해당 사용자의 읽은 책 리스트에서 삭제할 책의 이름을 찾아서 삭제
            read_book.remove(title)
        except ValueError: # 해당 책이 없는 경우
            print('해당 책이 없습니다')
            return None
        deleted_book_list = ','.join(read_book) # 구분 문자열로 변환
        sql = "UPDATE User SET bookRead = %s WHERE name = %s" # 삭제된 책을 db에 업데이트할 쿼리문
        db_cursor.execute(sql, (deleted_book_list, user_name)) # 해당 쿼리문 실행
        mysql_db.commit() # 갱신 
        db_cursor.close() # 파이썬 커넥션 닫기
        print('읽은 책 삭제 완료')
        return True


if __name__ == '__main__':
    # User.post_user('이독자','2000-07-07',22, 'M','밤의 여행자들','밝은 밤','이웃집 밤','이지은','소설')
    res = User.insert_read_book('이현준', '아몬드') # 읽은 책 추가
    res = User.delete_read_book('이현준', '아몬드') # 읽은 책 삭제
    res = User.get_read_book('이현준') # 읽은 책 가져오기
    print(res)