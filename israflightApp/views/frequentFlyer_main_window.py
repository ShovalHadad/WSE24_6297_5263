from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QLineEdit, QDateEdit, QListWidget, QListWidgetItem
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtCore import Qt, QDate
from views.base_window import BaseWindow



class FrequentFlyerMainWindow(BaseWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("IsraFlight - Flyer")
        self.setGeometry(500, 200, 800, 600)
        self.setMinimumSize(800, 600)
        self.showMaximized()

        self.create_toolbar()


        main_layout = QHBoxLayout(self)

        # --- Right Side: Search + Results ---
        right_layout = QVBoxLayout()

        title = QLabel("🔍 Find a Flight")
        title.setFont(QFont("Urbanist", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(title)

        self.arrival_input = QLineEdit()
        self.arrival_input.setPlaceholderText("Arrival Location")

        self.landing_input = QLineEdit()
        self.landing_input.setPlaceholderText("Landing Location")

        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate())

        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())

        self.search_button = QPushButton("Search Flights")
        self.search_button.clicked.connect(self.search_flights)

        for widget in [self.arrival_input, self.landing_input, self.start_date, self.end_date, self.search_button]:
            widget.setFixedHeight(30)
            right_layout.addWidget(widget)

        self.results_list = QListWidget()
        right_layout.addWidget(self.results_list)

        main_layout.addLayout(right_layout, 2)

    def search_flights(self):
        arrival = self.arrival_input.text()
        landing = self.landing_input.text()
        start = self.start_date.date()
        end = self.end_date.date()

        # Call controller to get flights (mocked here)
        flights = self.controller.find_flights(arrival, landing, start, end)

        self.results_list.clear()
        if not flights:
            self.results_list.addItem("No matching flights found.")
            return

        for flight in flights:
            item_text = f"{flight['flight_id']}: {flight['departure']} → {flight['arrival']} on {flight['date']}"
            item = QListWidgetItem(item_text)
            self.results_list.addItem(item)

            button = QPushButton("Order")
            button.clicked.connect(lambda _, f=flight: self.open_flight_details(f))
            self.results_list.setItemWidget(item, button)

    
