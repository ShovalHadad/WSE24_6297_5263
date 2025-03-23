from PySide6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QListWidget, QLineEdit, QDateTimeEdit, QSizePolicy
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

        # 🌟 Main Layout
        main_layout = QHBoxLayout()

        # ✈ Right Side: Flight List
        self.flight_list = QListWidget()
        self.flight_list.setFixedSize(600, 650)  # Adjust width
        self.flight_list.setStyleSheet("""
            QListWidget {
                background-color: white; 
                color: #1C3664;
                border-radius: 10px;
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
        self.flight_list.itemClicked.connect(self.select_flight)

        # ✅ Right Side Layout (Flight List)
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.flight_list)
        main_layout.addLayout(right_layout, 2)

        # 🔹 Left Side: Add Flight Button & Form
        self.add_flight_button = QPushButton("➕ Add Flight")
        self.add_flight_button.setFixedHeight(45)
        self.add_flight_button.setObjectName("addFlightButton")
        self.add_flight_button.setStyleSheet("""
            QPushButton#addFlightButton {
                background-color: #1C3664;
                color: white;
                border-radius: 20px;
                padding: 8px;
                font-size: 14px;
                width: 140px;
                border: none;
            }
            QPushButton#addFlightButton:hover {
                background-color: #3A5A89;
            }
            QPushButton#addFlightButton:pressed {
                background-color: #CDEBF6;
                border: none;
            }
        """)
        self.add_flight_button.clicked.connect(self.toggle_add_flight_form)

        # 🚀 Flight Form (Initially Hidden)
        self.form_widget = QWidget()
        self.form_widget.setFixedSize(580, 620)
        self.form_widget.setStyleSheet("""
            QWidget {
                background-color: #CDEBF6;  
                border-radius: 20px;  
                padding: 2px;                   
                border: none;
            }
        """)
        self.form_widget.hide()  # Form is hidden initially

        self.form_layout = QVBoxLayout()
        self.form_widget.setLayout(self.form_layout)

        # 🌟 Form Header
        self.form_header = QLabel("ADD NEW FLIGHT")
        self.form_header.setAlignment(Qt.AlignCenter)
        self.form_header.setFixedHeight(60)
        self.form_header.setFont(QFont("Urbanist", 12, QFont.Bold))
        self.form_header.setStyleSheet("color: #123456; margin-bottom: 0px; margin-top: 5px; text-transform: uppercase;")
        self.form_layout.addWidget(self.form_header)


        # 📝 Function to create form fields with labels
        def create_form_field(label_text, input_widget):
            container = QVBoxLayout()
            container.setSpacing(1)  

            label = QLabel(label_text)
            label.setAlignment(Qt.AlignLeft)
            label.setFont(QFont("Urbanist", 12, QFont.Bold))
            label.setStyleSheet("""
                QLabel {
                    color: #123456;
                    padding-top: 8px;  
                    padding-bottom: 8px;  
                    font-size: 12px;
                    margin-left: 15px; 
                }
            """)
            label.setFixedHeight(28)  
            input_widget.setStyleSheet("""
                QLineEdit, QDateTimeEdit {
                    background-color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 8px;
                    font-size: 10px;
                    margin-top: 3px;
                    margin-bottom: 8px;  
                    margin-left: 25px; 
                    margin-right: 25px;                                      
                    color: black;
                    max-width: 500px;                   
                }
                QLineEdit::placeholder, QDateTimeEdit::placeholder {
                    color: gray;
                }
            """)

            container.addWidget(label)
            container.addWidget(input_widget)
            return container

        # 📋 Form Fields
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

        # 🔗 Add Form Fields
        self.form_layout.addLayout(create_form_field("Arrival location", self.arrival_input))
        self.form_layout.addLayout(create_form_field("Departure location", self.departure_input))
        self.form_layout.addLayout(create_form_field("Departure Date Time", self.departure_time))
        self.form_layout.addLayout(create_form_field("Estimated Arrival Date Time", self.arrival_time))
        self.form_layout.addLayout(create_form_field("Plane ID", self.plane_id_input))

        # 💾 Save Button
        self.save_button = QPushButton("Save Flight")
        self.save_button.setFixedHeight(45)
        self.save_button.setFixedWidth(140)  # Adjust width as needed
        self.save_button.setObjectName("saveButton")
        self.save_button.setStyleSheet("""
            QPushButton#saveButton {
                background-color: #1C3664;
                color: white;
                border-radius: 20px;
                padding: 8px;
                font-size: 14px;
                border: none;
            }
            QPushButton#saveButton:hover {
                background-color: #3A5A89;
            }
            QPushButton#saveButton:pressed {
                background-color: #0D253F;
            }
        """)
        self.save_button.clicked.connect(self.save_flight)
        #self.form_layout.addWidget(self.save_button, alignment=Qt.AlignCenter)

        # 🗑️ Delete Button
        self.delete_button = QPushButton("Delete Flight")
        self.delete_button.setFixedHeight(45)
        self.delete_button.setFixedWidth(140)  # Adjust width as needed
        self.delete_button.setObjectName("deleteButton")
        self.delete_button.setStyleSheet("""
            QPushButton#deleteButton {
                background-color: #D32F2F;
                color: white;
                border-radius: 20px;
                padding: 4px;
                font-size: 14px;
                border: none;
            }
            QPushButton#deleteButton:hover {
                background-color: #B71C1C;
            }
            QPushButton#deleteButton:pressed {
                background-color: #7F0000;
            }
        """)
        self.delete_button.clicked.connect(self.delete_selected_flight)
        self.delete_button.hide()  # Hide by default

        self.save_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.delete_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        button_row = QHBoxLayout()
        button_row.setSpacing(6)  # רווח בין הכפתורים
        button_row.setContentsMargins(0, 0, 0, 0)  # ביטול שוליים פנימיים
        button_row.addWidget(self.save_button)
        button_row.addWidget(self.delete_button)
        self.form_layout.addLayout(button_row)


        # 📦 Left Side Container (Keeps Layout Consistent)
        left_container = QWidget()
        left_container.setFixedSize(600, 650)
        left_container_layout = QVBoxLayout(left_container)
        left_container_layout.addWidget(self.add_flight_button, alignment=Qt.AlignCenter)
        left_container_layout.addWidget(self.form_widget)

        main_layout.addWidget(left_container, 1)

        # 📌 Set Central Widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        central_widget.setStyleSheet("background-color: #F0F4F8;")
        self.setCentralWidget(central_widget)

        # 🚀 Load flights initially
        self.load_flights()

    def toggle_add_flight_form(self):
        """Toggles the visibility of the Add Flight form."""
        if self.form_widget.isVisible():
            self.form_widget.hide()
            self.add_flight_button.show()
        else:
            self.form_widget.show()
            self.add_flight_button.hide()


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
        else:
            self.flight_list.addItem("⚠️ Error adding flight")


    def update_flight(self):
        """Updates an existing flight via the controller."""
        flight_data = {
            "FlightId": self.selected_flight_id,
            "PlaneId": int(self.plane_id_input.text()),
            "DepartureLocation": self.departure_input.text(),
            "ArrivalLocation": self.arrival_input.text(),
            "DepartureDateTime": self.departure_time.dateTime().toString(Qt.ISODate),
            "EstimatedArrivalDateTime": self.arrival_time.dateTime().toString(Qt.ISODate),
        }

        success = self.controller.update_flight(flight_data)
        if success:
            self.load_flights()
            self.form_widget.hide()
            self.add_flight_button.show()
        else:
            self.flight_list.addItem("⚠️ Error updating flight")




    def select_flight(self, item):
        """Selects a flight from the list and loads it into the form for editing."""
        flight_text = item.text()
        selected_index = self.flight_list.currentRow()
        flights = self.controller.get_flights()
        selected_flight = flights[selected_index]
        self.selected_flight_id = selected_flight.flight_id

        # Fill form fields
        self.departure_input.setText(selected_flight.departure_location)
        self.arrival_input.setText(selected_flight.arrival_location)
        self.departure_time.setDateTime(selected_flight.departure_datetime)
        self.arrival_time.setDateTime(selected_flight.estimated_arrival_datetime)
        self.plane_id_input.setText(str(selected_flight.plane_id))

        # Change button to "Update Flight"
        self.save_button.setText("Update Flight")
        self.form_header.setText("UPDATE FLIGHT")
        self.delete_button.show()


        # Disconnect old slot to avoid stacking calls
        try:
            self.save_button.clicked.disconnect()
        except TypeError:
            pass
        self.save_button.clicked.connect(self.update_flight)




    def delete_selected_flight(self):
        """Deletes the selected flight."""
        if hasattr(self, "selected_flight_id"):
            success = self.controller.delete_flight(self.selected_flight_id)
            if success:
                self.load_flights()
        else:
            self.flight_list.addItem("⚠️ No flight selected")
