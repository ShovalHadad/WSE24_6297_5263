using Microsoft.EntityFrameworkCore;
using WebApp.Data;
using WebApp.Exceptions;
using WebApp.Interfaces;
using WebApp.models;
using WebApp.Models;

namespace WebApp.Repository
{
    public class FrequentFlyerRepository : IFrequentFlyerRepository
    {
        private readonly ApplicationDBContext _context;
        // Constructor
        public FrequentFlyerRepository(ApplicationDBContext context)
        {
            _context = context;
        }

        // read all frequent flyers
        public async Task<IEnumerable<FrequentFlyer>> GetFrequentFlyersAsync()
        {
            try
            {
                return await _context.FrequentFlyers.ToListAsync();
            }
            catch (Exception ex) 
            {
                throw new FrequentFlyerRepositoryException("Failed to retrieve frequent flyers.", ex);
            }
        }

        // read frequent flyer by id
        public async Task<FrequentFlyer> GetFrequentFlyerByIdAsync(int id)
        {
            try
            {
                var flyer = await _context.FrequentFlyers.FindAsync(id);
                if (flyer == null)
                    throw new FrequentFlyerRepositoryException($"Flyer with ID {id} not found.");
                return flyer;
            }
            catch (Exception ex)
            {
                throw new FrequentFlyerRepositoryException("An error occurred while retrieving the frequent flyer.", ex);
            }
        }

        // create new frequent flyer
        public async Task CreateFrequentFlyerAsync(FrequentFlyer frequentFlyer)
        {
            try
            {
                if (frequentFlyer.Password == "" || frequentFlyer.Password == "string")
                    throw new FrequentFlyerRepositoryException("Password is required.");
                if (frequentFlyer.FirstName == "" || frequentFlyer.FirstName == "string")
                    throw new FrequentFlyerRepositoryException("First name is required.");
                if (frequentFlyer.LastName == "" || frequentFlyer.LastName == "string")
                    throw new FrequentFlyerRepositoryException("Last name is required.");
                if (frequentFlyer.UserName == "" || frequentFlyer.UserName == "string")
                    throw new FrequentFlyerRepositoryException("User name is required.");
                else   // check if this user name already exist  
                {
                    bool flag = false;
                    foreach (FrequentFlyer flyer in await _context.FrequentFlyers.ToListAsync())
                    {
                        if (frequentFlyer.UserName ==  flyer.UserName)
                            flag = true;
                    }
                    if (flag == true)
                        throw new FrequentFlyerRepositoryException($"{frequentFlyer.UserName} This user name already exist.");
                }
                _context.FrequentFlyers.Add(frequentFlyer);
                await _context.SaveChangesAsync();
            }
            catch (Exception ex)
            {
                throw new FrequentFlyerRepositoryException("", ex);
            }
        }

        // update a frequent flyer
        public async Task UpdateFrequentFlyerAsync(FrequentFlyer frequentFlyer)
        {
            try
            {
                FrequentFlyer? newFrequentFlyer = _context.FrequentFlyers.FirstOrDefault(e => e.FlyerId == frequentFlyer.FlyerId);
                if(newFrequentFlyer.UserName != frequentFlyer.UserName)
                {
                    bool flag = false;
                    foreach (FrequentFlyer flyer in await _context.FrequentFlyers.ToListAsync())
                    {
                        if (frequentFlyer.UserName == flyer.UserName)
                            flag = true;
                    }
                    if (flag == true)
                        throw new FrequentFlyerRepositoryException($"{frequentFlyer.UserName} This user name already exist.");
                }
                newFrequentFlyer.UserName = frequentFlyer.UserName;
                newFrequentFlyer.LastName = frequentFlyer.LastName;
                newFrequentFlyer.FirstName = frequentFlyer.FirstName;
                newFrequentFlyer.PhoneNumber = frequentFlyer.PhoneNumber;
                newFrequentFlyer.Password = frequentFlyer.Password;
                newFrequentFlyer.Email = frequentFlyer.Email;
                newFrequentFlyer.IsManager = frequentFlyer.IsManager;
                //newFrequentFlyer.FlightsIds = frequentFlyer.FlightsIds;
                //_context.Entry(frequentFlyer).State = EntityState.Modified;
                await _context.SaveChangesAsync();
            }
            catch (Exception ex)
            {
                throw new FrequentFlyerRepositoryException("An error occurred while updating the frequent flyer.", ex);
            }
        }

        // delete flight by id
        public async Task DeleteFrequentFlyerAsync(int id)
        {
            try
            {
                var frequentFlyer = await _context.FrequentFlyers.FindAsync(id);
                if (frequentFlyer == null)
                    throw new FrequentFlyerRepositoryException($"can not find frequent flyer with {id} id to delete."); // return;
                if (frequentFlyer.FlightsIds == null)
                {
                    _context.FrequentFlyers.Remove(frequentFlyer);
                    await _context.SaveChangesAsync();
                }
                else
                {
                    List<int> ticketsIds = new List<int>();
                    foreach (int flightId in frequentFlyer.FlightsIds)
                    {
                        Flight flight = await _context.Flights.FindAsync(flightId);
                        foreach (FlightTicket flightTicket in await _context.FlightTickets.ToListAsync())
                        {
                            if (flightTicket.UserId == id && flightTicket.FlightId == flightId)
                            {
                                ticketsIds.Add(flightTicket.TicketId);
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
                        }
                    }
                    foreach (int ids in ticketsIds)
                        _context.FlightTickets.Remove(_context.FlightTickets.FirstOrDefault(e => e.TicketId == ids));
                    _context.FrequentFlyers.Remove(frequentFlyer);
                    await _context.SaveChangesAsync();
                }
            }
            catch (Exception ex)
            {
                throw new FrequentFlyerRepositoryException(ex.Message, ex);
            }
        }

        // function to know if the frequent flyer exist by id
        public async Task<bool> FrequentFlyerExistsAsync(int id)
        {
            return await _context.FrequentFlyers.AnyAsync(e => e.FlyerId == id);
        }
    }

}
