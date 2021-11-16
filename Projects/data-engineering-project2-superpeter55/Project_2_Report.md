# Project 2: Report

## Executive Summary

In this report I aim to answer the questions outlined below. Brief answers to these questions are provided in the executive summary and more detailed explanations of how I got these values are outlined in the detailed pipeline breakdown.

1. How many assessments are in the dataset?
2. What is the name of my Kafka topic? How did I come up with that name?
3. How many people took Learning Git?
4. What is the least common course taken? And the most common?
5. What time period is the dataset taken from? What is the earliest and latest start time?
6. How many unique assessments (i.e. unique courses) are in the dataset?
7. What issues are there within the data?

After building a pipeline and performing spark sql queries on the selected data, I concluded that there are 3280 entries or assessments in this data. There are 394 instances of people taking the course Learning Git. Learning Git was the most common course taken and there was a four way tie for the least common course taken. There were 103 different courses available in this dataset. This data was taken from November 21, 2017 to January 28, 2018. I decided to name my kafka topic "assessments" because it is a good descriptor of the data that is being pushed to the topic. There was one challenge when working with this data that I was unable to overcome which was unpacking the sequences structure which was nested in json.

## Repository Description

* Project_2_Report.md - This is the final report
* README.md - The readme file containing project specifications
* assessment-attempts-20180128-121051-nested.json - Raw json file we use in this project as a datasource
* docker-compose.yml - Docker Compose file which allows us to spin up docker containers
* python_history.txt - History from my pyspark session
* superpeter55-history.txt - History from my terminal

## Detailed Pipeline Breakdown

### Console

The first step of this pipeline is changing to the working directory using the cd command and also adding our docker-compose.yml file to the working directory. The docker-compose file is copied using the cp command from the week 8 material. The period "." at the end of the cp command tells the command to copy the file specified and paste in in my current working directory. I chose week 8 for my docker compose file because it allows us to spin up all the containers required for this project.

```console
cd ~/w205/project-2-superpeter55
cp ~/w205/course-content//08-Querying-Data/docker-compose.yml .
```

The next step is to get the raw json file in our working directory. This will be done using the curl command on the .json file specified in the project description. The curl command is capable of pulling data from an https server which we do in this scenario. The curl request is pulling data from the URL shown at the end of the command. There are 2 options specified in this request, -L and -o. The -L option is a safety precaution meaning if the request reports that the page has moved to a different location, it forces the curl request to try again at that specified location. The -o option saves the curl request in our current directory with the filename specified.

```console
curl -L -o assessment-attempts-20180128-121051-nested.json https://goo.gl/ME6hjp``
```

The next step is to spin up the docker compose cluster and ensure that it spun up properly. The first line spins up our cluster of containers and the -d option detaches the containers. This means that the containers are run in the background and we are able to continue to use our console. The next commands brings up the container logs for kafka as it is spinning up and will show an error if something did not spin up properly. The -f option follows the logs as it is spinning up. Finally, we check to make sure all the containers are up using docker-compose ps. This command lists all the containers spun up and some basic information on them. Since all the containers say they are in the state "up", we will proceed.

```console
docker-compose up -d
docker-compose logs -f kafka
docker-compose ps
```

```
               Name                           Command            State                                         Ports                                       
-----------------------------------------------------------------------------------------------------------------------------------------------------------
project-2-superpeter55_cloudera_1    cdh_startup_script.sh       Up      11000/tcp, 11443/tcp, 19888/tcp, 50070/tcp, 8020/tcp, 8088/tcp, 8888/tcp, 9090/tcp
project-2-superpeter55_kafka_1       /etc/confluent/docker/run   Up      29092/tcp, 9092/tcp                                                               
project-2-superpeter55_mids_1        /bin/bash                   Up      8888/tcp                                                                          
project-2-superpeter55_spark_1       docker-entrypoint.sh bash   Up                                                                                        
project-2-superpeter55_zookeeper_1   /etc/confluent/docker/run   Up      2181/tcp, 2888/tcp, 32181/tcp, 3888/tcp 
```

