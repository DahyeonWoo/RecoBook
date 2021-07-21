#from flask_login import UserMixin
from db_model.mysql import conn_mysqldb

#class User(UserMixin):

def __init__(self, name):
    self.name = name

def get(name):
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
    res = get('김독자')
    print(res)