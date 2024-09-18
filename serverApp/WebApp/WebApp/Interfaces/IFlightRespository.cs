using WebApp.Models;

namespace WebApp.Interfaces
{
    public interface IFlightRespository
    {
        Task<List<Flight>> GetFlightsAsync();
    }
}
