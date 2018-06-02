#!/usr/bin/python3

import argparse
import re
from wordcloud import WordCloud

from twitterClient import TwitterClient

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('consumer_key')
    parser.add_argument('consumer_secret')
    parser.add_argument('access_token')
    parser.add_argument('access_token_secret')
    parser.add_argument('query', type=str, help='Term to query')
    parser.add_argument('output_path', type=str, help='Path to output file')

    parser.add_argument('-c', '--count', default=5000, type=int, help='Number of tweets to get')

    args = parser.parse_args()

    # creating object of TwitterClient Class
    api = TwitterClient(args.consumer_key, args.consumer_secret,
                        args.access_token, args.access_token_secret)

    # calling function to get tweets
    tweets = api.get_tweets(query=args.query, count=args.count)

    print('Sample Tweets...')
    for tweet in tweets[:10]:
        print('Tweet: "{:s}"'.format(tweet))

    text = ' '.join(tweets)

    text = re.sub(args.query, '', text, flags=re.IGNORECASE)
    text = re.sub('http[s]?://[\.\w/]+', '', text)
    text = re.sub('RT', '', text)
    text = re.sub('@\w+[:]?', '', text)

    wordcloud = WordCloud(max_font_size=40, margin=10, width=800, height=600, max_words=5000).generate(text)
    wordcloud.to_file(args.output_path)
