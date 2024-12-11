from datetime import datetime, timedelta
import re

def extract_date(user_input):
    """
    Extracts and validates the date from user input. 
    Prevents booking for past dates.
    """
    user_input = re.sub(r"\s+", " ", user_input.lower().strip())  # Normalize spaces in the input
    today = datetime.now()

    # Handle "next <day>" (e.g., "next monday")
    days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    for i, day in enumerate(days_of_week):
        if f"next {day}" in user_input:
            next_day = today + timedelta((i - today.weekday() + 7) % 7 + 7)
            if next_day.date() < today.date():
                return "Cannot book a date in the past."
            return next_day.strftime("%Y-%m-%d")

    # Handle "tomorrow"
    if "tomorrow" in user_input:
        tomorrow = today + timedelta(days=1)
        return tomorrow.strftime("%Y-%m-%d")

    # Handle "yesterday"
    if "yesterday" in user_input:
        yesterday = today - timedelta(days=1)
        return "Cannot book a date in the past."

    # Handle "in X days" (e.g., "in 3 days")
    match = re.search(r"in (\d+) days", user_input)
    if match:
        days = int(match.group(1))
        future_date = today + timedelta(days=days)
        return future_date.strftime("%Y-%m-%d")

    # Handle specific dates (e.g., "2024-12-05" or "Dec 5, 2024")
    try:
        user_input = re.sub(r",\s*", ", ", user_input)  # Normalize comma spacing
        user_input = re.sub(r"(\D)(\d)", r"\1 \2", user_input)  # Add space between month and day if missing
        parsed_date = datetime.strptime(user_input, "%Y-%m-%d")
        if parsed_date.date() < today.date():
            return "Cannot book a date in the past."
        return parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        pass

    try:
        parsed_date = datetime.strptime(user_input, "%b %d, %Y")  # e.g., "Dec 5, 2024"
        if parsed_date.date() < today.date():
            return "Cannot book a date in the past."
        return parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        pass

    # Handle "today"
    if "today" in user_input:
        return today.strftime("%Y-%m-%d")

    # If no match, return None
    return None

# # Example usage
# user_input = "dec 5, 2024 " # Replace with user-provided input
# date = extract_date(user_input)
# print(date)
