WS_SERVER_PORT_ONE = 5001
WS_SERVER_PORT_MUTIL = 5000

#MQ配置,queue用于一对一不丢失，topic用于发布订阅，一对多会丢失
MQ_BROKERS = [('106.13.4.172', 61613)]
LOG_QUEUE_NAME = '/queue/log'
CMD_QUEUE_NAME = '/queue/cmd'
NOTIFY_TOPIC_NAME = '/topic/notify'


