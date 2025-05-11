﻿using Microsoft.EntityFrameworkCore;
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
                return flightTicket;
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
                FlightTicket emptyTicket = new FlightTicket();
                if(flightTicket.TicketType == emptyTicket.TicketType || flightTicket.UserId == emptyTicket.UserId || flightTicket.FlightId == emptyTicket.FlightId)
                    throw new FlightTicketRepositoryException("one of the fields is missing.");
                FrequentFlyer? flyer = _context.FrequentFlyers.FirstOrDefault(e => e.FlyerId == flightTicket.UserId);
                if (flyer == null)
                    throw new FlightTicketRepositoryException("can not find the flyer.");
                Flight? flight = _context.Flights.FirstOrDefault(e => e.FlightId == flightTicket.FlightId);
                if (flight == null)
                    throw new FlightTicketRepositoryException("can not find the flight.");
                else
                {
                    Flight emptyFlight = new Flight();
                    if (flight.EstimatedArrivalDateTime != emptyFlight.EstimatedArrivalDateTime)
                        flightTicket.ShabatTimes = await _hebCalService.GetShabbatTimesAndParashaAsync(flight.EstimatedArrivalDateTime);
                }
                switch (flightTicket.TicketType)
                {
                    case 1:
                        {
                            flightTicket.price = "1500$";
                            if (flight?.NumOfTakenSeats1 != 0)
                                flight.NumOfTakenSeats1--;
                            else
                                throw new FlightTicketRepositoryException("there is no sits left in this class");
                        }
                        break;
                    case 2:
                        {
                            flightTicket.price = "800$";
                            if (flight?.NumOfTakenSeats2 != 0)
                                flight.NumOfTakenSeats2--;
                            else
                                throw new FlightTicketRepositoryException("there is no sits left in this class");
                        }
                        break;
                    case 3:
                        {
                            flightTicket.price = "300$";
                            if (flight?.NumOfTakenSeats3 != 0)
                                flight.NumOfTakenSeats3--;
                            else
                                throw new FlightTicketRepositoryException("there is no sits left in this class");
                        }
                        break;
                    case 0:
                        throw new FlightTicketRepositoryException("Ticket Type is required.");
                    default:
                        throw new FlightTicketRepositoryException("something went wrong in ticket type.");
                }
                flightTicket.CreatedDate = DateTime.Now;
                _context.FlightTickets.Add(flightTicket);
                await _context.SaveChangesAsync();
                var flightT = _context.FlightTickets.FirstOrDefault(e => e.FlightId == flightTicket.FlightId && e.UserId == flightTicket.UserId);
                if (flyer.FlightsIds == null) flyer.FlightsIds = new List<int>();
                flyer.FlightsIds.Add(flightT.FlightId);
                await _context.SaveChangesAsync();
            }
            catch (Exception ex)
            {
                throw new FlightTicketRepositoryException("An error occurred while creating the flight ticket.", ex);
            }
        }

        // update a flight ticket
        public async Task UpdateFlightTicketAsync(int id, FlightTicket flightTicket)
        {
            try
            {
                FlightTicket emptyTicket = new FlightTicket();
                FlightTicket oldTicket = _context.FlightTickets.FirstOrDefault(e => e.TicketId == id);
                if (oldTicket == null)
                    throw new FlightTicketRepositoryException("Can not find the ticket.");
                if (oldTicket.TicketType != flightTicket.TicketType && flightTicket.TicketType != emptyTicket.TicketType) // changed the ticket class
                {
                    Flight flight = _context.Flights.FirstOrDefault(e => e.FlightId == oldTicket.FlightId);
                    if (flight == null)
                        throw new FlightTicketRepositoryException("can not find the flight that in the ticket.");
                    switch(oldTicket.TicketType)  // cancel the old seat
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
                    switch(flightTicket.TicketType)  // add the new seat
                    {
                        case 1:
                            {
                                if (flight.NumOfTakenSeats1 != 0)
                                {
                                    flight.NumOfTakenSeats1--;
                                    oldTicket.TicketType = flightTicket.TicketType;
                                    oldTicket.price = "1500$";
                                }
                                else
                                    throw new FlightTicketRepositoryException("there is no seats left in this class");
                            }
                            break;
                        case 2:
                            {
                                if (flight.NumOfTakenSeats2 != 0)
                                {
                                    flight.NumOfTakenSeats2--;
                                    oldTicket.TicketType = flightTicket.TicketType;
                                    oldTicket.price = "800$";
                                }
                                else 
                                    throw new FlightTicketRepositoryException("there is no seats left in this class");
                            }
                            break;
                        case 3:
                            {
                                if (flight.NumOfTakenSeats3 != 0)
                                {
                                    flight.NumOfTakenSeats3--;
                                    oldTicket.TicketType = flightTicket.TicketType;
                                    oldTicket.price = "300$";
                                }
                                else
                                    throw new FlightTicketRepositoryException("there is no seats left in this class");
                            }
                            break;
                        default:
                            break;
                    }
                }
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
                FlightTicket? flightTicket = _context.FlightTickets.FirstOrDefault(e => e.TicketId == id);
                Flight? flight = _context.Flights.FirstOrDefault(e => e.FlightId == flightTicket.FlightId);
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
                FrequentFlyer? flyer = _context.FrequentFlyers.FirstOrDefault(e => e.FlyerId == flightTicket.UserId);
                if(flyer != null)
                    flyer.FlightsIds.Remove(flightTicket.FlightId);
                
                if(flightTicket != null)
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