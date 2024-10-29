import requests
from models.ticket import FlightTicket  # Make sure to import your Plane model

class FlightTicketController:
    BASE_URL = "http://your_api_url/api/FlightTicket"

    def get_flight_tickets(self):
        response = requests.get(self.BASE_URL)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to retrieve flight tickets.")

    def get_flight_ticket(self, ticket_id):
        response = requests.get(f"{self.BASE_URL}/{ticket_id}")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to retrieve flight ticket with ID {ticket_id}.")

    def create_flight_ticket(self, flight_ticket):
        response = requests.post(self.BASE_URL, json=flight_ticket.to_dict())
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception("Failed to create flight ticket.")

    def update_flight_ticket(self, ticket_id, flight_ticket):
        response = requests.put(f"{self.BASE_URL}/{ticket_id}", json=flight_ticket.to_dict())
        if response.status_code == 204:
            return "Flight ticket updated successfully."
        else:
            raise Exception(f"Failed to update flight ticket with ID {ticket_id}.")

    def delete_flight_ticket(self, ticket_id):
        response = requests.delete(f"{self.BASE_URL}/{ticket_id}")
        if response.status_code == 204:
            return "Flight ticket deleted successfully."
        else:
            raise Exception(f"Failed to delete flight ticket with ID {ticket_id}.")
