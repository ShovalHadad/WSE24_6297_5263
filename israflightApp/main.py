import sys
from PySide6.QtWidgets import QApplication
from controllers.mainController import MainController


if __name__ == "__main__":
    app = QApplication(sys.argv)

  # Initialize the main controller
    main_controller = MainController()

    # Start the application event loop
    sys.exit(app.exec())
  

