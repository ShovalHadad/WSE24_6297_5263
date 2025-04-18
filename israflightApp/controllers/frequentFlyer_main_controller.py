from models.flight import Flight
from PySide6.QtCore import QDate
from models.ticket import FlightTicket
from views.frequentFlyer_main_window import FrequentFlyerMainWindow
from models.frequent_flyer import FrequentFlyer

class FrequentFlyerMainController:
    def __init__(self, main_controller, flyer_id):
        self.main_controller = main_controller
        self.flyer_id = flyer_id
        #self.api_base_url =  "http://localhost:5177/api/FrequentFlyer" # תעדכני לפי השרת שלך
        self.frequent_flyer_main_window = None

    def show_window(self):
        if not self.frequent_flyer_main_window:
                self.frequent_flyer_main_window = FrequentFlyerMainWindow(self, self.flyer_id)

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

    def get_flights(self, id_list):
        flights = []
        for id in id_list:
            flights.append(Flight.get_flight_by_id("http://localhost:5177/api/Flight",id))
        return flights
    
    def get_flyer_by_id(self, flyer_id):
        return FrequentFlyer.get_flyer_by_id(flyer_id)