# navigation_controller.py

class NavigationController:
    def __init__(self, main_controller):
        self.main_controller = main_controller

    def go_home(self):
        """Navigate to the home window."""
        self.main_controller.show_home_window()

    def go_back(self):
        """Navigate back to the previous window."""
        self.main_controller.go_back()
