import sys
sys.path.insert(1, 'project/flask/api/db_model')
from mysql import conn_mysqldb

class Author:

    @staticmethod
    def __init__(self, name):
        self.name = name

    @staticmethod
    def get_author(name):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM Book WHERE author = '" + str(name) + "'"
        # print (sql)
        db_cursor.execute(sql)
        author = db_cursor.fetchone()
        if not author:
            return None
        return author

if __name__ == '__main__':
    res = Author.get_author('김영하')
    print(res)