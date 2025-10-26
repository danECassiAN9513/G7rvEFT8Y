# 代码生成时间: 2025-10-26 10:20:20
import tornado.ioloop
import tornado.web
import json

# 一个简单的用户存储系统，用于验证用户名和密码
USERS = {
    "user1": "password1",
    "user2": "password2"
}

class MainHandler(tornado.web.RequestHandler):
    """
    主页处理登录请求，验证用户凭据
    """
    def post(self):
        # 解析JSON请求体
        try:
            data = json.loads(self.request.body)
            username = data['username']
            password = data['password']
        except (KeyError, ValueError):
            # 如果解析失败或缺少必要的参数，返回错误信息
            self.set_status(400)
            self.write(json.dumps({'error': 'Invalid request'}))
            return

        # 用户验证
        if username in USERS and USERS[username] == password:
            self.write(json.dumps({'message': 'Login successful'}))
        else:
            self.set_status(401)  # Unauthorized
            self.write(json.dumps({'error': 'Invalid username or password'}))

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/login", MainHandler),
        ]
        super(Application, self).__init__(handlers)

if __name__ == "__main__":
    # 创建并启动应用程序
    app = Application()
    app.listen(8888)
    print("Server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
