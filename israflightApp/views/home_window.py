from PySide6.QtWidgets import *
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
from views.base_window import BaseWindow
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QGuiApplication



class HomeWindow(BaseWindow):
    def __init__(self, controller):
        super(HomeWindow, self).__init__()
        self.controller = controller
        screen = QGuiApplication.primaryScreen()
        self.setWindowTitle("IsraFlight")
        self.setGeometry(screen.geometry())
        self.setMinimumSize(800, 600)
        self.showMaximized()
        screen_height = screen.size().height()
        screen_width = screen.size().width()
        print(f"screen hight: {screen_height}")
        print(f"screen width: {screen_width}")
        # Set the central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.create_toolbar()


        # Create a layout for the central widget
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        layout.setSpacing(0)  # Remove spacing
        central_widget.setLayout(layout)

        # Set the background label
        self.background_label = QLabel(self)
        pixmap = QPixmap("./israflightApp/images/background2.png")  # Replace with your image path
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)
        layout.addWidget(self.background_label)

        # Add the logo
        self.logo_below_text = QLabel(self.background_label)
        logo_pixmap = QPixmap("./israflightApp/images/israFlight_logo-03.png")  # Replace with your logo path
        self.logo_below_text.setPixmap(logo_pixmap.scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Resize logo
        self.logo_below_text.move(int(screen_width/16), 100)  # Position below the text

        # Overlay the text label
        self.text_label = QLabel(self.background_label)
        font = QFont("Urbanist", 12, QFont.Bold)
        self.text_label.setFont(font)
        self.text_label.setStyleSheet("color: #1C3664; margin-left: 20px;")  # Text color
        self.text_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.text_label.resize(600, 150)  # Adjust height to fit multiple lines
        self.text_label.move(int(screen_width/16), 370)  # Position the text label
        self.text_label.setText(
            "IsraFlight is a full-service airline offering a premium travel experience \n"
            "with modern aviation technology.\n"
            "Our platform makes booking easy and personalized.\n"
            "We are committed to safety, reliability, and outstanding service.\n"
            "Enjoy a seamless journey—from check-in to arrival.\n"
            "Experience the future of air travel with IsraFlight."
        )

        # Add a QStackedWidget to hold both forms
        self.stacked_widget = QStackedWidget(self.background_label)
        self.stacked_widget.setGeometry(int(screen_width*(5/8)), 120, 400, 450)

        # Add Sign-In and Registration forms
        self.sign_in_form = self.create_sign_in_form()
        self.registration_form = self.create_registration_form()

        self.stacked_widget.addWidget(self.sign_in_form)  # Page 0: Sign-In Form
        self.stacked_widget.addWidget(self.registration_form)  # Page 1: Registration Form

        self.stacked_widget.setCurrentWidget(self.sign_in_form)  # Show Sign-In form initially

    def create_sign_in_form(self):
        """Create the sign-in form."""
        form_widget = QWidget()
        form_widget.setStyleSheet("""
        QWidget{
            background-color: #F0F9FC;
            border-radius: 15px; 
            padding-top: 20px;
            padding-left: 15px;
            padding-right: 15px;                                                  
        }
        QLineEdit {
            background-color: #FFFFFF;  /* White background */
            color: #1C3664;  /* Text color */
            border: 2px solid #27AAE1;  /* Border color */
            border-radius: 8px;  /* Rounded corners */
            padding: 5px;  /* Internal padding */
            font-family: 'Urbanist';  /* Font family */
            font-size: 14px;  /* Font size */
            margin-top: 8px;
        }
        QLineEdit:focus {
            border-color: #1C3664;  /* Change border color when focused */
        }
        QLabel{
            color: #1C3664;
            font-family: 'Urbanist';  /* Font family */
            font-size: 14px;  /* Font size */
            font-weight: 500px;
            padding: 5px;  /* Internal padding */
        }
        """)
    
        form_layout = QFormLayout(form_widget)
        form_layout.setContentsMargins(40, 30, 90, 5)  # Padding inside the form

        # Add a heading
        form_heading = QLabel("Sign In")
        form_heading.setFont(QFont("Urbanist", 18, QFont.Bold))
        form_heading.setStyleSheet("color: #27AAE1;")
        form_heading.setAlignment(Qt.AlignCenter)
        form_layout.addRow(form_heading)
    
        # Add fields
        self.username_field = QLineEdit()
        self.username_field.setObjectName("username_field")  # Object name for easy access
    
        self.password_field = QLineEdit()
        self.password_field.setObjectName("password_field")  # Object name for easy access
        self.password_field.setEchoMode(QLineEdit.Password)
    
        # Sign In Button
        sign_in_button = QPushButton("Sign In")
        sign_in_button.setStyleSheet("""
            QPushButton {
                background-color: #27AAE1;
                color: #ffffff;
                border-radius: 10px;
                padding: 10px;
                font-family: 'Urbanist';
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #218FB5;
            }
            QPushButton:pressed {
                background-color: #82CEE8;
            }
        """)
    
        # Connect button with lambda function to send input values
        sign_in_button.clicked.connect(lambda: self.controller.sign_in_button_action(
            self.username_field.text(), self.password_field.text()
            ))

    
        # Sign Up Button
        sign_up_button = QPushButton("Sign Up")
        sign_up_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #1C3664;
                border-radius: 10px;
                padding: 10px;
                font-family: 'Urbanist';
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #27AAE1;
            }
            QPushButton:pressed {
                color: #82CEE8;
            }
        """)
        sign_up_button.clicked.connect(self.show_registration_form)
    
        # Labels
        username_label = QLabel("Username:")
        password_label = QLabel("Password:")
    
        # Add widgets to form layout
        form_layout.addRow(username_label, self.username_field)
        form_layout.addRow(password_label, self.password_field)
        form_layout.addWidget(sign_in_button)
        form_layout.addWidget(sign_up_button)
    
        return form_widget


   

    def create_registration_form(self):
        """Create the registration form."""
        form_widget = QWidget()
        form_widget.setStyleSheet("""
        QWidget{
            background-color: #F0F9FC;
            border-radius: 15px; 
            padding-top: 20px;
            padding-left: 15px;    
            padding-right: 15px;                       
        }
        QLineEdit {
            background-color: #FFFFFF;  /* White background */
            color: #1C3664;  /* Text color */
            border: 2px solid #27AAE1;  /* Border color */
            border-radius: 8px;  /* Rounded corners */
            padding: 5px;  /* Internal padding */
            font-family: 'Urbanist';  /* Font family */
            font-size: 14px;  /* Font size */
            margin-top: 8px;                      
            font-weight: 500px;
        }
        QLineEdit:focus {
            border-color: #1C3664;  /* Change border color when focused */
        }
        QLabel{
            color: #1C3664;
            font-family: 'Urbanist';  /* Font family */
            font-size: 14px;  /* Font size */
            font-weight: 500px;
            padding: 5px;  /* Internal padding */
            
        }
        """)
        form_layout = QFormLayout(form_widget)
        form_layout.setContentsMargins(40, 30, 90, 5)


        # Add a heading
        form_heading = QLabel("Register")
        form_heading.setFont(QFont("Urbanist", 22, QFont.Bold))
        form_heading.setStyleSheet("color: #27AAE1;")
        form_heading.setAlignment(Qt.AlignCenter)
        form_layout.addRow(form_heading)

        user_field = QLineEdit()
        user_field.setObjectName("user_field")  # Assign object name

        pass_field = QLineEdit()
        pass_field.setObjectName("password_field")  # Assign object name

        first_name_field = QLineEdit()
        first_name_field.setObjectName("first_name_field")  # Assign object name

        last_name_field = QLineEdit()
        last_name_field.setObjectName("last_name_field")  # Assign object name

        email_field = QLineEdit()
        email_field.setObjectName("email_field")  # Assign object name

        #phone_field = QLineEdit()
        #phone_field.setObjectName("phone_field")  # Assign object name

        #phone_field = None


        pass_field.setEchoMode(QLineEdit.Password)
        register_button = QPushButton("Register")
        register_button.setStyleSheet("""
            QPushButton {
                background-color: #27AAE1;
                color: #ffffff;
                border-radius: 10px;
                padding: 10px;
                font-family: 'Urbanist';
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #218FB5;
            }
            QPushButton:pressed {
                background-color: #82CEE8;
            }
        """)
        

        # Back to Sign In Button
        back_to_sign_in_button = QPushButton("Sign In")
        back_to_sign_in_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #1C3664;
                border-radius: 10px;
                padding: 10px;
                font-family: 'Urbanist';
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #27AAE1;
            }
            QPushButton:pressed {
                color: #82CEE8;
            }
        """)
        user_label = QLabel("Username:")
        pass_label = QLabel("Password:")
        first_name_label = QLabel("First Name:")
        last_name_label = QLabel("Last Name:")
        email_label = QLabel("Email:")
        #phone_label = QLabel("Phone Number:")
        
        form_layout.addRow(user_label, user_field)
        form_layout.addRow(pass_label, pass_field)
        form_layout.addRow(first_name_label, first_name_field)
        form_layout.addRow(last_name_label, last_name_field)
        form_layout.addRow(email_label, email_field)
        #form_layout.addRow(phone_label, phone_field)

        form_layout.addWidget(back_to_sign_in_button) 
    
        back_to_sign_in_button.clicked.connect(self.show_sign_in_form)

        #register_button.clicked.connect(self.controller.register_button_action())
         # Connect the button to a lambda function that gathers user input and calls register_button_action
        register_button.clicked.connect(lambda: self.controller.register_button_action({
            "username": user_field.text(),
            "password": pass_field.text(),
            "first_name": first_name_field.text(),
            "last_name": last_name_field.text(),
            "email": email_field.text()
        }))


        form_layout.addRow(register_button)

        return form_widget

    def show_registration_form(self):
        """Switch to the registration form."""
        self.stacked_widget.setCurrentWidget(self.registration_form)


    def show_sign_in_form(self):
        """Switch to the sign-in form."""
        self.stacked_widget.setCurrentWidget(self.sign_in_form)

    def action1_triggered(self):
        print("Sign In triggered")

    def action2_triggered(self):
        print("Registration triggered")

    def resizeEvent(self, event):
        """Resize the background label."""
        if hasattr(self, 'background_label') and self.background_label:
            self.background_label.resize(self.size())
        super().resizeEvent(event)

    def show_error_message(self, message):
        """Displays an error message in a pop-up window."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec()


    def show_success_message(self, message):
        """Displays a success message in a pop-up window."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Success")
        msg_box.setText(message)
        msg_box.exec()
