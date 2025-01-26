from PySide6.QtWidgets import (
    QMainWindow, QLabel, QToolBar, QWidget, QVBoxLayout, QLineEdit, QPushButton, QFormLayout, QSizePolicy, QStackedWidget
)
from views.home_window import HomeWindow
from models.frequent_flyer import FrequentFlyer

class HomeController:
    def __init__(self,Main_controller):
        self.mainController=Main_controller
        self.home_window = HomeWindow(self)

    def show_window(self):
        self.home_window.show()


    def register_button_action(self):
        # Collect input data from the registration form
        first_name = self.home_window.registration_form.findChild(QLineEdit, "first_name_field").text()
        last_name = self.HomeWindow.registration_form.findChild(QLineEdit, "last_name_field").text()
        email = self.HomeWindow.registration_form.findChild(QLineEdit, "email_field").text()
        password = self.HomeWindow.registration_form.findChild(QLineEdit, "password_field").text()

        # Validate input
        if not first_name or not last_name or not email or not password:
            self.views.show_error_message("All fields are required for registration.")
            return

        # Create a new Frequent Flyer instance
        new_flyer = FrequentFlyer(
            flyer_id=0,  # New flyer, ID will be assigned by the server
            username=email,  # Use email as the username
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=None,  # Optional field
            flights_ids=[],  # New user, no flights yet
            is_manager=False  # Default to non-manager
        )

        # Attempt to send data to the server
        try:
            base_url = "http://airline.mssql.somee.com"  # Replace with your server's base URL
            new_flyer.create(base_url)
            self.views.show_success_message("Registration successful!")
            self.views.show_sign_in_form()  # Redirect back to Sign In after successful registration
        except Exception as e:
            self.views.show_error_message(f"Failed to register: {str(e)}")