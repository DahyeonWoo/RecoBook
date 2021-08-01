import sys
import json
sys.path.insert(1, 'project/flask/api/db_model')
from mysql import conn_mysqldb

class Author:

    @staticmethod
    def get_author(name):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM Book WHERE author LIKE %s" 
        db_cursor.execute(sql, f"%{name}%")
        author = db_cursor.fetchall()
        if not author:
            return None
        return json.dump(author)

if __name__ == '__main__':
    res = Author.get_author('이지은')
    print(res)