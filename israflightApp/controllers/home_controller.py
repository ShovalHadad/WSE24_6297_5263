from PySide6.QtWidgets import (
    QMainWindow, QLabel, QToolBar, QWidget, QVBoxLayout, QLineEdit, QPushButton, QFormLayout, QSizePolicy, QStackedWidget
)
from views.home_window import HomeWindow
from models.frequent_flyer import FrequentFlyer
import re
import requests

class HomeController:
    def __init__(self, Main_controller):
        self.mainController = Main_controller
        self.home_window = HomeWindow(self)

    def show_window(self):
        self.home_window.show()

    def register_button_action(self, user_data):
        """Handles user registration by sending data to the API."""
        
        base_url = "http://localhost:5000/api/FrequentFlyer"  # Change to your server URL
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(base_url, json=user_data, headers=headers)

            if response.status_code == 201:
                self.home_window.show_success_message("Registration successful! Please log in.")
                self.home_window.show_sign_in_form()  # Redirect to Sign In page
            elif response.status_code == 400:
                self.home_window.show_error_message("User already exists or invalid data.")
            else:
                self.home_window.show_error_message(f"Unexpected error: {response.text}")

        except Exception as e:
            self.home_window.show_error_message(f"Failed to register: {str(e)}")


        

    def sign_in_button_action(self, username, password):
        """Sends a secure login request using POST."""
        base_url = "http://localhost:5000/api/FrequentFlyer/login"  # Change to your server URL
        headers = {"Content-Type": "application/json"}
        login_data = {"UserName": username, "Password": password}
    
        try:
            response = requests.post(base_url, json=login_data, headers=headers)

            if response.status_code == 200:
                self.home_window.show_success_message("Login successful!")
                self.home_window.show_home_screen()
            elif response.status_code == 401:
                self.home_window.show_error_message("Invalid password. Try again.")
            elif response.status_code == 404:
                self.home_window.show_error_message("User not found.")
            else:
                self.home_window.show_error_message(f"Unexpected error: {response.text}")

        except Exception as e:
            self.home_window.show_error_message(f"Failed to log in: {str(e)}")

      
    
    def is_valid_email(self, email):
        """Check if the email follows a valid format."""
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_regex, email)

    def is_strong_password(self, password):
        """Check if the password is strong enough (at least 8 characters, letters, and numbers)."""
        return len(password) >= 8 and any(c.isalpha() for c in password) and any(c.isdigit() for c in password)
    
    def send_login_request(self, url, data):
        """Send a login request to the server."""
        headers = {"Content-Type": "application/json"}
        return requests.post(url, json=data, headers=headers)