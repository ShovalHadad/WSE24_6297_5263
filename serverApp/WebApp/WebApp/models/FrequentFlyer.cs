
using System.ComponentModel.DataAnnotations;

namespace WebApp.Models
{
    public class FrequentFlyer
    {
        [Key]
        public int FlyerId { get; set; } // flyer number in the DB
        public string UserName { get; set; } = string.Empty;  // username in the system
        public string Password { get; set; } = string.Empty;  // password in the system
        public string FirstName { get; set; } = string.Empty; // user first name 
        public string LastName { get; set; } = string.Empty;  // user last name
        public string? Email { get; set; } = string.Empty;  // user email
        public int? PhoneNumber { get; set; }  // user phone number              
        public List<int>? FlightsIds { get; set; } // list of past flights
        public bool IsManager { get; set; } = false;  // false =  FrequentFlyer, true = manager
        // public int? CurrentFlight { get; set; } // the current flight
    }
}