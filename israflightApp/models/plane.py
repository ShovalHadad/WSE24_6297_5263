class Plane:
    def __init__(self, plane_id, name, year, made_by, picture, num_of_seats1, num_of_seats2, num_of_seats3):
        self.plane_id = plane_id
        self.name = name
        self.year = year
        self.made_by = made_by
        self.picture = picture
        self.num_of_seats1 = num_of_seats1
        self.num_of_seats2 = num_of_seats2
        self.num_of_seats3 = num_of_seats3

    def to_dict(self):
        return {
            'planeId': self.plane_id,
            'name': self.name,
            'year': self.year,
            'madeBy': self.made_by,
            'picture': self.picture,
            'numOfSeats1': self.num_of_seats1,
            'numOfSeats2': self.num_of_seats2,
            'numOfSeats3': self.num_of_seats3
        }
