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
        private readonly ApplicationDBContext _context;  // _context = list of flights
        // constractor 
        public FlightController(ApplicationDBContext context)
        {
            _context = context;
        }

        /// <summary>
        /// GET ALL - read all
        /// returns the flights from _context in a list
        /// </summary>
        /// <returns> list of flights </returns>
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Flight>>> GetFlights()
        {
            return await _context.Flights.ToListAsync();
        }

        /// <summary>
        /// GET - read
        /// returns a flight from _context that match the id
        /// </summary>
        /// <param name="id"> id of wanted flight </param>
        /// <returns> flight </returns>
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

        /// <summary>
        /// POST - create
        /// creates a new flight and add to _context
        /// </summary>
        /// <param name="flight"> the new flight </param>
        /// <returns> result of CreatedAtAction </returns>
        [HttpPost]
        public async Task<ActionResult<Flight>> CreateFlight(Flight flight)
        {
            // set the number of sites in the plane
            var plane = await _context.Planes.FindAsync(flight.PlaneId);
            flight.NumOfTakenSeats1 = plane?.NumOfSeats1;
            flight.NumOfTakenSeats2 = plane?.NumOfSeats2;
            flight.NumOfTakenSeats3 = plane?.NumOfSeats3;
            _context.Flights.Add(flight);
            await _context.SaveChangesAsync();
            return CreatedAtAction(nameof(GetFlight), new { id = flight.FlightId }, flight);
        }

        /// <summary>
        /// PUT- update
        /// updates the flight that match the id with the updatedFlight
        /// </summary>
        /// <param name="id"> the id fo the flight we need to update </param>
        /// <param name="updatedFlight"> the flight with the updated details </param>
        /// <returns> NoContent if update was successful </returns>
        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateFlight(int id, Flight updatedFlight)
        {
            var flight = await _context.Flights.FindAsync(id);
            if (flight == null)
            {
                return NotFound(); // Return a 404 Not Found if the flight does not exist
            }

            // Update the flight fields
            flight.PlaneId = updatedFlight.PlaneId;
            var plane = await _context.Planes.FindAsync(flight.PlaneId);
            flight.DepartureLocation = updatedFlight.DepartureLocation;
            flight.ArrivalLocation = updatedFlight.ArrivalLocation;
            flight.DepartureDateTime = updatedFlight.DepartureDateTime;
            flight.EstimatedArrivalDateTime = updatedFlight.EstimatedArrivalDateTime;
            flight.NumOfTakenSeats1 = plane?.NumOfSeats1;
            flight.NumOfTakenSeats2 = plane?.NumOfSeats2;
            flight.NumOfTakenSeats3 = plane?.NumOfSeats3;

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

        /// <summary>
        /// DELETE - delete
        /// deletes the flight that match the id
        /// </summary>
        /// <param name="id"> id of the flight we need to delete </param>
        /// <returns> NoContent if delete was successful </returns>
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
        
        // private function for Update function
        private bool FlightExists(int id)
        {
            return _context.Flights.Any(e => e.FlightId == id);
        }
    }
}
