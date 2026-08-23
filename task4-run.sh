#!/bin/bash

hadoop fs -rm -r -f /Output/task4

hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \
    -D stream.num.map.output.key.fields=2 \
    -D mapreduce.job.reduces=3 \
    -D mapred.text.key.partitioner.options=-k1,1 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -files task4-mapper.py,task4-reducer.py \
    -mapper ./task4-mapper.py \
    -reducer ./task4-reducer.py \
    -input /Input/Trips.txt \
    -output /Output/task4
