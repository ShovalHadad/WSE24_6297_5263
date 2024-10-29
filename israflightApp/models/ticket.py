class FlightTicket:
    def __init__(self, ticket_id, ticket_type, user_id, flight_id, shabat_times=None):
        self.ticket_id = ticket_id
        self.ticket_type = ticket_type  # 1 for first class, 2 for business, 3 for economy
        self.user_id = user_id
        self.flight_id = flight_id
        self.shabat_times = shabat_times

    def to_dict(self):
        return {
            'TicketId': self.ticket_id,
            'TicketType': self.ticket_type,
            'UserId': self.user_id,
            'FlightId': self.flight_id,
            'ShabatTimes': self.shabat_times
        }
