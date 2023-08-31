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

def calibrate_reading(s1: float, s2: float, s3: float, pm25: float, rh: float, i: float) -> float:
    """
    Calibrates a PM2.5 reading.

    Args:
        s1: the first coefficient in the calibration equation.
        s2: the second coefficient in the calibration equation.
        s3: the third coefficient in the calibration equation.
        pm25: the PM2.5 reading in raw units.
        rh: the relative humidity in percent.
        i: an intercept.

    Returns:
        The calibrated PM2.5 reading in ug/m^3.
    """

    adjusted_rh = rh**2 / (1 - rh)
    return s1 * pm25 + s2 * adjusted_rh * pm25 + s3 * adjusted_rh + i