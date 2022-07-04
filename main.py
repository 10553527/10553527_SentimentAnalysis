import tweepy
from tweepy import OAuthHandler
import re
from textblob import TextBlob


class TwitterClient(object):

    def __init__(self):

        api_key = 'XXX'
        api_secret_key = 'XXX'
        access_token = 'XXX'
        access_secret_token = 'XXX'

        try:
            self.auth = OAuthHandler(api_key, api_secret_key)
            self.auth.set_access_token(access_token, access_secret_token)
            self.api = tweepy.API(self.auth)
            print('Authentication Successful!')
        except tweepy.errors.TweepyException:
            print('Authentication Failed.')

    def get_tweets(self, query, count):

        tweets = []
        parsed_tweet = {}

        try:
            fetched_tweets = self.api.search_tweets(q=query, geocode='53.350140,-6.266155,35km', lang='en', count=count)

            for tweet in fetched_tweets:

                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(self.clean_tweet(parsed_tweet['text']))
                parsed_tweet['location'] = tweet.user.location
                parsed_tweet['screen_name'] = tweet.user.screen_name

                if tweet.retweet_count > 0:
                    if parsed_tweet.copy() not in tweets:
                        tweets.append(parsed_tweet.copy())
                else:
                    tweets.append(parsed_tweet.copy())

            return tweets
        except tweepy.errors.TweepyException as e:
            print("Error : " + str(e))

    def clean_tweet(self, tweet):

        return ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\ / \ / \S+)', ' ', tweet).split())

    def get_tweet_sentiment(self, tweet):

        analysis = TextBlob(tweet)
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'


def main():

    loop = True

    while loop is True:

        try:
            search_term = input('Search Term: ')
            number_of_tweets = int(input('Number of Tweets: '))
            loop = False
        except ValueError:
            print('Error... Number of Tweets as Integer.')

    api = TwitterClient()
    tweets = api.get_tweets(search_term, number_of_tweets)

    i = 1

    print('\nTweets Returned')

    for tweet in tweets:
        print(f'{i}: {tweet["text"]} | {tweet["location"]} | @{tweet["screen_name"]}')
        i += 1

    print('\nResults of Sentiment Analysis')
    # picking positive tweets from tweets
    positive_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print(f'Positive % of Tweets: {100 * len(positive_tweets) / len(tweets)}%')

    # picking neutral tweets from tweets
    neutral_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
    # percentage of neutral tweets
    print(f'Neutral % of Tweets: {(100 * len(neutral_tweets) / len(tweets))}%')

    # picking positive negative from tweets
    negative_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print(f'Negative % of Tweets: {(100 * len(negative_tweets) / len(tweets))}%')


if __name__ == "__main__":
    main()
