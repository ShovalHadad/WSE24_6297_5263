using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using WebApp.Data;
using WebApp.models;


namespace WebApp.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class FlightTicketController : ControllerBase
    {

        private readonly ApplicationDBContext _context; // _context = list of FlightTickets
        // constractor
        public FlightTicketController(ApplicationDBContext context)
        {
            _context = context;
        }

        /// <summary>
        /// GET ALL - read all
        /// returns the FlightTickets from _context in a list
        /// </summary>
        /// <returns> list of FlightTickets </returns>
        [HttpGet]
        public async Task<ActionResult<IEnumerable<FlightTicket>>> GetFlightTickets()
        {
            return await _context.FlightTickets.ToListAsync();
        }

        /// <summary>
        /// GET - read
        /// returns a FlightTicket from _context that match the id
        /// </summary>
        /// <param name="id"> id of wanted FlightTicket </param>
        /// <returns> FlightTicket </returns>
        [HttpGet("{id}")]
        public async Task<ActionResult<FlightTicket>> GetFlightTicket(int id)
        {
            var flightTicket = await _context.FlightTickets.FirstOrDefaultAsync(ft => ft.TicketId == id);

            if (flightTicket == null)
            {
                return NotFound();
            }

            return flightTicket;
        }

        /// <summary>
        /// POST - create
        /// creates a new FlightTicket and add to _context
        /// </summary>
        /// <param name="flightTicket"> the new FlightTicket </param>
        /// <returns> result of CreatedAtAction </returns>
        [HttpPost]
        public async Task<ActionResult<FlightTicket>> PostFlightTicket(FlightTicket flightTicket)
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
            return CreatedAtAction(nameof(GetFlightTicket), new { id = flightTicket.TicketId }, flightTicket);
        }

        /// <summary>
        /// PUT- update
        /// updates the flightTicket that match the id with the flightTicket
        /// </summary>
        /// <param name="id"> the id fo the flightTicket we need to update </param>
        /// <param name="flightTicket"> the flightTicket with the updated details </param>
        /// <returns> NoContent if update was successful </returns>
        [HttpPut("{id}")]
        public async Task<IActionResult> PutFlightTicket(int id, FlightTicket flightTicket)
        {
            if (id != flightTicket.TicketId)
            {
                return BadRequest();
            }
            _context.Entry(flightTicket).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!FlightTicketExists(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            return NoContent();
        }

        /// <summary>
        /// DELETE - delete
        /// deletes the FlightTicket that match the id
        /// </summary>
        /// <param name="id"> id of the FlightTicket we need to delete </param>
        /// <returns> NoContent if delete was successful </returns>
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteFlightTicket(int id)
        {
            var flightTicket = await _context.FlightTickets.FindAsync(id);
            if (flightTicket == null)
            {
                return NotFound();
            }

            _context.FlightTickets.Remove(flightTicket);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        // private function for Update function
        private bool FlightTicketExists(int id)
        {
            return _context.FlightTickets.Any(e => e.TicketId == id);
        }
    }
}