Before writing anything to hdfs we would like to check what is in currently in hadoop to make sure it is empty. This is done using the docker-compose exec command on our hadoop container. The -ls /tmp/ is listing in our hadoop container what is currently in the tmp directory. When we run this command the directory is empty except for hadoop-yarn and hive which exist when we first spin up the container.

```console
docker-compose exec cloudera hadoop fs -ls /tmp/
```

```Found 2 items
drwxrwxrwt   - mapred mapred              0 2018-02-06 18:27 /tmp/hadoop-yarn
drwx-wx-wx   - root   supergroup          0 2021-10-27 01:10 /tmp/hive
```

The next step is to create our kafka topic. We use the exec command on kafka to excecute a single kafka command. In this case we run the kafka-topics command with the --create option to create a topic. The --topic option is used to name the topic "assessments". I chose to name this topic assessments because assessments is a good description of the data that is used in this project. I also only chose to make one topic because there is only one datasource. We use the --partitions option to specify that we only need one partition. The --if-not-exists option is to prevent making two topics with the same name from being created. The --zookeeper option is specifying which port we would like to connect our topic to.

```console
docker-compose exec kafka   kafka-topics     --create     --topic assessments     --partitions 1     --replication-factor 1     --if-not-exists     --zookeeper zookeeper:32181
```

Now that our kafka topic is ready, we get to push our json data to that topic and start up pyspark. We use the exec command to run a bash command from the mids container. The first -c allows us to specify the bash command as a string which we have done. Inside the quotes, we use cat to get the contents of the specified file (our json file) and pipe this with the jq command. The jq command takes the output of our cat function and returns all elements as an array as specified by the '.[]'. The -c option for jq specifies a compact output which puts each json object on a single line. The output of our jq command is then piped with the kafkacat function. Kafkacat is used to produce and consume kafka messages and the example below shows we use -P which means we are producing a message. We then use the -b option which specifies the broker we would like to use and then we use the -t option to specify that we would like to produce our message to the assessments topic. We then use docker-compose exec to start our interactive pyspark instance.

```console
docker-compose exec mids   bash -c "cat /w205/project-2-superpeter55/assessment-attempts-20180128-121051-nested.json \
    | jq '.[]' -c \
    | kafkacat -P -b kafka:29092 -t assessments"
docker-compose exec spark pyspark
```

### PySpark

In pyspark, we must read in our kafka message. We use the spark.read to read in data and .format to specify that we are reading in data from kafka. There are four options specified. The first option tells which bootstrap server from kafka to read from. The second option tells us that we are reading from the assessments topic. The third and fourth options tell us the starting and ending offsets. By specifying earliest and latest it means we are going to read the entire kafka message. Finally, the load function loads the results into the raw_assessments dataframe.

```python
raw_assessments = spark \
  .read \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka:29092") \
  .option("subscribe","assessments") \
  .option("startingOffsets", "earliest") \
  .option("endingOffsets", "latest") \
  .load()
```

We will now use the cache() function on our raw_assessments dataframe to supress any warnings we might get in the future. We also convert the raw_assessments dataframe to the assessments dataframe by casting the message as a string. The final command shows the assessments dataframe. The problem with this is that this is currently a dataframe with one column where each row represents a json string. We will need to unwrap the string into multiple columns next.

```python
raw_assessments.cache()
assessments = raw_assessments.select(raw_assessments.value.cast('string')
assessments.show()
```

```
+--------------------+
|               value|
+--------------------+
|{"keen_timestamp"...|
|{"keen_timestamp"...|
|{"keen_timestamp"...|
|{"keen_timestamp"...|
|{"keen_timestamp"...|
|{"keen_timestamp"...|
|{"keen_timestamp"...|
|{"keen_timestamp"...|
|{"keen_timestamp"...|
|{"keen_timestamp"...|
|{"keen_timestamp"...|
|{"keen_timestamp"...|
|{"keen_timestamp"...|
|{"keen_timestamp"...|
|{"keen_timestamp"...|
|{"keen_timestamp"...|
|{"keen_timestamp"...|
|{"keen_timestamp"...|
|{"keen_timestamp"...|
|{"keen_timestamp"...|
+--------------------+
only showing top 20 rows
```

