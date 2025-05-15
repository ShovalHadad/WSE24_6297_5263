using WebApp.Models;

namespace WebApp.Interfaces
{
    public interface IFlightRepository
    {
        Task<IEnumerable<Flight>> GetFlightsAsync(); //אוסף נתונים של טיסה
        Task<Flight> GetFlightByIdAsync(int id);
        Task CreateFlightAsync(Flight flight);
        Task UpdateFlightAsync(int id, Flight flight);
        Task DeleteFlightAsync(int id);
        Task<bool> FlightExistsAsync(int id);
    }
}
