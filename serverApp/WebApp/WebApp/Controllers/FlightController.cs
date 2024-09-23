using Microsoft.AspNetCore.Mvc;
using System;
using WebApp.Models;
using WebApp.Data;
using WebApp.Interfaces;
using Microsoft.EntityFrameworkCore;


namespace WebApp.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class FlightController : ControllerBase
    {
        private readonly ApplicationDBContext _context;
        private readonly IFlightRepository _flightRepo;

        public FlightController(ApplicationDBContext context, IFlightRepository flightRepo)
        {
            _context = context;
            _flightRepo = flightRepo;
        }


        //GET - read
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Flight>>> GetFlights()
        {
            var flights = await _flightRepo.GetFlightsAsync();
            return Ok(flights);
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<Flight>> GetFlight(int id) //GetFlight([FromeRoute] int id) - optional
        {
            var flight = await _flightRepo.GetFlightByIdAsync(id);
            if (flight == null)
            {
                return NotFound();
            }
            return flight;
        }
        

        //POST - create
        [HttpPost]
        public async Task<ActionResult<Flight>> CreateFlight(Flight flight)
        {
            await _flightRepo.CreateFlightAsync(flight);
            return CreatedAtAction(nameof(GetFlight), new { id = flight.FlightId }, flight);
        }

        /*
        //PUT- update
        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateFlight(int id, Flight updatedFlight)
        {
            var flight = await _context.Flights.FindAsync(id);
            if (flight == null)
            {
                return NotFound(); // Return a 404 Not Found if the flight does not exist
            }

            // Update the flight fields
            flight.DepartureLocation = updatedFlight.DepartureLocation;
            flight.ArrivalLocation = updatedFlight.ArrivalLocation;
            flight.DepartureDateTime = updatedFlight.DepartureDateTime;
            flight.EstimatedArrivalDateTime = updatedFlight.EstimatedArrivalDateTime;
            flight.NumOfTakenSeats1 = updatedFlight.NumOfTakenSeats1;
            flight.NumOfTakenSeats2 = updatedFlight.NumOfTakenSeats2;
            flight.NumOfTakenSeats3 = updatedFlight.NumOfTakenSeats3;

            // Save changes to the database
            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!FlightExists(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            return NoContent(); // Return 204 No Content on successful update
        }
        */


        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateFlight(int id, Flight flight)
        {
            if (id != flight.FlightId)
            {
                return BadRequest();
            }

            try
            {
                await _flightRepo.UpdateFlightAsync(flight);
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!await _flightRepo.FlightExistsAsync(id))
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
         



        //DELETE
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteFlight(int id)
        {
            var flight = await _flightRepo.GetFlightByIdAsync(id);
            if (flight == null)
            {
                return NotFound();
            }

            await _flightRepo.DeleteFlightAsync(id);
            return NoContent();
        }

        private Task<bool> FlightExists(int id)
        {
            //return _context.Flights.Any(e => e.FlightId == id);
            return _flightRepo.FlightExistsAsync(id);
        }

    }
}
