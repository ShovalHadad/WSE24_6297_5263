from PySide6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QListWidget, QLineEdit, QDateTimeEdit
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class FlightManagementWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Flight Management")
        self.setGeometry(500, 200, 900, 600)
        self.setMinimumSize(900, 600)
        self.showMaximized()

        # Main Layout
        main_layout = QHBoxLayout()

        # ✈ Right Side: Flight List (Increased width)
        self.flight_list = QListWidget()
        self.flight_list.setFixedWidth(900)  # Set a fixed width
        self.flight_list.setStyleSheet("""
            QListWidget {
                margin: 60px;
                margin-top: 30px;
                background-color: #E3F2FD; /* Light blue */
                border-radius: 10px;
                padding: 15px;
                font-size: 14px;
                font-family: 'Urbanist';
                border: 2px solid #0277BD;
                width: 50%;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:selected {
                background-color: #29B6F6; /* Highlight */
                color: white;
            }
        """)
        self.flight_list.itemClicked.connect(self.select_flight)

        right_layout = QVBoxLayout()
        
        # ✈ Header for Flight List (Modified size & color)
        flight_header = QLabel("✈️ All Flights")
        flight_header.setAlignment(Qt.AlignCenter)
        flight_header.setFont(QFont("Urbanist", 18, QFont.Bold))
        flight_header.setStyleSheet("color: #01579B; margin-bottom: 10px; margin-top: 60px;")  # Dark Blue

        right_layout.addWidget(flight_header)
        right_layout.addWidget(self.flight_list)

        main_layout.addLayout(right_layout, 2)  # Increased proportion

        # 🔹 Left Side: Add Flight Button & Form
        self.add_flight_button = QPushButton("➕ Add Flight")
        self.add_flight_button.setStyleSheet("""
            QPushButton {
                background-color: #1C3664;
                color: white;
                border-radius: 8px;
                padding: 8px;
                font-size: 12px;
                width: 120px;  /* Reduced width */
                margin-left: 30px;
            }
            QPushButton:hover {
                background-color: #27AAE1;
            }
        """)
        self.add_flight_button.clicked.connect(self.show_add_flight_form)

        # 🚀 Apply styling to the entire form area
        self.form_widget = QWidget()
        self.form_widget.setStyleSheet("""
            QWidget {
                background-color: #F0F9FC;
                border-radius: 10px;
                padding: 15px;                   
                margin-top: 80px;
                margin-left: 20px;
                border: 2px solid #0277BD;
            }
            QLabel {
                border: none; /* Removes any default border */
                padding: 1px; /* Reduce extra padding */
                font-size: 14px; /* Reduce font size if necessary */
                background: none;
            }
            QLineEdit, QDateTimeEdit {
                background-color: #FFFFFF;
                border: none;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
                margin-top: 5px;
            }
            QLineEdit:focus, QDateTimeEdit:focus {
                border: 2px solid #0277BD;
                
            }
        """)

        self.form_layout = QVBoxLayout()
        self.form_widget.setLayout(self.form_layout)
        self.form_widget.hide()  # Initially hidden

        # Form Fields
        self.departure_input = QLineEdit()
        self.departure_input.setPlaceholderText("Departure Location")

        self.arrival_input = QLineEdit()
        self.arrival_input.setPlaceholderText("Arrival Location")

        self.departure_time = QDateTimeEdit()
        self.departure_time.setCalendarPopup(True)

        self.arrival_time = QDateTimeEdit()
        self.arrival_time.setCalendarPopup(True)

        self.plane_id_input = QLineEdit()
        self.plane_id_input.setPlaceholderText("Plane ID")

        self.save_button = QPushButton("💾 Save Flight")
        self.save_button.setStyleSheet("background-color: #0277BD; color: white; border-radius: 8px; padding: 10px;")
        self.save_button.clicked.connect(self.save_flight)

        self.delete_button = QPushButton("🗑 Delete Flight")
        self.delete_button.setStyleSheet("background-color: red; color: white; border-radius: 8px; padding: 10px;")
        self.delete_button.clicked.connect(self.delete_selected_flight)

        # Add Fields to Form
        form_header = QLabel("➕ Add New Flight")
        form_header.setAlignment(Qt.AlignCenter)
        form_header.setFont(QFont("Urbanist", 16, QFont.Bold))
        form_header.setStyleSheet("color: #0277BD; margin-bottom: 5px;")

        self.form_layout.addWidget(form_header)
        self.form_layout.addWidget(self.departure_input)
        self.form_layout.addWidget(self.arrival_input)
        #self.form_layout.addWidget(QLabel("Departure Time"))
        departure_time_label = QLabel("Departure Time")
        departure_time_label.setFixedHeight(80)  # Reduce height
        departure_time_label.setStyleSheet("""
            QLabel {
                border: none; /* Removes any default border */
                padding: 5px; /* Reduce extra padding */
                font-size: 14px; /* Reduce font size if necessary */
                background: none;
            } """)
        self.form_layout.addWidget(departure_time_label)
        self.form_layout.addWidget(self.departure_time)


        #self.form_layout.addWidget(QLabel("Estimated Arrival Time"))
        estimated_arrival_label = QLabel("Estimated Arrival Time")
        estimated_arrival_label.setFixedHeight(40)  # Reduce height
        estimated_arrival_label.setStyleSheet("""
            QLabel {
                border: none; /* Removes any default border */
                padding: 5px; /* Reduce extra padding */
                font-size: 14px; /* Reduce font size if necessary */
                background: none;
            } """)
        self.form_layout.addWidget(estimated_arrival_label)
        self.form_layout.addWidget(self.arrival_time)

        self.form_layout.addWidget(self.plane_id_input)
        self.form_layout.addWidget(self.save_button)
        self.form_layout.addWidget(self.delete_button)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.add_flight_button, alignment=Qt.AlignLeft)
        left_layout.addWidget(self.form_widget)
        main_layout.addLayout(left_layout, 1)  # Reduced proportion

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Load flights initially
        self.load_flights()

    def show_add_flight_form(self):
        """Shows the form to add a new flight."""
        self.form_widget.show()

    def load_flights(self):
        """Fetches and displays flights from the controller."""
        self.flight_list.clear()
        flights = self.controller.get_flights()
        for flight in flights:
            self.flight_list.addItem(f"✈ {flight.departure_location} → {flight.arrival_location} at {flight.departure_datetime}")

    def save_flight(self):
        """Saves a new flight via the controller."""
        flight_data = {
            "PlaneId": int(self.plane_id_input.text()),
            "DepartureLocation": self.departure_input.text(),
            "ArrivalLocation": self.arrival_input.text(),
            "DepartureDateTime": self.departure_time.dateTime().toString(Qt.ISODate),
            "EstimatedArrivalDateTime": self.arrival_time.dateTime().toString(Qt.ISODate),
        }

        success = self.controller.add_flight(flight_data)
        if success:
            self.load_flights()  # Refresh list
            self.form_widget.hide()  # Hide form after saving
        else:
            self.flight_list.addItem("⚠️ Error adding flight")

    def select_flight(self, item):
        """Selects a flight from the list."""
        flight_text = item.text()
        flight_id = flight_text.split()[1]  # Extract flight ID
        self.selected_flight_id = int(flight_id)

    def delete_selected_flight(self):
        """Deletes the selected flight."""
        if hasattr(self, "selected_flight_id"):
            success = self.controller.delete_flight(self.selected_flight_id)
            if success:
                self.load_flights()
        else:
            self.flight_list.addItem("⚠️ No flight selected")
