import pytest
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from data_process import (
    load_csv,
    normalize_event_type,
    parse_event_time,
    clean_data,
)

RAW_DATA = [
    {"user_id": "123", "event_type": "gate_in", "event_time": "2023-01-31T08:18:36.000Z"},
    {"user_id": "456", "event_type": "GATE_OUT", "event_time": "2023-01-31T18:00:00.000Z"},
    {"user_id": "", "event_type": "GATE_IN", "event_time": "2023-01-31T08:00:00.000Z"},  # Invalid: missing user_id
    {"user_id": "789", "event_type": "INVALID", "event_time": "2023-01-31T09:00:00.000Z"},  # Invalid: bad event_type
    {"user_id": "123", "event_type": "GATE_IN", "event_time": "INVALID_TIMESTAMP"},  # Invalid: bad event_time
]

EXPECTED_CLEANED_DATA = [
    {"user_id": "123", "event_type": "GATE_IN", "event_time": datetime(2023, 1, 31, 8, 18, 36)},
    {"user_id": "456", "event_type": "GATE_OUT", "event_time": datetime(2023, 1, 31, 18, 0, 0)},
]


def test_normalize_event_type():
    assert normalize_event_type("gate_in") == "GATE_IN"
    assert normalize_event_type(" GATE_OUT ") == "GATE_OUT"
    assert normalize_event_type(None) is None
    assert normalize_event_type("") == ""


def test_parse_event_time():
    assert parse_event_time("2023-01-31T08:18:36.000Z") == datetime(2023, 1, 31, 8, 18, 36)
    with pytest.raises(ValueError):
        parse_event_time("INVALID_TIMESTAMP")


def test_clean_data():
    cleaned_data = clean_data(RAW_DATA)
    assert cleaned_data == EXPECTED_CLEANED_DATA


#   123,gate_in,2023-01-31T08:18:36.000Z


def test_load_csv(tmp_path):
    csv_content = """user_id,event_type,event_time
455,GATE_OUT,2024-02-31T18:00:00.000Z
123,gate_in,2023-01-31T08:18:36.000Z
"""
    
    test_file = tmp_path / "testing.csv"
    test_file.write_text(csv_content)

    data = load_csv(test_file) 
    print(data[0])

    assert len(data) == 2
    assert data[0]["user_id"] == "455"
    assert data[0]["event_type"] == "GATE_OUT"
    assert data[0]["event_time"] == "2024-02-31T18:00:00.000Z"