import pytest
from datetime import datetime
import sys
import os
from collections import defaultdict
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from analytics import calculate_time_and_days, calculate_longest_session


def test_calculate_time_and_days():
    data = [
        {"user_id": "123", "event_type": "GATE_IN", "event_time": datetime(2023, 1, 1, 8, 0)},
        {"user_id": "123", "event_type": "GATE_OUT", "event_time": datetime(2023, 1, 1, 12, 0)},
        {"user_id": "123", "event_type": "GATE_IN", "event_time": datetime(2023, 1, 2, 8, 0)},
        {"user_id": "123", "event_type": "GATE_OUT", "event_time": datetime(2023, 1, 2, 12, 0)},
        {"user_id": "456", "event_type": "GATE_IN", "event_time": datetime(2023, 1, 1, 9, 0)},
        {"user_id": "456", "event_type": "GATE_OUT", "event_time": datetime(2023, 1, 1, 17, 0)},
    ]

    expected = [
        {"user_id": "123", "time": 8.0, "days": 2, "average_per_day": 4.0, "rank": 2},
        {"user_id": "456", "time": 8.0, "days": 1, "average_per_day": 8.0, "rank": 1},
    ]

    result = calculate_time_and_days(data)
    assert result == expected


def test_calculate_longest_session():
    # Test data
    data = [
        {"user_id": "123", "event_type": "IN", "event_time": datetime(2023, 1, 1, 8, 0)},
        {"user_id": "123", "event_type": "OUT", "event_time": datetime(2023, 1, 1, 12, 0)},
        {"user_id": "123", "event_type": "IN", "event_time": datetime(2023, 1, 1, 13, 0)},
        {"user_id": "123", "event_type": "OUT", "event_time": datetime(2023, 1, 1, 18, 0)},
        {"user_id": "456", "event_type": "IN", "event_time": datetime(2023, 1, 1, 9, 0)},
        {"user_id": "456", "event_type": "OUT", "event_time": datetime(2023, 1, 1, 17, 0)},
    ]

    # Expected output
    expected = [
        {"user_id": "123", "session_length": 10.0},  # 8:00-12:00 + 13:00-18:00
        {"user_id": "456", "session_length": 8.0},   # 9:00-17:00
    ]

    # Run the function
    result = calculate_longest_session(data)

    # Assertions
    assert result == expected

def test_no_events():
    data = []
    assert calculate_time_and_days(data) == []
    assert calculate_longest_session(data) == []

def test_missing_out_event():
    data = [
        {"user_id": "123", "event_type": "IN", "event_time": datetime(2023, 1, 1, 8, 0)},
    ]
    assert calculate_time_and_days(data) == [{"user_id": "123", "time": 0.0, "days": 0, "average_per_day": 0.0, "rank": 1}]
    assert calculate_longest_session(data) == [{"user_id": "123", "session_length": 0.0}]

def test_consecutive_in_out_events():
    data = [
        {"user_id": "123", "event_type": "IN", "event_time": datetime(2023, 1, 1, 8, 0)},
        {"user_id": "123", "event_type": "IN", "event_time": datetime(2023, 1, 1, 9, 0)},  # Consecutive IN
        {"user_id": "123", "event_type": "OUT", "event_time": datetime(2023, 1, 1, 12, 0)},
    ]
    expected_time_days = [
        {"user_id": "123", "time": 3.0, "days": 1, "average_per_day": 3.0, "rank": 1}
    ]
    expected_longest_session = [{"user_id": "123", "session_length": 3.0}]

    assert calculate_time_and_days(data) == expected_time_days
    assert calculate_longest_session(data) == expected_longest_session
