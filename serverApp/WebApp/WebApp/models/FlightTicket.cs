using WebApp.Models;

namespace WebApp.models
{
    public class FlightTicket
    {
        public int Id { get; set; } // Flight Ticket number
        public int TicketType { get; set; } = 0; // first class = 1 , business = 2 , economy = 3
        public Flight Flight { get; set; } = new Flight();  // the flight
    }
}
