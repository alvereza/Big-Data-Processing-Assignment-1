# imports

import sys
from math import sqrt

current_taxi = None

total_count = 0
total_sum = 0.0
mean = 0.0
squared_sum = 0.0

for lin in sys.stdin:
    line = line.strip()
    
    if not line:
        continue
    
    fields = line.split("\t")
    
    taxi_id = fields[0]
    record_type = fields[1]
    
    # new taxi
    if current_taxi is not None and taxi_id != current_taxi:
        std_dev = sqrt(squared_sum/total_count)
        
        print('%s\t%.2f\t%.2f' % (current_taxi, mean, std_dev))
        
        total_count = 0
        total_sum = 0.0
        mean = 0.0
        squared_sum = 0.0
        
    current_taxi = taxi_id
    
    # partial summary 
    if record_type == "0":
        count = int(fields[2])
        distance_sum = float(fields[3])
        total_count += count
        total_sum += distance_sum
        
    # individual distance
    elif record_type == "1":
        if mean == 0.0:
            mean = total_sum / total_count
            
        distance = float(fields[2])
        
        squared_sum += abs(distance - mean) ** 2
        
# output final taxi
if current_taxi is not None:
    std_dev = sqrt(squared_sum / total_count)
    
    print('%s\t%.2f\t%.2f' % (current_taxi, mean, std_dev))