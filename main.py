import os.path
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import threading
import time
import datetime
# tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import simplejson as json



from tornado.options import define
define("port", default=5000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/favicon.ico", FaviconHandler),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static'}),
            (r'/', WebHandler),
            (r'/ws', WSHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


# websocket
class FaviconHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect('/static/favicon.ico')

class WebHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html")

class WSHandler(tornado.websocket.WebSocketHandler):
    connections = []
    def open(self): 
        self.connections.append(self)
        cb = tornado.ioloop.PeriodicCallback(self.spew, 1000, io_loop=main_loop)
        cb.start()
        print 'new connection'
        self.write_message("Hi, client: connection is made ...")

    def on_message(self, message):
        pass

    #def callback(self, tweet):
    #    self.write_message('{"tweet":"%s"}' % status.text)

    def on_close(self):
        self.connections.remove(self)
        print 'connection closed'

    def spew(self):
        msg = 'spew!'
        print(msg)
        self.on_message(msg)



# new stream listener 
class StdOutListener(StreamListener, WSHandler):
    """ A listener handles tweets are the received from the stream. 
    This is a basic listener that just prints received tweets to stdout.

    """

    # tweet handling
    def on_status(self, status):
        print(status.user.screen_name.encode('utf-8') + ": " + status.text.encode('utf-8'))
        #self.on_message('hello world') # <--- THIS is where i want to send a msg to WSHandler.on_message
        for connection in WSHandler.connections:
            connection.write_message('{"tweet_text": status.text}')

    # limit handling
    def on_limit(self, track):
        return

    # error handling
    def on_error(self, status):
        print status


def OpenStream():
    #twitter auth
    consumer_key = os.environ.get('CONSUMER_KEY')
    consumer_secret = os.environ.get('CONSUMER_SECRET')
    access_token = os.environ.get('ACCESS_TOKEN')
    access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l, gzip=True) 
    stream.filter(track=['obama'])

def main():
    tornado.options.parse_command_line()
    threading.Thread(target=OpenStream).start()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(tornado.options.options.port)

    # start it up
    tornado.ioloop.IOLoop.instance().start()
    

if __name__ == "__main__":
    main()
    main_loop.start()
    
    






