# 유재성 flask 공부 파일

from flask import Flask, request, jsonify
app = Flask(__name__)
"""
HTTP 메서드별 CRUD 동작 설명

HTTP 메서드 | CRUD 동작 | 설명
POST         Create     서버 리소스를 생성할 때 사용
GET          Read       서버 리소스 읽어올 때 사용    
PUT          Update     서버 리소스 수정할 때 사용  
DELETE       Delete     서버 리소스 삭제할 때 사용  

request: 클라이언트로부터 HTTP 요청을 받았을 때 요청 정보를 확인
jsonify: 데이터 객체를 JSON 응답으로 변환해주는 Flask 유틸리티 함수
"""

# 서버 리소스
"""
GET, POST 메서드로 호출된 REST API를 통해 해당 리소스에 객체 추가, 불러오도록 구현
"""
resource = []

# 사용자 정보 조회
"""
user_id 값으로 저장된 데이터가 있다면 해당 객체를 JSON으로 응답
"""
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):

    for user in resource:
        if user['user_id'] is user_id:
            return jsonify(user)

    return jsonify(None)

# 사용자 추가
@app.route('/user', methods=['POST'])
def add_user():
    user = request.get_json() # HTTP 요청의 body에서 json 데이터를 불러옴
    resource.append(user) # 리소스 리스트에 추가
    return jsonify(resource)

@app.route('/info/<name>') #5000/info/haebuk으로 들어갈 경우 hello haebuk 출력
def get_name(name):
    return 'hello {}'.format(name)

"""@app.route('/user/<int:id>') # 위와 마찬가지, 대신 정수형만 받음
def get_user(id):
    return 'user id is {}'.format(id)"""

@app.route('/json/<int:dest_id>/<message>')
@app.route('/JSON/<int:dest_id>/<message>') #여러개의 URI 지정, 딕셔너리 형태로 출력함
def send_message(dest_id, message):
    json = {
        'bot_id': dest_id,
        'message': message
    }
    return json


if __name__ == '__main__':
    app.run()

"""


if __name__ == '__main__':
    app.run()"""

