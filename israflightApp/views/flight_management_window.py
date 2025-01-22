from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from views.base_window import BaseWindow


class FlightManagementWindow(BaseWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Flight Management")
        self.setGeometry(500, 200, 800, 600)
        self.setMinimumSize(800, 600)
        self.showMaximized()

        self.create_toolbar()

        # Set central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Title Label
        title_label = QLabel("Flight Management")
        title_label.setFont(QFont("Urbanist", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Horizontal layout for buttons
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        # Add Flight Button
        add_flight_button = QPushButton("Add Flight")
        add_flight_button.setStyleSheet("""
            QPushButton {
                background-color: #1C3664;
                color: white;
                border-radius: 15px;
                padding: 10px;
                font-family: 'Urbanist';
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #27AAE1;
            }
        """)
        add_flight_button.clicked.connect(self.add_flight_action)
        button_layout.addWidget(add_flight_button)

        # Edit Flight Button
        edit_flight_button = QPushButton("Edit Flight")
        edit_flight_button.setStyleSheet("""
            QPushButton {
                background-color: #1C3664;
                color: white;
                border-radius: 15px;
                padding: 10px;
                font-family: 'Urbanist';
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #27AAE1;
            }
        """)
        edit_flight_button.clicked.connect(self.edit_flight_action)
        button_layout.addWidget(edit_flight_button)

        # Delete Flight Button
        delete_flight_button = QPushButton("Delete Flight")
        delete_flight_button.setStyleSheet("""
            QPushButton {
                background-color: #1C3664;
                color: white;
                border-radius: 15px;
                padding: 10px;
                font-family: 'Urbanist';
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #27AAE1;
            }
        """)
        delete_flight_button.clicked.connect(self.delete_flight_action)
        button_layout.addWidget(delete_flight_button)

    def add_flight_action(self):
        print("Add Flight button clicked!")

    def edit_flight_action(self):
        print("Edit Flight button clicked!")

    def delete_flight_action(self):
        print("Delete Flight button clicked!")
