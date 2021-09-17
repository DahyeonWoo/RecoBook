import sys
import json
sys.path.append("./project/flask/")
sys.path.append("./project/flask/api/")
from api.utils.Agg import get_topn

"""
top n 개의 통계량을 반환
"""

class Top:
    def get_topn_bookRead(n):
        return get_topn("bookRead", "User", n)

    def get_topn_bookWant(n):
        return get_topn("bookWant", "User", n)

    def get_topn_interestBook(n):
        return get_topn("interestBook", "User", n)

    def get_topn_interestAuthor(n):
        return get_topn("interestAuthor", "User", n)

    def get_topn_interestCategory(n):
        return get_topn("interestCategory", "User", n)

    def accessing_dict_info(get_topn_returned: str):
        """
        딕셔너리(json)에 접근해 출력물을 만드는 함수
        

        :param get_topn_returned: 통계량을 반환한 json dump 파일
        :return: 출력물 ex) 1위: 아몬드 - 1명
                            2위: 윤동주 시집 - 1명
                            3위: 우아한 거짓말 - 1명
        """
        get_topn_returned = json.loads(get_topn_returned)
        answer = ''
        for grade, dict_info in get_topn_returned.items():
            answer += f'{grade}위: {dict_info["name"]} - {dict_info["count"]}명\n'
        return answer


if __name__ == "__main__":
    n=3
    # print(Top.get_topn_bookRead(n))
    # print(Top.get_topn_bookWant(n))
    # print(Top.get_topn_interestAuthor(n))
    # print(Top.get_topn_interestCategory(n))
    res = Top.get_topn_bookRead(n)
    # res = json.loads(Top.get_topn_bookRead(n))
    # res = json.loads(res)
    res = Top.accessing_dict_info(res)
    print(res)