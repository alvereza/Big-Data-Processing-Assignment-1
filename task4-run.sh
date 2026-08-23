hadoop fs -rm -r -f /Output/task4

hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \
    -D stream.num.map.output.key.fields=2 \
    -D mapreduce.job.reduces=3 \
    -D mapred.text.key.partitioner.options=-k1,1 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -files Task4-Mapper.py,Task4-Reducer.py \
    -mapper Task4-Mapper.py \
    -reducer Task4-Reducer.py \
    -input /Input/Trips.txt \
    -output /Output/task4
