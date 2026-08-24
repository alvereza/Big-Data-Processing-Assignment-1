def euclidean_distance(p1, p2):
    '''difference of similarity throught PAM
    p1, p2 == x, y (tuples)'''
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

def assign_to_nearest_medoid(point, medoid):
    """Assignment
    point == (x, y)one trip's drop off location
    medoid == list of (x, y). where the list index is medoid_id
    matches exactly how mapper output keys work: 0, 1, 2, ..., k-1
    
    function returns (medoid_id, distance_to_medoid)
    
    mapper emits 'medoid_id, (dropoff_x, dropoff_y, trip_id)'
    using the returned medoid_id as key."""

    # We assume the first medoid is the closest one.
    best_id = 0
    best_distance = euclidean_distance(point, medoid[0])

    # Check every medoid and update it if there is a closer one
    for medoid_id in range(1, len(medoid)):
        dist = euclidean_distance(point, medoid[medoid_id])
        if dist < best_distance:
            best_id = medoid_id
            best_distance = dist

    return best_id, best_distance

def average_dissimilarity(candidate, cluster_point):
    """Average dissimilarity of 'candidate' to every point
    currently in the cluster."""

    if not cluster_point:
        return 0.0
    total = 0
    for p in cluster_point:
        total = total + euclidean_distance(candidate, p)

    return total / len(cluster_point)

def update_medoid(cluster_point):
    """Update (swap evaluation)"""

    # We assume the first point in the cluster is the best medoid
    best_medoid = cluster_point[0]
    best_cost = average_dissimilarity(cluster_point[0], cluster_point)
    checked = {cluster_point[0]}

    for i in range(1, len(cluster_point)):
        candidate = cluster_point[i]
        if candidate in checked:
            continue
        checked.add(candidate)
        cost = average_dissimilarity(candidate, cluster_point)
        if cost < best_cost:
            best_medoid = candidate
            best_cost = cost

    return best_medoid, best_cost, len(cluster_point)







