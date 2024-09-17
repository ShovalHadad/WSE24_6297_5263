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

        private readonly ApplicationDBContext _context;

        public FlightTicketController(ApplicationDBContext context)
        {
            _context = context;
        }


        // GET: api/FlightTicket
        [HttpGet]
        public async Task<ActionResult<IEnumerable<FlightTicket>>> GetFlightTickets()
        {
            return await _context.FlightTickets.Include(ft => ft.Flight).ToListAsync();
        }

        // GET: api/FlightTicket/5
        [HttpGet("{id}")]
        public async Task<ActionResult<FlightTicket>> GetFlightTicket(int id)
        {
            var flightTicket = await _context.FlightTickets.Include(ft => ft.Flight).FirstOrDefaultAsync(ft => ft.TicketId == id);

            if (flightTicket == null)
            {
                return NotFound();
            }

            return flightTicket;
        }


        // POST api/<FlightTicketController>
        [HttpPost]
        public async Task<ActionResult<FlightTicket>> PostFlightTicket(FlightTicket flightTicket)
        {
            _context.FlightTickets.Add(flightTicket);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetFlightTicket), new { id = flightTicket.TicketId }, flightTicket);
        }


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

        // DELETE: api/FlightTicket/5
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

        private bool FlightTicketExists(int id)
        {
            return _context.FlightTickets.Any(e => e.TicketId == id);
        }
    }
}
