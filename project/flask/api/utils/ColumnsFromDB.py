import sys

sys.path.append("./project/flask/")
sys.path.append("./project/flask/api/")
from api.db_model.mysql import conn_mysqldb
from api.utils.CreateDict import create_dict
from flask import url_for, redirect


class ColumnsFromDB:
    @staticmethod
    def remove_values_from_list(the_list, val):
        """
        특정 값을 리스트에서 제거하는 함수

        :param the_list: 리스트
        :param val: 제거할 값
        :return: 제거된 리스트
        """

        return [value for value in the_list if value != val]


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
        :params col: 조건 컬럼명
        :params param: 조건문에 들어갈 이름

        :return: 리스트
        """
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = f"SELECT {db_col} FROM {table_name} WHERE {col} = '{param}'"
        db_cursor.execute(sql)
        db_data = db_cursor.fetchone()
        db_cursor.close()
        total_db_col = ColumnsFromDB.get_col_name(table_name)
        col_list = db_col.split(",")
        print('테이블 column 리스트:', col_list)
        dict = create_dict()
        if db_col == "*":
            for i in range(len(total_db_col)):
                dict.add(total_db_col[i], db_data[i])
        else:
            for i, col in enumerate(col_list):
                if col.strip() in total_db_col:
                    dict.add(col.strip(), db_data[i])
                else:
                    print("부적절한 col, 문법 체크")
        return dict

    @staticmethod
    def insert_db_data(table_name, select_col, col, param, value):
        """
        데이터를 db에 삽입하는 함수
        :params table_name: 테이블명
        :params select_col: SELECT 절에 입력할 컬럼
        :params col: WHERE 절에 입력할 컬럼
        :params param: col 대응되는 이름
        :params value: 삽입할 값
        """
        data = ColumnsFromDB.get_db_data(select_col, table_name, col, param)
        print("db에 저장된 데이터: ", data)
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        print(f"삽입할 값: {value}")
        try:
            data = list(data.values())[0].replace(" ", "")
            data = data.split(";")  # 해당 사용자의 데이터들을 리스트로 변환
            data = list(set(data))
            if value.replace(" ", "") not in data:  # 데이터가 이미 리스트에 있는지 확인
                data.append(value)  # 리스트에 없는 경우 데이터 추가
                remove_blank = ColumnsFromDB.remove_values_from_list(data, "") # 리스트에 있는는 공백 원소 제거
                sep_data = ";".join(remove_blank)  # 리스트를 ;구분 문자열로 변환
                print(sep_data)
                sql = f"UPDATE {table_name} SET {select_col} = '{sep_data}' WHERE {col} LIKE REPLACE('%{param}%', ' ', '')"  # 해당 사용자의 데이터 리스트를 업데이트할 쿼리문
                db_cursor.execute(sql)  # 해당 사용자의 데이터 리스트를 업데이트
                mysql_db.commit()  # 트랜잭션 저장
                db_cursor.close()
                print("데이터 추가 완료")
                return 1
            else:  # 해당 사용자의 데이터 리스트에 추가할 책이 있을 경우
                print("이미 존재합니다.")
                return 2
        except AttributeError:  # 해당 사용자의 데이터 리스트가 없을 경우
            sql = f"UPDATE {table_name} SET {select_col} = '{value}' WHERE {col} LIKE REPLACE('%{param}%', ' ', '')"  # 해당 사용자의 데이터 리스트를 업데이트할 쿼리문
            db_cursor.execute(sql)  # 해당 사용자의 데이터 리스트를 업데이트
            mysql_db.commit()  # 트랜잭션 저장
            db_cursor.close()
            print("추가 완료")
            return 1
        finally:
            db_cursor.close()

    @staticmethod
    def delete_db_data(table_name, select_col, col, param, value):
        """
        db 데이터를 삭제하는 함수
        :params table_name: 테이블명
        :params select_col: SELECT 절에 입력할 컬럼
        :params col: WHERE 절에 입력할 컬럼
        :params param: col 대응되는 이름
        :params value: 삭제할 값
        """
        data = ColumnsFromDB.get_db_data(select_col, table_name, col, param)

        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        print(f"value:{value}")
        try:
            data = list(data.values())[0].replace(" ", "")
            data = data.split(";")
            data.remove(value.replace(" ", ""))
        except (ValueError, AttributeError):  # 해당 책이 없는 경우
            sql = f"UPDATE {table_name} SET {select_col} = NULLIF({select_col}, '')"
            db_cursor.execute(sql)
            mysql_db.commit()
            db_cursor.close()
            print("삭제할 내용이 존재하지 않습니다")
            return 2
        sep_data = ";".join(data)  # 리스트를 ,구분 문자열로 변환
        sql = f"UPDATE {table_name} SET {select_col} = '{sep_data}' WHERE {col} LIKE REPLACE('%{param}%', ' ', '')"  # 해당 사용자의 읽은 책 리스트를 업데이트할 쿼리문
        db_cursor.execute(sql)  # 해당 사용자의 읽은 책 리스트를 업데이트
        mysql_db.commit()  # 트랜잭션 저장
        db_cursor.close()  # 커서 닫기
        print("삭제 완료")
        return 1


if __name__ == "__main__":
    # res = ColumnsFromDB.get_db_data('*', 'Book', 'title', '미스테리아') # done
    # print(res)
    # res = ColumnsFromDB.get_db_data('isbn13, title', 'Book', 'title', '미스테리아') # done
    # print(res)
    # res = ColumnsFromDB.get_col_name('Book')
    # res = ColumnsFromDB.get_db_data('isbn13, title', 'Book', 'title', '미스테리아')
    # res = ColumnsFromDB.get_db_data('bookRead', 'User', 'name', '이현준')
    res = ColumnsFromDB.get_db_data('interestAuthor', 'User', 'name', '이현준')
    # res = ColumnsFromDB.insert_db_data("User", "interestAuthor", "name", "이지후", "김영하")
    # res = ColumnsFromDB.delete_db_data("User", "interestAuthor", "name", "이지후", "김영하")
    print(res)
