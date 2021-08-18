from flask import request
from api.user import UserInfo
from api.book import get_isbn_to_info, get_title_to_info
import requests

BASE = "http://127.0.0.1:5000/"

dict = {'author': "이지은", 'title': "금각사", 'isbn13': "9788925588643"}

for key, value in dict.items():
    res = requests.get(BASE + f"bookinfo?{key}={value}")
    data = res.json()
    print(res, data)



# print(response.json())
# res = get_isbn_to_info(9772384289005)
