import requests
from datetime import datetime

class FlightTicket:
    def __init__(self, ticket_id , ticket_type , user_id , flight_id , 
                 shabat_times , created_date, price):
        self.ticket_id = ticket_id
        self.ticket_type = ticket_type
        self.user_id = user_id
        self.flight_id = flight_id
        self.shabat_times = shabat_times 
        self.created_date = created_date 
        self.price = price

    @classmethod
    def from_dict(cls, data):    
        return cls(
            ticket_id=data.get("ticketId"),
            ticket_type=data.get("ticketType"),
            user_id=data.get("userId"),
            flight_id=data.get("flightId"),
            shabat_times=data.get("shabatTimes"),
            created_date = datetime.fromisoformat(data["createdDate"]) if data.get("createdDate") else None,
            price=data.get("price")
        )

    def to_dict(self):
        return {
            "TicketId": self.ticket_id,
            "TicketType": self.ticket_type,
            "UserId": self.user_id,
            "FlightId": self.flight_id
        }
    
    @staticmethod
    def get_all_tickets(base_url):
        try:
            response = requests.get(f"{base_url}")
            response.raise_for_status()
            ticket_data_list = response.json()
            return [FlightTicket.from_dict(data) for data in ticket_data_list]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching flight tickets: {e}")
            return []

    @staticmethod
    def get_ticket_by_id(base_url, ticket_id):
        try:
            response = requests.get(f"{base_url}/api/flighttickets/{ticket_id}")
            response.raise_for_status()
            ticket_data = response.json()
            return FlightTicket.from_dict(ticket_data)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching flight ticket {ticket_id}: {e}")
            return None
        

    @staticmethod
    def get_tickets_by_user(base_url, user_id):
        try:
        # First try to get all tickets and filter by user ID
            all_tickets_data =[]
            response = requests.get(f"{base_url}")
            response.raise_for_status()
            ticket_data_list = response.json()
            for data in ticket_data_list:
                all_tickets_data.append(FlightTicket.from_dict(data))
            
        # Filter tickets belonging to this user
            user_tickets = []
            for ticket_data in all_tickets_data:
                if ticket_data.user_id == user_id:
                    try:
                        #ticket = FlightTicket.from_dict(ticket_data)
                        user_tickets.append(ticket)
                    except Exception as e:
                        print(f"Error creating ticket object: {e}")
                        continue
        
            if user_tickets:
                return user_tickets
            
        # If no tickets found with direct filter, try the original method
            flyer_url = f"http://localhost:5177/api/FrequentFlyer/{user_id}"
            flyer_response = requests.get(flyer_url)
            flyer_response.raise_for_status()
            flyer_data = flyer_response.json()
        
            flight_ids = flyer_data.get("FlightsIds", [])
            if not flight_ids:
                return []
        
        # Look for tickets matching these flight IDs
            tickets = []
            for flight_id in flight_ids:
                # Try to find a ticket for this flight and user
                for ticket_data in all_tickets_data:
                    if (ticket_data.get("FlightId") == flight_id and 
                        ticket_data.get("UserId") == user_id):
                        try:
                            ticket = FlightTicket.from_dict(ticket_data)
                            tickets.append(ticket)
                        except Exception as e:
                            print(f"Error creating ticket object: {e}")
                        break
                    
            return tickets
        except Exception as e:
            print(f"Error getting tickets for user {user_id}: {e}")
            return []

    def create(self, base_url):
        try:
            ticket_data = self.to_dict()
            if self.ticket_id==0:
                # Print the data being sent for debugging
                print("Sending ticket data:", ticket_data)
                response = requests.post("http://localhost:5177/api/FlightTicket", json=ticket_data)
                response.raise_for_status()
                print("Flight Ticket created successfully")
                return response 
            else:
                self.update(base_url)

        except requests.exceptions.RequestException as e:
            print(f"Error saving Flight Ticket: {e}")

    def update(self, base_url):
        try:
            if not self.ticket_id:
                raise ValueError("Ticket ID is required to update a flight ticket.")

            ticket_data = self.to_dict()
            response = requests.put(f"{base_url}/api/flighttickets/{self.ticket_id}", json=ticket_data)
            response.raise_for_status()
            print("Flight ticket updated successfully")
            return response 
        except requests.exceptions.RequestException as e:
            print(f"Error updating flight ticket {self.ticket_id}: {e}")

    def delete(self, base_url):
        try:
            response = requests.delete(f"{base_url}/api/flighttickets/{self.ticket_id}")
            response.raise_for_status()
            print("Flight ticket deleted successfully")
        except requests.exceptions.RequestException as e:
            print(f"Error deleting flight ticket {self.ticket_id}: {e}")
