using Microsoft.EntityFrameworkCore;
using WebApp.Data;
using WebApp.Exceptions;
using WebApp.Interfaces;
using WebApp.Models;
using WebApp.Services;


namespace WebApp.Repository
{
    public class PlaneRepository : IPlaneRepository
    {
        private readonly ApplicationDBContext _context;
        //private readonly ImaggaService _imaggaService;
        // Constructor
        public PlaneRepository(ApplicationDBContext context)
        {
            _context = context;
        }
        /*
         public PlaneRepository(ApplicationDBContext context, ImaggaService ImaggaService)
        {
            _context = context;
            _imaggaService = ImaggaService;
        }
        */

        // read all planes
        public async Task<IEnumerable<Plane>> GetPlanesAsync()
        {
            try
            {
                return await _context.Planes.ToListAsync();
            }
            catch(Exception ex) 
            {
                throw new PlaneRepositoryException("Failed to retrieve planes.", ex);
            } 
        }

        // read plane by id 
        public async Task<Plane> GetPlaneByIdAsync(int id)
        {
            try
            {
                var plane = await _context.Planes.FindAsync(id);
                if (plane == null)
                    throw new PlaneRepositoryException($"Flight with ID {id} not found.");
                return plane;
            }
            catch (Exception ex) 
            {
                throw new PlaneRepositoryException("An error occurred while retrieving the plane.", ex);
            }
        }

        // create new plane
        public async Task CreatePlaneAsync(Plane plane)
        {/*
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
            }*/
            try
            {
                if (plane.Name == "string" || plane.Name == "")
                    throw new PlaneRepositoryException("Plane name is required.");
                if (plane.Year < 1000)
                    throw new PlaneRepositoryException("Plane year can not be less then 1000");
                if (plane.MadeBy == "" || plane.MadeBy == "string")
                    throw new PlaneRepositoryException("Plane company name is required.");
                /* if (plane.Picture != null)  // check if the picture is indeed a plane 
                 {
                     var imageAnalysisResult = await _imaggaService.AnalyzeImage(plane.Picture);
                     // Check if the image matches a plane
                     if (!IsPlaneImage(imageAnalysisResult)) // Implement IsPlaneImage function to check if the image is a plane
                     {
                         throw new Exception("The uploaded image is not recognized as a plane.");
                     }
                 } */
                if (plane.NumOfSeats1 == null || plane.NumOfSeats2 == null || plane.NumOfSeats3 == null)
                    throw new PlaneRepositoryException("The number of sits for each department is required.");
                _context.Planes.Add(plane);
                await _context.SaveChangesAsync();
            }
            catch(Exception ex)
            {
                throw new PlaneRepositoryException("can not create new plane ", ex);
            }
        }

        // update a plane by id
        public async Task UpdatePlaneAsync(Plane plane)
        {
            try
            {
                Plane newPlane = _context.Planes.FirstOrDefault(e => e.PlaneId == plane.PlaneId);
                if(newPlane.Picture != plane.Picture) // change the picture 
                {
                    //if(_imaggaService.isPlane() == true)
                    newPlane.Picture = plane.Picture;
                    //else
                    //    throw new PlaneRepositoryException("There is no plane in this picture.");
                }
                if(newPlane.NumOfSeats1 != plane.NumOfSeats1)  // change number of seats in class 1
                {
                    foreach (Flight flight in await _context.Flights.ToListAsync())
                    {
                        if(flight.PlaneId == plane.PlaneId)
                        {
                            Flight? newFlight = _context.Flights.FirstOrDefault(e => e.FlightId == flight.FlightId);
                            newFlight.NumOfTakenSeats1 = newPlane.NumOfSeats1 - (newPlane.NumOfSeats1 - flight.NumOfTakenSeats1);
                        }
                    }
                    newPlane.NumOfSeats1 = plane.NumOfSeats1;
                }
                if (newPlane.NumOfSeats2 != plane.NumOfSeats2)  // change number of seats in class 2
                {
                    foreach (Flight flight in await _context.Flights.ToListAsync())
                    {
                        if (flight.PlaneId == plane.PlaneId)
                        {
                            Flight? newFlight = _context.Flights.FirstOrDefault(e => e.FlightId == flight.FlightId);
                            newFlight.NumOfTakenSeats2 = newPlane.NumOfSeats2 - (newPlane.NumOfSeats2 - flight.NumOfTakenSeats2);
                        }
                    }
                    newPlane.NumOfSeats2 = plane.NumOfSeats2;
                }
                if (newPlane.NumOfSeats3 != plane.NumOfSeats3)  // change number of seats in class 3
                {
                    foreach (Flight flight in await _context.Flights.ToListAsync())
                    {
                        if (flight.PlaneId == plane.PlaneId)
                        {
                            Flight? newFlight = _context.Flights.FirstOrDefault(e => e.FlightId == flight.FlightId);
                            newFlight.NumOfTakenSeats3 = newPlane.NumOfSeats3 - (newPlane.NumOfSeats3 - flight.NumOfTakenSeats3);
                        }
                    }
                    newPlane.NumOfSeats3 = plane.NumOfSeats3;
                }
                newPlane.Name = plane.Name;
                newPlane.Year = plane.Year;
                newPlane.MadeBy = plane.MadeBy;
                //_context.Entry(plane).State = EntityState.Modified;
                await _context.SaveChangesAsync();
            }
            catch(Exception ex)
            {
                throw new PlaneRepositoryException("An error occurred while updating the plane.", ex);
            }
        }

        // delete plane by id
        public async Task DeletePlaneAsync(int id)
        {
            try
            {
                var plane = await _context.Planes.FindAsync(id);
                foreach (Flight flight in await _context.Flights.ToListAsync())
                {
                    if (flight.PlaneId == id)
                    {
                        flight.PlaneId = 0;
                        flight.NumOfTakenSeats1 = null;
                        flight.NumOfTakenSeats2 = null;
                        flight.NumOfTakenSeats3 = null;
                    }
                }
                _context.Planes.Remove(plane);
                await _context.SaveChangesAsync();
            }
            catch (Exception ex)
            {
                throw new PlaneRepositoryException($"can not delete plane {id} ", ex);
            }
        }

        // function to know if the plane exist by id
        public async Task<bool> PlaneExistsAsync(int id)
        {
            return await _context.Planes.AnyAsync(e => e.PlaneId == id);
        }
    }
}