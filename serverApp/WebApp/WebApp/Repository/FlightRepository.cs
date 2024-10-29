using Microsoft.EntityFrameworkCore;
using WebApp.Data;
using WebApp.Interfaces;
using WebApp.Models;
using System.Collections.Generic;
using System.Threading.Tasks;
using WebApp.Exceptions;
using WebApp.models;
using WebApp.Services;
using System.Globalization;


namespace WebApp.Repositories
{
    public class FlightRepository : IFlightRepository
    {
        private readonly ApplicationDBContext _context;
        private readonly HebCalService _hebCalService;

        // Constructor
        public FlightRepository(ApplicationDBContext context, HebCalService hebCalService)
        {
            _context = context;
            _hebCalService = hebCalService;
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
                    if(flight.EstimatedArrivalDateTime != null)
                        if(await _hebCalService.IsDateInShabbat(flight.EstimatedArrivalDateTime) == false)
                            throw new FlightRepositoryException("can not create a flight that arrived in Shabbat.");
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
                Flight? oldFlight =  _context.Flights.FirstOrDefault(e => e.FlightId == flight.FlightId);
                if (oldFlight.PlaneId != flight.PlaneId)  // change planes 
                {
                    var oldPlane = await _context.Planes.FindAsync(oldFlight.PlaneId);
                    // number of people in every department in the flight
                    int? numOfFlyers1 = oldPlane.NumOfSeats1 - oldFlight.NumOfTakenSeats1;
                    int? numOfFlyers2 = oldPlane.NumOfSeats2 - oldFlight.NumOfTakenSeats2;
                    int? numOfFlyers3 = oldPlane.NumOfSeats3 - oldFlight.NumOfTakenSeats3;
                    Plane newPlane = await _context.Planes.FindAsync(flight.PlaneId);
                    // update number of people in every department
                    flight.NumOfTakenSeats1 = newPlane.NumOfSeats1 - numOfFlyers1;
                    flight.NumOfTakenSeats2 = newPlane.NumOfSeats2 - numOfFlyers2;
                    flight.NumOfTakenSeats3 = newPlane.NumOfSeats3 - numOfFlyers3;
                }
                if (flight.DepartureDateTime != oldFlight.DepartureDateTime || flight.EstimatedArrivalDateTime != oldFlight.EstimatedArrivalDateTime)  // change date times
                {
                    if (flight.EstimatedArrivalDateTime < flight.DepartureDateTime)
                        throw new FlightRepositoryException("Departure date time is bigger then arrival date time.");
                    if (flight.EstimatedArrivalDateTime != null && flight.EstimatedArrivalDateTime != oldFlight.EstimatedArrivalDateTime)
                    {
                        foreach (FlightTicket flightTicket in await _context.FlightTickets.ToListAsync())
                        {
                            if (flightTicket.FlightId == flight.FlightId) // to find the flight tickets that in this flight
                                flightTicket.ShabatTimes = await _hebCalService.GetShabbatTimesAndParashaAsync(flight.EstimatedArrivalDateTime); // update Shabbat times
                        }
                    }
                }
                oldFlight.EstimatedArrivalDateTime =(flight.EstimatedArrivalDateTime != null) ? flight.EstimatedArrivalDateTime : oldFlight.EstimatedArrivalDateTime;
                oldFlight.DepartureDateTime = (flight.DepartureDateTime != null) ? flight.DepartureDateTime : oldFlight.DepartureDateTime;
                oldFlight.ArrivalLocation = (flight.ArrivalLocation != null) ? flight.ArrivalLocation : oldFlight.ArrivalLocation;
                oldFlight.DepartureLocation = (flight.DepartureLocation != null) ? flight.DepartureLocation : oldFlight.DepartureLocation;
                oldFlight.NumOfTakenSeats1 = flight.NumOfTakenSeats1;
                oldFlight.NumOfTakenSeats2 = flight.NumOfTakenSeats2;
                oldFlight.NumOfTakenSeats3 = flight.NumOfTakenSeats3;
                oldFlight.PlaneId = flight.PlaneId;
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
                Flight? flight = _context.Flights.FirstOrDefault(e => e.FlightId == id);
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
                            frequentFlyer.FlightsIds.Remove(flightTicket.TicketId);
                        }
                    }
                    foreach (int ids in ticketsIds) // delete the flight tickets that are in this flight
                        _context.FlightTickets.Remove(_context.FlightTickets.FirstOrDefault(e => e.TicketId == ids));
                    if (flight != null)
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