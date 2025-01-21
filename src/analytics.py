from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict


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

    #print(results)
    return results


def calculate_longest_session(entries: List[Dict[str, str]]) -> List[Dict[str, float]]:
    """
    Calculate the longest work session for each user, considering the two-hour rule.

    Args:
        entries (List[Dict[str, str]]): List of dictionaries with keys:
            - "user_id": User ID (str)
            - "event_type": Either "IN" or "OUT" (str)
            - "event_time": Event timestamp (datetime)

    Returns:
        List[Dict[str, float]]: List of dictionaries with:
            - "user_id": User ID (str)
            - "session_length": Longest session duration in hours (float)
    """
    user_sessions = defaultdict(list)

    # Group events by user and pair IN/OUT events
    for entry in entries:
        user_id = entry["user_id"]
        event_time = entry["event_time"]
        event_type = entry["event_type"]

        if event_type == "IN":
            user_sessions[user_id].append({"start": event_time})
        elif event_type == "OUT":
            if user_sessions[user_id] and "start" in user_sessions[user_id][-1] and "end" not in user_sessions[user_id][-1]:
                user_sessions[user_id][-1]["end"] = event_time

    # Process sessions to respect the two-hour rule
    longest_sessions = []
    for user_id, sessions in user_sessions.items():
        adjusted_sessions = []
        current_session = None

        for session in sessions:
            if "start" in session and "end" in session:
                if current_session and (session["start"] - current_session["end"] <= timedelta(hours=2)):
                    # Extend the current session
                    current_session["end"] = session["end"]
                else:
                    # Finalize the current session and start a new one
                    if current_session:
                        adjusted_sessions.append(current_session)
                    current_session = {"start": session["start"], "end": session["end"]}

        # Add the last session if it exists
        if current_session:
            adjusted_sessions.append(current_session)

        # Calculate the longest session for this user
        max_duration = max(
            (s["end"] - s["start"]).total_seconds() / 3600 for s in adjusted_sessions if "end" in s
        ) if adjusted_sessions else 0

        longest_sessions.append({"user_id": user_id, "session_length": max_duration})

    return sorted(longest_sessions, key=lambda x: x["session_length"], reverse=True)


