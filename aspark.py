import os
import re
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from textblob import TextBlob
import hbase


def clean_tweet(tweet):
    try:
        fx = lambda x: ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ / \ / \S+)", " ", x).split())
        return fx(tweet)
    except:
        pass
    return " NULL "


def get_tweet_sentiment(tweet):
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'


def transform(xrow):
    class Struct:
        def __init__(self, **entries):
            self.__dict__.update(entries)

        def __str__(self):
            return self.__dict__.values()

    rows = xrow.collect()
    index=0
    for key_pair in rows:
        index=index+1
        key, value = key_pair
        if value:
            try:

                value = Struct(**eval(value))
                solution = (value.trending, value.text, 1)
                treding, analized, quantity = solution
                row = {b'family:trending': bytes(treding, 'utf-8'),
                       b'family:analized': bytes(get_tweet_sentiment(analized), 'utf-8'),
                       b'family:quantity': bytes("{quantity}".format(quantity=quantity), 'utf-8')}
                hbase.write_row_hbase(row)
                print("Row Ready {index}".format(index=index))

            except Exception as e:
                print("Error  {error} in index {index}".format(index=index,error=str(e)))
    print("Waitting ")

    return xrow


def main():
    #hbase.make_table(delete_table=True)
    print ("Ready to start")
    # Create a local StreamingContext with two working thread and batch interval of 3 second
    os.environ[
        'PYSPARK_SUBMIT_ARGS'] = '--jars /home/cloudera/bigdataml/spark-streaming-kafka.jar pyspark-shell'  # note that the "pyspark-shell" part is very important!!
    sc = SparkContext("local[2]", "OdometryConsumer")
    ssc = StreamingContext(sc, 3)
    kafkaStream = KafkaUtils.createDirectStream(ssc, ['tweets'], {'metadata.broker.list': 'localhost:9092'})
    parsed = kafkaStream.map(lambda v: v)
    parsed.foreachRDD(lambda t, rdd: transform(rdd))

    print("Ready to start Async Task process ")
    ssc.start()
    ssc.awaitTermination()



main()