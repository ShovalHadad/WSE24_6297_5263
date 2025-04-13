from models.plane import Plane
from views.plane_management_window import PlaneManagementWindow
#from services.imagga_service import is_airplane_image

class PlaneManagementController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.api_base_url = "http://localhost:5177/api/Plane" 
        self.plane_management_window = None

    def show_window(self):
        if not self.plane_management_window:
            self.plane_management_window = PlaneManagementWindow(self)

        self.plane_management_window.show()
        return self.plane_management_window
    
    def get_plane_by_id(self, plane_id):
        return Plane.get_plane_by_id(plane_id)

    
    def get_planes(self):
        try:
            planes = Plane.get_all_planes()
            return planes  # Return list of Flight objects
        except Exception as e:
            print(f"Error fetching planes: {e}")
            return []

    def add_plane(self, plane_data):
        plane = Plane(
            plane_id=0,
            name=plane_data["Name"],
            year=plane_data["Year"],
            made_by=plane_data["MadeBy"],
            picture=plane_data["Picture"],
            num_of_seats1=plane_data.get("NumOfSeats1", 0),
            num_of_seats2=plane_data.get("NumOfSeats2", 0),
            num_of_seats3=plane_data.get("NumOfSeats3", 0),
        )

        return plane.create()



    def delete_plane(self, plane_id):
        try:
            plane = Plane.get_plane_by_id(plane_id)
            plane.delete()
            return True
        except Exception as e:
            print(f"Error deleting plane: {e}")
            return False
    


    def search_planes(self, keyword):
        keyword_lower = keyword.lower()
        all_planes = Plane.get_all_planes()
        return [plane for plane in all_planes if keyword_lower in plane.name.lower() or keyword_lower in plane.made_by.lower()]
    

    def update_plane(self, plane_data):
        try:
            # נשלוף את המטוס הקיים לפי ה-ID
            plane = Plane.get_plane_by_id(plane_data["PlaneId"])

            # נעדכן את השדות
            plane.name = plane_data["Name"]
            plane.made_by = plane_data["MadeBy"]
            plane.year = int(plane_data["Year"])

            # לגבי תמונה – אם את שומרת path או base64, תעדכני בהתאם
            picture = plane_data["Picture"]
            if picture:  # נניח שזה QPixmap
                plane.picture = picture  # אם את משתמשת בקובץ – תעשי convert לפי הצורך

            # שולחים את העדכון לשרת
            plane.update()
            return True

        except Exception as e:
            print(f"Error updating plane: {e}")
            return False

