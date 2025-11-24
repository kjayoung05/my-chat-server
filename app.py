# app.py (서버 컴퓨터에서 실행)

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import eventlet # 비동기 처리를 위해 필요

# Flask 객체 생성
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
# WebSockets 라이브러리 초기화. async_mode='eventlet'을 사용하여 안정적인 비동기 처리
socketio = SocketIO(app, async_mode='eventlet')

# 웹 페이지 라우팅: 기본 접속 주소 (/)로 접근 시 chat.html 파일을 전송
@app.route('/')
def index():
    return render_template('chat.html')

# 클라이언트 연결/해제 이벤트 핸들링
@socketio.on('connect')
def handle_connect():
    print('Client connected!')
    # 새로 접속한 클라이언트에게만 상태 메시지 전송
    emit('status', {'msg': '연결되었습니다.'}, broadcast=False)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected!')
    # 모든 접속자에게 상태 메시지 전송
    emit('status', {'msg': '연결이 끊어졌습니다.'}, broadcast=True)

# 메시지 수신 및 중계 (실제 채팅 기능)
@socketio.on('message')
def handle_message(data):
    # data: {'msg': '메시지 내용', 'user': '닉네임'}
    print(f"[{data['user']}]: {data['msg']}")
   
    # 받은 메시지를 발신자를 포함한 모든 접속자에게 다시 전송
    emit('message', data, broadcast=True)

if __name__ == '__main__':
    # WebSockets 서버 시작 (9000 포트)
    # host='0.0.0.0'은 외부 컴퓨터의 접속을 모두 허용한다는 뜻입니다.
    # eventlet 웹 서버를 사용하여 실행합니다.
    eventlet.wsgi.server(eventlet.listen(('', 9000)), app)
    # ⚠️ 이전의 socketio.run 대신 eventlet.wsgi.server를 사용해 안정성을 높입니다.
