import csv
from datetime import datetime

def load_csv(file_path):
    data = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise Exception(f"An error occurred while loading the CSV: {e}")
    return data


def normalize_event_type(event_type):
    if event_type is None:
        return None
    return event_type.strip().upper()


def parse_event_time(event_time):
    try:
        return datetime.strptime(event_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        raise ValueError(f"Invalid timestamp format: {event_time}")


def clean_data(data):
    cleaned_data = []
    for row in data:
        try:
            user_id = row.get("user_id", "").strip()
            event_type = normalize_event_type(row.get("event_type", ""))
            event_time = parse_event_time(row.get("event_time", ""))
            
            # Validate required fields
            if not user_id or not event_type or not event_time:
                raise ValueError(f"Missing required fields in row: {row}")
            
            # Validate event type
            if event_type not in {"GATE_IN", "GATE_OUT"}:
                raise ValueError(f"Invalid event type: {event_type}")
            
            cleaned_data.append({
                "user_id": user_id,
                "event_type": event_type,
                "event_time": event_time
            })
        except Exception as e:
            print(f"Skipping invalid row: {row} | Error: {e}")
    
    return cleaned_data