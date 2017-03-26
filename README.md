# iwordcloudle
Immigration word cloud from Twitter with sentiment analysis.

Uses the Twiiter API to get the last n tweets with predetermined keywords from 
Twitter, then -

* Perform sentiment analysis
* Strip out common words like "the" and "a"
* Create word cloud

# Requirements
* Python 3+
* Tweepy
* Textblob

# Usage
Run `python3 create_cloud.py --help`

# Resources
Uses [this tutorial](http://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/)
as a guide.

