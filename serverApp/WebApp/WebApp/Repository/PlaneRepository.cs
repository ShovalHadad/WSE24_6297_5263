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
        private readonly ImaggaService _imaggaService;

        // Constructor
         public PlaneRepository(ApplicationDBContext context, ImaggaService ImaggaService)
        {
            _context = context;
            _imaggaService = ImaggaService;
        }

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
        {
            try
            {
                Plane emptyPlane = new Plane();
                if (plane.Name == emptyPlane.Name)
                    throw new PlaneRepositoryException("Plane name is required.");
                if (plane.NumOfSeats1 == emptyPlane.NumOfSeats1 || plane.NumOfSeats2 == emptyPlane.NumOfSeats2 || plane.NumOfSeats3 == emptyPlane.NumOfSeats3)
                    throw new PlaneRepositoryException("The number of sits for each department is required.");
                if (plane.Year == emptyPlane.Year || plane.MadeBy == emptyPlane.MadeBy)
                    throw new PlaneRepositoryException("one of the fields is missing.");
                if (plane.Year < 1000)
                    throw new PlaneRepositoryException("Plane year can not be less then 1000");
                if (plane.MadeBy == "" || plane.MadeBy == "string")
                    throw new PlaneRepositoryException("Plane company name is required.");
                 if (plane.Picture != null)  // check if the picture is indeed a plane 
                     if (!await _imaggaService.AnalyzeImageForPlane(plane.Picture)) // check the results if the image is a plane
                         throw new Exception("The uploaded image is not recognized as a plane.");
                _context.Planes.Add(plane);
                await _context.SaveChangesAsync();
            }
            catch(Exception ex)
            {
                throw new PlaneRepositoryException("can not create new plane ", ex);
            }
        }

        // update a plane by id
        public async Task UpdatePlaneAsync(int id, Plane plane)
        {
            try
            {
                Plane emptyPlane = new Plane();
                Plane oldPlane = _context.Planes.FirstOrDefault(e => e.PlaneId == id);
                if (emptyPlane == null)
                    throw new PlaneRepositoryException("can not find the plane.");
                if (oldPlane.Picture != plane.Picture && plane.Picture != null) // change the picture 
                {
                    if (await _imaggaService.AnalyzeImageForPlane(plane.Picture))
                        oldPlane.Picture = plane.Picture;
                    else
                        throw new PlaneRepositoryException("There is no plane in this picture.");
                }
                if(oldPlane.NumOfSeats1 != plane.NumOfSeats1 && plane.NumOfSeats1 != emptyPlane.NumOfSeats1)  // change number of seats in class 1
                {
                    foreach (Flight flight in await _context.Flights.ToListAsync())
                    {
                        if(flight.PlaneId == plane.PlaneId)
                        {
                            Flight? newFlight = _context.Flights.FirstOrDefault(e => e.FlightId == flight.FlightId);
                            newFlight.NumOfTakenSeats1 = oldPlane.NumOfSeats1 - (oldPlane.NumOfSeats1 - flight.NumOfTakenSeats1);
                        }
                    }
                    oldPlane.NumOfSeats1 = plane.NumOfSeats1;
                }
                if (oldPlane.NumOfSeats2 != plane.NumOfSeats2 && plane.NumOfSeats2 != emptyPlane.NumOfSeats2)  // change number of seats in class 2
                {
                    foreach (Flight flight in await _context.Flights.ToListAsync())
                    {
                        if (flight.PlaneId == plane.PlaneId)
                        {
                            Flight? newFlight = _context.Flights.FirstOrDefault(e => e.FlightId == flight.FlightId);
                            newFlight.NumOfTakenSeats2 = oldPlane.NumOfSeats2 - (oldPlane.NumOfSeats2 - flight.NumOfTakenSeats2);
                        }
                    }
                    oldPlane.NumOfSeats2 = plane.NumOfSeats2;
                }
                if (oldPlane.NumOfSeats3 != plane.NumOfSeats3 && plane.NumOfSeats3 != emptyPlane.NumOfSeats3)  // change number of seats in class 3
                {
                    foreach (Flight flight in await _context.Flights.ToListAsync())
                    {
                        if (flight.PlaneId == plane.PlaneId)
                        {
                            Flight? newFlight = _context.Flights.FirstOrDefault(e => e.FlightId == flight.FlightId);
                            newFlight.NumOfTakenSeats3 = oldPlane.NumOfSeats3 - (oldPlane.NumOfSeats3 - flight.NumOfTakenSeats3);
                        }
                    }
                    oldPlane.NumOfSeats3 = plane.NumOfSeats3;
                }
                oldPlane.Name = (plane.Name != oldPlane.Name && plane.Name != emptyPlane.Name) ? plane.Name : oldPlane.Name;
                oldPlane.Year = (plane.Year != oldPlane.Year && plane.Year != emptyPlane.Year) ? plane.Year : oldPlane.Year;
                oldPlane.MadeBy = (plane.MadeBy != oldPlane.MadeBy && plane.MadeBy != emptyPlane.MadeBy) ? plane.MadeBy : oldPlane.MadeBy;
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
                Plane? plane = _context.Planes.FirstOrDefault(e => e.PlaneId == id);
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
                if (plane != null)
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