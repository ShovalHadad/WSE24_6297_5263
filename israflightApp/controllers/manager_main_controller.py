from views.manager_main_window import ManagerMainWindow
from controllers.flight_management_controller import FlightManagementController


class ManagerMainWindowController:
    def __init__(self, main_controller, flyer_id):
        self.main_controller = main_controller
        self.manager_main_window = ManagerMainWindow(
            flyer_id=flyer_id,
            controller=self,
            nav_controller=main_controller.navigation_controller  
        )

        # Initialize controller connections in the window
        self.manager_main_window.initialize_controller(self,flyer_id)

    def show_window(self):
        self.manager_main_window.showMaximized()
        return self.manager_main_window

    def open_flight_management(self):
        """Handle the action for opening the Flight Management Window."""
        self.main_controller.show_flight_management_window()


    #def open_add_manager(self):
    #    self.main_controller.show_add_manager_window()

    def open_planes_management(self):
        self.main_controller.show_plane_management_window()

    def back_to_frequent_flyer(self, flyer_id):
        self.main_controller.show_frequent_flyer_window(flyer_id)



