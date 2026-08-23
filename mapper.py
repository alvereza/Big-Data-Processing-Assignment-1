import sys
from decimal import Decimal, InvalidOperation


def get_trip_type(distance):
    if distance >= Decimal("200"):
        return "long"
    if distance >= Decimal("100"):
        return "medium"
    return "short"


# In-mapper combining.
# key: (taxi_id, trip_type)
# value: [trip_count, fare_sum, max_fare, min_fare]
summary = {}

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    fields = line.split(",")
    if len(fields) != 8:
        continue

    try:
        taxi_id = fields[1].strip()
        fare = Decimal(fields[2].strip())
        distance = Decimal(fields[3].strip())
    except InvalidOperation:
        continue

    category = get_trip_type(distance)
    key = (taxi_id, category)

    if key not in summary:
        summary[key] = [1, fare, fare, fare]
    else:
        values = summary[key]
        values[0] += 1
        values[1] += fare
        if fare > values[2]:
            values[2] = fare
        if fare < values[3]:
            values[3] = fare

# Emit one partial aggregate per taxi/trip-type key handled by this mapper.
for (taxi_id, category), values in summary.items():
    count, fare_sum, max_fare, min_fare = values
    print(f"{taxi_id}|{category}\t{count}\t{fare_sum}\t{max_fare}\t{min_fare}")