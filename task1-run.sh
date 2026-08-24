#!/bin/bash
set -e

INPUT="/Input/Trips.txt"
OUTPUT="/Output/task1"

# Hadoop cannot write into an output directory that already exists.
hadoop fs -rm -r -f "$OUTPUT" >/dev/null 2>&1 || true

# Standard Hadoop Streaming jar location on AWS EMR.
STREAMING_JAR=$(find /usr/lib/hadoop-mapreduce -name 'hadoop-streaming*.jar' | head -n 1)

if [ -z "$STREAMING_JAR" ]; then
    echo "Could not find the Hadoop Streaming jar." >&2
    exit 1
fi

hadoop jar "$STREAMING_JAR" \
    -D mapreduce.job.reduces=3 \
    -files mapper.py,reducer.py \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -input "$INPUT" \
    -output "$OUTPUT"