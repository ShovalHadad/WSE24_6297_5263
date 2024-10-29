using System.ComponentModel.DataAnnotations;
using WebApp.Models;

namespace WebApp.models
{
    public class FlightTicket
    {
        [Key]
        public int TicketId { get; set; } // Flight Ticket number
        public int TicketType { get; set; } = 0; // first class = 1 , business = 2 , economy = 3
        public int UserId { get; set; }  // Navigation to user/flyer
        public int FlightId { get; set; }// Navigation to flight
        public string ShabatTimes { get; set; } = string.Empty; // shabat time in flight week
        public DateTime CreatedDate { get; set;} = DateTime.Now; // date of booking ticket
        public string price { get; set; } = string.Empty; // price of the ticket
     }
}