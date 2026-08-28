import sys

current = None
total = 0

for line in sys.stdin:
    parts = line.strip().split("\t")
    if len(parts) != 4:
        continue

    key = tuple(parts[:3])

    try:
        count = int(parts[3])
    except ValueError:
        continue

    if current is None:
        current = key
        total = count
    elif key == current:
        total += count
    else:
        print("\t".join(current) + f"\t{total}")
        current = key
        total = count

if current is not None:
    print("\t".join(current) + f"\t{total}")
