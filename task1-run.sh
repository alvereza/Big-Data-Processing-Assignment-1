#!/bin/bash
set -e

INPUT="/Input/Trips.txt"
OUTPUT="/Output/task1"

hadoop fs -rm -r -f "$OUTPUT" >/dev/null 2>&1 || true

STREAMING_JAR=$(find /usr/lib/hadoop-mapreduce /usr/lib/hadoop -name 'hadoop-streaming*.jar' | head -n 1)

if [ -z "$STREAMING_JAR" ]; then
    echo "Could not find Hadoop Streaming jar."
    exit 1
fi

hadoop jar "$STREAMING_JAR" \
    -D mapreduce.job.reduces=3 \
    -files task1-mapper.py,task1-reducer.py \
    -mapper "python3 task1-mapper.py" \
    -reducer "python3 task1-reducer.py" \
    -input "$INPUT" \
    -output "$OUTPUT"