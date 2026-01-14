from datetime import time, datetime, timedelta

def add_minutes(t: time, minutes: int) -> time:
    dummy_date = datetime(2000, 1, 1, t.hour, t.minute)
    new_time = dummy_date + timedelta(minutes=minutes)
    return new_time.time()
