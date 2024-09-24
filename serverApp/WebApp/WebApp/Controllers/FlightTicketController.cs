using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using WebApp.Data;
using WebApp.Interfaces;
using WebApp.models;


namespace WebApp.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class FlightTicketController : ControllerBase
    {

        private readonly ApplicationDBContext _context;
        private readonly IFlightTicketRepository _flightTicketRepository;

        public FlightTicketController(ApplicationDBContext context, IFlightTicketRepository flightTicketRepository)
        {
            _context = context;
            _flightTicketRepository = flightTicketRepository;
        }


        // GET: api/FlightTicket
        [HttpGet]
        public async Task<ActionResult<IEnumerable<FlightTicket>>> GetFlightTickets()
        {
            var tickets = await _flightTicketRepository.GetFlightTicketsAsync();
            return Ok(tickets);
        }

        // GET: api/FlightTicket/5
        [HttpGet("{id}")]
        public async Task<ActionResult<FlightTicket>> GetFlightTicket(int id)
        {
            var ticket = await _flightTicketRepository.GetFlightTicketByIdAsync(id);
            if (ticket == null)
            {
                return NotFound();
            }
            return Ok(ticket);
        }


        // POST api/<FlightTicketController>
        [HttpPost]
        public async Task<ActionResult<FlightTicket>> CreateFlightTicket(FlightTicket flightTicket)
        {
            await _flightTicketRepository.CreateFlightTicketAsync(flightTicket);
            return CreatedAtAction(nameof(GetFlightTicket), new { id = flightTicket.TicketId }, flightTicket);
        }


        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateFlightTicket(int id, FlightTicket flightTicket)
        {
            if (id != flightTicket.TicketId)
            {
                return BadRequest();
            }

            var exists = await _flightTicketRepository.FlightTicketExistsAsync(id);
            if (!exists)
            {
                return NotFound();
            }

            await _flightTicketRepository.UpdateFlightTicketAsync(flightTicket);
            return NoContent();
        }

        // DELETE: api/FlightTicket/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteFlightTicket(int id)
        {
            var ticket = await _flightTicketRepository.GetFlightTicketByIdAsync(id);
            if (ticket == null)
            {
                return NotFound();
            }

            await _flightTicketRepository.DeleteFlightTicketAsync(id);
            return NoContent();
        }


        private Task<bool> FlightTicketExists(int id)
        {
            return _flightTicketRepository.FlightTicketExistsAsync(id);
        }
    }
}
