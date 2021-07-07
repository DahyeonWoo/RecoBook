import socket

class BotServer:
    def __init__(self, srv_port, listen_num):
        self.port = srv_port # 생성할 소켓 서버의 포트 번호
        self.listen = listen_num # 동시에 연결을 수락할 클라이언트 수
        self.mySock = None

    # sock 생성
    def create_sock(self):
        """
        TCP/IP 소켓 생성 뒤 지정 서버 포트(self.port)로 지정한 연결 수 (self.listen)만큼 클라이언트 연결 수락
        """
        self.mySock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mySock.bind(("0.0.0.0", int(self.port)))
        self.mySock.listen(int(self.listen))
        return self.mySock

    # client 대기
    """
    챗봇 클라이언트 연결 대기하고 있다가 수락하는 메서드
    클라이언트가 연결을 요청하는 즉시 accept() 함수는 클라이언트와 통신할 수 있는 클라이언트용 소켓 객체를 반환
    반환값 (conn, address) 튜플
    conn: 연결된 챗봇 클라이언트와 데이터를 송수신할 수 있는 클라이언트 소켓
    address: 연결된 챗봇 클라이언트 소켓의 바인드된 주소
    """
    def ready_for_client(self):
        return self.mySock.accept()

    # sock 반환
    def get_sock(self):
        return self.mySock

    