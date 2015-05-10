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

# Project assets
import credentials


# Embedded class for the stream listener that will pull from the Twitter Streaming API
class CustomStreamListener(tweepy.StreamListener):

    # Initialize the class
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()

        # Setup RabbitMQ Connection
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = connection.channel()

        # Set max queue size
        args = {"x-max-length": 2000}

        self.channel.queue_declare(queue='twitter_topic_feed', arguments=args)

    # When a status is recieved, this will execute
    def on_status(self, status):

        print status.text, "\n"

        data = {}
        if status.coordinates is not None:
            data['lon'] = status.coordinates['coordinates'][0]
            data['lat'] = status.coordinates['coordinates'][1]
        else:
            pass

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
    def __init__(self):
        self.auth = tweepy.OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        self.auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)
        self.stream_listener = CustomStreamListener(self.api)
        self.streaming_api = tweepy.streaming.Stream(self.auth, self.stream_listener)

    def stream(self):
        print 'Starting the stream...'

        # TODO: Let this be customizable, i.e. take a bounding box from the web interface
        # Filter by location using a bounding box on the contiguous united states.
        self.streaming_api.filter(locations=[-125.06,24.57,-67.3,49.03])
