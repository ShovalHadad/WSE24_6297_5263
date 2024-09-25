using Microsoft.EntityFrameworkCore;
using WebApp.Data;
using WebApp.Interfaces;
using WebApp.Models;

namespace WebApp.Repository
{
    public class FrequentFlyerRepository : IFrequentFlyerRepository
    {
        private readonly ApplicationDBContext _context;

        public FrequentFlyerRepository(ApplicationDBContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<FrequentFlyer>> GetFrequentFlyersAsync()
        {
            return await _context.FrequentFlyers.ToListAsync();
        }

        public async Task<FrequentFlyer> GetFrequentFlyerByIdAsync(int id)
        {
            return await _context.FrequentFlyers.FindAsync(id);

        }

        public async Task CreateFrequentFlyerAsync(FrequentFlyer frequentFlyer)
        {
            _context.FrequentFlyers.Add(frequentFlyer);
            await _context.SaveChangesAsync();
        }

        public async Task UpdateFrequentFlyerAsync(FrequentFlyer frequentFlyer)
        {
            _context.Entry(frequentFlyer).State = EntityState.Modified;
            await _context.SaveChangesAsync();
        }

        public async Task DeleteFrequentFlyerAsync(int id)
        {
            var frequentFlyer = await _context.FrequentFlyers.FindAsync(id);
            if (frequentFlyer != null)
            {
                _context.FrequentFlyers.Remove(frequentFlyer);
                await _context.SaveChangesAsync();
            }
        }

        public async Task<bool> FrequentFlyerExistsAsync(int id)
        {
            return await _context.FrequentFlyers.AnyAsync(e => e.FlyerId == id);
        }

    }

}
