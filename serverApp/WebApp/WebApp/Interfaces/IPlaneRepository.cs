using WebApp.Models;

namespace WebApp.Interfaces
{
    public interface IPlaneRepository
    {
        Task<List<Plane>> GetPlanesAsync();
        Task<Plane> GetPlaneByIdAsync(int id);
        Task CreatePlaneAsync(Plane plane);
        Task UpdatePlaneAsync(Plane plane);
        Task DeletePlaneAsync(int id);
        Task<bool> PlaneExistsAsync(int id);

    }
}
