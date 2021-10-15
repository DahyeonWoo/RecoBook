import sys
from io import BytesIO
from PIL import Image
sys.path.append("./project/flask/api")
import cv2
import requests
# import urllib.request
from tqdm import tqdm
import numpy as np
from db_model.mysql import conn_mysqldb

headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36" }

def get_info_from_db():
    db = conn_mysqldb()
    db_cursor = db.cursor()
    sql = 'SELECT isbn13, cover FROM Book'
    db_cursor.execute(sql)
    result = db_cursor.fetchall()
    db.close()
    return result

def url_to_image_and_resizing():
    """
    이미지 url을 받아 numpy array로 바꾼 후에
    resizing한 이미지를 반환
    """

    info_list = get_info_from_db()
    for info in tqdm(info_list, total=len(info_list), desc='resizing ...'):
        isbn, url = info
        res = requests.get(url, headers=headers)
        image = Image.open(BytesIO(res.content))
        image = np.asarray(image, dtype="uint8")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # res = urllib.request.urlopen(url, headers=headers)
        # image = np.asarray(bytearray(res.read()), dtype="uint8")
        # image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        resized_image = cv2.resize(image, (200, 200))
        cv2.imwrite('./project/flask/api/images/{}.jpg'.format(isbn), resized_image)
    print('resizing Completed.')

if __name__ == '__main__':
    result = get_info_from_db()
    image = url_to_image_and_resizing()

