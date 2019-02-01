from flask import request, render_template
from geventwebsocket.websocket import WebSocket, WebSocketError
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from app import app
import time
from service.mq.TopicService import ReceiveTopicService, TopicListener


@app.route('/index/')
def index():
    return render_template('mutil.html')

listener = TopicListener()
receive_service = ReceiveTopicService(listener)
receive_service.receive(app.config['NOTIFY_TOPIC_NAME'])
admin_notify_socket_dict = {}


@app.route('/ws/admin/<id>')
def admin_notify(id):
    print('ws request')
    user_socket = request.environ.get("wsgi.websocket")
    if not user_socket:
        return "not websocket"

    admin_notify_socket_dict[id] = user_socket
    print(admin_notify_socket_dict)

    listener.set_ws_dict(admin_notify_socket_dict)

    while True:
        try:
            user_socket.receive()
        except WebSocketError as e:
            admin_notify_socket_dict.pop(id)
            print(admin_notify_socket_dict)
            break
    return id+' end '

if __name__ == '__main__':
    http_serve = WSGIServer(("0.0.0.0", app.config['WS_SERVER_PORT_MUTIL']), app, handler_class=WebSocketHandler)
    http_serve.serve_forever()