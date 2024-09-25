using Microsoft.EntityFrameworkCore;
using WebApp.Data;
using WebApp.Interfaces;
using WebApp.Models;
using System.Collections.Generic;
using System.Threading.Tasks;


namespace WebApp.Repositories
{
    public class FlightRepository : IFlightRepository
    {
        private readonly ApplicationDBContext _context;

        public FlightRepository(ApplicationDBContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<Flight>> GetFlightsAsync()
        {
            return await _context.Flights.ToListAsync();
        }

        public async Task<Flight> GetFlightByIdAsync(int id)
        {
            return await _context.Flights.FindAsync(id);
        }

        public async Task CreateFlightAsync(Flight flight)
        {
            var plane = await _context.Planes.FindAsync(flight.PlaneId);
            flight.NumOfTakenSeats1 = plane?.NumOfSeats1;
            flight.NumOfTakenSeats2 = plane?.NumOfSeats2;
            flight.NumOfTakenSeats3 = plane?.NumOfSeats3;
            _context.Flights.Add(flight);
            await _context.SaveChangesAsync();
            //לבדוק
        }

        public async Task UpdateFlightAsync(Flight flight)
        {
            _context.Entry(flight).State = EntityState.Modified;
            await _context.SaveChangesAsync();
        }

        public async Task DeleteFlightAsync(int id)
        {
            var flight = await _context.Flights.FindAsync(id);
            if (flight != null)
            {
                _context.Flights.Remove(flight);
                await _context.SaveChangesAsync();
            }
        }

        public async Task<bool> FlightExistsAsync(int id)
        {
            return await _context.Flights.AnyAsync(e => e.FlightId == id);
        }
    }
}
