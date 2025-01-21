import pytest
import os
import csv
from datetime import datetime
from io import StringIO
from src.data_process import (
    load_csv,
    clean_data_for_user_analytics,
    clean_data_for_longest_session,
    write_to_csv,
)

@pytest.fixture
def sample_csv(tmp_path):
    csv_content = """user_id,event_type,event_time
123,GATE_IN,2023-01-31T08:00:00.000Z
123,GATE_OUT,2023-01-31T12:00:00.000Z
,INVALID_EVENT,2023-01-31T12:00:00.000Z
456,GATE_IN,INVALID_TIMESTAMP
"""
    file_path = tmp_path / "sample.csv"
    file_path.write_text(csv_content)
    return file_path


@pytest.fixture
def expected_cleaned_data_user_analytics():
    return [
        {"user_id": "123", "event_type": "GATE_IN", "event_time": datetime(2023, 1, 31, 8, 0)},
        {"user_id": "123", "event_type": "GATE_OUT", "event_time": datetime(2023, 1, 31, 12, 0)},
    ]


@pytest.fixture
def expected_cleaned_data_longest_session():
    return [
        {"user_id": "123", "event_type": "IN", "event_time": datetime(2023, 1, 31, 8, 0)},
        {"user_id": "123", "event_type": "OUT", "event_time": datetime(2023, 1, 31, 12, 0)},
    ]


def test_load_csv(sample_csv):
    data = load_csv(sample_csv)
    assert len(data) == 4  # All rows are read
    assert data[0]["user_id"] == "123"
    assert data[1]["event_type"] == "GATE_OUT"


def test_clean_data_for_user_analytics(sample_csv, expected_cleaned_data_user_analytics):
    raw_data = load_csv(sample_csv)
    cleaned_data = clean_data_for_user_analytics(raw_data)

    # Validate the number of cleaned rows
    assert len(cleaned_data) == len(expected_cleaned_data_user_analytics)

    # Validate the content of cleaned rows
    for i, row in enumerate(cleaned_data):
        assert row["user_id"] == expected_cleaned_data_user_analytics[i]["user_id"]
        assert row["event_type"] == expected_cleaned_data_user_analytics[i]["event_type"]
        assert row["event_time"] == expected_cleaned_data_user_analytics[i]["event_time"]


def test_clean_data_for_longest_session(sample_csv, expected_cleaned_data_longest_session):
    raw_data = load_csv(sample_csv)
    cleaned_data = clean_data_for_longest_session(raw_data)

    # Validate the number of cleaned rows
    assert len(cleaned_data) == len(expected_cleaned_data_longest_session)

    # Validate the content of cleaned rows
    for i, row in enumerate(cleaned_data):
        assert row["user_id"] == expected_cleaned_data_longest_session[i]["user_id"]
        assert row["event_type"] == expected_cleaned_data_longest_session[i]["event_type"]
        assert row["event_time"] == expected_cleaned_data_longest_session[i]["event_time"]


def test_write_to_csv(tmp_path, expected_cleaned_data_user_analytics):
    file_path = tmp_path / "output.csv"
    fieldnames = ["user_id", "event_type", "event_time"]

    write_to_csv(file_path, expected_cleaned_data_user_analytics, fieldnames)

    # Read the file back and validate the content
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    assert len(rows) == len(expected_cleaned_data_user_analytics)

    for i, row in enumerate(rows):
        assert row["user_id"] == expected_cleaned_data_user_analytics[i]["user_id"]
        assert row["event_type"] == expected_cleaned_data_user_analytics[i]["event_type"]
        assert datetime.strptime(row["event_time"], "%Y-%m-%d %H:%M:%S") == expected_cleaned_data_user_analytics[i][
            "event_time"
        ]
