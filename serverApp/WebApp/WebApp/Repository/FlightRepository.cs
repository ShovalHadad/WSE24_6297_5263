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
        private readonly ApplicationDBContext _context;  //הערך של המשתנה יכול להיות מאותחל רק פעם אחת
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
            Console.WriteLine($"🔹 Flight Data Received: {Newtonsoft.Json.JsonConvert.SerializeObject(flight)}");
            try
            {
               

                Flight emptyFlight = new Flight();
                if (flight.ArrivalLocation == emptyFlight.ArrivalLocation)
                    throw new FlightRepositoryException("Arrival locations is required.");
                if (flight.DepartureLocation == emptyFlight.DepartureLocation)
                    throw new FlightRepositoryException("Departure locations is required.");
                if (flight.PlaneId == emptyFlight.PlaneId)
                    throw new FlightRepositoryException("Plane Id is required.");
                var plane = await _context.Planes.FindAsync(flight.PlaneId);
                if (plane == null)
                    throw new FlightRepositoryException("A valid plane ID is required to create a flight.");
                flight.NumOfTakenSeats1 = plane.NumOfSeats1;
                flight.NumOfTakenSeats2 = plane.NumOfSeats2;
                flight.NumOfTakenSeats3 = plane.NumOfSeats3;
                if (flight.ArrivalLocation == emptyFlight.ArrivalLocation || flight.DepartureLocation == emptyFlight.ArrivalLocation || flight.ArrivalLocation == "string" || flight.DepartureLocation == "string")
                    throw new FlightRepositoryException("one of Departure or arrival location is null");
                if (flight.EstimatedArrivalDateTime.ToString("O").EndsWith("Z"))
                    throw new FlightRepositoryException("The Arrival date time is null");
                if (flight.DepartureDateTime.ToString("O").EndsWith("Z"))
                    throw new FlightRepositoryException("The Departure date time is null");
                if (flight.EstimatedArrivalDateTime != emptyFlight.EstimatedArrivalDateTime && flight.DepartureDateTime != emptyFlight.DepartureDateTime)
                {
                    if (await _hebCalService.IsDateInShabbat(flight.EstimatedArrivalDateTime) == true)
                        throw new FlightRepositoryException("can not create a flight that arrived in Shabbat.");
                    if (flight.EstimatedArrivalDateTime < flight.DepartureDateTime)
                        throw new FlightRepositoryException("Departure date time is bigger then arrival date time.");
                }
                else
                    throw new FlightRepositoryException("one of Departure or Arrival date time is null");
                _context.Flights.Add(flight);
                await _context.SaveChangesAsync();
            }
            catch (Exception ex)
            {
                throw new FlightRepositoryException("An error occurred while creating the flight.", ex);
            }
        }

        // update a flight
        public async Task UpdateFlightAsync(int id, Flight flight)
        {
            try
            {
                Flight emptyFlight = new Flight();
                emptyFlight.EstimatedArrivalDateTime = DateTime.Now;
                emptyFlight.DepartureDateTime = DateTime.Now;
                Flight? oldFlight = _context.Flights.FirstOrDefault(e => e.FlightId == id);
                if (oldFlight == null)
                    throw new FlightRepositoryException("can not find the flight.");
                if (oldFlight.PlaneId != flight.PlaneId && flight.PlaneId != emptyFlight.PlaneId)  // change planes 
                {
                    var oldPlane = await _context.Planes.FindAsync(oldFlight.PlaneId);
                    // number of people in every department in the flight
                    int? numOfFlyers1 = oldPlane.NumOfSeats1 - oldFlight.NumOfTakenSeats1;
                    int? numOfFlyers2 = oldPlane.NumOfSeats2 - oldFlight.NumOfTakenSeats2;
                    int? numOfFlyers3 = oldPlane.NumOfSeats3 - oldFlight.NumOfTakenSeats3;
                    Plane newPlane = await _context.Planes.FindAsync(flight.PlaneId);
                    // update number of people in every department
                    oldFlight.NumOfTakenSeats1 = newPlane.NumOfSeats1 - numOfFlyers1;
                    oldFlight.NumOfTakenSeats2 = newPlane.NumOfSeats2 - numOfFlyers2;
                    oldFlight.NumOfTakenSeats3 = newPlane.NumOfSeats3 - numOfFlyers3;
                    oldFlight.PlaneId = flight.PlaneId;  // update planeId
                }
               
                if (flight.DepartureDateTime.Date != emptyFlight.DepartureDateTime.Date &&
                   flight.EstimatedArrivalDateTime.Date != emptyFlight.EstimatedArrivalDateTime.Date)  // change date times
                {
                    if (flight.EstimatedArrivalDateTime < flight.DepartureDateTime)
                        throw new FlightRepositoryException("Departure date time is bigger then arrival date time.");
                    if (await _hebCalService.IsDateInShabbat(flight.EstimatedArrivalDateTime) == true)
                        throw new FlightRepositoryException("can not create a flight that arrived in Shabbat.");
                    oldFlight.DepartureDateTime = flight.DepartureDateTime;
                    oldFlight.EstimatedArrivalDateTime = flight.EstimatedArrivalDateTime;
                }
                else
                {
                    if (flight.DepartureDateTime.Date != emptyFlight.DepartureDateTime.Date)
                    {
                        if (oldFlight.EstimatedArrivalDateTime < flight.DepartureDateTime)
                            throw new FlightRepositoryException("Departure date time is bigger then arrival date time.");
                        oldFlight.DepartureDateTime = flight.DepartureDateTime;
                    }
                    else
                    {
                        if (flight.EstimatedArrivalDateTime.Date != emptyFlight.EstimatedArrivalDateTime.Date)
                        {
                            if (flight.EstimatedArrivalDateTime < oldFlight.DepartureDateTime)
                                throw new FlightRepositoryException("Departure date time is bigger then arrival date time.");
                            if (await _hebCalService.IsDateInShabbat(flight.EstimatedArrivalDateTime) == true)
                                throw new FlightRepositoryException("can not create a flight that arrived in Shabbat.");
                            foreach (FlightTicket flightTicket in await _context.FlightTickets.ToListAsync())
                            {
                                if (flightTicket.FlightId == flight.FlightId) // to find the flight tickets that in this flight
                                    flightTicket.ShabatTimes = await _hebCalService.GetShabbatTimesAndParashaAsync(flight.EstimatedArrivalDateTime); // update Shabbat times
                            }
                            oldFlight.EstimatedArrivalDateTime = flight.EstimatedArrivalDateTime;
                        }
                    }
                }
                oldFlight.ArrivalLocation = (flight.ArrivalLocation != emptyFlight.ArrivalLocation && flight.ArrivalLocation != "string") ? flight.ArrivalLocation : oldFlight.ArrivalLocation;
                oldFlight.DepartureLocation = (flight.DepartureLocation != emptyFlight.DepartureLocation && flight.DepartureLocation != "string") ? flight.DepartureLocation : oldFlight.DepartureLocation;
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
                            frequentFlyer.FlightsIds.Remove(flightTicket.FlightId);
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