#from flask_login import UserMixin
from db_model.mysql import conn_mysqldb

class User():

    @staticmethod
    def __init__(self, name):
        self.name = name

    @staticmethod
    def get_user(name):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM User WHERE name = '" + str(name) + "'"
        # print (sql)
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            return None
        return user

if __name__ == '__main__':
    res = User.get_user('김독자')
    print(res)