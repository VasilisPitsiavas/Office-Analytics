import csv
from datetime import datetime

def load_csv(file_path):
    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

'''
def normalize_event_type(event_type):
    if event_type is None:
        return None
    return event_type.strip().upper()


def parse_event_time(event_time):
    try:
        return datetime.strptime(event_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        raise ValueError(f"Invalid timestamp format: {event_time}")
'''

def clean_data(data):
    
    data = []
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append({
                'user_id': row['user_id'],
                'event_type': row['event_type'],
                'event_time': datetime.strptime(row['event_time'], "%Y-%m-%dT%H:%M:%S.%fZ")
            })
    return data