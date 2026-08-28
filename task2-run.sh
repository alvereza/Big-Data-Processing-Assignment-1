#!/bin/bash
set -e

INPUT="/Input/Trips.txt"
OUTPUT="/Output/task2"
TEMP="/tmp/task2_$$"
MEDOIDS="current_medoids.txt"
SUMMARY="task2_summary.txt"

STREAMING_JAR=$(find /usr/lib/hadoop-mapreduce /usr/lib/hadoop -name 'hadoop-streaming*.jar' | head -n 1)

if [ ! -f initialization.txt ]; then
    echo "initialization.txt not found"
    exit 1
fi

V=$(head -n 1 initialization.txt | tr -d '[:space:]')
tail -n +2 initialization.txt | awk 'NF >= 2 {print $1 "\t" $2}' > "$MEDOIDS"
K=$(wc -l < "$MEDOIDS" | tr -d ' ')
echo "$K" > cluster_count.txt

hadoop fs -rm -r -f "$OUTPUT" >/dev/null 2>&1 || true
hadoop fs -rm -r -f "$TEMP" >/dev/null 2>&1 || true
hadoop fs -mkdir -p "$TEMP"

LAST_OUTPUT=""

for ((i=1; i<=V; i++)); do
    ITER_OUTPUT="$TEMP/iteration_$i"

    hadoop jar "$STREAMING_JAR" \
        -D mapreduce.job.reduces=3 \
        -D stream.num.map.output.key.fields=3 \
        -D mapred.text.key.partitioner.options=-k1,1 \
        -D mapreduce.partition.keypartitioner.options=-k1,1 \
        -files task2-mapper.py,task2-combiner.py,task2-reducer.py,"$MEDOIDS" \
        -cmdenv STAGE=iterate \
        -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
        -mapper "python3 task2-mapper.py" \
        -combiner "python3 task2-combiner.py" \
        -reducer "python3 task2-reducer.py" \
        -input "$INPUT" \
        -output "$ITER_OUTPUT"

    hadoop fs -getmerge "$ITER_OUTPUT/part*" "$SUMMARY"
    sort -n -k1,1 "$SUMMARY" -o "$SUMMARY"

    echo "Iteration $i"
    awk -F '\t' '{printf "Cluster %s: medoid=(%s, %s), #points=%s, avg_dissimilarity=%.2f\n", $1, $2, $3, $4, $5}' "$SUMMARY"

    awk -F '\t' '{print $2 "\t" $3}' "$SUMMARY" > "$MEDOIDS.new"
    LAST_OUTPUT="$ITER_OUTPUT"

    if cmp -s "$MEDOIDS" "$MEDOIDS.new"; then
        mv "$MEDOIDS.new" "$MEDOIDS"
        echo "Converged after iteration $i"
        break
    fi

    mv "$MEDOIDS.new" "$MEDOIDS"
    rm -f "$SUMMARY"
done

hadoop jar "$STREAMING_JAR" \
    -D mapreduce.job.reduces=3 \
    -D stream.num.map.output.key.fields=2 \
    -D mapred.text.key.partitioner.options=-k1,1 \
    -D mapreduce.partition.keypartitioner.options=-k1,1 \
    -files task2-mapper.py,task2-reducer.py,cluster_count.txt \
    -cmdenv STAGE=final \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -mapper "python3 task2-mapper.py" \
    -reducer "python3 task2-reducer.py" \
    -input "$LAST_OUTPUT" \
    -output "$OUTPUT"

hadoop fs -rm -r -f "$TEMP" >/dev/null 2>&1 || true
rm -f "$MEDOIDS" "$SUMMARY" cluster_count.txt

echo "Final output written to $OUTPUT"
