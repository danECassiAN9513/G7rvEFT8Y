# 代码生成时间: 2025-10-15 03:26:19
import tornado.ioloop
import tornado.web
import json
import inspect
from tornado.web import RequestHandler

def get_api_docs(application):
    """
    Recursively generates API documentation from Tornado web application handlers.
    :param application: Tornado web application instance.
    :return: A dictionary representing the API documentation.
    """
    api_docs = {}
    for route in application.routes():
        handler = route[1].handler_class
        # Check if the handler has a get method since we only support GET requests for simplicity
        if hasattr(handler, 'get'):
            # Get the docstring from the handler's get method
            docstring = inspect.getdoc(handler.get)
            route_path = route[1].regex.pattern
            if route_path not in api_docs:
                api_docs[route_path] = {}
            api_docs[route_path]['doc'] = docstring
            api_docs[route_path]['methods'] = ['GET']
    return api_docs

class MainHandler(tornado.web.RequestHandler):
    """
    Main handler that serves the API documentation.
    """
    def get(self):
        application = self.application
        try:
            docs = get_api_docs(application)
            self.write(json.dumps(docs, indent=4))
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({'error': str(e)}))

class Application(tornado.web.Application):
    """
    Tornado application that includes the API documentation handler.
    """
    def __init__(self):
        handlers = [
            (r"/api/docs", MainHandler),
        ]
        settings = {
            "debug": True,  # Enable debug mode for development
        }
        super(Application, self).__init__(handlers, **settings)

if __name__ == '__main__':
    application = Application()
    print("Starting API documentation server...")
    tornado.ioloop.IOLoop.current().start()
