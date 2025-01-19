from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict


from collections import defaultdict
from datetime import datetime

def calculate_time_and_days(data):
    """
    Calculate the total time, number of days spent in the office, average time per day, and rank for each user.

    Args:
        data (list): List of dictionaries containing cleaned event data.
                     Each dictionary has keys: 'user_id', 'event_type', 'event_time'.

    Returns:
        list: A list of dictionaries with keys: 
              'user_id', 'time', 'days', 'average_per_day', 'rank'.
    """
    # Dictionary to hold user stats
    user_stats = defaultdict(lambda: {'time': 0, 'days': set(), 'last_in': None})

    # Process events
    for row in data:
        user_id = row['user_id']
        event_type = row['event_type']
        event_time = row['event_time']

        if event_type == "GATE_IN":
            user_stats[user_id]['last_in'] = event_time
        elif event_type == "GATE_OUT":
            last_in = user_stats[user_id]['last_in']
            if last_in:
                session_time = (event_time - last_in).total_seconds() / 3600  # Convert to hours
                user_stats[user_id]['time'] += session_time
                user_stats[user_id]['days'].add(last_in.date())
                user_stats[user_id]['last_in'] = None  # Reset after calculating

    # Prepare results
    results = []
    for user_id, stats in user_stats.items():
        total_time = stats['time']
        days_present = len(stats['days'])
        average_per_day = total_time / days_present if days_present > 0 else 0
        results.append({
            'user_id': user_id,
            'time': round(total_time, 2),
            'days': days_present,
            'average_per_day': round(average_per_day, 2)
        })

    # Rank users by average_per_day
    results.sort(key=lambda x: x['average_per_day'], reverse=True)
    for rank, result in enumerate(results, start=1):
        result['rank'] = rank

    return results


''' 
    def calculate_longest_session(entries: List[Dict[str, str]]) -> List[Dict[str, str]]:
        user_sessions = defaultdict(list)
        
        for entry in entries:
            user_id = entry["user_id"]
            timestamp = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
            event_type = entry["event_type"]
            
            if event_type == "IN":
                user_sessions[user_id].append({"start": timestamp})
            elif event_type == "OUT" and user_sessions[user_id]:
                session = user_sessions[user_id][-1]
                if "start" in session:
                    session["end"] = timestamp
                    session["duration"] = (session["end"] - session["start"]).total_seconds() / 3600

        longest_sessions = [
            {"user_id": user_id, "session_length": max((s["duration"] for s in sessions if "duration" in s), default=0)}
            for user_id, sessions in user_sessions.items()
        ]
        return sorted(longest_sessions, key=lambda x: x["session_length"], reverse=True)
    
    '''