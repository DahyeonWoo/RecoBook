import sys
import json
sys.path.insert(1, 'project/flask/model')
from db_model.mysql import conn_mysqldb
from CreateDict import create_dict

class Author:
    

    @staticmethod
    def get_author(name):
        """
        작가 이름을 검색하면 작가 정보를 나타내는 함수
        :param name: 작가 이름
        :return: 작가 정보 딕셔너리(json) 
        """
        dict = create_dict()
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM Author WHERE name LIKE %s" 
        db_cursor.execute(sql, f"%{name}%")
        author = db_cursor.fetchall()
        if not author:
            return None
        return json.dumps(author, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    res = Author.get_author('이지은')
    print(res)