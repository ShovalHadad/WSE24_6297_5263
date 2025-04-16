from views.home_window import HomeWindow
from models.frequent_flyer import FrequentFlyer
import re
import requests

class HomeController:
    def __init__(self, Main_controller):
        self.mainController = Main_controller
        self.home_window = HomeWindow(self)
        self.api_base_url = "http://localhost:5177/api/FrequentFlyer"  # Update with correct API URL

    def show_window(self):
        self.home_window.show()

    def register_button_action(self, user_data):
        """Handles user registration using the FrequentFlyer model."""
        try:
            new_flyer = FrequentFlyer(
                flyer_id=0,  # New user (ID assigned by the server)
                username=user_data["username"],  # Use email as username
                password=user_data["password"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                email=user_data["email"],
                phone_number=None,
                flights_ids=None,
                is_manager=False
            )

            new_flyer.create(self.api_base_url)  # Call the model method to create the flyer
            self.home_window.show_success_message("Registration successful! Please log in.")
            self.home_window.show_sign_in_form()

        except Exception as e:
            self.home_window.show_error_message(f"Failed to register: {str(e)}")

    
    def sign_in_button_action(self, username, password):
        """Handles user login and checks if the user is a manager."""
        try:
            flyer = FrequentFlyer.get_flyer_by_username(self.api_base_url, username)

            if not flyer:
                self.home_window.show_error_message("User not found.")
                return

            if flyer.password != password:
                self.home_window.show_error_message("Invalid password. Try again.")
                return

            # Successful login
            self.home_window.show_success_message("Login successful!")

            # Redirect user based on role
            if flyer.is_manager:
                self.mainController.show_manager_window()
            else:
                self.mainController.show_frequent_flyer_window(flyer.flyer_id)

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