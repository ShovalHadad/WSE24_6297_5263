from views.home_window import HomeWindow

class HomeController:
    def __init__(self,Main_controller):
        self.mainController=Main_controller
        self.home_window = HomeWindow(self)

    def show_window(self):
        self.home_window.show()

