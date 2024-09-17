
using System.ComponentModel.DataAnnotations;

namespace WebApp.Models
{
    public class FrequentFlyer
    {
        [Key]
        public int FlyerId { get; set; } // flyer number in the DB

        public string UserName { get; set; } = string.Empty;  // username in the system
        public string Password { get; set; } = string.Empty;  // password in the system
        public string FirstName { get; set; } = string.Empty; 
        public string LastName { get; set; } = string.Empty;  
        public string Email { get; set; } = string.Empty;    
        public int PhoneNumber { get; set; }                
        //public List<Flight>? UserFlights { get; set; } 
        public List<Flight> UserFlights { get; set; } = new List<Flight>(); // list of past flights
        public bool IsManager { get; set; } = false;  // false =  FrequentFlyer, true = manager
    }
}