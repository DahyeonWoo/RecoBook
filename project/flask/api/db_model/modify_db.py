import sys
import re
sys.path.append("./project/flask/")
sys.path.append("./project/flask/api/")
import pandas as pd
import gensim
import numpy as py
from konlpy.tag import Okt
from api.db_model.mysql import conn_mysqldb
from api.utils.ColumnsFromDB import *

class ModifyDB:
    def __init__(self):
        self.conn = conn_mysqldb()
        self.cursor = self.conn.cursor()

    def get_description(self):
        # Book table에서 description 가져오는 함수
        sql = "SELECT description FROM Book"
        self.cursor.execute(sql)
        description = self.cursor.fetchall()
        return description

    def refine_description(self, description):
        # description에서 특수문자를 제거하는 함수
        refined_description = []
        regex = '[^ 0-9가-힣]'
        for i in range(len(description)):
            refined_description.append(re.sub(regex, '', description[i][0]))
        return refined_description

if __name__ == '__main__':
    raw_description = ModifyDB().get_description()
    print(len(raw_description))
    refined_description = ModifyDB().refine_description(raw_description)
    print(len(refined_description))