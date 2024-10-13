using Microsoft.EntityFrameworkCore;
using WebApp.Data;
using WebApp.Exceptions;
using WebApp.Interfaces;
using WebApp.models;
using WebApp.Models;
using WebApp.Services;

namespace WebApp.Repository
{
    public class FlightTicketRepository : IFlightTicketRepository
    {
        private readonly ApplicationDBContext _context;
        private readonly HebCalService _hebCalService;

        // Constructor
        public FlightTicketRepository(ApplicationDBContext context, HebCalService hebCalService)
        {
            _context = context;
            _hebCalService = hebCalService;
        }

        // read all flight tickets
        public async Task<IEnumerable<FlightTicket>> GetFlightTicketsAsync()
        {
            try
            {
                return await _context.FlightTickets.ToListAsync();
            }
            catch (Exception ex)
            {
                throw new FlightTicketRepositoryException("Failed to retrieve flight tickets.", ex);
            }
        }

        // read flight ticket by id
        public async Task<FlightTicket> GetFlightTicketByIdAsync(int id)
        {
            try
            {
                var flightTicket = await _context.FlightTickets.FindAsync(id);
                if (flightTicket == null)
                    throw new FlightTicketRepositoryException($"Flight ticket with ID {id} not found.");
                return flightTicket;   // return await _context.FlightTickets.FirstOrDefaultAsync(ft => ft.TicketId == id);
            }
            catch (Exception ex)
            {
                throw new FlightTicketRepositoryException("An error occurred while retrieving the flight ticket.", ex);
            }
        }

        // create new flight ticket
        public async Task CreateFlightTicketAsync(FlightTicket flightTicket)
        {
            try
            {
                if (await _context.FrequentFlyers.FindAsync(flightTicket.UserId) == null)
                    throw new FlightTicketRepositoryException();
                var flight = await _context.Flights.FindAsync(flightTicket.FlightId);
                if ( flight == null) 
                    throw new FlightTicketRepositoryException();
                else
                {
                    if(flight.EstimatedArrivalDateTime != null)
                    {
                        flightTicket.ShabatTimes = await _hebCalService.GetHebrewDates(flight.EstimatedArrivalDateTime.ToString()); 
                        // flightTicket.ShabatTimes = _hebCalService.GetHebrewDates(flight.EstimatedArrivalDateTime.ToString()).Result;
                    }
                }
                switch (flightTicket.TicketType)  
                {
                    case 1:
                        if (flight?.NumOfTakenSeats1 != 0)
                            flight.NumOfTakenSeats1--;  
                            //_context.Flights.Update(flight);
                        else 
                            throw new FlightTicketRepositoryException("there is no sits left in this class");
                        break;
                    case 2:
                        if (flight?.NumOfTakenSeats2 != 0)
                            flight.NumOfTakenSeats2--;
                        else 
                            throw new FlightTicketRepositoryException("there is no sits left in this class");
                        break;
                    case 3:
                        if (flight?.NumOfTakenSeats3 != 0)
                            flight.NumOfTakenSeats3--;
                        else 
                            throw new FlightTicketRepositoryException("there is no sits left in this class");
                        break;
                    case 0:
                        throw new FlightTicketRepositoryException("Ticket Type is required.");
                    default:
                        throw new FlightTicketRepositoryException("something went wrong in ticket type.");
                }
                _context.FlightTickets.Add(flightTicket);
                await _context.SaveChangesAsync();
            }
            catch (Exception ex)
            {
                throw new FlightTicketRepositoryException("An error occurred while creating the flight ticket.", ex);
            }
        }

        // update a flight ticket
        public async Task UpdateFlightTicketAsync(FlightTicket flightTicket)
        {
            try
            {
                FlightTicket newTicket = _context.FlightTickets.FirstOrDefault(e => e.TicketId == flightTicket.TicketId);
                if(newTicket.TicketType != flightTicket.TicketType) // changed the ticket class
                {
                    Flight flight = _context.Flights.FirstOrDefault(e => e.FlightId == flightTicket.FlightId);
                    switch(newTicket.TicketType)  // cancel the old set
                    {
                        case 1:
                            flight.NumOfTakenSeats1++;
                            break;
                        case 2:
                            flight.NumOfTakenSeats2++;
                            break;
                        case 3:
                            flight.NumOfTakenSeats3++;
                            break;
                        default:
                            break;
                    }
                    switch(flightTicket.TicketType)  // add the new set
                    {
                        case 1:
                            {
                                if (flight.NumOfTakenSeats1 != 0)
                                {
                                    flight.NumOfTakenSeats1--;
                                    newTicket.TicketType = flightTicket.TicketType;
                                }
                                else
                                    throw new FlightTicketRepositoryException("there is no sits left in this class");
                            }
                            break;
                        case 2:
                            {
                                if (flight.NumOfTakenSeats2 != 0)
                                {
                                    flight.NumOfTakenSeats2--;
                                    newTicket.TicketType = flightTicket.TicketType;
                                }
                                else 
                                    throw new FlightTicketRepositoryException("there is no sits left in this class");
                            }
                            break;
                        case 3:
                            {
                                if (flight.NumOfTakenSeats3 != 0)
                                {
                                    flight.NumOfTakenSeats3--;
                                    newTicket.TicketType = flightTicket.TicketType;
                                }
                                else
                                    throw new FlightTicketRepositoryException("there is no sits left in this class");
                            }
                            break;
                        default:
                            break;
                    }
                }
                if (newTicket.UserId != flightTicket.UserId || newTicket.FlightId != flightTicket.FlightId)
                    throw new FlightTicketRepositoryException("can not have different user or flight numbers.");
               // _context.Entry(flightTicket).State = EntityState.Modified;
                await _context.SaveChangesAsync();
            }
            catch (Exception ex)
            {
                throw new FlightTicketRepositoryException("An error occurred while updating the flight ticket.", ex);
            }
        }

        // delete flight ticket by id
        public async Task DeleteFlightTicketAsync(int id)
        {
            try
            {
                var flightTicket = await _context.FlightTickets.FindAsync(id);
                if (flightTicket == null)
                    throw new FlightTicketRepositoryException($"can not find flight ticket with {id} id to delete.");
                Flight? flight = await _context.Flights.FindAsync(flightTicket.FlightId);
                if (flight != null)
                {
                    switch (flightTicket.TicketType)
                    {
                        case 1:
                            flight.NumOfTakenSeats1++;
                            break;
                        case 2:
                            flight.NumOfTakenSeats2++;
                            break;
                        case 3:
                            flight.NumOfTakenSeats3++;
                            break;
                        default:
                            break;
                    }
                }
                FrequentFlyer? flyer = await _context.FrequentFlyers.FindAsync(flightTicket.UserId);
                if(flyer != null)
                {
                    flyer.FlightsIds.Remove(flight.FlightId);
                }
                _context.FlightTickets.Remove(flightTicket);
                await _context.SaveChangesAsync();
            }
            catch (Exception ex)
            {
                throw new FlightTicketRepositoryException("An error occurred while deleting the flight ticket.", ex);
            }
        }

        // function to know if the flight ticket exist by id
        public async Task<bool> FlightTicketExistsAsync(int id)
        {
            return await _context.FlightTickets.AnyAsync(e => e.TicketId == id);
        }
    }
}
