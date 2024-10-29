import requests
from models.flyer import FrequentFlyer  # Make sure to import your Plane model

class FrequentFlyerController:
    BASE_URL = "http://localhost:5000/api/frequentflyer"  # Update the URL as necessary

    @staticmethod
    def get_frequent_flyers():
        response = requests.get(FrequentFlyerController.BASE_URL)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_frequent_flyer(flyer_id):
        response = requests.get(f"{FrequentFlyerController.BASE_URL}/{flyer_id}")
        response.raise_for_status()
        return response.json()

    @staticmethod
    def create_frequent_flyer(frequent_flyer):
        response = requests.post(FrequentFlyerController.BASE_URL, json=frequent_flyer.__dict__)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def update_frequent_flyer(frequent_flyer):
        response = requests.put(f"{FrequentFlyerController.BASE_URL}/{frequent_flyer.flyer_id}", json=frequent_flyer.__dict__)
        response.raise_for_status()
        return response.status_code

    @staticmethod
    def delete_frequent_flyer(flyer_id):
        response = requests.delete(f"{FrequentFlyerController.BASE_URL}/{flyer_id}")
        response.raise_for_status()
        return response.status_code
