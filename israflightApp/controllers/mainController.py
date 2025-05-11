from controllers.manager_main_controller import ManagerMainWindowController
from controllers.home_controller import HomeController
from controllers.flight_management_controller import FlightManagementController
from controllers.plane_management_controller import PlaneManagementController
from controllers.frequentFlyer_main_controller import FrequentFlyerMainController
from controllers.flight_controller import FlightController
from controllers.navigation_controller import NavigationController  


class MainController:
    def __init__(self):
        self.home_controller = HomeController(self)
        self.manager_main_controller = None
        self.flight_management_controller = None
        self.add_manager_controller = None
        self.plane_management_controller = None
        self.frequent_flyer_controller = None

        self.history_stack = []  # ✅ לשמור היסטוריה

        self.navigation_controller = NavigationController(self)  # ✅ יצירת נוויגציה

        self.current_window = self.home_controller.show_window()

    def navigate_to(self, show_func):
        """General navigation function to keep history."""
        if self.current_window:
            self.history_stack.append(self.current_window)
            self.current_window.close()
        self.current_window = show_func()

    def go_back(self):
        if self.history_stack:
            prev_window = self.history_stack.pop()
            if self.current_window:
                self.current_window.close()
            self.current_window = prev_window
            self.current_window.show()
        else:
            self.show_home_window()

    def show_home_window(self):
        if self.current_window:
            self.current_window.close()
        self.current_window = self.home_controller.show_window()
        self.history_stack.clear()

    def show_manager_window(self, flyer_id):
        if not self.manager_main_controller:
            self.manager_main_controller = ManagerMainWindowController(self, flyer_id)
        self.navigate_to(self.manager_main_controller.show_window)

    def show_flight_management_window(self):
        if not self.flight_management_controller:
            self.flight_management_controller = FlightManagementController(self)
        self.navigate_to(self.flight_management_controller.show_window)

    def show_plane_management_window(self):
        if not self.plane_management_controller:
            self.plane_management_controller = PlaneManagementController(self)
        self.navigate_to(self.plane_management_controller.show_window)

    def show_flight_window(self):
        if not self.flight_controller:
            self.flight_controller = FlightController(self)
        self.navigate_to(self.flight_controller.show_window)

    def show_frequent_flyer_window(self, flyer_id):
        if not self.frequent_flyer_controller:
            self.frequent_flyer_controller = FrequentFlyerMainController(self, flyer_id)
        self.navigate_to(self.frequent_flyer_controller.show_window)
