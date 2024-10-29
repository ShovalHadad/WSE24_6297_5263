import sys
from PySide6.QtWidgets import QApplication
from views.plane_view import PlaneView
from controllers.plane_controller import PlaneController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = PlaneView()
    controller = PlaneController(view)
    view.show()
    sys.exit(app.exec())
