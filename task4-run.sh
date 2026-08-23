#!/bin/bash

hadoop fs -rm -r -f /Output/task4

hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \
    -D stream.num.map.output.key.fields=2 \
    -D mapreduce.job.reduces=3 \
    -D mapred.text.key.partitioner.options=-k1,1 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -file ./task4-mapper.py \
    -mapper ./task4-mapper.py \
    -file ./task4-reducer.py \
    -reducer ./task4-reducer.py \
    -input /Input/Trips.txt \
    -output /Output/task4
