from controllers.manager_main_controller import ManagerMainWindowController
from controllers.home_controller import HomeController
from controllers.flight_management_controller import FlightManagementController


class MainController:
    def __init__(self):
        # Initialize controllers
        self.home_controller = HomeController(self)
        self.manager_main_controller = None
        self.flight_management_controller = None

        # Track the currently active window
        self.current_window = None

    def show_home_window(self):
        # Close the currently active window
        self.close_all_windows()

        # Show the Home Window
        self.current_window = self.home_controller.show_window()

    def show_manager_window(self):
        # Close the currently active window
        self.close_all_windows()

        # Lazy initialize the ManagerMainWindowController
        if not self.manager_main_controller:
            self.manager_main_controller = ManagerMainWindowController(self)

        # Show the Manager Main Window
        self.current_window = self.manager_main_controller.show_window()

    def show_flight_management_window(self):
        # Close the currently active window
        self.close_all_windows()

        # Lazy initialize the FlightManagementController
        if not self.flight_management_controller:
            self.flight_management_controller = FlightManagementController(self)

        # Show the Flight Management Window
        self.current_window = self.flight_management_controller.show_window()

    def close_all_windows(self):
        # Close the currently active window, if any
        if self.current_window:
            self.current_window.close()
            self.current_window = None
