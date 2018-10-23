# -*- coding: utf-8 -*-
import json
import re
import time
import uuid
from kafka import KafkaProducer
import json

import tweepy
from textblob import TextBlob

import config

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
kafka_producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'),bootstrap_servers=config.KAFKA_SERVER)


def get_trendings():
    trends = api.trends_place(config.COUNTRY_WOE_ID)
    trends = json.loads(json.dumps(trends, indent=1))
    for trend in trends[0]["trends"]:
        if trend:
            yield (u'{data}'.format(data=trend.get("name")).replace("#", ""))


def get_tweet_sentiment(tweet):
    clean_tweet = lambda x: u' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ / \ / \S+)", " ", x).split())
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'

    return 'negative'


def get_tweets(query="trump", count=100):
    dataset = api.search(q=query, count=count)
    tweets = []
    for tweet in dataset:
        sub_set_tweet = {}
        sub_set_tweet['text'] = tweet.text
        if tweet.retweet_count > 0:
            if sub_set_tweet not in tweets:
                tweets.append(sub_set_tweet)
        else:
            tweets.append(sub_set_tweet)
    return tweets


def write_solution(text):
    with open(config.PATH_TO.format(id=uuid.uuid4().hex), 'w') as out:
        out.write(text)
    return True


def crawler():

    for trending in (get_trendings()):
        dataset = get_tweets(query=trending, count=config.TWITTER_MAX_NUM_HASHTAG)
        for element in dataset:
            element["trending"] = trending
            info=kafka_producer.send(config.KAFKA_TOPIC, element)
            print ("Status data ",info)
    return True


def main():
    while True:
        try:
            print("Now we try to get the most important tweets")
            crawler()
            print("Wee need sleep a little by the next tweets")
            time.sleep(config.TIME_TO_SLEEP_BY_NEXT_TWEETS)
        except:

            print("Error , we try again on few seconds")
            time.sleep(config.TIME_TO_SLEEP_BY_NEXT_TWEETS_ERROR)


main()
