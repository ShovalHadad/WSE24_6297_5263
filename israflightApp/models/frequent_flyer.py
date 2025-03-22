import requests

class FrequentFlyer:
    def __init__(self, flyer_id, username, password, first_name, last_name, 
                 email=None, phone_number=None, flights_ids=None, is_manager=False):
        self.flyer_id = flyer_id
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.flights_ids = flights_ids if flights_ids else []
        self.is_manager = is_manager

    @classmethod
    def from_dict(cls, data):
        return cls(
            flyer_id=data.get("flyerId"),  
            username=data.get("userName"),  
            password=data.get("password"),
            first_name=data.get("firstName"),
            last_name=data.get("lastName"),
            email=data.get("email"),
            phone_number=data.get("phoneNumber"),
            flights_ids=data.get("flightsIds", []),
            is_manager=data.get("isManager", False)
        )

    def to_dict(self):
        return {
            "FlyerId": self.flyer_id,
            "UserName": self.username,
            "Password": self.password,
            "FirstName": self.first_name,
            "LastName": self.last_name,
            "Email": self.email,
            "PhoneNumber": self.phone_number,
            "FlightsIds": self.flights_ids,
            "IsManager": self.is_manager
        }

    @staticmethod
    def get_all_flyers(base_url):
        try:
            response = requests.get(f"{base_url}")
            response.raise_for_status()

            flyer_data_list = response.json()
            flyers = [FrequentFlyer.from_dict(data) for data in flyer_data_list]

            return flyers

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching frequent flyers: {e}")
            return []
   
   
    @staticmethod
    def get_flyer_by_id(base_url, flyer_id):
        try:
            response = requests.get(f"{base_url}/{flyer_id}")
            response.raise_for_status()
            flyer_data = response.json()
            return FrequentFlyer.from_dict(flyer_data)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching frequent flyer {flyer_id}: {e}")
            return None
        

    @staticmethod
    def get_flyer_by_username(base_url, username):
        """Fetches a frequent flyer by username (email)."""
        try:
            if not username:
                print("Error: Username is None or empty.")
                return None

            # Fetch all frequent flyers
            flyers = FrequentFlyer.get_all_flyers(base_url)  # This returns a list of dictionaries

            # Ensure username is valid before calling `.lower()`
            flyer = next((f for f in flyers if f.username and f.username.lower() == username.lower()), None)

            if flyer:
                return flyer
            else:
                print(f"Frequent flyer with username '{username}' not found.")
                return None

        except Exception as e:
            print(f"Error fetching frequent flyer {username}: {e}")
            return None

        

    def create(self, base_url):
        try:
            flyer_data = self.to_dict()
            if self.flyer_id == 0:  # יצירת נוסע מתמיד חדש
                response = requests.post(f"{base_url}/api/FrequentFlyer", json=flyer_data)
                response.raise_for_status()
                print("Frequent flyer created successfully")
            else:  # עדכון נוסע מתמיד קיים
                self.update(base_url)  # קריאה לפונקציית update
        except requests.exceptions.RequestException as e:
            print(f"Error saving frequent flyer: {e}")

    def update(self, base_url):
        try:
            if not self.flyer_id:
                raise ValueError("Flyer ID is required to update a frequent flyer.")

            flyer_data = self.to_dict()
            response = requests.put(f"{base_url}/api/frequentflyers/{self.flyer_id}", json=flyer_data)
            response.raise_for_status()
            print("Frequent flyer updated successfully")
        except requests.exceptions.RequestException as e:
            print(f"Error updating frequent flyer {self.flyer_id}: {e}")

    def delete(self, base_url):
        try:
            response = requests.delete(f"{base_url}/api/frequentflyers/{self.flyer_id}")
            response.raise_for_status()
            print("Frequent flyer deleted successfully")
        except requests.exceptions.RequestException as e:
            print(f"Error deleting frequent flyer {self.flyer_id}: {e}")
