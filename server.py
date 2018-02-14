from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from app import app, db

db.init_app(app)

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(80)
IOLoop.instance().start()
