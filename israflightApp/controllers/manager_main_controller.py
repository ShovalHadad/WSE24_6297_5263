from views.manager_main_window import ManagerMainWindow
from controllers.flight_management_controller import FlightManagementController


class ManagerMainWindowController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.manager_main_window = ManagerMainWindow(self)

        # Initialize controller connections in the window
        self.manager_main_window.initialize_controller(self)

    def show_window(self):
        self.manager_main_window.showMaximized()
        return self.manager_main_window

    def open_flight_management(self):
        """Handle the action for opening the Flight Management Window."""
        self.main_controller.show_flight_management_window()


    def open_add_manager(self):
        self.main_controller.show_add_manager_window()


