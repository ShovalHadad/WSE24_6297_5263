from models.frequent_flyer import FrequentFlyer
from models.ticket import FlightTicket
from models.flight import Flight
from datetime import datetime
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
        # Create a flight ticket with all required information

            new_ticket = FlightTicket(
                ticket_id=0,
                user_id=flyer_id,
                flight_id=flight_id,
                ticket_type=seat_class
                #shabat_times=None,
                #created_date=None,
                #price=None
            )
    
            # Save the ticket
            success = new_ticket.create(self.api_base_url_ticket)
            if success:
                #self.refresh_registered_flights()
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
        try:
            print(f"Searching for ticket with flight_id={flight_id}, user_id={user_id}")
    
        # Get all tickets
            tickets = FlightTicket.get_all_tickets(self.api_base_url_ticket)
        
            for ticket in tickets:
                print(f"Checking ticket {ticket.ticket_id} : flight_id={ticket.flight_id}, user_id={ticket.user_id}")
                if int(ticket.flight_id) == int(flight_id) and int(ticket.user_id) == int(user_id):
                    return ticket

            print("No matching ticket found")
            return None

        except Exception as e:
            print(f"Error getting ticket: {e}")
            import traceback
            traceback.print_exc()  # Print full stack trace
            return None  