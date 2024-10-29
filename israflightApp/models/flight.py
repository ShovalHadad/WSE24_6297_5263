class FlightModel:
    def __init__(self, flight_id, plane_id, departure_location, arrival_location, departure_datetime, estimated_arrival_datetime, taken_seats_1, taken_seats_2, taken_seats_3):
        self.flight_id = flight_id
        self.plane_id = plane_id
        self.departure_location = departure_location
        self.arrival_location = arrival_location
        self.departure_datetime = departure_datetime
        self.estimated_arrival_datetime = estimated_arrival_datetime
        self.taken_seats_1 = taken_seats_1
        self.taken_seats_2 = taken_seats_2
        self.taken_seats_3 = taken_seats_3

    def to_dict(self):
        return {
            "flightId": self.flight_id,
            "planeId": self.plane_id,
            "departureLocation": self.departure_location,
            "arrivalLocation": self.arrival_location,
            "departureDateTime": self.departure_datetime,
            "estimatedArrivalDateTime": self.estimated_arrival_datetime,
            "numOfTakenSeats1": self.taken_seats_1,
            "numOfTakenSeats2": self.taken_seats_2,
            "numOfTakenSeats3": self.taken_seats_3
        }





'''
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class Flight(BaseModel):
    flight_id: int  # Flight number
    plane_id: int   # Navigation to plane
    departure_location: str = Field(..., title="Departure Location")  # Departure Location
    arrival_location: str = Field(..., title="Arrival Location")  # Arrival Location
    departure_date_time: datetime  # Departure Date
    estimated_arrival_date_time: datetime  # Arrival Date
    num_of_taken_seats_1: Optional[int] = None  # Number of taken seats in first class
    num_of_taken_seats_2: Optional[int] = None  # Number of taken seats in business
    num_of_taken_seats_3: Optional[int] = None  # Number of taken seats in economy

    def __str__(self):
        return f"Flight {self.flight_id}: {self.departure_location} to {self.arrival_location} on {self.departure_date_time}"

    def is_full(self):
        """Check if the flight is full."""
        # Assuming you have total seat counts for each class, you can implement your logic here.
        # Example:
        total_seats_1 = 10  # Example total for first class
        total_seats_2 = 20  # Example total for business
        total_seats_3 = 100  # Example total for economy
        return (self.num_of_taken_seats_1 >= total_seats_1 and
                self.num_of_taken_seats_2 >= total_seats_2 and
                self.num_of_taken_seats_3 >= total_seats_3)
'''
