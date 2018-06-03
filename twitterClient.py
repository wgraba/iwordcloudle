import logging
import tweepy
from tweepy import OAuthHandler
# from textblob import TextBlob

logger = logging.getLogger(__name__)


class TwitterClient(object):
    """
    Generic Twitter Class for sentiment analysis.
    """

    def __init__(self, consumer_key, consumer_secret, access_token,
                 access_token_secret):
        """
        Class constructor or initialization method.
        """

        logger.info('Attempting Twitter authentication...')
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # def get_tweet_sentiment(self, tweet):
    #     """
    #     Utility function to classify sentiment of passed tweet
    #     using textblob's sentiment method
    #     """
    #
    #     # create TextBlob object of passed tweet text
    #     analysis = TextBlob(self.clean_tweet(tweet))
    #     # set sentiment
    #     if analysis.sentiment.polarity > 0:
    #         return 'positive'
    #     elif analysis.sentiment.polarity == 0:
    #         return 'neutral'
    #     else:
    #         return 'negative'

    def get_tweets(self, query, count):
        """
        Main function to fetch tweets and parse them.
        """

        tweets = []

        logger.info('Getting tweets...')
        fetched_tweets = tweepy.Cursor(self.api.search, q=query).items(count)
        # logger.info('Found {:d} total Tweets'.format(len(fetched_tweets)))

        # logger.info('Removing re-Tweets...')
        for tweet in fetched_tweets:
            # parsed_tweet = {'text': tweet.text}
            #
            # # saving text of tweet
            # # saving sentiment of tweet
            # # parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
            #
            # # appending parsed tweet to tweets list
            # if tweet.retweet_count > 0:
            #     # if tweet has retweets, ensure that it is appended only once
            #     if parsed_tweet not in tweets:
            #         tweets.append(parsed_tweet['text'])
            # else:
            #     tweets.append(parsed_tweet['text'])

            tweets.append(tweet.text)

        logger.info('Found {:d} Tweets'.format(len(tweets)))

        return tweets
