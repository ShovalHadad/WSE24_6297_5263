from PySide6.QtWidgets import *
from PySide6.QtGui import QFont, QPixmap, QIcon
from PySide6.QtCore import Qt
from models.ticket import FlightTicket
from views.base_window import BaseWindow
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

class FlightWindow(BaseWindow):
    def __init__(self, controller, flight_id, flyer_id, is_booking=0):
        super().__init__()
        self.controller = controller
        self.flight_id = flight_id
        self.flyer_id = flyer_id
        self.is_booking = is_booking
        self.flight = controller.get_flight(flight_id)
    
    # Ensure the window is large enough
        self.setMinimumSize(800, 600)  # Increase from 600, 500
    
    # Setup window based on mode
        if is_booking == 0:
            self.setWindowTitle(f"flight booking #{flight_id}")
        else:
            self.setWindowTitle(f"flight #{flight_id}")
    
    # Create UI    
        self.init_ui()
    
    # Force layout update
        self.adjustSize()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
    
        # Now create and set the main layout on the central widget
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Flight information header with plane icon
        header_layout = QHBoxLayout()
        
        # Try to add plane icon - with proper error handling
        plane_icon = QLabel()
        try:
            #pixmap = QPixmap("./images/f_managment.png")
            pixmap = QPixmap("./israflightApp/images/f_managment.png")  # Tehila path
            #pixmap = QPixmap("./images/flight_managment.png")
            #pixmap = QPixmap("./israflightApp/images/flight_managment.png") # Tehila path
            if not pixmap.isNull():
                plane_icon.setPixmap(pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                header_layout.addWidget(plane_icon)
        except Exception as e:
            print(f"Failed to load airplane icon: {e}")
            # Continue without the icon
            
        # Flight title
        if self.is_booking == 0:
            header_text = f"book the flight #{self.flight_id}"
        else:
            header_text = f"flight information #{self.flight_id}"
            
        flight_info = QLabel(f"{header_text}: {self.flight.departure_location} → {self.flight.arrival_location}")
        flight_info.setFont(QFont("Urbanist", 18, QFont.Bold))
        flight_info.setStyleSheet("color: #1C3664; margin: 10px 0;")
        flight_info.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(flight_info, 1)
        main_layout.addLayout(header_layout)
        
        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        divider.setStyleSheet("background-color: #27AAE1;")
        main_layout.addWidget(divider)
        
        # Flight details in a styled card
        details_card = QFrame()
        details_card.setObjectName("detailsCard")
        details_card.setStyleSheet("""
            QFrame#detailsCard {
                background-color: #F5F8FA;
                border-radius: 15px;
                padding: 15px;
            }
            QLabel {
                font-family: 'Urbanist';
                color: #333;
            }
            QLabel.header {
                font-weight: bold;
                color: #1C3664;
            }
        """)
        
        details_layout = QGridLayout(details_card)
        details_layout.setSpacing(15)
        details_layout.setContentsMargins(20, 20, 20, 20)
        
        # Add detailed flight information
        # Column 1
        detail_labels = [
            ("Flight Number: ", f"{self.flight.flight_id}"),
            ("Departure Location: ", f"{self.flight.departure_location}"),
            ("Departure Datetime", f"{self.flight.departure_datetime}"),
        ]
        
        # Column 2
        detail_labels2 = [
            ("Status: ", "Ready for flight"), 
            ("Arrival Location", f"{self.flight.arrival_location}"),
            ("Arrival Datetime", f"{self.flight.estimated_arrival_datetime}"),
        ]
        
        # Add first column
        for i, (label, value) in enumerate(detail_labels):
            header = QLabel(label)
            header.setProperty("class", "header")
            header.setFont(QFont("Urbanist", 12, QFont.Bold))
            
            value_label = QLabel(value)
            value_label.setFont(QFont("Urbanist", 12))
            
            details_layout.addWidget(header, i, 0)
            details_layout.addWidget(value_label, i, 1)
        
        # Add second column
        for i, (label, value) in enumerate(detail_labels2):
            header = QLabel(label)
            header.setProperty("class", "header")
            header.setFont(QFont("Urbanist", 12, QFont.Bold))
            
            value_label = QLabel(value)
            value_label.setFont(QFont("Urbanist", 12))
            
            details_layout.addWidget(header, i, 2)
            details_layout.addWidget(value_label, i, 3)
        
        main_layout.addWidget(details_card)
        
        # For booking mode, show ticket class selection
        if self.is_booking == 0:
            # Ticket class selection with visual indicators
            seats_label = QLabel("Select seat type: ")
            seats_label.setFont(QFont("Urbanist", 14, QFont.Bold))
            seats_label.setStyleSheet("color: #1C3664; margin-top: 10px;")
            main_layout.addWidget(seats_label)
            
            # Ticket class options in cards
            class_selection_layout = QHBoxLayout()
            class_selection_layout.setSpacing(15)
            
            self.class_buttons = []
            
            # Create radio button for each class
            class_info = [
                {"name": "First Class", "price": "$1500", "description": "Premium experience with fully adjustable seats"},
                {"name": "Business Class", "price": "$800", "description": "Comfortable seats with increased legroom"},
                {"name": "Economy Class", "price": "$300", "description": "Standard and comfortable ride"}
            ]
            
            self.class_button_group = QButtonGroup()
            
            for i, info in enumerate(class_info):
                class_card = QFrame()
                class_card.setObjectName(f"classCard{i}")
                class_card.setStyleSheet(f"""
                    QFrame#classCard{i} {{
                        background-color: white;
                        border: 1px solid #DDD;
                        border-radius: 10px;
                        padding: 10px;
                    }}
                    QFrame#classCard{i}:hover {{
                        border: 2px solid #27AAE1;
                    }}
                """)
                
                card_layout = QVBoxLayout(class_card)
                
                # Radio button for selection
                radio = QRadioButton(info["name"])
                radio.setFont(QFont("Urbanist", 13, QFont.Bold))
                radio.setStyleSheet("color: #1C3664;")
                self.class_button_group.addButton(radio, i+1)  # Use i+1 to match ticket type values
                
                # Price
                price_label = QLabel(info["price"])
                price_label.setFont(QFont("Urbanist", 16, QFont.Bold))
                price_label.setStyleSheet("color: #27AAE1;")
                
                # Description
                desc_label = QLabel(info["description"])
                desc_label.setWordWrap(True)
                desc_label.setFont(QFont("Urbanist", 11))
                desc_label.setStyleSheet("color: #555;")
                
                card_layout.addWidget(radio)
                card_layout.addWidget(price_label)
                card_layout.addWidget(desc_label)
                
                class_selection_layout.addWidget(class_card)
                self.class_buttons.append(radio)
            
            # Set default selection to Economy (last option)
            self.class_buttons[2].setChecked(True)
            
            main_layout.addLayout(class_selection_layout)
            
        else:
            # For view mode, show ticket information if available
            ticket_info_card = QFrame()
            ticket_info_card.setObjectName("ticketInfoCard")
            ticket_info_card.setStyleSheet("""
                QFrame#ticketInfoCard {
                    background-color: white;
                    border: 1px solid #27AAE1;
                    border-radius: 15px;
                    padding: 15px;
                    margin-top: 20px;
                }
            """)
            
            ticket_layout = QVBoxLayout(ticket_info_card)
            
            # Try to get the ticket for this flight and user
            ticket_title = QLabel("Ticket details: ")
            ticket_title.setFont(QFont("Urbanist", 14, QFont.Bold))
            ticket_title.setStyleSheet("color: #1C3664;")
            ticket_layout.addWidget(ticket_title)
            
            # Try to fetch the ticket information
            try:
                ticket = self.controller.get_ticket_by_flight_user(self.flight_id, self.flyer_id)
                
                if ticket:
                    ticket_grid = QGridLayout()
                    
                    # Add ticket details
                    seat_class = self.controller.get_seat_class_name(ticket.ticket_type)
                    
                    ticket_details = [
                        ("Ticket number: ", f"{ticket.ticket_id}"),
                        ("Seat type: ", f"{seat_class}"),
                        ("rice: ", f"{ticket.price}"),
                        ("Order date: ", f"{ticket.created_date.strftime('%d/%m/%Y %H:%M')}")
                    ]
                    
                    for i, (label, value) in enumerate(ticket_details):
                        header = QLabel(label)
                        header.setProperty("class", "header")
                        header.setFont(QFont("Urbanist", 12, QFont.Bold))
                        
                        value_label = QLabel(value)
                        value_label.setFont(QFont("Urbanist", 12))
                        
                        ticket_grid.addWidget(header, i, 0)
                        ticket_grid.addWidget(value_label, i, 1)
                    
                    ticket_layout.addLayout(ticket_grid)
                else:
                    # No ticket found
                    no_ticket = QLabel("No ticket found for this flight.")
                    no_ticket.setFont(QFont("Urbanist", 12))
                    no_ticket.setAlignment(Qt.AlignCenter)
                    ticket_layout.addWidget(no_ticket)
            except Exception as e:
                print(f"Error loading ticket information: {e}")
                error_label = QLabel("An error occurred while loading the card details.")
                error_label.setFont(QFont("Urbanist", 12))
                error_label.setAlignment(Qt.AlignCenter)
                ticket_layout.addWidget(error_label)
            
            main_layout.addWidget(ticket_info_card)
        
        # Buttons section
        buttons_layout = QHBoxLayout()
        
        # Different buttons based on mode
        if self.is_booking == 0:
            self.book_button = QPushButton("Book a ticket")
            self.book_button.setFixedSize(200, 50)
            self.book_button.setFont(QFont("Urbanist", 14, QFont.Bold))
            self.book_button.setStyleSheet("""
                QPushButton {
                    background-color: #1C3664;
                    color: white;
                    border-radius: 15px;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background-color: #27AAE1;
                }
            """)
            self.book_button.clicked.connect(self.book_flight)
            buttons_layout.addWidget(self.book_button)
        
        self.close_button = QPushButton("close")
        self.close_button.setFixedSize(150, 50)
        self.close_button.setFont(QFont("Urbanist", 14))
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #F5F5F5;
                color: #333;
                border: 1px solid #CCC;
                border-radius: 15px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #E5E5E5;
            }
        """)
        self.close_button.clicked.connect(self.close_window)
        self.print_button = QPushButton("print")
        self.print_button.setFixedSize(150, 50)
        self.print_button.setFont(QFont("Urbanist", 14))
        self.print_button.setStyleSheet("""
            QPushButton {
                background-color: #F5F5F5;
                color: #333;
                border: 1px solid #CCC;
                border-radius: 15px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #E5E5E5;
            }
        """)
        self.print_button.clicked.connect(self.generate_pdf_ticket)
        buttons_layout.addWidget(self.print_button)
        buttons_layout.addWidget(self.close_button)
        buttons_layout.setAlignment(Qt.AlignRight)
        
        main_layout.addLayout(buttons_layout)
        
        self.setLayout(main_layout)

        # Force update layout and repaint
        self.repaint()
    
    def close_window(self):
        """Close the window"""
        self.controller. refresh_registered_flights()
        self.close()
    
    def book_flight(self):
        """Book a flight with the selected class"""
        # Only available in booking mode
        if self.is_booking != 0:
            return
            
        # Get selected class (ID 1-3)
        selected_class = self.class_button_group.checkedId()
        print(selected_class)
        if selected_class < 1:  # If nothing selected (shouldn't happen with defaults)
            selected_class = 3  # Default to economy
        
        try:
        # Call controller to book flight
            success = self.controller.book_flight(self.flyer_id, self.flight_id, selected_class)
        
            if success:
                self.controller.refresh_registered_flights()
                class_name = self.controller.get_seat_class_name(selected_class)
                QMessageBox.information(
                    self, 
                    "Order placed successfully", 
                    f"Successfully booked a ticket!\n\n Order details: \n Flight #{self.flight_id}\n Seat type: {class_name}"
                )
                self.close()
            else:
                QMessageBox.warning(self, "Error", "The order cannot be placed. Please try again.")
        except Exception as e:
            print(f"Booking error: {e}")
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def generate_pdf_ticket(self):
        """Generate a better-designed PDF ticket"""
        from reportlab.lib import colors
        from reportlab.lib.units import inch

        try:
            pdf_dir = "./pdfFiles"
            if not os.path.exists(pdf_dir):
                os.makedirs(pdf_dir)

            ticket = self.controller.get_ticket_by_flight_user(self.flight_id, self.flyer_id)
            if not ticket:
                QMessageBox.warning(self, "Error", "No ticket found for this flight.")
                return

            seat_class = self.controller.get_seat_class_name(ticket.ticket_type)
            passenger = self.controller.get_flyer_by_id(self.flyer_id)

            pdf_path = f"{pdf_dir}/ticket_{ticket.ticket_id}_flight_{self.flight_id}.pdf"
            pdf = canvas.Canvas(pdf_path, pagesize=letter)
            width, height = letter

            # === Styling ===
            margin = 50
            line_height = 18
            start_y = height - margin

            def draw_label_val(label, value, x, y, bold=False):
                if bold:
                    pdf.setFont("Helvetica-Bold", 11)
                else:
                    pdf.setFont("Helvetica", 11)
                pdf.drawString(x, y, f"{label}")
                pdf.setFont("Helvetica", 11)
                pdf.drawRightString(width - margin, y, value)

            # === Header ===
            pdf.setFont("Helvetica-Bold", 20)
            pdf.drawString(margin, start_y, "✈ IsraFlight - Boarding Pass")
            pdf.setStrokeColor(colors.grey)
            pdf.line(margin, start_y - 10, width - margin, start_y - 10)

            # === Ticket Info ===
            y = start_y - 40
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(margin, y, "Flight Information")

            y -= line_height * 1.5
            draw_label_val("Ticket Number:", str(ticket.ticket_id), margin, y)
            y -= line_height
            draw_label_val("Flight Number:", str(self.flight_id), margin, y)
            y -= line_height
            draw_label_val("Route:", f"{self.flight.departure_location} → {self.flight.arrival_location}", margin, y)
            y -= line_height
            draw_label_val("Departure:", str(self.flight.departure_datetime), margin, y)
            y -= line_height
            draw_label_val("Arrival:", str(self.flight.estimated_arrival_datetime), margin, y)
            y -= line_height
            draw_label_val("Seat Class:", seat_class, margin, y)
            y -= line_height
            draw_label_val("Price:", f"${ticket.price}", margin, y)
            y -= line_height
            draw_label_val("Order Date:", ticket.created_date.strftime('%d/%m/%Y %H:%M'), margin, y)

            # === Divider ===
            y -= line_height * 1.5
            pdf.setStrokeColor(colors.lightgrey)
            pdf.line(margin, y, width - margin, y)

            # === Passenger Info ===
            y -= line_height * 1.5
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(margin, y, "Passenger")

            y -= line_height * 1.5
            draw_label_val("Name:", f"{passenger.first_name} {passenger.last_name}", margin, y)
            y -= line_height
            draw_label_val("Email:", passenger.email, margin, y)
            y -= line_height
            draw_label_val("Phone:", passenger.phone_number or "N/A", margin, y)

            # === Footer ===
            y -= line_height * 2
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawCentredString(width / 2, y, "** VALID TICKET **")

            y -= line_height * 3
            pdf.setFont("Helvetica", 10)
            pdf.drawCentredString(width / 2, y, "This ticket is required for boarding. Thank you for flying with IsraFlight.")

            # === Save ===
            pdf.save()
            QMessageBox.information(self, "Success", f"PDF saved to: {pdf_path}")

        except Exception as e:
            print(f"Error generating PDF: {e}")
            QMessageBox.warning(self, "Error", f"Failed to generate PDF: {str(e)}")
