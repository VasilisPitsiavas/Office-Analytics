import pytest
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from data_process import load_csv, clean_data, write_to_csv

# Sample raw data for testing
RAW_DATA = [
    {"user_id": "123", "event_type": "gate_in", "event_time": "2023-01-31T08:18:36.000Z"},
    {"user_id": "456", "event_type": "GATE_OUT", "event_time": "2023-01-31T18:00:00.000Z"},
    {"user_id": "", "event_type": "GATE_IN", "event_time": "2023-01-31T08:00:00.000Z"},  # Invalid: missing user_id
    {"user_id": "789", "event_type": "INVALID", "event_time": "2023-01-31T09:00:00.000Z"},  # Invalid: bad event_type
    {"user_id": "123", "event_type": "GATE_IN", "event_time": "INVALID_TIMESTAMP"},  # Invalid: bad event_time
]

# Expected cleaned data
EXPECTED_CLEANED_DATA = [
    {"user_id": "123", "event_type": "GATE_IN", "event_time": datetime(2023, 1, 31, 8, 18, 36)},
    {"user_id": "456", "event_type": "GATE_OUT", "event_time": datetime(2023, 1, 31, 18, 0, 0)},
]


def test_load_csv(tmp_path):
    """
    Test the load_csv function to ensure it correctly loads data from a file.
    """
    # Create a temporary CSV file
    csv_content = """user_id,event_type,event_time
123,GATE_IN,2023-01-31T08:18:36.000Z
456,GATE_OUT,2023-01-31T18:00:00.000Z
"""
    test_file = tmp_path / "test.csv"
    test_file.write_text(csv_content)

    # Load the data
    data = load_csv(test_file)

    # Assertions
    assert len(data) == 2
    assert data[0]["user_id"] == "123"
    assert data[0]["event_type"] == "GATE_IN"
    assert data[0]["event_time"] == "2023-01-31T08:18:36.000Z"
    assert data[1]["user_id"] == "456"
    assert data[1]["event_type"] == "GATE_OUT"
    assert data[1]["event_time"] == "2023-01-31T18:00:00.000Z"


def test_clean_data():
    """
    Test the clean_data function to ensure it processes raw data correctly and skips invalid rows.
    """
    cleaned_data = clean_data(RAW_DATA)

    # Assertions
    assert len(cleaned_data) == len(EXPECTED_CLEANED_DATA)
    for cleaned, expected in zip(cleaned_data, EXPECTED_CLEANED_DATA):
        assert cleaned["user_id"] == expected["user_id"]
        assert cleaned["event_type"] == expected["event_type"]
        assert cleaned["event_time"] == expected["event_time"]


def test_write_to_csv(tmp_path):
    """
    Test the write_to_csv function to ensure it correctly writes data to a file.
    """
    # Prepare test data and file
    test_data = [
        {"user_id": "123", "event_type": "GATE_IN", "event_time": "2023-01-31T08:18:36.000Z"},
        {"user_id": "456", "event_type": "GATE_OUT", "event_time": "2023-01-31T18:00:00.000Z"},
    ]
    fieldnames = ["user_id", "event_type", "event_time"]
    output_file = tmp_path / "output.csv"

    # Write to CSV
    write_to_csv(output_file, test_data, fieldnames)

    # Read the file and validate
    with open(output_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    assert lines[0].strip() == "user_id,event_type,event_time"
    assert lines[1].strip() == "123,GATE_IN,2023-01-31T08:18:36.000Z"
    assert lines[2].strip() == "456,GATE_OUT,2023-01-31T18:00:00.000Z"
