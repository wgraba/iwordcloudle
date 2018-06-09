# iwordcloudle
Word cloud from Twitter query.

Uses the Twiter API to get the last n tweets with predetermined keywords from 
Twitter, then -

* Strip out common words like "the" and "a"
* Strip out words from Twitter query
* Create word cloud with optional image as a stencil

# Requirements
* Python 3+
* Tweepy
* Wordcloud

# Usage
Run `python3 create_cloud.py --help`.

# Resources
Uses [this tutorial](http://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/)
as a guide.

