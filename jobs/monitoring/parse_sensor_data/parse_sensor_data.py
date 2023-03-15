from connectors.purple_air.purple_air_config import PurpleAirConfig
from datetime import datetime
import requests


class PurpleAirParser:
    '''
    Gets the latest air quality data from Clean Air Nottingham
    sensors via the Purple Air API.

    API documentation can be found here: https://api.purpleair.com
    '''

    def __init__(self):
        self.config = PurpleAirConfig()

    def _sort_latest_data(self, data: dict) -> dict:
        '''Returns key sensor stats from API response.'''
        sensor = data.get('sensor', {})
        sorted_data = {
            "sensor_index": sensor.get('sensor_index'),
            "last_modified": sensor.get('last_modified'),
            "humidity": sensor.get('humidity'),
            "temperature": sensor.get('temperature'),
            "pressure": sensor.get('pressure'),
            "pm1": sensor.get('pm1'),
            "pm2.5": sensor.get('pm2.5'),
            "pm10.0": sensor.get('pm2.5'),
            "scattering_coefficient": sensor.get('scattering_coefficient')
        }
        return sorted_data

    def _load_latest_data(self, sensor_index: int) -> dict:
        headers = {"X-API-Key": self.config.API_KEY_R}
        latest_data = requests.get(f"{self.config.API_ADDRESS}/{sensor_index}", headers=headers)
        return latest_data.json()

    def _load_historical_data(self, sensor_index: int) -> dict:
        headers = {"X-API-Key": self.config.API_KEY_R}
        latest_data = requests.get(f"{self.config.API_ADDRESS}/{sensor_index}/history", headers=headers)
        return latest_data.json()

    def _parse_latest_data(self) -> list:
        return [self._sort_latest_data(self._load_latest_data(index)) for index in self.config.CAN_SENSOR_INDICES]
