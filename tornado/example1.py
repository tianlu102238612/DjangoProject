import tornado.web
import tornado.ioloop

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello Tornado')

def main():
    app = tornado.web.Application(handlers=[(r'/',MainHandler),])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
    
if __name__ == '__main__':
    main()

