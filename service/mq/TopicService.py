import stomp, json
from app import app
from geventwebsocket.websocket import WebSocketError


class SendTopicService():
    def __init__(self):
        self.conn = stomp.Connection10(app.config['MQ_BROKERS'])
        self.conn.start()
        self.conn.connect()

    def send(self, topic_name, msg):
        self.conn.send(topic_name, msg)
        self.conn.disconnect()


class ReceiveTopicService():
    def __init__(self, mqListener):
        self.MQListener = mqListener
        self.conn = stomp.Connection10(app.config['MQ_BROKERS'])
        self.conn.set_listener('', mqListener)
        self.conn.start()
        self.conn.connect()

    def receive(self, topic_name):
        self.conn.subscribe(topic_name)
        # while True:
        #     time.sleep(3)
        #     self.receive(topic_name)
        # self.conn.disconnect()

    def disconnect(self):
        self.conn.disconnect()


class TopicListener(stomp.ConnectionListener):
    _ws_dict = {}

    def on_message(self, headers, message):
        print('topic receive msg ', message)
        message_dict = self.parse_message(message)
        if message_dict:
            print(self._ws_dict)
            for id, u_socket in self._ws_dict.items():
                try:
                    u_socket.send(json.dumps(message_dict))
                except WebSocketError as e:
                    self._ws_dict.pop(id)
                    print(self._ws_dict)
                    print(e)

    def set_ws_dict(self, ws_dict):
        self._ws_dict = ws_dict

    def parse_message(self, message):
        data_obj = json.loads(message)
        _notify = {}
        if 'message' not in data_obj:
            print('无效的notify消息', message)
            return
        else:
            _notify['message'] = data_obj['message']
        if 'color' in data_obj:
            _notify['color'] = data_obj['color']
        if 'autoClose' in data_obj:
            _notify['autoClose'] = data_obj['autoClose']
        return _notify

