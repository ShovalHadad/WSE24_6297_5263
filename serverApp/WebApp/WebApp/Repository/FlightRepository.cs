using Microsoft.EntityFrameworkCore;
using WebApp.Data;
using WebApp.Interfaces;
using WebApp.Models;
using System.Collections.Generic;
using System.Threading.Tasks;
using WebApp.Exceptions;
using WebApp.models;


namespace WebApp.Repositories
{
    public class FlightRepository : IFlightRepository
    {
        private readonly ApplicationDBContext _context;
        // Constructor
        public FlightRepository(ApplicationDBContext context)
        {
            _context = context;
        }

        // read all flights
        public async Task<IEnumerable<Flight>> GetFlightsAsync()
        {
            try
            {
                return await _context.Flights.ToListAsync();
            }
            catch (Exception ex)
            {
                throw new FlightRepositoryException("Failed to retrieve flights.", ex);
            }
        }

        // read flight by id
        public async Task<Flight> GetFlightByIdAsync(int id)
        {
            try
            {
                var flight = await _context.Flights.FindAsync(id);
                if (flight == null)
                    throw new FlightRepositoryException($"Flight with ID {id} not found.");
                return flight;
            }
            catch (Exception ex)
            {
                throw new FlightRepositoryException("An error occurred while retrieving the flight.", ex);
            }
        }

        // create new flight
        public async Task CreateFlightAsync(Flight flight)
        {
            try
            {
                if (flight.DepartureLocation == "string" || flight.ArrivalLocation == "string" || flight.ArrivalLocation == "" || flight.DepartureLocation == "")
                    throw new FlightRepositoryException("Departure or arrival locations are required.");
                var plane = await _context.Planes.FindAsync(flight.PlaneId);
                if (plane == null)
                    throw new FlightRepositoryException("A valid plane ID is required to create a flight.");
                flight.NumOfTakenSeats1 = plane.NumOfSeats1;
                flight.NumOfTakenSeats2 = plane.NumOfSeats2;
                flight.NumOfTakenSeats3 = plane.NumOfSeats3;
                if (flight.EstimatedArrivalDateTime != null || flight.DepartureDateTime != null)
                {
                    if (flight.EstimatedArrivalDateTime != null && flight.DepartureDateTime != null)
                    {
                        if (flight.EstimatedArrivalDateTime < flight.DepartureDateTime)
                            throw new FlightRepositoryException("Departure date time is bigger then arrival date time.");
                    }
                    else 
                        throw new FlightRepositoryException("one of Departure or arrival date time is null");
                }
                _context.Flights.Add(flight);
                await _context.SaveChangesAsync();
            }
            catch (Exception ex)
            {
                throw new FlightRepositoryException("An error occurred while creating the flight.", ex);
            }
        }

        // update a flight
        public async Task UpdateFlightAsync(Flight flight)
        {
            try
            {
                var newFlight =  _context.Flights.FirstOrDefault(e => e.FlightId == flight.FlightId);
                if (newFlight.PlaneId != flight.PlaneId)  // change planes 
                {
                    var oldPlane = await _context.Planes.FindAsync(newFlight.PlaneId);
                    int? numOfFlyers1 = oldPlane.NumOfSeats1 - newFlight.NumOfTakenSeats1;
                    int? numOfFlyers2 = oldPlane.NumOfSeats2 - newFlight.NumOfTakenSeats2;
                    int? numOfFlyers3 = oldPlane.NumOfSeats3 - newFlight.NumOfTakenSeats3;
                    Plane newPlane = await _context.Planes.FindAsync(flight.PlaneId);
                    flight.NumOfTakenSeats1 = (newPlane.NumOfSeats1 == flight.NumOfTakenSeats1)? flight.NumOfTakenSeats1 - numOfFlyers1 : flight.NumOfTakenSeats1;
                    flight.NumOfTakenSeats2 = (newPlane.NumOfSeats2 == flight.NumOfTakenSeats2)? flight.NumOfTakenSeats2 - numOfFlyers2 : flight.NumOfTakenSeats2;
                    flight.NumOfTakenSeats3 = (newPlane.NumOfSeats3 == flight.NumOfTakenSeats3)? flight.NumOfTakenSeats3 - numOfFlyers3 : flight.NumOfTakenSeats3;
                }
                if(flight.DepartureDateTime != newFlight.DepartureDateTime || flight.EstimatedArrivalDateTime != newFlight.EstimatedArrivalDateTime)  // change date times
                    if (flight.EstimatedArrivalDateTime < flight.DepartureDateTime)
                        throw new FlightRepositoryException("Departure date time is bigger then arrival date time.");
                newFlight.EstimatedArrivalDateTime = flight.EstimatedArrivalDateTime;
                newFlight.DepartureDateTime = flight.DepartureDateTime;
                newFlight.ArrivalLocation = flight.ArrivalLocation;
                newFlight.DepartureLocation = flight.DepartureLocation;
                newFlight.NumOfTakenSeats1 = flight.NumOfTakenSeats1;
                newFlight.NumOfTakenSeats2 = flight.NumOfTakenSeats2;
                newFlight.NumOfTakenSeats3 = flight.NumOfTakenSeats3;
                newFlight.PlaneId = flight.PlaneId;
                await _context.SaveChangesAsync();
            }
            catch (Exception ex)
            {
                throw new FlightRepositoryException("An error occurred while updating the flight.", ex);
            }
        }

        // delete flight by id
        public async Task DeleteFlightAsync(int id)
        {
            try
            {
                var flight = await _context.Flights.FindAsync(id);
                if (flight == null)
                    throw new FlightRepositoryException($"can not find flight with {id} id to delete.");  // return;
                if (!await _context.FlightTickets.AnyAsync(e => e.FlightId == id)) // no flyer booked this flight
                {
                    _context.Flights.Remove(flight);
                    await _context.SaveChangesAsync();
                }
                else // flyer booked this flight
                {
                    List<int> ticketsIds = new List<int>();
                    foreach (FlightTicket flightTicket in await _context.FlightTickets.ToListAsync())
                    {
                        if(flightTicket.FlightId == id) // to find the people that in this flight
                        {
                            ticketsIds.Add(flightTicket.TicketId);
                            var frequentFlyer = _context.FrequentFlyers.FirstOrDefault(e => e.FlyerId == flightTicket.UserId);
                            frequentFlyer.FlightsIds.Remove(id);
                        }
                    }
                    foreach (int ids in ticketsIds)
                        _context.FlightTickets.Remove(_context.FlightTickets.FirstOrDefault(e => e.TicketId == ids));
                    _context.Flights.Remove(flight);
                    await _context.SaveChangesAsync();  
                }
            }
            catch (Exception ex)
            {
                throw new FlightRepositoryException("An error occurred while deleting the flight.", ex);
            }
        }

        // function to know if the flight exist by id
        public async Task<bool> FlightExistsAsync(int id)
        {
            return await _context.Flights.AnyAsync(e => e.FlightId == id);
        }
    }
}