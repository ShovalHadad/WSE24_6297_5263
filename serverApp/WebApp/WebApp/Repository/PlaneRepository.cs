using Microsoft.EntityFrameworkCore;
using WebApp.Data;
using WebApp.Interfaces;
using WebApp.Models;

namespace WebApp.Repository
{
    public class PlaneRepository : IPlaneRepository
    {
        private readonly ApplicationDBContext _context;
        public PlaneRepository(ApplicationDBContext context)
        {
            _context = context;
        }
        public Task<List<Plane>> GetPlanesAsync()
        {
            return _context.Planes.ToListAsync();
        }
         //לבדוק לגבי הasync 
        public async Task<Plane> GetPlaneByIdAsync(int id)
        {
            return await _context.Planes.FindAsync(id);
        }

        public async Task CreatePlaneAsync(Plane plane)
        {
            _context.Planes.Add(plane);
            await _context.SaveChangesAsync();
        }

        public async Task UpdatePlaneAsync(Plane plane)
        {
            _context.Entry(plane).State = EntityState.Modified;
            await _context.SaveChangesAsync();
        }

        public async Task DeletePlaneAsync(int id)
        {
            var plane = await _context.Planes.FindAsync(id);
            if (plane != null)
            {
                _context.Planes.Remove(plane);
                await _context.SaveChangesAsync();
            }
        }

        public async Task<bool> PlaneExistsAsync(int id)
        {
            return await _context.Planes.AnyAsync(e => e.PlaneId == id);
        }
    }


}

