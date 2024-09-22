using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using WebApp.Data;
using WebApp.Interfaces;
using WebApp.Models;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace WebApp.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class PlaneController : ControllerBase
    {
        private readonly ApplicationDBContext _context; // _context = list of planes
        private readonly IPlaneRepository _planeRepo;
        // constractor 
        public PlaneController(ApplicationDBContext context, IPlaneRepository planeRepo) //add the interface
        {
            _planeRepo = planeRepo;
            _context = context;
        }

        /// <summary>
        /// GET ALL - read all
        /// returns the planes from _context in a list
        /// </summary>
        /// <returns> list of planes </returns>
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Plane>>> GetPlanes()
        {
            //return await _planeRepo.GetPlanesAsync();
            var planes = await _planeRepo.GetPlanesAsync();
            return Ok(planes);
        }

        /// <summary>
        /// GET - read
        /// returns a plane from _context that match the id
        /// </summary>
        /// <param name="id"> id of wanted plane </param>
        /// <returns> plane </returns>
        [HttpGet("{id}")]
        public async Task<ActionResult<Plane>> GetPlane(int id)
        {
            var plane = await _planeRepo.GetPlaneByIdAsync(id);
            if (plane == null)
            {
                return NotFound();
            }
            return plane;
        }

        /// <summary>
        /// POST - create
        /// creates a new plane and add to _context
        /// </summary>
        /// <param name="plane"> the new plane </param>
        /// <returns> result of CreatedAtAction </returns>
        [HttpPost]
        public async Task<ActionResult<Flight>> CreatePlane(Plane plane)
        {
            //_context.Planes.Add(plane);
           // await _context.SaveChangesAsync();
            await _planeRepo.CreatePlaneAsync(plane);
            return CreatedAtAction(nameof(GetPlane), new { id = plane.PlaneId }, plane);
        }

        /// <summary>
        /// PUT- update
        /// updates the plane that match the id with the plane
        /// </summary>
        /// <param name="id"> the id fo the plane we need to update </param>
        /// <param name="plane"> the plane with the updated details </param>
        /// <returns> NoContent if update was successful </returns>
        [HttpPut("{id}")]
        public async Task<IActionResult> PutPlane(int id, Plane plane)
        {
            if (id != plane.PlaneId)
            {
                return BadRequest();
            }

            try
            {
                await _planeRepo.UpdatePlaneAsync(plane);
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!await _planeRepo.PlaneExistsAsync(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            return NoContent();
        }

        /// <summary>
        /// DELETE - delete
        /// deletes the plane that match the id
        /// </summary>
        /// <param name="id"> id of the plane we need to delete </param>
        /// <returns> NoContent if delete was successful </returns>
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeletePlane(int id)
        {
            var plane = await _planeRepo.GetPlaneByIdAsync(id);
            if (plane == null)
            {
                return NotFound();
            }

            await _planeRepo.DeletePlaneAsync(id);
            return NoContent();
        }

        // private function for Update function
        private async Task<bool> PlaneExistsAsync(int id)
        {
            //return _context.Planes.Any(e => e.PlaneId == id);
            return await _planeRepo.PlaneExistsAsync(id);
        }

    }
}
