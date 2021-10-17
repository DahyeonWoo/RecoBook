import sys
import json
sys.path.append("./project/flask/")
sys.path.append("./project/flask/api/")
from db_model.mysql import conn_mysqldb
from api.utils.CreateDict import create_dict
from api.utils.ColumnsFromDB import ColumnsFromDB

class Author:
    
    @staticmethod
    def get_author_info(name):
        """
        작가 이름을 검색하면 작가 정보를 나타내는 함수
        :param name: 작가 이름
        :return: 작가 정보 딕셔너리(json) 
        """
        data = ColumnsFromDB.get_db_data('author, info', 'AuthorTest', 'author', name)
        return json.dumps(data, indent=2, default=str, ensure_ascii=False)

if __name__ == '__main__':
    res = Author.get_author_info('조애너 콜')
    print(res)