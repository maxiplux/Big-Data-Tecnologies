# -*- coding: utf-8 -*-
import os
import  os
consumer_key = 'https://developer.twitter.com/en/account/get-started'
consumer_secret = 'https://developer.twitter.com/en/account/get-started'
access_token = 'https://developer.twitter.com/en/account/get-started'
access_token_secret = 'https://developer.twitter.com/en/account/get-started'

TWITTER_MAX_NUM_HASHTAG=5
COUNTRY_WOE_ID=23424977
KAFKA_SERVER='localhost:9092'



PATH_TO = os.path.join(os.getcwd(), "solution/{id}dataset.json")
SECONDS=60
TIME_TO_SLEEP_BY_NEXT_TWEETS=SECONDS*10
TIME_TO_SLEEP_BY_NEXT_TWEETS_ERROR=SECONDS*30
KAFKA_TOPIC="tweets"


MAIN_HOST="quickstart.cloudera"
HBASE_TABLE = "infographis"
HBASE_HOST = MAIN_HOST
HDFS_HOST=MAIN_HOST