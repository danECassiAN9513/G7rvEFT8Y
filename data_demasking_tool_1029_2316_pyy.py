# 代码生成时间: 2025-10-29 23:16:36
import tornado.web
import re
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 数据脱敏模式
DESENSITIZATION_PATTERNS = {
    "phone": r"(\d{3})\d{4}(\d{4})",
    "email": r"(\w+)@(\w+)\.(\w+)"
}

# 数据脱敏替换函数
def demasking(data, pattern_type):
    """
    对输入的数据进行脱敏处理

    Args:
        data (str): 需要脱敏的数据字符串
        pattern_type (str): 脱敏模式类型，如 'phone' 或 'email'

    Returns:
        str: 脱敏后的数据字符串
    """
    pattern = DESENSITIZATION_PATTERNS.get(pattern_type)
    if not pattern:
        raise ValueError(f"Unsupported demasking pattern type: {pattern_type}")
    return re.sub(pattern, lambda x: x.group(1) + '****' + x.group(2), data)

# Tornado Web Handler
class DemaskingHandler(tornado.web.RequestHandler):
    """
    处理数据脱敏请求的Tornado Web Handler
    """
    def post(self):
        """
        处理POST请求，接收数据和脱敏类型，返回脱敏后的数据
        """
        try:
            data = self.get_body_argument('data')
            pattern_type = self.get_body_argument('pattern_type')
            demasked_data = demasking(data, pattern_type)
            self.write({'status': 'success', 'demasked_data': demasked_data})
        except ValueError as e:
            self.write({'status': 'error', 'message': str(e)})
            self.set_status(400)
        except Exception as e:
            logger.error(f"Error in demasking: {str(e)}")
            self.write({'status': 'error', 'message': 'Internal Server Error'})
            self.set_status(500)

# Tornado Application
class DemaskingApp(tornado.web.Application):
    """
    Tornado应用程序
    """
    def __init__(self):
        handlers = [
            (r"/demask", DemaskingHandler),
        ]
        super(DesensitizationApp, self).__init__(handlers)

# 主程序入口点
if __name__ == "__main__":
    app = DemaskingApp()
    app.listen(8888)
    logger.info("Desensitization application is running on port 8888")
    tornado.ioloop.IOLoop.current().start()
