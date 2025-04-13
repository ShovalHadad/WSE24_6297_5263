from models.flight import Flight
from PySide6.QtCore import QDate

class FrequentFlyerMainController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.api_base_url = "https://yourserver.com/api/flights"  # תעדכני לפי השרת שלך
        self.frequent_flyer_main_window = FrequentFlyerMainWindow(self)

    def show_window(self):
        self.frequent_flyer_main_window.showMaximized()
        return self.frequent_flyer_main_window

    def find_flights(self, arrival, landing, start_date, end_date):
        all_flights = Flight.get_all_flights(self.api_base_url)

        filtered = []
        for f in all_flights:
            if arrival and arrival.lower() not in f.departure_location.lower():
                continue
            if landing and landing.lower() not in f.arrival_location.lower():
                continue

            flight_date = QDate(f.departure_datetime.year, f.departure_datetime.month, f.departure_datetime.day)
            if flight_date < start_date or flight_date > end_date:
                continue

            filtered.append({
                "flight_id": f.flight_id,
                "departure": f.departure_location,
                "arrival": f.arrival_location,
                "date": f.departure_datetime.strftime("%Y-%m-%d"),
                "plane_id": f.plane_id,
                "full_obj": f  # למעבר לפרטי טיסה
            })

        return filtered

    def order_flight(self, flight, user_id, ticket_type, price, shabat_times):
        from models.flight_ticket import FlightTicket
        ticket = FlightTicket(
            ticket_id=0,
            ticket_type=ticket_type,
            user_id=user_id,
            flight_id=flight.flight_id,
            shabat_times=shabat_times,
            created_date=datetime.now(),
            price=price
        )
        ticket.create("https://yourserver.com")
