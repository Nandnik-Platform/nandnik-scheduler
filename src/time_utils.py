from datetime import datetime
from zoneinfo import ZoneInfo  # Requires Python 3.9+

def get_current_time(tz: str = "Asia/Kolkata") -> tuple[str, str]:
    now = datetime.now(ZoneInfo(tz))
    current_time = now.strftime("%H%M")
    current_day = now.strftime("%A")  # e.g., 'Monday', 'Tuesday'
    return current_time, current_day


def format_time_ist(time_str: str) -> str:
    """Convert HHMM string to 12-hour format with AM/PM and IST"""
    dt = datetime.strptime(time_str, "%H%M")
    dt_ist = dt.replace(tzinfo=ZoneInfo("Asia/Kolkata"))
    return dt_ist.strftime("%I:%M %p IST")