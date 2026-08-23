# imports

import sys

# store partial count and distance sum for each taxi
taxi_stats = {}

for line in sys.stdin:
    line = line.strip()
    
    if not line:
        continue

    fields = line.split(",")
    
    taxi_id = fields[1]
    distance = float(fields[3])
    
    # individual distance
    print('%s\t%s\t%s' % (taxi_id, 1, distance))
    
    if taxi_id not in taxi_stats:
        taxi_stats[taxi_id] = [0, 0.0]
        
    taxi_stats[taxi_id][0] += 1 
    taxi_stats[taxi_id][1] += distance
    
# partial summary
for taxi_id in taxi_stats:
    count = taxi_stats[taxi_id][0]
    distance_sum = taxi_stats[taxi_id][1]
    
    print('%s\t%s\t%s\t' % (taxi_id, 0, count, distance_sum))