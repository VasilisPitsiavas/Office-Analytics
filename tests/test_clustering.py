import pytest
from src.clustering import employee_clustering

def test_employee_clustering_valid_input():
    user_analytics = [
        {"user_id": "123", "average_per_day": 6.5, "days": 15},
        {"user_id": "456", "average_per_day": 5.8, "days": 20},
        {"user_id": "789", "average_per_day": 7.2, "days": 10},
        {"user_id": "101", "average_per_day": 6.0, "days": 18},
    ]
    result = employee_clustering(user_analytics, k=2)
    assert len(result) == len(user_analytics)
    assert all("user_id" in item and "cluster" in item for item in result)
    assert all(1 <= item["cluster"] <= 2 for item in result)

def test_employee_clustering_missing_keys():
    user_analytics = [
        {"user_id": "123", "average_per_day": 6.5},  # Missing 'days'
    ]
    with pytest.raises(ValueError, match="Missing keys in user analytics entry"):
        employee_clustering(user_analytics, k=2)

def test_employee_clustering_empty_input():
    user_analytics = []
    with pytest.raises(ValueError, match="Input data is empty"):
        employee_clustering(user_analytics, k=3)
