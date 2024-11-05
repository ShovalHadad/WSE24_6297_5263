import requests
from models.flight import FlightModel

class FlightController:
    BASE_URL = "http://localhost:5000/api/flights"

    @staticmethod
    def get_flight(flight_id):
        response = requests.get(f"{FlightController.BASE_URL}/{flight_id}")
        if response.status_code == 200:
            flight_data = response.json()
            return FlightModel(
                flight_data['flightId'],
                flight_data['planeId'],
                flight_data['departureLocation'],
                flight_data['arrivalLocation'],
                flight_data['departureDateTime'],
                flight_data['estimatedArrivalDateTime'],
                flight_data['numOfTakenSeats1'],
                flight_data['numOfTakenSeats2'],
                flight_data['numOfTakenSeats3']
            )
        else:
            print(f"Error: {response.status_code}")
            return None

    @staticmethod
    def create_flight(flight_model):
        response = requests.post(FlightController.BASE_URL, json=flight_model.to_dict())
        if response.status_code == 201:
            print("Flight created successfully")
        else:
            print(f"Error: {response.status_code} - {response.text}")

    @staticmethod
    def update_flight(flight_id, flight_model):
        response = requests.put(f"{FlightController.BASE_URL}/{flight_id}", json=flight_model.to_dict())
        if response.status_code == 204:
            print("Flight updated successfully")
        else:
            print(f"Error: {response.status_code} - {response.text}")

    @staticmethod
    def delete_flight(flight_id):
        response = requests.delete(f"{FlightController.BASE_URL}/{flight_id}")
        if response.status_code == 204:
            print("Flight deleted successfully")
        else:
            print(f"Error: {response.status_code} - {response.text}")
