from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtCore import Qt
from views.base_window import BaseWindow


class ManagerMainWindow(BaseWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("IsraFlight - Manager")
        self.setGeometry(500, 200, 800, 600)
        self.setMinimumSize(800, 600)
        self.showMaximized()

        self.create_toolbar()

        # Additional ManagerMainWindow-specific layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Add a QLabel for the background image
        self.background_label = QLabel(central_widget)
        #self.background_label.setGeometry(self.rect())  # Set to cover the entire window
        self.background_label.setPixmap(QPixmap("./israflightApp/images/manager_background.png").scaled(
            self.size(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        ))
        self.background_label.setScaledContents(True)

        # Main vertical layout to center the buttons
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Center the content vertically and horizontally
        central_widget.setLayout(layout)

        # Example content
        label = QLabel("Manager Main Page")
        label.setFont(QFont("Urbanist", 22, 700))
        label.setStyleSheet("""color: #27AAE1 """)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Add a horizontal layout for buttons
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(25)  # Space between buttons

        # Add a spacer widget with fixed height
        spacer = QWidget()
        spacer.setFixedHeight(30)  # Adjust height as needed
        layout.addWidget(spacer)
        layout.addLayout(self.button_layout)

        # Add buttons (connections will be initialized later)
        self.create_buttons()

    def create_buttons(self):
        # Button 1
        self.button1 = QPushButton("Flight Management")  # ניהול טיסות
        self.button1.setIcon(QIcon("./israflightApp/images/flight_managment.png"))  # Replace with your icon path
        self.button1.setFixedSize(250, 75)  # Resize the button
        self.button1.setStyleSheet("""
            QPushButton {
                background-color: #1C3664;
                color: white;
                border-radius: 15px;
                padding: 10px;
                font-family: 'Urbanist';       /* Font family */
                font-size: 19px;              /* Font size */
            }
            QPushButton:hover {
                background-color: #27AAE1;
            }
        """)
        self.button_layout.addWidget(self.button1)

        # Button 2
        self.button2 = QPushButton("Add Manager")  # מינוי מנהל
        self.button2.setIcon(QIcon("./israflightApp/images/add_manager.png"))  # Replace with your icon path
        self.button2.setFixedSize(250, 75)  # Resize the button
        self.button2.setStyleSheet("""
            QPushButton {
                background-color: #1C3664;
                color: white;
                border-radius: 15px;
                padding: 10px;
                font-family: 'Urbanist';       /* Font family */
                font-size: 19px;
            }
            QPushButton:hover {
                background-color: #27AAE1;
            }
        """)
        self.button_layout.addWidget(self.button2)

        # Button 3
        self.button3 = QPushButton("Planes Management")
        self.button3.setIcon(QIcon("./israflightApp/images/planes_managment.png"))  # Replace with your icon path
        self.button3.setFixedSize(250, 75)  # Resize the button
        self.button3.setStyleSheet("""
            QPushButton {
                background-color: #1C3664;
                color: white;
                border-radius: 15px;
                padding: 20px;
                font-family: 'Urbanist';       /* Font family */
                font-size: 19px;
            }
            QPushButton:hover {
                background-color: #27AAE1;
            }
        """)
        self.button_layout.addWidget(self.button3)

    def initialize_controller(self, controller):
        """Initialize the controller and connect button actions."""
        self.controller = controller

        # Connect buttons to controller methods
        self.button1.clicked.connect(self.controller.open_flight_management)
        self.button2.clicked.connect(self.controller.open_add_manager)
        self.button3.clicked.connect(self.controller.open_planes_management)