import sys
sys.path.append('./project/flask/')
from api.db_model.mysql import conn_mysqldb

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
    return list(col_name_list)

def get_db_data(name, table_name, db_col):
        """
        지정한 한 개의 컬럼에 관한 정보를 불러오는 함수
        :params name: 조건문에 들어갈 이름
        :params table_name: 테이블명
        :params db_col: 조회할 컬럼명
        :return: 리스트
        """
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = f"SELECT {db_col} FROM {table_name} WHERE name = '{name}'"
        db_cursor.execute(sql)
        db_data = db_cursor.fetchone()
        return db_data[0]

# if __name__ == '__main__':
    # res = get_col_name('User')
    # print(res)
    # for i in zip(res, ):
    #     print(
    # print(get_db_data('이현준', 'User', 'bookRead'))