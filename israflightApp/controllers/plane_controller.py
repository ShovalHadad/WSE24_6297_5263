import requests
from models.plane import Plane  # Make sure to import your Plane model

class PlaneController:
    BASE_URL = "http://your_api_base_url/api/plane"  # Replace with your actual API base URL

    def get_planes(self):
        response = requests.get(self.BASE_URL)
        response.raise_for_status()  # Raises an error for 4xx/5xx responses
        return [Plane(**data) for data in response.json()]

    def get_plane(self, plane_id):
        response = requests.get(f"{self.BASE_URL}/{plane_id}")
        response.raise_for_status()
        return Plane(**response.json())

    def create_plane(self, plane):
        response = requests.post(self.BASE_URL, json=plane.to_dict())
        response.raise_for_status()
        return Plane(**response.json())

    def update_plane(self, plane):
        response = requests.put(f"{self.BASE_URL}/{plane.plane_id}", json=plane.to_dict())
        response.raise_for_status()
        return Plane(**response.json())

    def delete_plane(self, plane_id):
        response = requests.delete(f"{self.BASE_URL}/{plane_id}")
        response.raise_for_status()
