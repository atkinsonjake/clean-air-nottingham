from datetime import datetime
import requests
from typing import List, Union
from connectors.purple_air.purple_air_config import PurpleAirConfig

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


    def _load_historical_data(self, sensor_index: int, 
                              start_timestamp: datetime = None, 
                              end_timestamp:datetime = None, 
                              measurement: Union[str, List[str]] = None,
                              average_time: int = 10) -> dict:
        
        '''
        Parameters:
            - sensor_index (int): the PurpleAir index allocated to a sensor
            - start_timestamp (unix timestamp): the start time of returned readings
            - end_timestamp (unix timestamp): the end time of returned readings
            - measurement (str or list): sensor data to include in the response (e.g. pm2.5_alt). 
            - average_time (int): the time between readings
        
        Returns:
            - (dict) values
        '''
        headers = {"X-API-Key": self.config.API_KEY_R}
        measurement_str = "%2C".join(measurement) if isinstance(measurement, list) else measurement

        if start_timestamp and end_timestamp and measurement and average_time:
            url = f"{self.config.API_ADDRESS}/{sensor_index}/history?start_timestamp={start_timestamp}&end_timestamp={end_timestamp}&average={average_time}&fields={measurement_str}"
        else:
            url = f"{self.config.API_ADDRESS}/{sensor_index}/history?average={average_time}&fields={measurement_str}"
        
        historical_data = requests.get(url, headers=headers)
        return historical_data.json()


    def _parse_latest_data(self) -> list:
        return [self._sort_latest_data(self._load_latest_data(index)) for index in self.config.CAN_SENSOR_INDICES]


    def parse_api_response(self, response):
        """
        Parses the response from PurpleAir.

        Args:
            response (dict): The response data from the PurpleAir API, including 'fields' and 'data' keys.

        Returns:
            list: A list of dictionaries representing individual records, where each record maps field names to values.

        Raises:
            KeyError: If the 'fields' or 'data' key is not found in the response data.

        Example:
            response_data = {
                "fields": ["timestamp", "pm2.5", "temperature"],
                "data": [
                    [1637326800, 10.2, 25.0],
                    [1637326860, 9.8, 25.5],
                    # ...
                ]
            }
            records = parse_api_response(response_data)
        """
        fields = response["fields"]
        data_entries = response["data"]

        records = []
        for entry in data_entries:
            record = dict(zip(fields, entry))
            records.append(record)
        return records
