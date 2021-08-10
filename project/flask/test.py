from flask import request
from api.ColumnsFromDB import get_col_name, get_db_data
from api.user import UserInfo
from api.book import get_isbn_to_info, get_title_to_info
import requests

BASE = "http://127.0.0.1:5000/"

name = '이지은'
# author = request.args.get('author', name)
# print(author)
# response = requests.get(BASE + "book?author=" + name)
# print(response.json())
# res = get_isbn_to_info(9772384289005)
res = get_col_name('Book')
res = get_title_to_info('미스테리아')
print(res)