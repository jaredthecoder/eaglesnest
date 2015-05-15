####################################################################################
#
# File: harvester.py
# Description: Pull tweets from twitter and pushs them onto RabbitMQ
# Author: Jared M. Smith <jaredmichaelsmith.com>
#
####################################################################################

# Python standard library assets
import sys
import json
import time

# 3rd Party assets
import tweepy
import pika
from textblob import TextBlob

# Project assets
import credentials
from sentiment import SentimentAnalyzer


# Embedded class for the stream listener that will pull from the Twitter Streaming API
class CustomStreamListener(tweepy.StreamListener):

    # Initialize the class
    def __init__(self, api, filter_type):
        self.api = api
        self.filter_type = filter_type
        self.analyzer = SentimentAnalyzer()

        super(tweepy.StreamListener, self).__init__()

        # Setup RabbitMQ Connection
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = connection.channel()

        # Set max queue size
        args = {"x-max-length": 2000}

        self.channel.queue_declare(queue='twitter_sentiment_feed', arguments=args)

    # When a status is recieved, this will execute
    def on_status(self, status):

        # Get the sentiment score and assign the correct color to it.
        # Default to gray for neutral, and we don't have to check
        # if it returns neutral.
        def get_sentiment():
            color = 'gray'
            sentiment = self.analyzer.trivially_analyze(status.text)
            if sentiment == 'pos':
                color = 'green'
            elif sentiment == 'neg':
                color = 'red'
            return color


        data = {}
        if status.coordinates is not None and status.coordinates['type'] == 'Point':
            color = get_sentiment()
            print "[ %s ] -- %s" % (color, status.text)

            data['lon'] = status.coordinates['coordinates'][0]
            data['lat'] = status.coordinates['coordinates'][1]
            data['color'] = color
            data['id_str'] = status.id_str
            data['user_profile_image_url'] = status.user.profile_image_url
            data['user_screen_name'] = status.user.screen_name

            # Push the tweet onto the AMPQ RabbitMQ channel
            self.channel.basic_publish(exchange='',
                                        routing_key='twitter_sentiment_feed',
                                        body=json.dumps(data))

    # Execute on error
    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True  # Don't kill the stream

    # Execute on timeout
    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True  # Don't kill the stream


# Harvester class consumes the twitter feed and pushes tweets onto the queue.
class Harvester(object):

    # Initialize the class
    def __init__(self, filter_type='location', location=[-125.06,24.57,-67.3,49.03], keywords=None):
        self.filter_type = filter_type
        self.location = location
        self.keywords = keywords
        self.auth = tweepy.OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        self.auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)
        self.stream_listener = CustomStreamListener(self.api, self.filter_type)
        self.streaming_api = tweepy.streaming.Stream(self.auth, self.stream_listener)

    def stream(self):
        print 'Starting the stream...'

        while (1):
            try:
                if self.filter_type == 'location':
                    # TODO: Let this be customizable, i.e. take a bounding box from the web interface
                    # Filter by location using a bounding box on the contiguous united states.
                    self.streaming_api.filter(locations=self.location)
                elif self.filter_type == 'keyword':
                    # Filter by keywords
                    self.streaming_api.filter(keywords=keywords)
            except (Exception, SystemExit) as e:
                print "Exception occured!"
                print e
