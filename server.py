import socket
import threading

# 클라이언트 목록
clients = []

# 서버 설정
HOST = '0.0.0.0' # 모든 IP 주소로부터의 접속 허용
PORT = 9000      # 약속된 포트 번호 (클라이언트와 통일해야 함)

def broadcast(message, connection):
    """특정 연결을 제외한 모든 클라이언트에게 메시지를 전달"""
    for client in clients:
        if client != connection:
            try:
                client.send(message)
            except:
                # 연결 오류 발생 시 클라이언트 목록에서 제거
                client.close()
                clients.remove(client)

def handle_client(client_socket):
    """클라이언트 연결 처리 및 메시지 수신"""
    while True:
        try:
            # 클라이언트로부터 데이터 수신
            message = client_socket.recv(1024)
            if message:
                print(f"[{client_socket.getpeername()[0]}:{client_socket.getpeername()[1]}] : {message.decode('utf-8')}")
                broadcast(message, client_socket)
            else:
                # 연결 종료 시 처리
                clients.remove(client_socket)
                client_socket.close()
                break
        except:
            # 연결 해제 처리
            clients.remove(client_socket)
            client_socket.close()
            break

def start_server():
    """서버 소켓을 열고 연결 대기"""
    # 1. TCP 소켓 생성
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 포트 재사용 설정
    
    # 2. IP와 포트 바인딩
    server.bind((HOST, PORT))
    
    # 3. 연결 대기 (최대 5개 동시 대기)
    server.listen(5)
    print(f"🌟 서버가 {PORT} 포트에서 대기 중입니다...")

    while True:
        # 4. 클라이언트 연결 수락
        client_socket, addr = server.accept()
        print(f"✅ 새로운 연결 수락: {addr[0]}:{addr[1]}")
        
        clients.append(client_socket)
        
        # 5. 새 스레드에서 클라이언트 처리
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

# 서버 시작
if __name__ == "__main__":
    start_server()
