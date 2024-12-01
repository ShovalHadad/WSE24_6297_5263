using WebApp.models;

namespace WebApp.Interfaces
{
    public interface IFlightTicketRepository
    {
        Task<IEnumerable<FlightTicket>> GetFlightTicketsAsync();
        Task<FlightTicket> GetFlightTicketByIdAsync(int id);
        Task CreateFlightTicketAsync(FlightTicket flightTicket);
        Task UpdateFlightTicketAsync(int id, FlightTicket flightTicket);
        Task DeleteFlightTicketAsync(int id);
        Task<bool> FlightTicketExistsAsync(int id);
    }
}
