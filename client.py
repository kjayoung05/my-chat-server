import socket
import threading
import sys

# 서버 설정 (여기에 서버 IP 주소 또는 Render 도메인을 입력해야 함!)
SERVER_HOST = '여기에 서버의 IP 주소 또는 Render 도메인을 입력하세요' 
SERVER_PORT = 9000  # 서버와 동일한 포트 번호

def receive_messages(client_socket):
    """서버로부터 메시지를 수신하여 출력"""
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                print(f"\n📢 수신: {message.decode('utf-8')}")
            else:
                print("서버 연결이 끊겼습니다.")
                client_socket.close()
                sys.exit() # 프로그램 종료
        except:
            print("\n연결 중 오류가 발생하여 종료합니다.")
            client_socket.close()
            sys.exit()
            
def start_client():
    """클라이언트 소켓 생성 및 서버 연결"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # 1. 서버에 연결 시도
        client.connect((SERVER_HOST, SERVER_PORT))
        print(f"✨ 서버 {SERVER_HOST}:{SERVER_PORT}에 연결 성공!")
        
        # 2. 메시지 수신용 스레드 시작
        receive_thread = threading.Thread(target=receive_messages, args=(client,))
        receive_thread.daemon = True # 메인 스레드 종료 시 함께 종료
        receive_thread.start()
        
        # 3. 메시지 입력 및 전송 (메인 스레드)
        while True:
            message = input("나 > ")
            if message.lower() == 'exit':
                client.close()
                break
            client.send(message.encode('utf-8'))
            
    except ConnectionRefusedError:
        print("❌ 연결 실패: 서버가 켜져 있는지, IP 주소와 포트가 올바른지 확인하세요.")
    except socket.gaierror:
        print("❌ 연결 실패: 호스트 이름(Render 도메인) 또는 IP 주소가 유효하지 않습니다.")
    except Exception as e:
        print(f"❌ 예상치 못한 오류 발생: {e}")

# 클라이언트 시작
if __name__ == "__main__":
    start_client()
