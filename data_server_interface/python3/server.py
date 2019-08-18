# -*- coding:utf-8 -*-
# @Time     : 2019-08-18 11:33
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

from tornado import ioloop, web, httpserver


class MainHandler(web.RequestHandler):
    def get(self):
        self.write("Hello, world")


app = web.Application([
    (r"/index", MainHandler),
])

if __name__ == "__main__":
    server = httpserver.HTTPServer(app)
    server.bind(8888)
    server.start()
    ioloop.IOLoop.current().start()
