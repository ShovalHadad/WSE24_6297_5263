import sys
from PySide6.QtWidgets import QApplication
from controllers.mainController import MainController


if __name__ == "__main__":
    app = QApplication(sys.argv)


    #main_window = HomeWindow(None)
    #main_controller = MainController(main_window)

    #main_window.controller = main_controller

    #main_window.show()  # Show the Home Window


  # Initialize the main controller
    main_controller = MainController()

    # Show the manager window as the starting point
    main_controller.show_manager_window()

    # Start the application event loop
    sys.exit(app.exec())
  

