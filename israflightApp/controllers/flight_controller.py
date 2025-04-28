from models.frequent_flyer import FrequentFlyer
from models.ticket import FlightTicket
from models.flight import Flight
import requests
import json

class FlightController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.api_base_url_ticket = "http://localhost:5177/api/FlightTicket"  
        self.api_base_url_flyer = "http://localhost:5177/api/FrequentFlyer"
        self.api_base_url_flight = "http://localhost:5177/api/Flight"
        self.flight_window = None
        
    def show_window(self, flight_id, flyer_id, is_booking=0):
        """
        Display the flight window for either booking or viewing
        
        Args:
            flight: The Flight object
            flyer_id: The ID of the FrequentFlyer
            is_booking: 0 for booking mode, 1 for view mode
        
        Returns:
            The FlightWindow instance
        """
        from views.flight_window import FlightWindow
        
        # Create a new flight window
        self.flight_window = FlightWindow(self, flight_id, flyer_id, is_booking)
        
        # Show the window
        self.flight_window.show()
        
        return self.flight_window

    def book_flight(self, flyer_id, flight_id, seat_class):
        try:
            # Calculate ticket price based on seat class
            base_price = 100  # Base price in dollars
            class_multiplier = {
                1: 3.0,  # First class - 3x base price
                2: 2.0,  # Business class - 2x base price
                3: 1.0,  # Economy class - 1x base price
            }
            
            price = str(base_price * class_multiplier.get(seat_class, 1.0))
            
            # Create a flight ticket
            new_ticket = FlightTicket(
                ticket_id=0,  # API will assign real ID
                user_id=flyer_id,
                flight_id=flight_id,
                ticket_type=seat_class,
                price=price
            )
        
            # Save the ticket
            success = new_ticket.create(self.api_base_url_ticket)
        
            # Update flyer's flights list
            if success:
                current_flyer = FrequentFlyer.get_flyer_by_id(flyer_id)
                if current_flyer and flight_id not in current_flyer.flights_ids:
                    if not current_flyer.flights_ids:
                        current_flyer.flights_ids = []
                    current_flyer.flights_ids.append(flight_id)
                    current_flyer.update(self.api_base_url_flyer)
            
                # Refresh the registered flights list in the main window if it exists
                if hasattr(self.main_controller, 'frequent_flyer_main_window') and self.main_controller.frequent_flyer_main_window:
                    self.refresh_registered_flights()
                
            return success
        except Exception as e:
            print(f"Error booking flight: {e}")
            return False
    
    def refresh_registered_flights(self):
        """Refresh the registered flights list in the main window"""
        try:
            # Get the main window
            main_window = self.main_controller.frequent_flyer_main_window
            if not main_window:
                return
            
            # Clear the current list
            main_window.flight_list.clear()
            
            # Get the flyer
            flyer = self.main_controller.get_flyer_by_id(self.main_controller.flyer_id)
            if not flyer or not flyer.flights_ids:
                main_window.flight_list.addItem("No registered flights.")
                return
            
            # Get and display the flights
            flights = self.main_controller.get_flights(flyer.flights_ids)
            for flight in flights:
                flight_info = f"{flight.flight_id}   | ✈ {flight.departure_location} → {flight.arrival_location} at {flight.departure_datetime}"
                main_window.flight_list.addItem(flight_info)
        except Exception as e:
            print(f"Error refreshing registered flights: {e}")
            
    def get_seat_class_name(self, seat_class):
        """Get the name of the seat class based on its ID"""
        classes = {
            1: "First Class",
            2: "Business Class",
            3: "Economy Class"
        }
        return classes.get(seat_class, "Unknown")
    
    def get_flight(self, flight_id):
        return Flight.get_flight_by_id(self.api_base_url_flight ,flight_id)

    def get_ticket_by_flight_user(self, flight_id, user_id):
        """Get a ticket by flight ID and user ID"""
        try:
            print(f"Searching for ticket with flight_id={flight_id}, user_id={user_id}")
        
            # Try a direct API call first (if your API supports this)
            direct_url = f"{self.api_base_url_ticket}?flightId={flight_id}&userId={user_id}"
            try:
                response = requests.get(direct_url)
                if response.status_code == 200:
                    data = response.json()
                    if data and len(data) > 0:
                        ticket = FlightTicket.from_dict(data[0])
                        print(f"Found ticket directly: {ticket.ticket_id}")
                        return ticket
            except Exception as e:
                print(f"Direct ticket search failed: {e}")
        
            # Get all tickets for the user
            tickets = FlightTicket.get_tickets_by_user(self.api_base_url_ticket, user_id)
        
            if not tickets:
                print("No tickets found for user")
                return None
        
            print(f"Found {len(tickets)} tickets for user")
        
            # Find the ticket for this flight
            for ticket in tickets:
                print(f"Checking ticket: flight_id={ticket.flight_id}, user_id={ticket.user_id}")
                if int(ticket.flight_id) == int(flight_id):
                    print(f"Found matching ticket: {ticket.ticket_id}")
                    return ticket
        
            print("No matching ticket found for this flight")
            return None
        except Exception as e:
            print(f"Error getting ticket: {e}")
            return None