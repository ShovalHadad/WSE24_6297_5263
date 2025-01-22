from views.add_manager_window import AddManagerWindow


class AddManagerController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.add_manager_window = AddManagerWindow(self)

    def show_window(self):
        self.add_manager_window.show()
        return self.add_manager_window
