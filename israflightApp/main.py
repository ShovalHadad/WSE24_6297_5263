import sys
from PySide6.QtWidgets import QApplication
from views.home_window import HomeWindow
from views.admin_main_window import ManagerMainWindow
from controllers.mainController import MainController

if __name__ == "__main__":
    app = QApplication(sys.argv)


    main_window = HomeWindow(None)
    main_controller = MainController(main_window)

    main_window.controller = main_controller

    #main_window.show()  # Show the Home Window


    manager_window = ManagerMainWindow(None)  # Replace `None` with an actual controller if needed
    manager_window.show()  # Show the ManagerMainWindow



    sys.exit(app.exec())
  

