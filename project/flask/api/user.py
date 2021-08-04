from db_model.mysql import conn_mysqldb

class User():

    class UserInfo():

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

    class UserRead():

        # @staticmethod
        # def get_db_data(name, db_col):
        #     """
        #     읽은 책을 불러오는 함수
        #     :params name: 사용자의 이름
        #     :params db_col: 조회할 컬럼
        #     :return: 읽은 책의 정보
        #     """
        #     mysql_db = conn_mysqldb()
        #     db_cursor = mysql_db.cursor()
        #     sql = "SELECT %s FROM User WHERE name = %s"
        #     db_cursor.execute(sql, (name, db_col))
        #     db_data = db_cursor.fetchone()
        #     return db_data[0]

        @staticmethod
        def get_read_book(user_name):
            """
            읽은 책 리스트를 가져오는 함수
            :params user_name: 유저의 이름 
            :return: 읽은 책 리스트
            """
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            sql = "SELECT NULLIF(bookRead, '') FROM User WHERE name = '" + str(user_name) + "'"
            db_cursor.execute(sql)
            user = db_cursor.fetchone()
            return user[0]


        @staticmethod
        def insert_read_book(user_name, title):
            """
            읽은 책을 추가하는 함수
            :params name: 사용자의 이름
            :params title: 추가할 책 이름
            """
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            # read_book = User.get_db_data(user_name, 'bookRead')
            read_book = User.UserRead.get_read_book(user_name)
            try:
                read_book =  read_book.split(',') # 해당 사용자의 읽은 책들을 리스트로 변환
                if title not in read_book: # 읽은 책이 이미 리스트에 있는지 확인
                    read_book.append(title) # 리스트에 없는 경우 읽은 책 추가
                    sep_read_book = ','.join(read_book) # 리스트를 ,구분 문자열로 변환
                    sql = "UPDATE User SET bookRead = %s WHERE name = %s" # 해당 사용자의 읽은 책 리스트를 업데이트할 쿼리문
                    db_cursor.execute(sql, (sep_read_book, user_name)) # 해당 사용자의 읽은 책 리스트를 업데이트
                    mysql_db.commit() # 트랜잭션 저장
                    db_cursor.close() # 커서 닫기
                    print('읽은 책 추가 완료')
                else:# 해당 사용자의 읽은 책 리스트에 추가할 책이 있을 경우
                    print('추가할 책이 이미 존재합니다.')
            except AttributeError: # 해당 사용자의 읽은 책 리스트가 없을 경우
                sql = "UPDATE User SET bookRead = %s WHERE name = %s" # 해당 사용자의 읽은 책 리스트를 업데이트할 쿼리문
                db_cursor.execute(sql, (title, user_name)) # 해당 사용자의 읽은 책 리스트를 업데이트
                mysql_db.commit() # 트랜잭션 저장
                db_cursor.close() # 커서 닫기
                print('책 추가 완료')

        @staticmethod
        def delete_read_book(user_name, title):
            """
            읽은 책 삭제하는 함수
            :params name: 사용자의 이름
            :params book: 삭제할 책 이름
            """
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            # read_book = User.get_db_data(user_name, 'bookRead')
            read_book = User.UserRead.get_read_book(user_name)
            try: # 해당 사용자의 읽은 책 리스트에서 삭제할 책의 이름을 찾아서 삭제
                read_book = read_book.split(',') # 튜플로 받은 읽은 책 문자열을 리스트로 변환
                read_book.remove(title)
            except (ValueError, AttributeError) as e: # 해당 책이 없는 경우
                print('해당 책이 없습니다')
                sql = "UPDATE User SET bookRead = NULLIF(bookRead, '')"
                db_cursor.execute(sql)
                mysql_db.commit()
                db_cursor.close()
                return None
            deleted_book_list = ','.join(read_book) # 구분 문자열로 변환
            sql = "UPDATE User SET bookRead = %s WHERE name = %s" # 삭제된 책을 db에 업데이트할 쿼리문
            db_cursor.execute(sql, (deleted_book_list, user_name)) # 해당 쿼리문 실행
            mysql_db.commit() # 갱신 
            db_cursor.close() # 파이썬 커넥션 닫기
            print('읽은 책 삭제 완료')
            return True

    class UserWish():
        @staticmethod
        def get_book_want(user_name):
            """
            위시 리스트를 가져오는 함수
            :params user_name: 유저의 이름 
            :return: 위시 리스트
            """
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            sql = "SELECT NULLIF(bookWant, '') FROM User WHERE name = '" + str(user_name) + "'"
            db_cursor.execute(sql)
            book_want = db_cursor.fetchone()
            return book_want[0]


        @staticmethod
        def insert_book_want(user_name, title):
            """
            위시 리스트를 추가하는 함수
            :params user_name: 사용자의 이름
            :params title: 추가할 책 이름
            """
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            book_want = User.UserWish.get_book_want(user_name)
            
            try:
                book_want =  book_want.split(',') # 해당 사용자의 읽은 책들을 리스트로 변환
                if title not in book_want: # 읽은 책이 이미 리스트에 있는지 확인
                    book_want.append(title) # 리스트에 없는 경우 읽은 책 추가
                    sep_book_want = ','.join(book_want) # 리스트를 ,구분 문자열로 변환
                    sql = "UPDATE User SET bookWant = %s WHERE name = %s" # 해당 사용자의 읽은 책 리스트를 업데이트할 쿼리문
                    db_cursor.execute(sql, (sep_book_want, user_name)) # 해당 사용자의 읽은 책 리스트를 업데이트
                    mysql_db.commit() # 트랜잭션 저장
                    db_cursor.close() # 커서 닫기
                    print('위시리스트 추가 완료')
                else:# 해당 사용자의 읽은 책 리스트에 추가할 책이 있을 경우
                    print('추가할 책이 이미 존재합니다.')
            except AttributeError: # 위시리스트가 비어있는 경우
                sql = "UPDATE User SET bookWant = %s WHERE name = %s" # 해당 사용자의 읽은 책 리스트를 업데이트할 쿼리문
                db_cursor.execute(sql, (title, user_name)) # 해당 사용자의 읽은 책 리스트를 업데이트
                mysql_db.commit() # 트랜잭션 저장
                db_cursor.close() # 커서 닫기
                print('위시리스트 추가 완료')


        @staticmethod
        def delete_book_want(user_name, title):
            """
            위시 리스트를 삭제하는 함수
            :params user_name: 사용자의 이름
            :params title: 삭제할 책 이름
            """
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            book_want = User.UserWish.get_book_want(user_name)
            
            try:
                book_want = book_want.split(',')
                book_want.remove(title)
            except (ValueError, AttributeError): # 해당 책이 없는 경우
                print('해당 책이 없습니다')
                sql = "UPDATE User SET bookWant = NULLIF(bookWant, '')"
                db_cursor.execute(sql)
                mysql_db.commit()
                db_cursor.close()
                return None
            sep_book_want = ','.join(book_want) # 리스트를 ,구분 문자열로 변환
            sql = "UPDATE User SET bookWant = %s WHERE name = %s" # 해당 사용자의 읽은 책 리스트를 업데이트할 쿼리문
            db_cursor.execute(sql, (sep_book_want, user_name)) # 해당 사용자의 읽은 책 리스트를 업데이트
            mysql_db.commit() # 트랜잭션 저장
            db_cursor.close() # 커서 닫기
            print('위시리스트 삭제 완료')

    class UserAuthor:
        @staticmethod
        def get_interest_author(user_name):
            """
            선호 작가 목록을 가져오는 함수
            :params user_name: 유저의 이름
            :return: 선호 작가 목록
            """
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            sql = "SELECT NULLIF(interestAuthor, '') FROM User WHERE name = '" + str(user_name) + "'"
            db_cursor.execute(sql)
            author_list = db_cursor.fetchone()
            return author_list[0]

        @staticmethod
        def insert_interest_author(user_name, author_name):
            """
            선호 작가를 추가하는 함수
            :params user_name: 유저의 이름
            :params author_name: 추가할 작가의 이름
            """
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            author_list = User.UserAuthor.get_interest_author(user_name)
            
            try:
                author_list = author_list.split(',')
                if author_name not in author_list:
                    author_list.append(author_name)
                    sep_author_list = ','.join(author_list)
                    sql = "UPDATE User SET interestAuthor = %s WHERE name = %s"
                    db_cursor.execute(sql, (sep_author_list, user_name))
                    mysql_db.commit()
                    db_cursor.close()
                    print('추가 완료')
                else:
                    print('이미 추가되어 있습니다.')
                    return None
            except TypeError:
                sql = "UPDATE User SET interestAuthor = %s WHERE name = %s"
                db_cursor.execute(sql, (author_name, user_name))
                mysql_db.commit()
                db_cursor.close()
                print('추가 완료')



        @staticmethod
        def delete_interest_author(user_name, author_name):
            """
            선호 작가를 삭제하는 함수
            :params user_name: 유저의 이름
            :params author_name: 삭제할 작가의 이름
            """
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            author_list = User.UserAuthor.get_interest_author(user_name)
            try:
                author_list = author_list.split(',')
                author_list.remove(author_name)
            except (ValueError, AttributeError) as e:
                print('해당 작가가 없습니다.')
                sql = "UPDATE User SET interestAuthor = NULLIF(interestAuthor, '')"
                db_cursor.execute(sql)
                mysql_db.commit()
                db_cursor.close()
                return None
            sep_author_list = ','.join(author_list)
            sql = "UPDATE User SET interestAuthor = %s WHERE name = %s"
            db_cursor.execute(sql, (sep_author_list, user_name))
            mysql_db.commit()
            db_cursor.close()
            print('삭제 완료')

    class UserGenre():

        @staticmethod
        def get_interest_genre(user_name):
            """
            선호 장르 목록을 가져오는 함수
            :params user_name: 유저의 이름
            :return: 선호 장르 목록
            """
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            sql = "SELECT NULLIF(interestCategory, '') FROM User WHERE name = '" + str(user_name) + "'"
            db_cursor.execute(sql)
            genre_list = db_cursor.fetchone()
            return genre_list[0]

        @staticmethod
        def insert_interest_genre(user_name, genre):
            """
            선호 장르를 추가하는 함수
            :params user_name: 유저의 이름
            :params genre: 추가할 장르
            """
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            genre_list = User.UserGenre.get_interest_genre(user_name)
            try:
                genre_list = genre_list.split(',')
                if genre not in genre_list:
                    genre_list.append(genre)
                    sep_genre_list = ','.join(genre_list)
                    sql = "UPDATE User SET interestCategory = %s WHERE name = %s"
                    db_cursor.execute(sql, (sep_genre_list, user_name))
                    mysql_db.commit()
                    db_cursor.close()
                    print('리스트에 추가 완료')
                else:
                    print('이미 추가되어 있습니다.')
                    return None
            except AttributeError:
                sql = "UPDATE User SET interestCategory = %s WHERE name = %s"
                db_cursor.execute(sql, (genre, user_name))
                mysql_db.commit()
                db_cursor.close()
                print('새로 추가 완료')

        @staticmethod
        def delete_interest_genre(user_name, genre):
            """
            선호 장르를 삭제하는 함수
            :params user_name: 유저의 이름
            :params genre: 삭제할 장르
            """
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            genre_list = User.UserGenre.get_interest_genre(user_name)
            try:
                genre_list = genre_list.split(',')
                genre_list.remove(genre)
            except (ValueError, AttributeError) as e:
                print('해당 장르가 없습니다.')
                sql = "UPDATE User SET interestCategory = NULLIF(interestCategory, '')"
                db_cursor.execute(sql)
                mysql_db.commit()
                db_cursor.close()
                return None
            sep_genre_list = ','.join(genre_list)
            print()
            sql = "UPDATE User SET interestCategory = %s WHERE name = %s"
            db_cursor.execute(sql, (sep_genre_list, user_name))
            mysql_db.commit()
            db_cursor.close()
            print('삭제 완료')


if __name__ == '__main__':
    # User.post_user('이독자','2000-07-07',22, 'M','밤의 여행자들','밝은 밤','이웃집 밤','이지은','소설')
    # res = User.UserRead.insert_read_book('김민준', '아몬드') # 읽은 책 추가
    # res = User.UserRead.delete_read_book('김민준', '아몬드') # 읽은 책 삭제
    # res = User.UserRead.get_read_book('김민준') # 읽은 책 가져오기
    # res = User.UserWish.insert_book_want('김민준', '아몬드')
    # res = User.UserWish.delete_book_want('김민준', '아몬드')
    # res = User.UserWish.get_book_want('김민준')
    # res = User.UserAuthor.insert_interest_author('김민준', '김영하')
    # res = User.UserAuthor.delete_interest_author('김민준', '김영하')
    # res = User.UserAuthor.get_interest_author('김민준')
    # res = User.UserGenre.insert_interest_genre('박지훈', '로맨스')
    res = User.UserGenre.delete_interest_genre('박지훈', '로맨스')
    res = User.UserGenre.get_interest_genre("박지훈")
    
    
    print(res)