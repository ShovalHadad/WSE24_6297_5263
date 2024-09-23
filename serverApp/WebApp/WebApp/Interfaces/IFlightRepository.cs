using WebApp.Models;

namespace WebApp.Interfaces
{
    public interface IFlightRepository
    {
        Task<IEnumerable<Flight>> GetFlightsAsync();
        Task<Flight> GetFlightByIdAsync(int id);
        Task CreateFlightAsync(Flight flight);
        Task UpdateFlightAsync(Flight flight);
        Task DeleteFlightAsync(int id);
        Task<bool> FlightExistsAsync(int id);
    }
}
