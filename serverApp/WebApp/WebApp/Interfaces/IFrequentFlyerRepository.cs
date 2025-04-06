using WebApp.Models;
using Microsoft.AspNetCore.Mvc;

namespace WebApp.Interfaces
{
    public interface IFrequentFlyerRepository
    {
        Task<IEnumerable<FrequentFlyer>> GetFrequentFlyersAsync();
        Task<FrequentFlyer> GetFrequentFlyerByIdAsync(int id);
        Task CreateFrequentFlyerAsync(FrequentFlyer frequentFlyer);
        Task LoginFrequentFlyerAsync(FrequentFlyer loginRequest);
        Task UpdateFrequentFlyerAsync(int id, FrequentFlyer frequentFlyer);
        Task DeleteFrequentFlyerAsync(int id);
        Task<bool> FrequentFlyerExistsAsync(int id);
    }
}
