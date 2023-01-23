import pymongo
from connectors.purple_air.purple_air_config import PurpleAirConfig
from typing import Generator


class PurpleAirConnector:

    def __init__(self):
        self.config = PurpleAirConfig()
        