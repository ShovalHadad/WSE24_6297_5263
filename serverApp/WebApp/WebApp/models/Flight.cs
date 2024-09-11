using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace WebApp.Models
{
    public class Flight
    {
        public int FlightId { get; set; } // flight number
        public int PlaneId { get; set; } // plan number
        //public Plane? Plane { get; set; }
        public string DepartureLocation { get; set; } = string.Empty; // Departure Location /\
        public string ArrivalLocation { get; set; } = string.Empty; // Arrival Location  \/
        public DateTime DepartureDateTime { get; set; }  // Departure Date
        public DateTime EstimatedArrivalDateTime { get; set; }  // Arrival Date
        public int NumOfTakenSeats1 { get; set; } // number of taken seats in first class
        public int NumOfTakenSeats2 { get; set; } // number of taken seats in business
        public int NumOfTakenSeats3 { get; set; } // number of taken seats in economy    
    }
}