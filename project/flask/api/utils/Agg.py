import sys
import json
from collections import Counter

sys.path.append("./project/flask/")
sys.path.append("./project/flask/api/")
from api.db_model.mysql import conn_mysqldb
from api.utils.CreateDict import create_dict


def remove_values_from_list(the_list, val):
    """
    특정 값을 리스트에서 제거하는 함수
    ';' 기준 split을 할 경우 리스트 맨 앞에 '' 원소가 잡히는 경우가 있어 이를 제거할 때 주로 사용

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
    :return: top n 개의 값이 담긴 리스트
    ex) {
            1: {'name': '아몬드', 'count': 10},
            2: {'name': '오렌지', 'count': 6},
            3: {'name': '바나나', 'count': 4}
        }
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
    for i in range(1, len(top_n)+1):
        dict_value = {'name': top_n[i-1][0], 'count': top_n[i-1][1]}
        d.add(i, dict_value)
    #return json.dumps(d, indent=2, ensure_ascii=False)
    return d

    


if __name__ == "__main__":
    #print(get_topn("bookRead", "User", 3))
    #print(get_topn("bookWant", "User", 3))
    #print(get_topn("interestAuthor", "User", 3))
    #print(get_topn("interestCategory", "User", 3))
    res = get_topn("bookRead", "User", 3)
    for r in res:
        print('k')