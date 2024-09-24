using WebApp.Models;

namespace WebApp.Interfaces
{
    public interface IFrequentFlyerRepository
    {
        Task<IEnumerable<FrequentFlyer>> GetFrequentFlyersAsync();
        Task<FrequentFlyer> GetFrequentFlyerByIdAsync(int id);
        Task CreateFrequentFlyerAsync(FrequentFlyer frequentFlyer);
        Task UpdateFrequentFlyerAsync(FrequentFlyer frequentFlyer);
        Task DeleteFrequentFlyerAsync(int id);
        Task<bool> FrequentFlyerExistsAsync(int id);
    }
}
