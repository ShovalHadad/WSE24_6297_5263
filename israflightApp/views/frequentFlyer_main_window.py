from PySide6.QtWidgets import *
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtCore import Qt, QDate
from views.base_window import BaseWindow
from PySide6.QtGui import QGuiApplication
from models.flight import Flight
from PySide6.QtWidgets import QGraphicsOpacityEffect

class FrequentFlyerMainWindow(BaseWindow):
    def __init__(self, controller, flyer_id):
        super().__init__()
        self.controller = controller
        screen = QGuiApplication.primaryScreen()
        flyer = self.controller.get_flyer_by_id(flyer_id)

        self.setWindowTitle("IsraFlight - Frequent Flyer")
        self.setGeometry(screen.geometry())
        self.setMinimumSize(800, 600)
        self.showMaximized()

        self.create_toolbar()

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(80, 50, 80, 50)  # ✅ Add page margin

        # --- Right Side: Search + Results ---
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignTop)

        search_container = QVBoxLayout()
        search_container.setSpacing(5)

        # Title for booking section
        book_title = QLabel("BOOK A FLIGHT")
        book_title.setFont(QFont("Urbanist", 18, QFont.Black))
        book_title.setStyleSheet("color: #1C3664; margin-top: 60px; margin-bottom: 30px; font-weight: 1000;")
        book_title.setAlignment(Qt.AlignCenter)
        search_container.addWidget(book_title)

        search_row = QHBoxLayout()
        search_row.setSpacing(15)

        def styled_input(label_text, widget):
            container = QVBoxLayout()
            container.setSpacing(2.5)
            label = QLabel(label_text)
            label.setFont(QFont("Urbanist", 12, QFont.Bold))
            label.setStyleSheet("color: #27AAE1;")
            label.setAlignment(Qt.AlignLeft)
            widget.setFixedSize(200, 50)
            widget.setStyleSheet("""
                QLineEdit, QDateEdit {
                    background-color: #FFFFFF;
                    border-radius: 10px;
                    padding: 6px;
                    font-size: 13px;
                    font-family: 'Urbanist';
                    color: #222;
                    margin-bottom: 10px;
                    margin-top: 5px;
                }
            """)
            container.addWidget(label)
            container.addWidget(widget)
            return container
        
        self.landing_input = QLineEdit()
        self.landing_input.setPlaceholderText("Landing location")
        search_row.addLayout(styled_input("Landing location", self.landing_input))

        self.arrival_input = QLineEdit()
        self.arrival_input.setPlaceholderText("Arrival location")
        search_row.addLayout(styled_input("Arrival location", self.arrival_input))

        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate())
        search_row.addLayout(styled_input("Landing date", self.start_date))

        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        search_row.addLayout(styled_input("Arrival date", self.end_date))

        

        search_container.addLayout(search_row)

        self.search_button = QPushButton("Search flight")
        self.search_button.setFixedSize(150, 55)
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #1C3664;
                color: white;
                border-radius: 12px;
                font-size: 15px;
                font-family: 'Urbanist';
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #27AAE1;
            }
        """)
        search_container.addWidget(self.search_button, alignment=Qt.AlignHCenter)

        # 🔹 Temporary image shown before search
        self.flight_image = QLabel()
        self.flight_image.setContentsMargins(0, 110, 0, 0)
        self.flight_image.setPixmap(QPixmap("./israflightApp/images/findFlight.png").scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.flight_image.setAlignment(Qt.AlignHCenter)
        opacity = QGraphicsOpacityEffect()
        opacity.setOpacity(0.4)  
        self.flight_image.setGraphicsEffect(opacity)
        search_container.addWidget(self.flight_image)


        right_layout.addLayout(search_container)

        results_label = QLabel("Matching Flights:")
        results_label.setFont(QFont("Urbanist", 14, QFont.Bold))
        results_label.setStyleSheet("color: #0B4F6C; margin-top: 10px")
        right_layout.addWidget(results_label)

        self.results_list = QListWidget()
        self.results_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 10px;
                font-size: 13px;
                font-family: 'Urbanist';
            }
        """)
        results_label.hide()
        self.results_list.hide()

        right_layout.addWidget(self.results_list)







        # --- Left Side: Flyer Info in a card ---
        left_layout = QVBoxLayout()
        form_card = QFrame()
        form_card.setFixedWidth(500)
        form_card.setFixedHeight(430)
        form_card.setObjectName("formCard")
        form_card.setStyleSheet("""
            QFrame#formCard {
                background-color: white;
                border-radius: 20px;
                padding: 30px;
                margin-bottom: 5px;
                margin-top: 30px;
            }
        """)

        form_inner_layout = QHBoxLayout(form_card)
        form_inner_layout.setSpacing(10)

        picture_container = QVBoxLayout()
        picture_label = QLabel()
        pixmap = QPixmap("./israflightApp/images/user.png")
        pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        picture_label.setPixmap(pixmap)
        picture_label.setAlignment(Qt.AlignHCenter)
        picture_label.setStyleSheet("""margin-top: 20px; """)

        hi_label = QLabel(f"Hi {flyer.first_name}")
        hi_label.setAlignment(Qt.AlignHCenter)
        hi_label.setStyleSheet("""
            font-size: 14px;
            font-family: 'Urbanist';
            color: #1C3664;
            margin-top: 2px;
        """)

        picture_container.addWidget(picture_label)
        picture_container.addWidget(hi_label)
        #picture_container.setSpacing(0)
        form_inner_layout.addLayout(picture_container)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        def add_field(label_text, line_edit):
            label = QLabel(label_text)
            label.setAlignment(Qt.AlignLeft)
            label.setStyleSheet("""
                font-size: 13px;
                font-family: 'Urbanist';
                color: #1C3664;
                margin-bottom: 3px;
            """)

            line_edit.setFixedWidth(250)
            line_edit.setFixedHeight(30)
            line_edit.setStyleSheet("""
                QLineEdit {
                    background-color: white;
                    border-radius: 10px;
                    padding: 8px;
                    font-size: 13px;
                    border: 1px solid #ccc;
                    font-family: 'Urbanist';
                    margin-bottom: 0px;
                    margin-top: 0px;
                                    
                }
            """)

            container = QVBoxLayout()
            container.setSpacing(2)
            container.addWidget(label)
            container.addWidget(line_edit)
            form_layout.addLayout(container)

        self.first_input = QLineEdit()
        self.first_input.setPlaceholderText(f"{flyer.first_name}")
        add_field("First Name:", self.first_input)

        self.last_input = QLineEdit()
        self.last_input.setPlaceholderText(f"{flyer.last_name}")
        add_field("Last Name:", self.last_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText(f"{flyer.email}")
        add_field("Email:", self.email_input)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText(f"{flyer.phone_number}")
        add_field("Phone Number:", self.phone_input)

        self.update_button = QPushButton("Update")
        self.update_button.setFixedSize(130, 38)
        self.update_button.setStyleSheet("""
            QPushButton {
                background-color: #1C3664;
                color: white;
                border-radius: 12px;
                padding: 10px 16px;
                font-size: 14px;
                font-family: 'Urbanist';
                margin-top: 5px;
            }
            QPushButton:hover {
                background-color: #27AAE1;
            }
        """)

        form_layout.addWidget(self.update_button)
        form_inner_layout.addLayout(form_layout)

        left_layout.addWidget(form_card)
        left_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)


        self.flight_list = QListWidget()
        self.registered_flights_list = []
        self.flight_list.setFixedWidth(int(screen.size().width()/3 - 100))
        self.flight_list.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.flight_list.setStyleSheet("""
            QListWidget {
                background-color: white;
                color: #1C3664;
                border-radius: 10px;
                margin-top: 15px;
                margin-bottom: 30px;
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

        # עטיפה בלייאאוט אנכי עם מרווח קטן
        registered_flights_container = QVBoxLayout()
        registered_flights_container.setSpacing(5)  # קטן

        registered_label = QLabel("Registered Flights:")
        registered_label.setFont(QFont("Urbanist", 13))
        registered_label.setContentsMargins(0, 0, 0, 10)
        registered_label.setAlignment(Qt.AlignCenter)

        registered_flights_container.addWidget(registered_label)

        self.flight_list = QListWidget()
        self.flight_list.setFixedWidth(500)
        self.flight_list.setStyleSheet("""
            QListWidget {
                background-color: white;
                color: #1C3664;
                border-radius: 10px;
                padding: 10px;
                font-size: 13px;
                font-family: 'Urbanist';
            }
        """)
        if flyer.flights_ids:
            flights = self.controller.get_flights(flyer.flights_ids)
            for flight in flights:
                flight_info = f"{flight.flight_id}   | ✈ {flight.departure_location} → {flight.arrival_location} at {flight.departure_datetime}"
                self.flight_list.addItem(flight_info)
        else:
            self.flight_list.addItem("No registered flights.")

        registered_flights_container.addWidget(self.flight_list)
        left_layout.addLayout(registered_flights_container)


        main_layout.addLayout(right_layout, 3)  # Search section on the left (wider)
        main_layout.addLayout(left_layout, 1)   # User details + registered flights on the right
        main_layout.setSpacing(60)


        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        #self.search_button.clicked.connect(self.show_results_section)

    def show_results_section(self):
        self.results_label.show()
        self.results_list.show()
        self.flight_image.hide()  # 🔹 הסתרת התמונה לאחר לחיצה על כפתור החיפוש

