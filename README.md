# Big-Data-Tecnologies

# Big Data Technologies (Spark Streaming Sentiment analysis from API twitter)

## Platform cloudera Centos 6 
Be Sure that Hbase is running
sudo service hbase-regionserver start
sudo service hbase-master start

# Install kafka and run the next command
kafka-console-producer --broker-list localhost:9092 --topic tweets

# Install conda and run the next commands

1 source activate /home/cloudera/anaconda3/envs/py351

1.1 install al libraries using pip

1.2  pip install -r requirements.txt

1.3 ( If like run you need go to twitter and make your own KEYS account access and install on 
confi.py)

##  Run daemons
2 python aspark.py

3 python atwitter.py


Install on hive the table table.hive , using 

if you like run the graphis run the next command

juppyter notebook and find Graph 1.ipynb and QueryHiveToVisualized.ipynb
