from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QHBoxLayout, QComboBox
)
from PySide6.QtCore import Qt

class UserMainWindow(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("User Dashboard")
        self.setGeometry(100, 100, 800, 600)

        # Main Layout
        main_layout = QHBoxLayout(self)

        # ✈️ Left Side: Upcoming Landings (with filter)
        self.landing_list = QListWidget()
        self.landing_list.setStyleSheet("background-color: #F0F9FC; padding: 5px;")
        
        # Time filter dropdown (1-5 hours ahead)
        self.time_filter = QComboBox()
        self.time_filter.addItems(["1 Hour Ahead", "2 Hours Ahead", "3 Hours Ahead", "4 Hours Ahead", "5 Hours Ahead"])
        self.time_filter.currentIndexChanged.connect(self.filter_landings)

        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("🛬 Upcoming Landings", alignment=Qt.AlignCenter))
        left_layout.addWidget(self.time_filter)
        left_layout.addWidget(self.landing_list)
        main_layout.addLayout(left_layout, 1)  # Left side

        # ✈️ Right Side: Flights (with search)
        self.flight_list = QListWidget()
        self.flight_list.setStyleSheet("background-color: #F0F9FC; padding: 5px;")

        # Search field
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("🔍 Search flights...")
        self.search_field.textChanged.connect(self.search_flights)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("✈️ All Flights", alignment=Qt.AlignCenter))
        right_layout.addWidget(self.search_field)
        right_layout.addWidget(self.flight_list)
        main_layout.addLayout(right_layout, 2)  # Right side (wider)

        self.setLayout(main_layout)

        # Load initial data
        self.load_flights()
        self.load_landings()

    def load_flights(self):
        """Loads all available flights into the list."""
        self.flight_list.clear()
        flights = self.controller.get_flights()
        for flight in flights:
            self.flight_list.addItem(f"✈️ {flight['departure']} → {flight['destination']} at {flight['time']}")

    def load_landings(self):
        """Loads all upcoming landings into the list."""
        self.landing_list.clear()
        landings = self.controller.get_landings(hours_ahead=1)  # Default: 1 hour ahead
        for landing in landings:
            self.landing_list.addItem(f"🛬 {landing['flight']} arriving at {landing['time']}")

    def search_flights(self):
        """Filters flights based on search input."""
        search_text = self.search_field.text().lower()
        self.flight_list.clear()
        flights = self.controller.get_flights()
        for flight in flights:
            if search_text in f"{flight['departure']} {flight['destination']} {flight['time']}".lower():
                self.flight_list.addItem(f"✈️ {flight['departure']} → {flight['destination']} at {flight['time']}")

    def filter_landings(self):
        """Filters upcoming landings based on selected time range."""
        selected_hours = int(self.time_filter.currentText().split()[0])  # Extract number from "1 Hour Ahead"
        self.landing_list.clear()
        landings = self.controller.get_landings(hours_ahead=selected_hours)
        for landing in landings:
            self.landing_list.addItem(f"🛬 {landing['flight']} arriving at {landing['time']}")
