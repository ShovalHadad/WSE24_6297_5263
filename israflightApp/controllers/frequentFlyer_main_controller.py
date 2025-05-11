from models.flight import Flight
from PySide6.QtCore import QDate
from models.ticket import FlightTicket
from views.frequentFlyer_main_window import FrequentFlyerMainWindow
from models.frequent_flyer import FrequentFlyer
from views.flight_window import FlightWindow


class FrequentFlyerMainController:
    def __init__(self, main_controller, flyer_id):
        self.main_controller = main_controller
        self.flyer_id = flyer_id
        self.api_base_url_ticket = "http://localhost:5177/api/FlightTicket"
        self.api_base_url_flyer =  "http://localhost:5177/api/FrequentFlyer" # תעדכני לפי השרת שלך
        self.api_base_url_flight = "http://localhost:5177/api/Flight"
        self.frequent_flyer_main_window = None

    def show_window(self):
        if not self.frequent_flyer_main_window:
                self.frequent_flyer_main_window = FrequentFlyerMainWindow(self, self.flyer_id, nav_controller=self.main_controller.navigation_controller
            )

        self.frequent_flyer_main_window.show()
        return self.frequent_flyer_main_window

    def find_flights(self, departure_widget, arrival_widget, date_widget):
        all_flights = Flight.get_all_flights(self.api_base_url_flight)
        
        if(all_flights == None):
            return all_flights
        
        flights = []

        # Extract values from the widgets
        departure_text = departure_widget.text() if departure_widget else ""
        arrival_text = arrival_widget.text() if arrival_widget else ""
        selected_date = date_widget.date() if date_widget else QDate.currentDate()
        
        for f in all_flights:
            if departure_text and departure_text.lower() not in f.departure_location.lower():
                continue
            if arrival_text and arrival_text.lower() not in f.arrival_location.lower():
                continue
            flight_date = QDate(f.departure_datetime.year, f.departure_datetime.month, f.departure_datetime.day)
            if flight_date < selected_date:
                continue
            flights.append(f)

        return flights

    def get_flights(self, id_list):
        flights = []
        for id in id_list:
            flights.append(Flight.get_flight_by_id(self.api_base_url_flight,id))
        return flights
    
    def get_flyer_by_id(self, flyer_id):
        return FrequentFlyer.get_flyer_by_id(flyer_id)
    
    def update_flyer(self, flyer_id, first_name, last_name, email, phone):
        # Get current flyer object with all properties
        current_flyer = FrequentFlyer.get_flyer_by_id(flyer_id)
    
        if not current_flyer:
            print(f"Error: No flyer found with ID {flyer_id}")
            return False
    
        # Only update fields that have actually changed
        # The server rejects updates where the field matches an "empty" value
        try:
        # Create a new object retaining all original data
            updated_flyer = FrequentFlyer(
                flyer_id=current_flyer.flyer_id,
                username=current_flyer.username,    # Don't change username
                password=current_flyer.password,    # Don't change password 
                first_name=first_name if first_name else current_flyer.first_name,
                last_name=last_name if last_name else current_flyer.last_name,
                email=email if email else current_flyer.email,
                phone_number=phone if phone else current_flyer.phone_number,
                flights_ids=current_flyer.flights_ids,
                is_manager=current_flyer.is_manager
            )
        
        # Let's add more debugging to see what data we're sending
            print(f"Sending update with data: {updated_flyer.to_dict()}")
        
            updated_flyer.update(self.api_base_url_flyer)
            return True
        except Exception as e:
            print(f"Error updating flyer: {e}")
        # If error contains a response, print its content
            if hasattr(e, 'response') and e.response:
                print(f"Response content: {e.response.text}")
            return False
    
    def open_flight_booking(self, flight_id):
        # Import here to avoid circular imports
    
        # Create the booking window
        booking_window = FlightWindow(self, flight_id, self.flyer_id, 0)
    
        # Show the window
        booking_window.show()
    
        # Optional: Store a reference to the window
        self.booking_window = booking_window

    def open_flight_user(self, flight_id):
        # Import here to avoid circular imports
    
        # Create the booking window
        flight_window = FlightWindow(self, flight_id , self.flyer_id, 1)
    
        # Show the window
        flight_window.show()
    
        # Optional: Store a reference to the window
        self.flight_window = flight_window

    def get_flight_user(self, flight_id):
        return Flight.get_flight_by_id(self.api_base_url_flight, flight_id)
    
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
    

    # Add this method to FrequentFlyerMainController class
    def book_flight(self, flyer_id, flight_id, seat_class):
        try:
        # Calculate ticket price based on seat class
           
        
        # Create a flight ticket
            new_ticket = FlightTicket(
                ticket_id=0,  # API will assign real ID
                user_id=flyer_id,
                flight_id=flight_id,
                ticket_type=seat_class
            )
    
        # Save the ticket
            success = new_ticket.create(self.api_base_url_ticket)
    
            if success:
            # Refresh the registered flights list
                self.refresh_registered_flights()

            return success
        except Exception as e:
            print(f"Error booking flight: {e}")
            return False

    def refresh_registered_flights(self):
        """Refresh the registered flights list in the main window"""
        try:
            if self.frequent_flyer_main_window:
                # Get the flyer
                flyer = self.get_flyer_by_id(self.flyer_id)
            
            # Clear the current list
                self.frequent_flyer_main_window.flight_list.clear()
            
                if flyer and flyer.flights_ids:
                # Get and display the flights
                    flights = self.get_flights(flyer.flights_ids)
                    for flight in flights:
                        flight_info = f"{flight.flight_id}   | ✈ {flight.departure_location} → {flight.arrival_location} at {flight.departure_datetime}"
                        self.frequent_flyer_main_window.flight_list.addItem(flight_info)
                else:
                    self.frequent_flyer_main_window.flight_list.addItem("No registered flights.")
        except Exception as e:
            print(f"Error refreshing registered flights: {e}")