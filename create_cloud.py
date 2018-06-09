#!/usr/bin/python3

import logging
import argparse
import re
from wordcloud import WordCloud
from PIL import Image
import numpy as np

import twitterClient

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--consumer_key', help='Consumer key from Twitter app')
    parser.add_argument('-s', '--consumer_secret', help='Consumer secret from Twitter app')
    parser.add_argument('-t', '--access_token', help='Access token from Twitter app')
    parser.add_argument('-a', '--access_token_secret', help='Secret access token from Twitter app')
    parser.add_argument('-q', '--query', type=str, help='Terms to query separated by commas')
    parser.add_argument('output_path', type=str, help='Path to output file')

    parser.add_argument('-c', '--count', default=5000, type=int, help='Number of tweets to get')
    parser.add_argument('-f', '--file', type=str, help='Input file of words instead of Twitter')
    parser.add_argument('-i', '--image', type=str, help='Path to image file to mask')
    parser.add_argument('-w', '--write', type=str, help='Path to file to write Twitter output; can be used to cache'
                                                        'Twitter results and used later with -f. -w is ignored if '
                                                        '-f is used')

    args = parser.parse_args()

    if args.file is not None:
        with open(args.file, 'r') as in_file:
            print('Reading from file instead of Twitter...')
            text = in_file.read()

    else:
        # Check required argument for Twitter search
        if args.query is None:
            raise Exception('No query specified')

        if args.consumer_key is None:
            raise Exception('No consumer key specified')

        if args.access_token is None:
            raise Exception('No access token specified')

        if args.access_token_secret is None:
            raise Exception('No access token secret specified')

        # Perform twitter search
        query_terms = args.query.split(',')

        api = twitterClient.TwitterClient(args.consumer_key, args.consumer_secret,
                                          args.access_token, args.access_token_secret)

        print('Getting tweets...')
        tweets = api.get_tweets(query=' OR '.join(query_terms), count=args.count)

        print('\nFound {:d} Tweets; examples...'.format(len(tweets)))
        for tweet in tweets[:10]:
            print('Tweet: "{:s}"'.format(tweet))

        text = ' '.join(tweets)

        print('\nCleaning tweets...')
        text = re.sub('|'.join(query_terms), '', text, flags=re.IGNORECASE)
        text = re.sub('http[s]?://[\.\w/]+', '', text)
        text = re.sub('RT', '', text)
        text = re.sub('@\w+[:]?', '', text)
        text = re.sub('&amp', '', text)

        if args.write:
            with open(args.write, 'w') as out_file:
                print('Writing Twitter results to file...')
                out_file.write(text)

    print('\nCreating word cloud...')
    if args.image is not None:
        mask = np.array(Image.open(args.image))

    else:
        mask = None

    wordcloud = WordCloud(max_font_size=80, width=1920, height=1080, mask=mask).generate(text)
    wordcloud.to_file(args.output_path)
