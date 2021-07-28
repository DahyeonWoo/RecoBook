from db_model.mysql import conn_mysqldb
import pymysql
from decouple import config

class User():

    @staticmethod
    def __init__(self, name):
        self.name = name

    @staticmethod
    def post_user(name, birthday, age, gender, bookRead, bookWant, interestBook, interestAuthor,interestCategory):
        db = pymysql.connect(host=config('host'),port=3306,user=config('user'),passwd=config('passwd'),db=config('db'),charset='utf8mb4')
        db_cursor = db.cursor()
        sql = """INSERT INTO User(name, birthday, age, gender, bookRead, bookWant, interestBook, interestAuthor,interestCategory) 
            values (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
        db_cursor.execute(sql,(name, birthday, age, gender, bookRead, bookWant, interestBook, interestAuthor,interestCategory))
        db.commit()
        db_cursor.close()

    @staticmethod
    def get_user(name):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM User WHERE name = '" + str(name) + "'"
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        return user

if __name__ == '__main__':
    User.post_user('이독자','2000-07-07',22, 'M','밤의 여행자들','밝은 밤','이웃집 밤','이지은','소설')
    res = User.get_user('이독자')
    print(res)