# 代码生成时间: 2025-10-11 03:47:20
import tornado.ioloop
import tornado.web
from datetime import datetime

# 定义一个简单的存储结构来保存消息
class MessageStore:
    def __init__(self):
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages

# 定义一个消息模型
class Message:
    def __init__(self, sender, receiver, content, timestamp=None):
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.timestamp = timestamp if timestamp else datetime.now()

# 定义一个Tornado HTTP请求处理器
class MessageHandler(tornado.web.RequestHandler):
    def initialize(self, message_store):
        self.message_store = message_store

    def post(self):
        try:
            sender = self.get_argument('sender')
            receiver = self.get_argument('receiver')
            content = self.get_argument('content')
            message = Message(sender, receiver, content)
            self.message_store.add_message(message)
            self.write({'status': 'success', 'message': 'Message sent successfully'})
        except Exception as e:
            self.write({'status': 'error', 'message': str(e)})
            self.set_status(400)  # Bad Request

    def get(self):
        messages = self.message_store.get_messages()
        self.write({'status': 'success', 'messages': [vars(msg) for msg in messages]})

# 定义一个Tornado应用
class SchoolHomeCommunicationApp(tornado.web.Application):
    def __init__(self):
        message_store = MessageStore()
        handlers = [
            (r"/message", MessageHandler, dict(message_store=message_store))
        ]
        settings = {
            "debug": True,
        }
        super(SchoolHomeCommunicationApp, self).__init__(handlers, **settings)

# 启动Tornado IOLoop和应用
def main():
    app = SchoolHomeCommunicationApp()
    app.listen(8888)
    print("Server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
