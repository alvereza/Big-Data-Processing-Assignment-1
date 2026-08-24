import os
import sys
from core_pam import update_medoid

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
    print(f"{cluster}\t{medoid[0]:.3f}\t{medoid[1]:.3f}\t{count}\t{cost:.2f}")


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
