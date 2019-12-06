from http.server import HTTPServer, BaseHTTPRequestHandler
from json import dumps, loads
import threading
import re
from textblob import TextBlob
import tweepy
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')


class TwitterClient(object):
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''

    def clean_tweet(self, tweet):
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'


api = TwitterClient()
sid = SentimentIntensityAnalyzer()


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        text = self.rfile.read(int(self.headers.get("content-length")))
        texts = loads(text)
        result = []
        for x in texts:
            tweetN = api.clean_tweet(x)
            print(x)
            tweetNsentiment2 = sid.polarity_scores(tweetN)
            result.append(tweetNsentiment2)
            print(tweetNsentiment2)
        self.send_response(200)
        self.send_header("access-control-allow-headers",
                         "Origin, X-Requested-With, Content-Type, Accept")
        self.send_header("access-control-allow-origin", "*")
        self.end_headers()  # GET DATA FROM DB
        self.wfile.write(bytes(dumps(result), "utf-8"))


def main():
    httpd = HTTPServer(("", 7768), SimpleHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    # calling main function
    main()
