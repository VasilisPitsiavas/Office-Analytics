import random
import math
import csv


def euclidean_distance(point1, point2):
    """Calculate Euclidean distance between two points."""
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(point1, point2)))

def initialize_centroids(data, k):
    """Randomly initialize centroids."""
    return random.sample(data, k)

def assign_clusters(data, centroids):
    """Assign each data point to the nearest centroid."""
    clusters = [[] for _ in centroids]
    for point in data:
        distances = [euclidean_distance(point, centroid) for centroid in centroids]
        closest_centroid = distances.index(min(distances))
        clusters[closest_centroid].append(point)
    return clusters

def calculate_new_centroids(clusters):
    """Calculate new centroids as the mean of each cluster."""
    return [
        [sum(values) / len(values) for values in zip(*cluster)]
        for cluster in clusters if cluster
    ]

def k_means_clustering(data, k, max_iterations=100):
    """
    Perform k-means clustering.

    Args:
        data (list): List of data points, where each point is a list of features.
        k (int): Number of clusters.
        max_iterations (int): Maximum number of iterations.

    Returns:
        dict: Cluster assignments and centroids.
    """
    if not data:
        raise ValueError("Input data is empty. Clustering cannot be performed.")
    
    if k > len(data):
        raise ValueError("Number of clusters (k) cannot exceed the size of the dataset.")
    
    centroids = initialize_centroids(data, k)
    for _ in range(max_iterations):
        clusters = assign_clusters(data, centroids)
        new_centroids = calculate_new_centroids(clusters)
        if centroids == new_centroids:  
            break
        centroids = new_centroids
    return {"centroids": centroids, "clusters": clusters}

def employee_clustering(user_analytics, k=3):
    """
    Cluster employees based on attendance features.

    Args:
        user_analytics (list): List of dictionaries containing user analytics.
        k (int): Number of clusters.

    Returns:
        list: Cluster assignments.
    """
    # Verify input structure
    for entry in user_analytics:
        if "average_per_day" not in entry or "days" not in entry:
            raise ValueError(f"Missing keys in user analytics entry: {entry}")

    # Extract features for clustering
    data = [[entry["average_per_day"], entry["days"]] for entry in user_analytics]

    # Perform clustering
    clustering_result = k_means_clustering(data, k)

    # Map employees to clusters
    cluster_assignments = []
    for cluster_id, cluster in enumerate(clustering_result["clusters"]):
        for point in cluster:
            employee = next(
                (e for e in user_analytics if [e["average_per_day"], e["days"]] == point),
                None,
            )
            if employee:
                cluster_assignments.append({
                    "user_id": employee["user_id"],
                    "cluster": cluster_id + 1
                })

    return cluster_assignments


def save_clusters_to_csv(cluster_assignments, output_path):
    """Save cluster assignments to a CSV file."""
    with open(output_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["user_id", "cluster"])
        writer.writeheader()
        writer.writerows(cluster_assignments)


