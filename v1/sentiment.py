###################################################################################
#
# File: sentiment.py
# Description: Sentiment analysis portion of the code.
# Author: Jared M. Smith <jaredmichaelsmith.com>
#
###################################################################################

# 3rd Party assets
from textblob import TextBlob, Word
from textblob.wordnet import Synset
from textblob.classifiers import NaiveBayesClassifier


class SentimentAnalyzer(object):

    # Initialize the class
    def __init__(self):
        pass

    # Return 'pos', 'neg', or 'neutral' based on the built-in sentiment analyzer of TextBlob
    # Uses the polarity measure of the sentiment analyzer to judge the data passed in.
    def trivially_analyze(self, data):
        blob = TextBlob(data)

        sentiment = blob.sentiment

        if (0 < sentiment.polarity <= 1.0):
            return 'pos'
        elif (-1.0 <= sentiment.polarity < 0):
            return 'neg'
        elif (sentiment.polarity == 0):
            return 'neutral'
