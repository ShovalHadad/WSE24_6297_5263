using System.ComponentModel.DataAnnotations;
using WebApp.Models;


namespace WebApp.models
{
    public class FlightTicket
    {
        [Key]
        public int TicketId { get; set; } // Flight Ticket number
        public int TicketType { get; set; } = 0; // first class = 1 , business = 2 , economy = 3
        public int UserId { get; set; } // Navigation to FrequentFlyer
        public int FlightId { get; set; } // Navigation to flight

        //public Flight Flight { get; set; } = new Flight();  // Navigation to flight
    }
}