To do this, we will use the json python package. We first import the json package and then we use a lambda function to transform each row which is a single json string into a row with multiple columns that are the contents of that json string. The .toDF() function is then used to save the results to the extracted_assessments dataframe. The final command shows our new dataframe and we can see that it is in a structure that is now queryable except for the sequences column which still has more nested json.

```python
import json
extracted_assessments = assessments.rdd.map(lambda x: json.loads(x.value)).toDF()
extracted_assessments.show()
```

```
+--------------------+-------------+--------------------+------------------+--------------------+------------------+------------+--------------------+--------------------+--------------------+
|        base_exam_id|certification|           exam_name|   keen_created_at|             keen_id|    keen_timestamp|max_attempts|           sequences|          started_at|        user_exam_id|
+--------------------+-------------+--------------------+------------------+--------------------+------------------+------------+--------------------+--------------------+--------------------+
|37f0a30a-7464-11e...|        false|Normal Forms and ...| 1516717442.735266|5a6745820eb8ab000...| 1516717442.735266|         1.0|Map(questions -> ...|2018-01-23T14:23:...|6d4089e4-bde5-4a2...|
|37f0a30a-7464-11e...|        false|Normal Forms and ...| 1516717377.639827|5a674541ab6b0a000...| 1516717377.639827|         1.0|Map(questions -> ...|2018-01-23T14:21:...|2fec1534-b41f-441...|
|4beeac16-bb83-4d5...|        false|The Principles of...| 1516738973.653394|5a67999d3ed3e3000...| 1516738973.653394|         1.0|Map(questions -> ...|2018-01-23T20:22:...|8edbc8a8-4d26-429...|
|4beeac16-bb83-4d5...|        false|The Principles of...|1516738921.1137421|5a6799694fc7c7000...|1516738921.1137421|         1.0|Map(questions -> ...|2018-01-23T20:21:...|c0ee680e-8892-4e6...|
|6442707e-7488-11e...|        false|Introduction to B...| 1516737000.212122|5a6791e824fccd000...| 1516737000.212122|         1.0|Map(questions -> ...|2018-01-23T19:48:...|e4525b79-7904-405...|
|8b4488de-43a5-4ff...|        false|        Learning Git| 1516740790.309757|5a67a0b6852c2a000...| 1516740790.309757|         1.0|Map(questions -> ...|2018-01-23T20:51:...|3186dafa-7acf-47e...|
|e1f07fac-5566-4fd...|        false|Git Fundamentals ...|1516746279.3801291|5a67b627cc80e6000...|1516746279.3801291|         1.0|Map(questions -> ...|2018-01-23T22:24:...|48d88326-36a3-4cb...|
|7e2e0b53-a7ba-458...|        false|Introduction to P...| 1516743820.305464|5a67ac8cb0a5f4000...| 1516743820.305464|         1.0|Map(questions -> ...|2018-01-23T21:43:...|bb152d6b-cada-41e...|
|1a233da8-e6e5-48a...|        false|Intermediate Pyth...|  1516743098.56811|5a67a9ba060087000...|  1516743098.56811|         1.0|Map(questions -> ...|2018-01-23T21:31:...|70073d6f-ced5-4d0...|
|7e2e0b53-a7ba-458...|        false|Introduction to P...| 1516743764.813107|5a67ac54411aed000...| 1516743764.813107|         1.0|Map(questions -> ...|2018-01-23T21:42:...|9eb6d4d6-fd1f-4f3...|
|4cdf9b5f-fdb7-4a4...|        false|A Practical Intro...|1516744091.3127241|5a67ad9b2ff312000...|1516744091.3127241|         1.0|Map(questions -> ...|2018-01-23T21:45:...|093f1337-7090-457...|
|e1f07fac-5566-4fd...|        false|Git Fundamentals ...|1516746256.5878439|5a67b610baff90000...|1516746256.5878439|         1.0|Map(questions -> ...|2018-01-23T22:24:...|0f576abb-958a-4c0...|
|87b4b3f9-3a86-435...|        false|Introduction to M...|  1516743832.99235|5a67ac9837b82b000...|  1516743832.99235|         1.0|Map(questions -> ...|2018-01-23T21:40:...|0c18f48c-0018-450...|
|a7a65ec6-77dc-480...|        false|   Python Epiphanies|1516743332.7596769|5a67aaa4f21cc2000...|1516743332.7596769|         1.0|Map(questions -> ...|2018-01-23T21:34:...|b38ac9d8-eef9-495...|
|7e2e0b53-a7ba-458...|        false|Introduction to P...| 1516743750.097306|5a67ac46f7bce8000...| 1516743750.097306|         1.0|Map(questions -> ...|2018-01-23T21:41:...|bbc9865f-88ef-42e...|
|e5602ceb-6f0d-11e...|        false|Python Data Struc...|1516744410.4791961|5a67aedaf34e85000...|1516744410.4791961|         1.0|Map(questions -> ...|2018-01-23T21:51:...|8a0266df-02d7-44e...|
|e5602ceb-6f0d-11e...|        false|Python Data Struc...|1516744446.3999851|5a67aefef5e149000...|1516744446.3999851|         1.0|Map(questions -> ...|2018-01-23T21:53:...|95d4edb1-533f-445...|
|f432e2e3-7e3a-4a7...|        false|Working with Algo...| 1516744255.840405|5a67ae3f0c5f48000...| 1516744255.840405|         1.0|Map(questions -> ...|2018-01-23T21:50:...|f9bc1eff-7e54-42a...|
|76a682de-6f0c-11e...|        false|Learning iPython ...| 1516744023.652257|5a67ad579d5057000...| 1516744023.652257|         1.0|Map(questions -> ...|2018-01-23T21:46:...|dc4b35a7-399a-4bd...|
|a7a65ec6-77dc-480...|        false|   Python Epiphanies|1516743398.6451161|5a67aae6753fd6000...|1516743398.6451161|         1.0|Map(questions -> ...|2018-01-23T21:35:...|d0f8249a-597e-4e1...|
+--------------------+-------------+--------------------+------------------+--------------------+------------------+------------+--------------------+--------------------+--------------------+
only showing top 20 rows
```

