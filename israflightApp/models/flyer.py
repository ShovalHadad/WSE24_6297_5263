class FrequentFlyer:
    def __init__(self, flyer_id: int, username: str, password: str, first_name: str, last_name: str, email: str, phone_number: int, is_manager: bool):
        self.flyer_id = flyer_id
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.is_manager = is_manager

    def to_dict(self):
        return {
            "flyerId": self.flyer_id,
            "userName": self.username,
            "password": self.password,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "phoneNumber": self.phone_number,
            "isManager": self.is_manager
        }

    def __repr__(self):
        return f"FrequentFlyer(flyer_id={self.flyer_id}, username={self.username}, first_name={self.first_name}, last_name={self.last_name})"
