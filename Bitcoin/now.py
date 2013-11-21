from urllib.request import urlopen, HTTPError
import tornado.ioloop
import tornado.httpserver
import tornado.web


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/now", BitNowHandler),
        ]
        settings = dict(
            template_path="templates",
            static_path="static",
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class BitNowHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            r = urlopen('http://blockchain.info/ticker')
            data = r.read().decode()
            r.close()
            self.write(str(data))
        except HTTPError as err:
            print(err)


if __name__ == "__main__":
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(8088)
    tornado.ioloop.IOLoop.instance().start()