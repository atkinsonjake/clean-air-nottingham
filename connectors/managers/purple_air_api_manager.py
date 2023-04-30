import requests
import json
from connectors.purple_air.purple_air_config import PurpleAirConfig

class PurpleAirApiManager:

    def __init__(self):
        self.config = PurpleAirConfig()

    def create_group_member(self, group_id: int, member_id: int) -> dict:
        """
        Create a new group PurpleAir API group member.

        Args:
            group_id: The ID of the group.
            member_id: The ID of the member.

        Returns:
            A dictionary containing the details of the new group member.
        """

        url = f"https://api.purpleair.com/v1/groups/{group_id}/members"
        headers = {
            "X-API-Key": self.config.API_KEY_W,
            "Content-Type": "application/json"
        }

        data = {
            "sensor_index": member_id
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error creating group member in group {group_id}: {response.status_code}")
        

    def get_group_details(self, group_id: int) -> dict:
        """
        Get the details of a PurpleAir API group.

        Args:
            group_id: The ID of the group.

        Returns:
            A dictionary containing the details of the group.
        """

        url = f"https://api.purpleair.com/v1/groups/{group_id}"
        headers = {
            "X-API-Key": self.config.API_KEY_R,
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error getting group details: {response.status_code}")