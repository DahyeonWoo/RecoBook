import sys
sys.path.append('./project/flask/')
sys.path.append('./project/flask/api/')
from api.db_model.mysql import conn_mysqldb
from utils.CreateDict import create_dict

class ColumnsFromDB:
    @staticmethod   
    def get_col_name(table_name):
        """
        해당 테이블의 컬럼명을 반환하는 함수
        json으로 바꿀 때 키 값으로 할당하기 위해 사용
        :params table_name: 테이블명
        :return: 테이블의 컬럼명 리스트
        """
        db = conn_mysqldb()
        db_cursor = db.cursor()
        sql = f"""
        SELECT `COLUMN_NAME`
        FROM `INFORMATION_SCHEMA`.`COLUMNS` 
        WHERE `TABLE_NAME`='{table_name}'
        """
        db_cursor.execute(sql)
        col_name_list = db_cursor.fetchall()
        db.close()
        total_col_list = []
        for col_name in col_name_list:
            total_col_list.append(col_name[0])
        return total_col_list

    @staticmethod
    def get_db_data(db_col, table_name, col, param):
            """
            지정한 컬럼에 관한 정보를 불러오는 함수
            :params db_col: 조회할 컬럼명
            :params table_name: 테이블명
            :params col: 
            :params param: 조건문에 들어갈 이름

            :return: 리스트
            """
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            sql = f"SELECT {db_col} FROM {table_name} WHERE {col} LIKE REPLACE('%{param}%', ' ', '')"
            db_cursor.execute(sql)
            db_data = db_cursor.fetchone()
            total_db_col = ColumnsFromDB.get_col_name(table_name)
            col_list = db_col.split(',')
            dict = create_dict()
            if db_col == '*':
                for i in range(len(total_db_col)):
                    dict.add(total_db_col[i], db_data[i])
            else:
                for i, col in enumerate(col_list):
                    if col.strip() in total_db_col:
                        dict.add(col.strip(), db_data[i])
                    else:
                        print('부적절한 col, 문법 체크')
            return dict

if __name__ == '__main__':
    res = ColumnsFromDB.get_db_data('*', 'Book', 'title', '미스테리아') # done
    # print(res)
    # res = get_db_data('isbn13, title', 'Book', 'title', '미스테리아') # done
    # print(res)
    # res = ColumnsFromDB.get_col_name('Book')
    # res = ColumnsFromDB.get_db_data('isbn13, title', 'Book', 'title', '미스테리아')
    print(res)