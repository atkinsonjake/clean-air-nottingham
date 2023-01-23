from datetime import datetime

def unix_to_datetime(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp)

def unix_to_datetime_list(timestamp: int) -> list:
    date_time_obj = datetime.fromtimestamp(timestamp)
    date_str = date_time_obj.strftime("%Y-%m-%d")
    time_str = date_time_obj.strftime("%H:%M:%S")
    return [date_str, time_str]

def fahrenheit_to_celsius(fahrenheit: float) -> float:
    celsius = (fahrenheit - 32) * 5/9
    return celsius

