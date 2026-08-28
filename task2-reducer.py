import os
import sys


def euclidean_distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def average_dissimilarity(candidate, cluster_points):
    if not cluster_points:
        return 0.0

    total = 0

    for point in cluster_points:
        total += euclidean_distance(candidate, point)

    return total / len(cluster_points)


def update_medoid(cluster_points):
    best_medoid = cluster_points[0]
    best_cost = average_dissimilarity(cluster_points[0], cluster_points)

    checked = {cluster_points[0]}

    for i in range(1, len(cluster_points)):
        candidate = cluster_points[i]

        if candidate in checked:
            continue

        checked.add(candidate)

        cost = average_dissimilarity(candidate, cluster_points)

        if cost < best_cost:
            best_medoid = candidate
            best_cost = cost

    return best_medoid, best_cost, len(cluster_points)


stage = os.environ.get("STAGE", "iterate")

if stage == "final":
    for line in sys.stdin:
        parts = line.strip().split("\t")

        if len(parts) == 6:
            print("\t".join(parts[2:]))

    sys.exit()


def output_cluster(cluster, points):
    if cluster is None or not points:
        return

    medoid, cost, count = update_medoid(points)

    print(
        f"{cluster}\t{medoid[0]:.3f}\t{medoid[1]:.3f}\t"
        f"{count}\t{cost:.2f}"
    )


current_cluster = None
points = []

for line in sys.stdin:
    parts = line.strip().split("\t")

    if len(parts) != 4:
        continue

    try:
        cluster = int(parts[0])
        point = (float(parts[1]), float(parts[2]))
        count = int(parts[3])
    except ValueError:
        continue

    if current_cluster is None:
        current_cluster = cluster

    if cluster != current_cluster:
        output_cluster(current_cluster, points)
        current_cluster = cluster
        points = []

    points.extend([point] * count)

output_cluster(current_cluster, points)