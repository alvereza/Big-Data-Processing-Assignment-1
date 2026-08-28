import os
import sys


def euclidean_distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def assign_to_nearest_medoid(point, medoids):
    best_id = 0
    best_distance = euclidean_distance(point, medoids[0])

    for medoid_id in range(1, len(medoids)):
        distance = euclidean_distance(point, medoids[medoid_id])

        if distance < best_distance:
            best_id = medoid_id
            best_distance = distance

    return best_id, best_distance


stage = os.environ.get("STAGE", "iterate")

if stage == "final":
    with open("cluster_count.txt") as file:
        k = int(file.read().strip())

    for line in sys.stdin:
        parts = line.strip().split("\t")

        if len(parts) != 5:
            continue

        try:
            cluster = int(parts[0])
        except ValueError:
            continue

        group = min(2, cluster * 3 // k)

        print(
            f"{group}\t{cluster:012d}\t"
            f"{parts[1]}\t{parts[2]}\t{parts[3]}\t{parts[4]}"
        )

    sys.exit()

medoids = []

with open("current_medoids.txt") as file:
    for line in file:
        parts = line.strip().split()

        if len(parts) == 2:
            medoids.append((float(parts[0]), float(parts[1])))

for line in sys.stdin:
    parts = line.strip().split(",")

    if len(parts) != 8:
        continue

    try:
        point = (float(parts[6]), float(parts[7]))
    except ValueError:
        continue

    cluster, distance = assign_to_nearest_medoid(point, medoids)

    print(f"{cluster}\t{point[0]}\t{point[1]}\t1")