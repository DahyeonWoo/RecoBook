import sys
from collections import Counter

sys.path.append("./project/flask/")
sys.path.append("./project/flask/api/")
from api.db_model.mysql import conn_mysqldb
from api.utils.CreateDict import create_dict


def remove_values_from_list(the_list, val):
    """
    특정 값을 리스트에서 제거하는 함수

    :param the_list: 리스트
    :param val: 제거할 값
    :return: 제거된 리스트
    """

    return [value for value in the_list if value != val]


def get_topn(select_col, table_name, n):
    """
    top n개의 값과 개수를 출력하는 함수

    :param select_col: 선택할 컬럼
    :param table_name: 테이블 명
    :param n: top n
    :return: top n 리스트
    """
    mysql_db = conn_mysqldb()
    db_cursor = mysql_db.cursor()
    sql = f"SELECT GROUP_CONCAT({select_col} separator ';') FROM {table_name} WHERE {select_col} IS NOT NULL"
    db_cursor.execute(sql)
    result = db_cursor.fetchone()[0]
    db_cursor.close()

    list_ = result.split(";")
    remove_blank = remove_values_from_list(list_, "")
    count = Counter(remove_blank)
    top_n = count.most_common(n)
    d = create_dict()
    for feature, n in top_n:
        d.add(feature, n)
    return dict(sorted(d.items(), key=lambda item: item[1], reverse=True))
    


if __name__ == "__main__":
    print(get_topn("bookRead", "User", 3))
    print(get_topn("bookWant", "User", 3))
    print(get_topn("interestAuthor", "User", 3))
    print(get_topn("interestCategory", "User", 3))
