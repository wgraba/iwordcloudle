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
    parser.add_argument('consumer_key')
    parser.add_argument('consumer_secret')
    parser.add_argument('access_token')
    parser.add_argument('access_token_secret')
    parser.add_argument('query', type=str, help='Terms to query separated by commas')
    parser.add_argument('output_path', type=str, help='Path to output file')

    parser.add_argument('-c', '--count', default=5000, type=int, help='Number of tweets to get')
    parser.add_argument('-i', '--image', type=str, help='Path to image file to mask')

    args = parser.parse_args()

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

    print('\nCreating word cloud...')
    if args.image is not None:
        mask = np.array(Image.open(args.image))

    else:
        mask = None

    wordcloud = WordCloud(max_font_size=80, width=1920, height=1080, mask=mask).generate(text)
    wordcloud.to_file(args.output_path)
