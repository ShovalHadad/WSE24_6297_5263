import requests
from requests.auth import HTTPBasicAuth

class ImaggaServiceException(Exception):
    """Custom exception for ImaggaService errors."""
    pass

class ImaggaService:
    def __init__(self, api_key, api_secret):
        self.api_url = "https://api.imagga.com/v2/tags"
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(api_key, api_secret)

    def analyze_image_for_plane(self, image_url):
        """Analyze the image to check if it contains a plane.

        Args:
            image_url (str): The URL of the image to analyze.

        Returns:
            bool: True if the image contains a plane, False otherwise.

        Raises:
            ImaggaServiceException: If there is an error in the API call.
        """
        try:
            # URL encode the image URL
            response = self.session.get(self.api_url, params={'image_url': image_url})
            response.raise_for_status()  # Raise an exception for HTTP errors

            json_response = response.json()
            return self.contains_plane_tag(json_response)

        except requests.exceptions.HTTPError as http_err:
            error_message = response.json().get('message', 'No detailed error message provided.')
            raise ImaggaServiceException(f"Failed to analyze image with Imagga API. Status Code: {response.status_code}, Response: {error_message}") from http_err

    def contains_plane_tag(self, json_response):
        """Check if the JSON response contains tags related to planes.

        Args:
            json_response (dict): The JSON response from the Imagga API.

        Returns:
            bool: True if any tag indicates a plane, False otherwise.
        """
        tags = json_response.get("result", {}).get("tags", [])

        # Check for plane-related tags
        for tag in tags:
            tag_name = tag['tag']['en']
            if tag_name.lower() in ['plane', 'airplane', 'jet']:
                return True  # Found a plane-related tag
        return False  # No plane-related tags found

# Example usage
if __name__ == "__main__":
    api_key = "acc_10e9963589d24bf"  # Replace with your actual API key
    api_secret = "84512d28c964121b6b0681dec2a116aa"  # Replace with your actual API secret
    imagga_service = ImaggaService(api_key, api_secret)
    
    image_url = "https://example.com/path/to/image.jpg"  # Replace with your actual image URL
    try:
        is_plane = imagga_service.analyze_image_for_plane(image_url)
        if is_plane:
            print("The image contains a plane.")
        else:
            print("The image does not contain a plane.")
    except ImaggaServiceException as e:
        print(e)
