import os
from typing import List, Dict

from pydantic import BaseSettings, Field

class PurpleAirConfig(BaseSettings):
    '''
    These configs define the structure of the data pulled from the Purple Air API.
    API_KEY should be stored in a local .env file.
    '''
    API_KEY: str = Field(None, env="PA_API_KEY")
    CAN_SENSOR_INDEX: List[str] = Field(["index_1", 'index_2', 'index_3'])
    AVERAGE_HUMIDITY: str = Field('id')
    AVERAGE_TEMP: str = Field('id')
    AVERAGE_PRESSURE:str = Field('id')
    ESTIMATED_PM_1: str = Field('pm1.0')
    ESTIMATED_PM_2_POINT_5: str = Field('pm2.5')
    ESTIMATED_PM_10: str = Field('pm10.0')
    BATCH_SIZE = 100  # CHECK THIS