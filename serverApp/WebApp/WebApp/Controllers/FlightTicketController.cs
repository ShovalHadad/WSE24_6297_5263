using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using WebApp.Data;
using WebApp.Interfaces;
using WebApp.models;
using WebApp.Repository;


namespace WebApp.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class FlightTicketController : ControllerBase
    {
        private readonly ApplicationDBContext _context;
        private readonly IFlightTicketRepository _flightTicketRepository;
        // Constructor
        public FlightTicketController(ApplicationDBContext context, IFlightTicketRepository flightTicketRepository)
        {
            _context = context;
            _flightTicketRepository = flightTicketRepository;
        }

        // GET - read all
        [HttpGet]
        public async Task<ActionResult<IEnumerable<FlightTicket>>> GetFlightTickets()
        {
            try
            {
                var tickets = await _flightTicketRepository.GetFlightTicketsAsync();
                return Ok(tickets);
            }
            catch (Exception ex)
            {
                throw new Exception("can not read all flight tickets ", ex);
            }
        }

        // GET - read
        [HttpGet("{id}")]
        public async Task<ActionResult<FlightTicket>> GetFlightTicket(int id)
        {
            try
            {
                var ticket = await _flightTicketRepository.GetFlightTicketByIdAsync(id);
                if (ticket == null)
                {
                    return NotFound();
                }
                return Ok(ticket);
            }
            catch (Exception ex)
            {
                throw new Exception($"can not read the flight ticket {id} ", ex);
            }
        }

        // POST - create
        [HttpPost]
        public async Task<ActionResult<FlightTicket>> CreateFlightTicket(FlightTicket flightTicket)
        {
            try
            {
                await _flightTicketRepository.CreateFlightTicketAsync(flightTicket);
                return CreatedAtAction(nameof(GetFlightTicket), new { id = flightTicket.TicketId }, flightTicket);
            }
            catch (Exception ex) 
            {
                throw new Exception("can not create new flight ticket ", ex);
            }
        }

        // PUT - update
        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateFlightTicket(int id, FlightTicket flightTicket)
        {
            if (id != flightTicket.TicketId)
                return BadRequest();
            if (!await _flightTicketRepository.FlightTicketExistsAsync(id))
                return NotFound();
            try
            {
                await _flightTicketRepository.UpdateFlightTicketAsync(id, flightTicket);
                return NoContent();
            }
            catch (Exception ex) 
            {
                throw new Exception($"can not update the flight ticket {id} ", ex);
            }
        }

        // DELETE - delete
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteFlightTicket(int id)
        {
            var ticket = await _flightTicketRepository.GetFlightTicketByIdAsync(id);
            if (ticket == null)
                return NotFound();
            try
            {
                await _flightTicketRepository.DeleteFlightTicketAsync(id);
                return NoContent();
            }
            catch(Exception ex) 
            {
                throw new Exception($"can not delete the flight ticket {id} ", ex);
            }
        }

        private Task<bool> FlightTicketExists(int id)
        {
            return _flightTicketRepository.FlightTicketExistsAsync(id);
        }
    }
    
}
