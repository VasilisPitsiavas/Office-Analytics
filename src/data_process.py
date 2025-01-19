import csv
from datetime import datetime

def load_csv(file_path):
    """
    Loads raw data from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        list: List of rows as dictionaries from the CSV.
    """
    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


def clean_data_for_user_analytics(data):
    """
    Cleans raw data for user analytics.

    Args:
        data (list): List of dictionaries with raw data.

    Returns:
        list: Cleaned data suitable for user analytics calculations.
    """
    cleaned_data = []
    for row in data:
        try:
            user_id = row.get("user_id", "").strip()
            event_type = row.get("event_type", "").strip().upper()
            event_time = datetime.strptime(row.get("event_time", ""), "%Y-%m-%dT%H:%M:%S.%fZ")

            # Validate required fields
            if not user_id or event_type not in {"GATE_IN", "GATE_OUT"}:
                raise ValueError("Invalid row data")

            cleaned_data.append({
                "user_id": user_id,
                "event_type": event_type,
                "event_time": event_time
            })
        except Exception as e:
            print(f"Skipping invalid row: {row} | Error: {e}")
    return cleaned_data



def clean_data_for_longest_session(data):
    """
    Cleans raw data for longest session calculations.

    Args:
        data (list): List of dictionaries with raw data.

    Returns:
        list: Cleaned data suitable for longest session calculations.
    """
    cleaned_data = []
    for row in data:
        try:
            user_id = row.get("user_id", "").strip()
            event_type = row.get("event_type", "").strip().upper()
            event_time_str = row.get("event_time", "")

            # Validate user_id and event_type
            if not user_id or event_type not in {"GATE_IN", "GATE_OUT"}:
                continue  # Skip invalid rows

            # Normalize event type
            event_type = "IN" if event_type == "GATE_IN" else "OUT"

            # Parse event_time (lenient validation)
            try:
                event_time = datetime.strptime(event_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            except ValueError:
                continue  # Skip rows with invalid timestamps

            cleaned_data.append({
                "user_id": user_id,
                "event_type": event_type,
                "event_time": event_time,
            })

        except Exception as e:
            # Log unexpected errors
            print(f"Skipping invalid row (longest_session): {row} | Error: {e}")

    return cleaned_data


def write_to_csv(file_path, data, fieldnames):
    """
    Writes processed data to a CSV file.

    Args:
        file_path (str): Path to the CSV file.
        data (list): List of dictionaries to write to the file.
        fieldnames (list): List of column headers for the CSV.
    """
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)