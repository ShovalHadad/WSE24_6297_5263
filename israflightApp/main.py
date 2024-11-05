import sys
from PySide6.QtWidgets import QApplication
from views.home_window import HomeWindow
from controllers.mainController import MainController

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Initialize the Main Controller and Home Window
    main_window = HomeWindow(None)
    main_controller = MainController(main_window)

    # Link the controller to the view
    main_window.controller = main_controller

    main_window.show()  # Show the Home Window
    sys.exit(app.exec())
  

