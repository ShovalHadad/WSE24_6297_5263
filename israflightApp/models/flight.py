import requests
from datetime import datetime

class Flight:
    def __init__(self, flight_id=None, plane_id=None, departure_location="", arrival_location="",
                 departure_datetime=None, estimated_arrival_datetime=None, 
                 num_of_taken_seats1=0, num_of_taken_seats2=0, num_of_taken_seats3=0):
        self.flight_id = flight_id
        self.plane_id = plane_id
        self.departure_location = departure_location
        self.arrival_location = arrival_location
        self.departure_datetime = departure_datetime
        self.estimated_arrival_datetime = estimated_arrival_datetime
        self.num_of_taken_seats1 = num_of_taken_seats1
        self.num_of_taken_seats2 = num_of_taken_seats2
        self.num_of_taken_seats3 = num_of_taken_seats3

    @classmethod
    def from_dict(cls, data):
        return cls(
            flight_id=data.get("flightId"),
            plane_id=data.get("planeId"),
            departure_location=data.get("departureLocation", ""),
            arrival_location=data.get("arrivalLocation", ""),
            departure_datetime=datetime.fromisoformat(data["departureDateTime"]) if data.get("departureDateTime") else None,
            estimated_arrival_datetime=datetime.fromisoformat(data["estimatedArrivalDateTime"]) if data.get("estimatedArrivalDateTime") else None,
            num_of_taken_seats1=data.get("numOfTakenSeats1", 0),
            num_of_taken_seats2=data.get("numOfTakenSeats2", 0),
            num_of_taken_seats3=data.get("numOfTakenSeats3", 0)
        )

    @staticmethod
    def get_all_flights(api_base_url):
        url = f"{api_base_url}"
        response = requests.get(url)
        response.raise_for_status()
        flights_data = response.json()
        return [Flight.from_dict(data) for data in flights_data]

    @staticmethod
    def get_flight_by_id(api_base_url, flight_id):
        url = f"{api_base_url}/flights/{flight_id}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return Flight.from_dict(data)

    def create(self, api_base_url):
        url = f"{api_base_url}/flights"
        flight_data = self.to_dict()
        response = requests.post(url, json=flight_data)
        response.raise_for_status()
        created_flight_data = response.json()
        self.flight_id = created_flight_data["flightId"]

    def update(self, api_base_url):
        if not self.flight_id:
            raise ValueError("Flight ID is required to update a flight.")
        url = f"{api_base_url}/flights/{self.flight_id}"
        flight_data = self.to_dict()
        response = requests.put(url, json=flight_data)
        response.raise_for_status()

    def delete(self, api_base_url):
        if not self.flight_id:
            raise ValueError("Flight ID is required to delete a flight.")
        
        url = f"{api_base_url}/flights/{self.flight_id}"
        response = requests.delete(url)
        response.raise_for_status()

    def to_dict(self):
        return {
            "flightId": self.flight_id,
            "planeId": self.plane_id,
            "departureLocation": self.departure_location,
            "arrivalLocation": self.arrival_location,
            "departureDateTime": self.departure_datetime.isoformat() if self.departure_datetime else None,
            "estimatedArrivalDateTime": self.estimated_arrival_datetime.isoformat() if self.estimated_arrival_datetime else None,
            "numOfTakenSeats1": self.num_of_taken_seats1,
            "numOfTakenSeats2": self.num_of_taken_seats2,
            "numOfTakenSeats3": self.num_of_taken_seats3,
        }
