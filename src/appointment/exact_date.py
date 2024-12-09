from datetime import datetime, timedelta
import re

def extract_date(user_input):
    user_input = user_input.lower().strip()
    today = datetime.now()

    # Handle "next <day>" (e.g., "next monday")
    days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    for i, day in enumerate(days_of_week):
        if f"next {day}" in user_input:
            next_day = today + timedelta((i - today.weekday() + 7) % 7 + 7)
            return next_day.strftime("%Y-%m-%d")

    # Handle "tomorrow"
    if "tomorrow" in user_input:
        tomorrow = today + timedelta(days=1)
        return tomorrow.strftime("%Y-%m-%d")

    # Handle "in X days" (e.g., "in 3 days")
    match = re.search(r"in (\d+) days", user_input)
    if match:
        days = int(match.group(1))
        future_date = today + timedelta(days=days)
        return future_date.strftime("%Y-%m-%d")

    # Handle specific dates (e.g., "2024-12-05" or "Dec 5, 2024")
    try:
        parsed_date = datetime.strptime(user_input, "%Y-%m-%d")
        return parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        pass

    try:
        parsed_date = datetime.strptime(user_input, "%b %d, %Y")  # e.g., "Dec 5, 2024"
        return parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        pass

    # Handle "today"
    if "today" in user_input:
        return today.strftime("%Y-%m-%d")

    # If no match, return None
    return None
