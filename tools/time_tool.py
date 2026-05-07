"""
Time tool that returns local date and time.
"""

from datetime import datetime


def get_current_time() -> str:
    """Return a user-friendly current local time string."""
    now = datetime.now()
    return now.strftime("Current time is %A, %d %B %Y, %I:%M:%S %p")
