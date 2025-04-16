from PySide6.QtWidgets import *
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtCore import Qt, QDate
from views.base_window import BaseWindow
from PySide6.QtGui import QGuiApplication
from models.frequent_flyer import FrequentFlyer
from models.flight import Flight

class FrequentFlyerMainWindow(BaseWindow):
    def __init__(self, controller, flyer_id):
        super().__init__()
        self.controller = controller
        self.api_base_url = "http://localhost:5177/api/FrequentFlyer"
        screen = QGuiApplication.primaryScreen()
        flyer = FrequentFlyer.get_flyer_by_id(self.api_base_url, flyer_id)
        #screen_width = screen.size().width()

        self.setWindowTitle("IsraFlight - Frequent Flyer")
        self.setGeometry(screen.geometry())
        self.setMinimumSize(800, 600)
        self.showMaximized()

        self.create_toolbar()

        # ✅ יצירת לייאאוט ראשי מבלי לחבר אותו לחלון
        main_layout = QHBoxLayout()

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
        #self.search_button.clicked.connect(self.search_flights)

        for widget in [self.arrival_input, self.landing_input, self.start_date, self.end_date, self.search_button]:
            widget.setFixedHeight(30)
            right_layout.addWidget(widget)

        self.results_list = QListWidget()
        right_layout.addWidget(self.results_list)

        left_layout = QVBoxLayout()
        title = QLabel("Personal Details")
        title.setFont(QFont("Urbanist", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(title)
        self.first_input = QLineEdit()
        self.first_input.setPlaceholderText(f"{flyer.first_name}")
        self.last_input = QLineEdit()
        self.last_input.setPlaceholderText(f"{flyer.last_name}")
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText(f"{flyer.username}")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText(f"{flyer.email}")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText(f"{flyer.phone_number}")
        left_layout.addWidget( QLabel("First Name:"))
        left_layout.addWidget(self.first_input)
        left_layout.addWidget( QLabel("Last Name:"))
        left_layout.addWidget(self.last_input)
        left_layout.addWidget( QLabel("Username:"))
        left_layout.addWidget(self.user_input)
        left_layout.addWidget( QLabel("Email:"))
        left_layout.addWidget(self.email_input)
        left_layout.addWidget(QLabel("Phone Number:"))
        left_layout.addWidget(self.phone_input)
        self.update_button = QPushButton("Update")
        left_layout.addWidget(self.update_button)
  # Right Side: Flight List
        self.flight_list = QListWidget()
        self.registered_flights_list = []
        self.flight_list.setFixedWidth(int(screen.size().width()/2 - 10))
        self.flight_list.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        #self.flight_list.setFixedSize(600, 620)  # Adjust width
        self.flight_list.setStyleSheet("""
            QListWidget {
                background-color: white; 
                color: #1C3664;
                border-radius: 10px;
                margin-top: 15px;
                margin-bottom: 70px;                    
                padding: 15px;
                font-size: 14px;
                font-family: 'Urbanist';
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:selected {
                background-color: #29B6F6; 
                color: white;
            }
            /* SCROLLBAR DESIGN */
            QListWidget::verticalScrollBar {
                border: none;
                background: transparent;
                width: 8px;  
            }
            QListWidget::verticalScrollBar::handle {
                background: rgba(0, 0, 0, 0.2);
                border-radius: 4px;  
                min-height: 30px;  
                border: none;                       
            }
            QListWidget::verticalScrollBar::handle:hover {
                background: rgba(0, 0, 0, 0.3); 
                border: none;
            }
            QListWidget::verticalScrollBar::add-line,
            QListWidget::verticalScrollBar::sub-line {
                background: none;
                border: none;
            }
            """)
        if flyer.flights_ids:
            
            flights = self.controller.get_flights(flyer.flights_ids)
            for flight in flights:
                flight_info = f"{flight.flight_id}   | ✈ {flight.departure_location} → {flight.arrival_location} at {flight.departure_datetime}"
                self.flight_list.addItem(flight_info)

                #item = QListWidgetItem(f"Flight ID: {flight_id}")
                #self.flight_list.addItem(item)
            #self.flight_list.itemClicked.connect(self.show_flight_ticket())
        else:
            self.flight_list.addItem("No registered flights.")
        registered_flights_label = QLabel("Registered Flights:")
        registered_flights_label.setFont(QFont("Urbanist", 14))
        registered_flights_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(registered_flights_label)
        left_layout.addWidget(self.flight_list)
        main_layout.addLayout(left_layout, 2)

        main_layout.addLayout(right_layout, 2)


        # ✅ עטיפה בווידג'ט והגדרת כ-central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    
