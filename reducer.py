import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


current_key = None
total_count = 0
total_fare = Decimal("0")
max_fare = None
min_fare = None


def money(value):
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def output_result(key, count, fare_sum, maximum, minimum):
    taxi_id, category = key.split("|", 1)
    average_fare = money(fare_sum / count)
    print(
        f"{taxi_id}\t{category}\t{count}\t"
        f"{money(maximum):.2f}\t{money(minimum):.2f}\t{average_fare:.2f}"
    )


for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    fields = line.split("\t")
    if len(fields) != 5:
        continue

    key = fields[0]

    try:
        count = int(fields[1])
        fare_sum = Decimal(fields[2])
        partial_max = Decimal(fields[3])
        partial_min = Decimal(fields[4])
    except (ValueError, InvalidOperation):
        continue

    if current_key is None:
        current_key = key
        total_count = count
        total_fare = fare_sum
        max_fare = partial_max
        min_fare = partial_min
    elif key == current_key:
        total_count += count
        total_fare += fare_sum
        if partial_max > max_fare:
            max_fare = partial_max
        if partial_min < min_fare:
            min_fare = partial_min
    else:
        output_result(current_key, total_count, total_fare, max_fare, min_fare)

        current_key = key
        total_count = count
        total_fare = fare_sum
        max_fare = partial_max
        min_fare = partial_min

if current_key is not None:
    output_result(current_key, total_count, total_fare, max_fare, min_fare)