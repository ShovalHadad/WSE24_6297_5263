from models.flight import Flight  # Import the Flight model
import requests

class FlightManagementController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.api_base_url = "http://localhost:5177/api/Flight"  # Update with actual API URL
        self.flight_management_window = None

    def show_window(self):
        if not self.flight_management_window:
            from views.flight_management_window import FlightManagementWindow
            self.flight_management_window = FlightManagementWindow(self)

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
            flight = Flight(
                plane_id=int(flight_data["PlaneId"]),
                departure_location=flight_data["DepartureLocation"],
                arrival_location=flight_data["ArrivalLocation"],
                departure_datetime=flight_data["DepartureDateTime"],
                estimated_arrival_datetime=flight_data["EstimatedArrivalDateTime"],
            )
            flight.create(self.api_base_url)
            return True  # Successfully created
        except Exception as e:
            print(f"Error adding flight: {e}")
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