Now we have a dataframe that is set up in a proper format for us to be able to perform queries on and we are ready to push this data to HDFS. We do this using the write.parquet() function to write a parquet file to HDFS. We specify that we would like to safe this in the tmp directory with the name extracted_assessments. 

```python
extracted_assessments.write.parquet("/tmp/extracted_assessments")
```

We now have queryable data in HDFS which was the first goal of this project. The second goal was to answer the business questions identified in the executive summary so the rest of the report will focus on using spark sql to answer these question. First, we must create a temporary table for us to query from. This is done using the registerTempTable function and we name our table "assessments".

```python
extracted_assessments.registerTempTable('assessments')
```

Our first question we would like to answer is how many assessments are in the data. To do this we use the spark.sql command which allows us to perform sql commands on our temporary table. To answer our question, we select the count of an arbitrary column in the dataset. In this case I chose "base_exam_id". The .show() function is used to show our results. As you can see, there are 3280 assessments in this dataset.

```python
spark.sql("select count(base_exam_id) as number_assessments from assessments").show()
```

```
+------------------+
|number_assessments|
+------------------+
|              3280|
+------------------+
```

Next, we would like to know how many people took the course learning git. Once again we will use the spark.sql().show() framework to compose a query. In this case, we still are selecting the count of "base_exam_id" but only when the "exam_name" column is equal to "Learning Git". This is done using the command below. As you can see, there are 394 instances of people taking Learning Git in this dataset.

```python
spark.sql("select count(base_exam_id) as count_learning_git from assessments where exam_name = 'Learning Git'").show()
```

```
+------------------+
|count_learning_git|
+------------------+
|               394|
+------------------+
```

