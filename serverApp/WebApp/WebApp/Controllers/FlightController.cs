using Microsoft.AspNetCore.Mvc;
using System;
using WebApp.Models;
using WebApp.Data;
using Microsoft.EntityFrameworkCore;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace WebApp.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class FlightController : ControllerBase
    {
        private readonly ApplicationDBContext _context;

        public FlightController(ApplicationDBContext context)
        {
            _context = context;
        }



        //GET - read
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Flight>>> GetFlights()
        {
            return await _context.Flights.ToListAsync();
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<Flight>> GetFlight(int id) //GetFlight([FromeRoute] int id) - optional
        {
            var flight = await _context.Flights.FindAsync(id);
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
            _context.Flights.Add(flight);
            await _context.SaveChangesAsync();
            return CreatedAtAction(nameof(GetFlight), new { id = flight.FlightId }, flight);
        }


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

        private bool FlightExists(int id)
        {
            return _context.Flights.Any(e => e.FlightId == id);
        }


        /* another option->
         public async Task<IActionResult> PutFlight(int id, Flight flight)
        {
            if (id != flight.FlightId)
            {
                return BadRequest();
            }

            _context.Entry(flight).State = EntityState.Modified;

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

            return NoContent();
        }
         */



        //DELETE
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteFlight(int id)
        {
            var flight = await _context.Flights.FindAsync(id);
            if (flight == null)
            {
                return NotFound(); // Return 404 if the flight doesn't exist
            }

            // Remove the flight from the database
            _context.Flights.Remove(flight);
            await _context.SaveChangesAsync();

            return NoContent(); // Return 204 No Content after successful deletion
        }

    }
}
