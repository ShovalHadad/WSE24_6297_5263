from models.flight import Flight
from PySide6.QtCore import QDate
from models.ticket import FlightTicket
from views.frequentFlyer_main_window import FrequentFlyerMainWindow

class FrequentFlyerMainController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        #self.api_base_url = "https://yourserver.com/api/flights"  # תעדכני לפי השרת שלך
        self.frequent_flyer_main_window = None

    def show_window(self):
        if not self.frequent_flyer_main_window:
                self.frequent_flyer_main_window = FrequentFlyerMainWindow(self)

        self.frequent_flyer_main_window.show()
        return self.frequent_flyer_main_window

    def find_flights(self, arrival, landing, start_date, end_date):
        all_flights = Flight.get_all_flights()

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

    