import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)

def validate_phone(phone):
    pattern = r'^\+?\d{10,15}$'  # Supports international formats
    return re.match(pattern, phone)