Next we would like to know the most common and least common courses taken. To do this, we will group by the "exam_name" and once again count the the number of instances for each exam. We will then order the results by the number of instances of each exam. We will go in descending order to find the course taken the most and ascending order for the course taken the least. For the show function, the first argument specifies how many rows to display. For the least taken course there was a four way tie so we need to display all four rows. The second argument "False" argument tells the show function to not cut off any of the columns when the text gets too long and instead will make the columns wider.

```python
# Most taken course
spark.sql("select distinct exam_name as course, count(exam_name) as times_taken from assessments \
group by exam_name order by times_taken desc").show(1,False)
# Least taken course
spark.sql("select distinct exam_name as course, count(exam_name) as times_taken from assessments \
group by exam_name order by times_taken").show(4,False)
```

```
+------------+-----------+                                                      
|course      |times_taken|
+------------+-----------+
|Learning Git|394        |
+------------+-----------+

+-------------------------------------------------+-----------+                 
|course                                           |times_taken|
+-------------------------------------------------+-----------+
|Native Web Apps for Android                      |1          |
|Operating Red Hat Enterprise Linux Servers       |1          |
|Learning to Visualize Data with D3.js            |1          |
|Nulls, Three-valued Logic and Missing Information|1          |
+-------------------------------------------------+-----------+
```

The next question I would like to know the answer to is what the earliest and latest start time is for an exam. This tells us the time period which this data is collected. To do that we select the both the minimum and maximum values in the "started_at" column. Running this query shows that the data spans from November 21, 2017 to January 28, 2018. 

```python
spark.sql("select min(started_at) as earliest_test,max(started_at) as latest_test from assessments").show(10,False)
```

```
+------------------------+------------------------+
|earliest_test           |latest_test             |
+------------------------+------------------------+
|2017-11-21T00:42:08.990Z|2018-01-28T19:17:53.796Z|
+------------------------+------------------------+
```

Finally I'd like to know how many unique assessments there are in this dataset. This tells us the total number of courses someone has to choose from (assuming every course was taken at least once during this time period). To do this I once again used spark.sql.show() and selected the count of distinct exam names in the dataset. As you can see, there are 103 unique assessments in this dataset.

```python
spark.sql("select count(distinct exam_name) as unique_assessments from assessments").show()
```

```
+------------------+                                                            
|unique_assessments|
+------------------+
|               103|
+------------------+
```

Now that we have answered all our questions and have a queryable parquet file in HDFS, we can safely exit our pyspark session using the exit() command. Back in the terminal, we can check and make sure our parquet file is in hdfs. This is done using the exact same command we used earlier to ensure nothing unusual is in HDFS. The explanation of this command is shown above when it was first run. This time, we have an extra file in our directory named extracted_assessments which means we successfully pushed our data to HDFS. 

### Back to Console

```console
docker-compose exec cloudera hadoop fs -ls /tmp/
```

```
Found 3 items
drwxr-xr-x   - root   supergroup          0 2021-10-24 23:23 /tmp/extracted_assessments
drwxrwxrwt   - mapred mapred              0 2018-02-06 18:27 /tmp/hadoop-yarn
drwx-wx-wx   - root   supergroup          0 2021-10-24 23:19 /tmp/hive
```

The final step is to write our history files for the terminal and pyspark instance to txt files. This is done below using the exec command to prompt spark to get the python history, and then using the standard "history >" to get the terminal history. One thing to keep in mind is that I deleted the first 151 lines of my terminal history because I had used the same terminal for things that were not this project before using the same terminal to work on this project. For that reason I manually deleted entries before this project after creating the history file. In addition, I added one line to the python history manually as I forgot to run the command "assessments.show()" and I wanted to include this output in my report.

```console
docker-compose exec spark cat /root/.python_history > python_history.txt
history > superpeter55-history.txt
```

One final thing I would like to address is that there was some difficulty examining the data. The "sequences" column of the json file was more wrapped json and I was having trouble extracting it. This was not required for this project but if I had an easier time unwrapping the data, I would have liked to answer the following questions. Which exams are the hardest/easiest and which exams are the longest/shortest.
