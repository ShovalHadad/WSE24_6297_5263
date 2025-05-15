from models.flight import Flight  # Import the Flight model
import requests
from datetime import datetime
from models.flight import Flight
import json

class FlightManagementController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.api_base_url = "http://localhost:5177/api/Flight"  # Update with actual API URL
        self.flight_management_window = None

    def show_window(self):
        if not self.flight_management_window:
            from views.flight_management_window import FlightManagementWindow
            self.flight_management_window = FlightManagementWindow(controller=self,
                nav_controller=self.main_controller.navigation_controller
            )

        self.flight_management_window.show()
        return self.flight_management_window

    def get_flights(self):
        """Fetches all flights from the API and returns a list of Flight objects."""
        try:
            flights = Flight.get_all_flights(self.api_base_url)
            return flights  # Return list of Flight objects
        except Exception as e:
            print(f"Error fetching flights: {e}")
            return []

    def add_flight(self, flight_data):
        """Creates a new flight using the Flight model."""
        try:
            departure_datetime = datetime.fromisoformat(flight_data["DepartureDateTime"])
            estimated_arrival_datetime = datetime.fromisoformat(flight_data["EstimatedArrivalDateTime"])
            
            # Create a Flight instance
            flight = Flight(
                flight_id=None,  # Ensure it's not sent
                plane_id=int(flight_data["PlaneId"]),
                departure_location=flight_data["DepartureLocation"],
                arrival_location=flight_data["ArrivalLocation"],
                departure_datetime=departure_datetime,
                estimated_arrival_datetime=estimated_arrival_datetime,
                num_of_taken_seats1=0,  # Default values
                num_of_taken_seats2=0,
                num_of_taken_seats3=0,
            )

            json_data=flight.to_dict()
            print(f"🔹 JSON Sent from Python: {json.dumps(json_data, indent=4)}")  # Print JSON payload
            # Call the `create` method from the Flight model
            flight.create(self.api_base_url)
            return True  # Successfully created
        
        except requests.exceptions.HTTPError as http_err:
            print(f"❌ HTTP Error: {http_err}")
            print(f"❌ Response Content: {http_err.response.text}")  # Print server error details
            return False
        except Exception as e:
            print(f"❌ General Error: {e}")
            return False


    def update_flight(self, flight_data):
        try:
            updated_flight = Flight(
                flight_id=flight_data.get("FlightId"),
                plane_id=flight_data.get("PlaneId"),
                departure_location=flight_data.get("DepartureLocation"),
                arrival_location=flight_data.get("ArrivalLocation"),
                departure_datetime=datetime.fromisoformat(flight_data.get("DepartureDateTime")),
                estimated_arrival_datetime=datetime.fromisoformat(flight_data.get("EstimatedArrivalDateTime")),
                num_of_taken_seats1=flight_data.get("NumOfTakenSeats1", 0),
                num_of_taken_seats2=flight_data.get("NumOfTakenSeats2", 0),
                num_of_taken_seats3=flight_data.get("NumOfTakenSeats3", 0)
            )
            updated_flight.update(self.api_base_url)
            return True
        except Exception as e:
            print(f"❌ Failed to update flight: {e}")
            return False

    
    def delete_flight(self, flight_id):
        """Deletes a flight by ID."""
        try:
            flight = Flight.get_flight_by_id(self.api_base_url, flight_id)
            flight.delete(self.api_base_url)
            return True
        except Exception as e:
            print(f"Error deleting flight: {e}")
            return False
