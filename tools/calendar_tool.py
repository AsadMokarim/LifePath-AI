import json
import os
from datetime import datetime, timedelta

CALENDAR_FILE = "data/calendar.json"


def load_events():
    """
    Load all calendar events from JSON.
    """
    if not os.path.exists(CALENDAR_FILE):
        return []

    with open(CALENDAR_FILE, "r") as file:
        return json.load(file)


def save_events(events):
    """
    Save calendar events to JSON.
    """
    with open(CALENDAR_FILE, "w") as file:
        json.dump(events, file, indent=4)


def is_time_slot_free(start_time, end_time):
    """
    Check if a given time slot is free.
    """
    events = load_events()

    for event in events:
        existing_start = datetime.fromisoformat(event["start"])
        existing_end = datetime.fromisoformat(event["end"])

        # Overlap check
        if start_time < existing_end and end_time > existing_start:
            return False

    return True


def schedule_event(title, start_time, duration_minutes):
    """
    Schedule an event if the time slot is free.
    """
    end_time = start_time + timedelta(minutes=duration_minutes)

    if not is_time_slot_free(start_time, end_time):
        return {
            "success": False,
            "message": "Time slot is not available"
        }

    event = {
        "title": title,
        "start": start_time.isoformat(),
        "end": end_time.isoformat()
    }

    events = load_events()
    events.append(event)
    save_events(events)

    return {
        "success": True,
        "event": event
    }


def get_events():
    """
    Return all scheduled events.
    """
    return load_events()
