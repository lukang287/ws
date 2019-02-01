import json, stomp


class JsonListener(stomp.ConnectionListener):

    def on_message(self, headers, message):
        pass


