using Microsoft.EntityFrameworkCore;
using WebApp.Data;
using WebApp.models;

namespace WebApp.Repository
{
    public class FlightTicketRepository
    {
        private readonly ApplicationDBContext _context;

        public FlightTicketRepository(ApplicationDBContext context)
        {
            _context = context;
        }

        // Get all flight tickets with their associated flights
        public async Task<IEnumerable<FlightTicket>> GetFlightTicketsAsync()
        {
            return await _context.FlightTickets.ToListAsync();
        }

        // Get a flight ticket by its ID with associated flight
        public async Task<FlightTicket> GetFlightTicketByIdAsync(int id)
        {
            return await _context.FlightTickets.FirstOrDefaultAsync(ft => ft.TicketId == id);
        }

        // Create a new flight ticket
        public async Task CreateFlightTicketAsync(FlightTicket flightTicket)
        {
            var flight = await _context.Flights.FindAsync(flightTicket.FlightId);
            switch (flightTicket.TicketType)  // ?
            {
                case 1:
                    if (flight?.NumOfTakenSeats1 != 0)
                    {
                        flight.NumOfTakenSeats1--;
                        _context.Flights.Update(flight);
                    }
                    else throw new Exception("there is no sits left in this class");
                    break;
                case 2:
                    if (flight?.NumOfTakenSeats2 != 0)
                    {
                        flight.NumOfTakenSeats2--;
                        _context.Flights.Update(flight);
                    }
                    else throw new Exception("there is no sits left in this class");
                    break;
                case 3:
                    if (flight?.NumOfTakenSeats3 != 0)
                    {
                        flight.NumOfTakenSeats3--;
                        _context.Flights.Update(flight);
                    }
                    else throw new Exception("there is no sits left in this class");
                    break;
                case 0:
                    throw new Exception("did not chose a Ticket Type");
            }
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
