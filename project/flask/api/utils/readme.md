# 이미지 resize 프로세스
1. db에서 `isbn`, `image url` 호출
2. opencv를 활용해(`utils/resize_image.py`) 이미지를 정사각형으로 resize
3. 로컬 img 폴더에 `{isbn}.jpg` 형태로 저장
4. 로컬 폴더를 ncp object storage에 업로드(`api/bucket.py`)
5. 업로드 된 각각의 object들은 url이 생성됨
6. object 공개로 설정(유출 주의)
7. db에 새로운 열 `resizedCover`에 업로드 (`db_model/modifyDB`)