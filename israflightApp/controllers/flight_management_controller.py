from views.flight_management_window import FlightManagementWindow


class FlightManagementController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.flight_management_window = FlightManagementWindow(self)

    def show_window(self):
        self.flight_management_window.show()
        return self.flight_management_window
