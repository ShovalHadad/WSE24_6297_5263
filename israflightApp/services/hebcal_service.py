import requests
from datetime import datetime, timedelta

class HebCalServiceException(Exception):
    """Custom exception for HebCalService errors."""
    pass

class HebCalService:
    def __init__(self):
        self.base_url = "https://www.hebcal.com/hebcal"

    def get_shabbat_times(self, city, date):
        """Get Shabbat times for a specific city and date.

        Args:
            city (str): The name of the city.
            date (datetime): The date for which to fetch Shabbat times.

        Returns:
            str: A string indicating when Shabbat starts and ends.

        Raises:
            HebCalServiceException: If there is an error in fetching or parsing the data.
        """
        try:
            # Calculate the start and end of the week
            start_of_week = self.start_of_week(date)
            end_of_week = start_of_week + timedelta(days=6)

            # Construct the API URL
            url = f"{self.base_url}?cfg=json&v=1&maj=on&geo=city&city={requests.utils.quote(city)}&start={start_of_week.strftime('%Y-%m-%d')}&end={end_of_week.strftime('%Y-%m-%d')}"

            # Make the HTTP request
            response = requests.get(url)
            response.raise_for_status()

            # Parse the JSON response
            json_response = response.json()

            # Extract Shabbat times
            shabbat_start = json_response.get("shabbat", {}).get("start")
            shabbat_end = json_response.get("shabbat", {}).get("end")

            if not shabbat_start or not shabbat_end:
                raise HebCalServiceException("Shabbat times not found for the specified location.")

            shabbat_start_time = datetime.fromisoformat(shabbat_start.replace("Z", "+00:00"))
            shabbat_end_time = datetime.fromisoformat(shabbat_end.replace("Z", "+00:00"))

            # Check if the specified date is during Shabbat
            if start_of_week <= date <= end_of_week:
                raise HebCalServiceException("The specified date is during Shabbat. Please provide a date outside of Shabbat.")

            return f"Shabbat starts at: {shabbat_start_time.strftime('%Y-%m-%d %H:%M')}, ends at: {shabbat_end_time.strftime('%Y-%m-%d %H:%M')}"

        except Exception as ex:
            raise HebCalServiceException("Failed to fetch Shabbat times.") from ex

    @staticmethod
    def start_of_week(dt):
        """Calculate the start of the week (Sunday) for a given date.

        Args:
            dt (datetime): The date to calculate the start of the week.

        Returns:
            datetime: The start of the week (Sunday).
        """
        return dt - timedelta(days=dt.weekday() + 1) if dt.weekday() != 6 else dt

# Example usage
if __name__ == "__main__":
    hebcal_service = HebCalService()
    city = "Jerusalem"
    date = datetime(2024, 10, 18)  # Example date
    try:
        shabbat_times = hebcal_service.get_shabbat_times(city, date)
        print(shabbat_times)
    except HebCalServiceException as e:
        print(e)
