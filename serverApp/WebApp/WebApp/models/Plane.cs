using System.ComponentModel.DataAnnotations;

namespace WebApp.Models
{
    public class Plane
    {
        [Key]
        public int PlaneId { get; set; }  // plane number
        public string Name { get; set; } = string.Empty; // plane name
        public int Year { get; set; } // Year of manufacture
        public string MadeBy { get; set; } = string.Empty; // plane company name
        public string? Picture { get; set; } // plane pic (URL or base64 string)
        public int NumOfSeats1 { get; set; } // number of seats in first class
        public int NumOfSeats2 { get; set; } // number of seats in business
        public int NumOfSeats3 { get; set; } // number of seats in economy
    }
}