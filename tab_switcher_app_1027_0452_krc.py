# 代码生成时间: 2025-10-27 04:52:38
import tornado.ioloop
import tornado.web
def make_app():
    """
    创建并返回一个Tornado应用程序，该应用程序包含一个标签页切换器。
    """
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/switch/(\w+)", TabSwitchHandler),
    ])

class MainHandler(tornado.web.RequestHandler):
    """
    主页处理器，显示标签页切换器页面。
    """
    def get(self):
        # 渲染页面
        self.render("index.html")

class TabSwitchHandler(tornado.web.RequestHandler):
    """
    标签页切换处理器，根据请求参数切换标签页。
    """
    def get(self, tab_name):
        # 验证标签页名称
        if tab_name not in ["home", "about", "contact"]:
            self.set_status(404)
            self.write("Tab not found")
            return
        # 渲染对应标签页
        self.render(f"{tab_name}.html")

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Tab Switcher App started on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()