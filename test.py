from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json

consumer_key = "muBHyzsmbgb0Aa9xjXF0wg"
consumer_secret = "bJ97B7PdGY46amtEhvzzN9vH2XhyvxRmzDggxFfKvc"
access_token = "16931374-TusvFdBgBKYp8Nn1zvKN0X1daxuMu51FrO7Z39u0U"
access_token_secret = "EyR8cLkaRtFxwM90dct5ZDU89JtlMjJSqkTskdLHg"


class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
    	d = json.loads(data)
    	text = d["text"].rstrip('\r\n')
        print text
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=['miami'])