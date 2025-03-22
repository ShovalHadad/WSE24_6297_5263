using Microsoft.AspNetCore.Mvc;
using System;
using WebApp.Models;
using WebApp.Data;
using WebApp.Interfaces;
using Microsoft.EntityFrameworkCore;
using Newtonsoft.Json;





namespace WebApp.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class FlightController : ControllerBase
    {
        private readonly ApplicationDBContext _context;
        private readonly IFlightRepository _flightRepo;
        // Constructor
        public FlightController(ApplicationDBContext context, IFlightRepository flightRepo)
        {
            _context = context;
            _flightRepo = flightRepo;
        }

        // GET - read all
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Flight>>> GetFlights()
        {
            try
            {
                var flights = await _flightRepo.GetFlightsAsync();
                return Ok(flights);
            }
            catch (Exception ex)
            {
                throw new Exception("can not read all flights ", ex);
            }
        }

        // GET - read
        [HttpGet("{id}")]
        public async Task<ActionResult<Flight>> GetFlight(int id) 
        {
            try
            {
                var flight = await _flightRepo.GetFlightByIdAsync(id);
                if (flight == null)
                {
                    return NotFound();
                }
                return flight;
            }
            catch (Exception ex)
            {
                throw new Exception($"can not read the flight {id} ", ex);
            }
        }

        // POST - create
        [HttpPost]
        public async Task<ActionResult<Flight>> CreateFlight(Flight flight)
        {
            Console.WriteLine($"🔹 Incoming Flight Data: {JsonConvert.SerializeObject(flight)}");
            try
            {
                await _flightRepo.CreateFlightAsync(flight);
                return CreatedAtAction(nameof(GetFlight), new { id = flight.FlightId }, flight);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"❌ Error in CreateFlight: {ex.Message}");
                return BadRequest(ex.Message);
            }
        }




        // PUT - update
        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateFlight(int id, Flight flight)
        {
            if (id != flight.FlightId)
                return BadRequest();
            if (!await _flightRepo.FlightExistsAsync(id))
                return NotFound();
            try
            {
                await _flightRepo.UpdateFlightAsync(id, flight);
                return NoContent();
            }
            catch (Exception ex)
            {
                throw new Exception($"can not update the flight {id} ", ex);
            }
        }
         
        // DELETE - delete
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteFlight(int id)
        {
            var flight = await _flightRepo.GetFlightByIdAsync(id);
            if (flight == null)
                return NotFound();
            try
            {
                await _flightRepo.DeleteFlightAsync(id);
                return NoContent();
            }
            catch(Exception ex) { throw new Exception($"can not delete the flight {id} ", ex); }
        }

        private Task<bool> FlightExists(int id)
        {
            return _flightRepo.FlightExistsAsync(id);
        }
    }
}
