# 代码生成时间: 2025-10-21 19:03:19
import os
import mimetypes
from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line

# 定义一个全局变量来解析命令行参数
define("port", default=8888, help="run on the given port", type=int)

class FileTypeHandler(RequestHandler):
    """
    Handler for file type detection.
    """
    # 处理GET请求，返回文件的MIME类型
    def get(self):
        try:
            # 检查请求参数中是否包含filename
            if "filename" not in self.request.arguments:
                self.write("Error: No filename provided.")
                self.set_status(400)
                return

            # 获取文件名
            filename = self.get_argument("filename")[0]

            # 检查文件是否存在
            if not os.path.exists(filename):
                self.write("Error: File not found.")
                self.set_status(404)
                return

            # 使用mimetypes猜文件类型
            file_type, _ = mimetypes.guess_type(filename)
            # 如果文件类型未知，则返回'application/octet-stream'
            file_type = file_type or 'application/octet-stream'

            self.write(f"The file type of {filename} is: {file_type}")
        except Exception as e:
            # 处理异常情况
            self.write(f"An error occurred: {str(e)}")
            self.set_status(500)

def make_app():
    """
    Create the Tornado application.
    """
    return Application(
        [
            (r"/file_type", FileTypeHandler),
        ]
    )

if __name__ == "__main__":
    # 解析命令行参数
    parse_command_line()

    # 创建并运行应用
    app = make_app()
    app.listen(options.port)
    print(f"Server is running on http://localhost:{options.port}")
    IOLoop.current().start()