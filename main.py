import os.path
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import threading
import time
import datetime

# websocket
class FaviconHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect('/static/favicon.ico')

class WebHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("websockets.html")

class WSHandler(tornado.websocket.WebSocketHandler):
    connections = []
    def open(self): 
        self.connections.append(self)
        cb = tornado.ioloop.PeriodicCallback(self.spew, 1000, io_loop=main_loop)
        cb.start()
        print 'new connection'
        self.write_message("Hi, client: connection is made ...")

    def on_message(self, message):
        print 'message received: \"%s\"' % message
        self.write_message("Echo: \"" + message + "\"")
        if (message == "green"):
            self.write_message("green!")

    def on_close(self):
        self.connections.remove(self)
        print 'connection closed'

    def spew(self):
        msg = 'spew!'
        print(msg)
        self.on_message(msg)

handlers = [
    (r"/favicon.ico", FaviconHandler),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static'}),
    (r'/', WebHandler),
    (r'/ws', WSHandler),
]

settings = dict(
    template_path=os.path.join(os.path.dirname(__file__), "static"),
)

application = tornado.web.Application(handlers, **settings)


# tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import simplejson as json


# new stream listener 
class StdOutListener(StreamListener, WSHandler):
    """ A listener handles tweets are the received from the stream. 
    This is a basic listener that just prints received tweets to stdout.

    """

    # tweet handling
    def on_status(self, status):
        print('@%s: %s' % (status.user.screen_name, status.text))
        handler = WSHandler()
        handler.on_message('hello world') # <--- THIS is where i want to send a msg to WSHandler.on_message
        for connection in WSHandler.connections:
            connection.write_message(status.text)

    # limit handling
    def on_limit(self, track):
        return

    # error handling
    def on_error(self, status):
        print status


def OpenStream():
    #twitter auth
    consumer_key = "muBHyzsmbgb0Aa9xjXF0wg"
    consumer_secret = "bJ97B7PdGY46amtEhvzzN9vH2XhyvxRmzDggxFfKvc"
    access_token = "16931374-TusvFdBgBKYp8Nn1zvKN0X1daxuMu51FrO7Z39u0U"
    access_token_secret = "EyR8cLkaRtFxwM90dct5ZDU89JtlMjJSqkTskdLHg"

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l, gzip=True) 
    stream.filter(track=['obama'])



if __name__ == "__main__":
    threading.Thread(target=OpenStream).start()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    main_loop = tornado.ioloop.IOLoop.instance()
#   main_loop.add_callback(OpenStream)
    main_loop.start()
