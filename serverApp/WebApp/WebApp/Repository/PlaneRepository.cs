using Microsoft.EntityFrameworkCore;
using WebApp.Data;
using WebApp.Interfaces;
using WebApp.Models;
using WebApp.Services;


namespace WebApp.Repository
{
    public class PlaneRepository : IPlaneRepository
    {
        private readonly ApplicationDBContext _context;
        private readonly ImaggaService _imaggaService;
        public PlaneRepository(ApplicationDBContext context, ImaggaService ImaggaService)
        {
            _context = context;
            _imaggaService = ImaggaService;
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
            if (plane.Image != null)
            {
                // Convert image to a stream
                using var stream = imageFile.OpenReadStream();

                // Upload the image to Imagga or any external service and get the image URL
                string imageUrl = await UploadImageAndGetUrl(stream);

                // Use ImaggaService to verify the image
                var imageAnalysisResult = await _imaggaService.AnalyzeImage(imageUrl);

                // Check if the image matches a plane
                if (!IsPlaneImage(imageAnalysisResult)) // Implement IsPlaneImage function to check if the image is a plane
                {
                    throw new Exception("The uploaded image is not recognized as a plane.");
                }

                // If image is valid, assign the imageUrl to the plane object
                plane.ImageUrl = imageUrl;
            }
            else
            {
                throw new Exception("An image file is required.");
            }
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

