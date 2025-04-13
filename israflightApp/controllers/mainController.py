from controllers.manager_main_controller import ManagerMainWindowController
from controllers.home_controller import HomeController
from controllers.flight_management_controller import FlightManagementController
from controllers.add_manager_controller import AddManagerController
from controllers.plane_management_controller import PlaneManagementController
from controllers.frequentFlyer_main_controller import FrequentFlyerMainController



class MainController:
    def __init__(self):
        # Initialize controllers
        self.home_controller = HomeController(self)
        self.manager_main_controller = None
        self.flight_management_controller = None
        self.add_manager_controller = None
        self.plane_management_controller = None
        self.frequent_flyer_controller = None


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



    def show_add_manager_window(self):
        if not self.add_manager_controller:
            self.add_manager_controller = AddManagerController(self)
        self.close_all_windows()
        self.current_window = self.add_manager_controller.show_window()

        
    def show_plane_management_window(self):
        if not self.plane_management_controller:
            self.plane_management_controller = PlaneManagementController(self)
        self.close_all_windows()
        self.current_window = self.plane_management_controller.show_window()


    def show_frequent_flyer_window(self):
        # Close the currently active window
        self.close_all_windows()

        if not self.frequent_flyer_controller:
            self.frequent_flyer_controller = FrequentFlyerMainController(self)

        self.current_window = self.frequent_flyer_controller.show_window()




    def close_all_windows(self):
        # Close the currently active window, if any
        if self.current_window:
            self.current_window.close()
            self.current_window = None
