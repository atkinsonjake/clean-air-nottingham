import os
from typing import List, Dict

from pydantic import BaseSettings, Field

class PurpleAirConfig(BaseSettings):
    '''
    These configs define the structure of the data pulled from the Purple Air API.
    API_KEY should be stored in a local .env file.
    '''
    API_ADDRESS: str = Field("https://api.purpleair.com/v1/sensors")
    API_KEY_R: str = Field(None, env="PA_API_KEY_R")
    API_KEY_W: str = Field(None, env="PA_API_KEY_W")
    LATITUDE: str = Field('latitude')
    LONGITUDE: str = Field('longitude')
    ALTITUDE: str = Field('altitude')
    CAN_SENSOR_GROUP: int = Field(1711) # Created 30 Apr 2023
    CAN_SENSOR_INDICES: List[str] = Field([145006, 182825, 179027, 144918, 144988, 182587]) # Updated June 2023
    AVERAGE_HUMIDITY: str = Field('temperature')
    AVERAGE_TEMPERATURE: str = Field('humidity')
    AVERAGE_PRESSURE: str = Field('pressure')
    ESTIMATED_PM_1: str = Field('pm1.0_atm')
    ESTIMATED_PM_2_POINT_5: str = Field('pm2.5_atm')
    ESTIMATED_PM_10: str = Field('pm10.0_atm')
    AVERAGE_VOC: str = Field('voc')
    OZONE: str = Field('ozone1')
    SCATTERING_COEFF: str = Field('scattering_coefficient')
    BATCH_SIZE = 100  # CHECK THIS
    
    CAN_COLOURS = ["#3d5a80", "#98c1d9", "#ee6c4d", "#e0fbfc"]

    # Multi-channel readings
    ESTIMATED_PM_1_A: str = Field('pm1.0_atm_a')
    ESTIMATED_PM_1_B: str = Field('pm1.0_atm_b')
    ESTIMATED_PM_2_POINT_5_A: str = Field('pm2.5_atm_a')
    ESTIMATED_PM_2_POINT_5_B: str = Field('pm2.5_atm_b')
    ESTIMATED_PM_10_A: str = Field('pm10.0_atm_a')
    ESTIMATED_PM_10_B: str = Field('pm10.0_atm_b')
    
