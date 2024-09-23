using Microsoft.EntityFrameworkCore;
using WebApp.Data;
using WebApp.Interfaces;
using WebApp.models;

namespace WebApp.Repository
{
    public class FlightTicketRepository : IFlightTicketRepository
    {
        private readonly ApplicationDBContext _context;

        public FlightTicketRepository(ApplicationDBContext context)
        {
            _context = context;
        }

        // Get all flight tickets with their associated flights
        public async Task<IEnumerable<FlightTicket>> GetFlightTicketsAsync()
        {
            return await _context.FlightTickets
                                 .Include(ft => ft.Flight) // Include associated flight details
                                 .ToListAsync();
        }

        // Get a flight ticket by its ID with associated flight
        public async Task<FlightTicket> GetFlightTicketByIdAsync(int id)
        {
            return await _context.FlightTickets
                                 .Include(ft => ft.Flight) // Include associated flight details
                                 .FirstOrDefaultAsync(ft => ft.TicketId == id);
        }

        // Create a new flight ticket
        public async Task CreateFlightTicketAsync(FlightTicket flightTicket)
        {
            _context.FlightTickets.Add(flightTicket);
            await _context.SaveChangesAsync();
        }

        // Update an existing flight ticket
        public async Task UpdateFlightTicketAsync(FlightTicket flightTicket)
        {
            _context.Entry(flightTicket).State = EntityState.Modified;
            await _context.SaveChangesAsync();
        }

        // Delete a flight ticket by ID
        public async Task DeleteFlightTicketAsync(int id)
        {
            var flightTicket = await _context.FlightTickets.FindAsync(id);
            if (flightTicket != null)
            {
                _context.FlightTickets.Remove(flightTicket);
                await _context.SaveChangesAsync();
            }
        }

        // Check if a flight ticket exists by ID
        public async Task<bool> FlightTicketExistsAsync(int id)
        {
            return await _context.FlightTickets.AnyAsync(e => e.TicketId == id);
        }
    }
}
