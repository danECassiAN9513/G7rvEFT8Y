# 代码生成时间: 2025-09-24 15:58:38
import tornado.ioloop
import tornado.web
import random
from datetime import datetime

"""
RandomNumberGenerator Application
This application creates a web service that generates random numbers.
It follows Python best practices and Tornado framework conventions.
"""

class RandomNumberHandler(tornado.web.RequestHandler):
    """
    Request handler for generating random numbers.
    It accepts GET requests with optional parameters for min and max values.
    If no parameters are provided, it defaults to generating a random integer between 0 and 100.
    """
    def get(self):
        try:
            min_val = self.get_query_argument('min', 0)
            max_val = self.get_query_argument('max', 100)
            min_val = int(min_val)
            max_val = int(max_val)
            if min_val > max_val:
                raise ValueError('Minimum value cannot be greater than maximum value.')
            random_number = random.randint(min_val, max_val)
            self.write({'timestamp': datetime.now().isoformat(), 'random_number': random_number})
        except ValueError as e:
            self.set_status(400)
            self.write({'error': str(e)})
        except Exception as e:
            self.set_status(500)
            self.write({'error': 'An unexpected error occurred.'})

class Application(tornado.web.Application):
    """
    Tornado application setup.
    It defines the URL routes and the corresponding handlers.
    """
    def __init__(self):
        handlers = [
            (r"/random", RandomNumberHandler),
        ]
        super(Application, self).__init__(handlers)

def make_app():
    """
    Factory method for creating the Tornado application instance.
    This allows for easy testing and extension.
    """
    return Application()

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Starting Tornado application on http://127.0.0.1:8888")
    tornado.ioloop.IOLoop.current().start()