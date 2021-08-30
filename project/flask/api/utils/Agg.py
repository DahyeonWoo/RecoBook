import sys

from project.flask.api.db_model import mysql

sys.path.append("./project/flask/")
sys.path.append("./project/flask/api/")
from api.utils.CreateDict import create_dict
from api.db_model.mysql import conn_mysqldb

def get_top3(select_col, table_name, n):
    """
    :param select_col: 선택할 컬럼
    :param table_name: 테이블 명
    :param n: top n
    :return: top n 리스트
    """
    mysql_db = conn_mysqldb()
    db_cursor = mysql_db.cursor()
    sql = f"SELECT GROUP_CONCAT({select_col} seperator ';') FROM {table_name} WHERE {select_col} IS NOT NULL"
    db_cursor.execute(sql)
    result = db_cursor.fetchall()
    db_cursor.close()
    list_ = result.split(';')
    
    