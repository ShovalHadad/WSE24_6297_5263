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
        private readonly ApplicationDBContext _context;
        private readonly IPlaneRepository _planeRepo;
        // Constructor
        public PlaneController(ApplicationDBContext context, IPlaneRepository planeRepo) 
        {
            _planeRepo = planeRepo;
            _context = context;
        }

        // GET - read all
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Plane>>> GetPlanes()
        {
            try
            {
                var planes = await _planeRepo.GetPlanesAsync();
                return Ok(planes);
            }
            catch (Exception ex)
            {
                throw new Exception("can not read all planes ", ex);
            }
        }

        // GET - read 
        [HttpGet("{id}")]
        public async Task<ActionResult<Plane>> GetPlane(int id)
        {
            try
            {
                var plane = await _planeRepo.GetPlaneByIdAsync(id);
                if (plane == null)
                {
                    return NotFound();
                }
                return plane;
            }
            catch (Exception ex)
            {
                throw new Exception($"can not read the plane {id} ", ex);
            }
        }

        // POST - create
        [HttpPost]
        public async Task<ActionResult<Flight>> CreatePlane(Plane plane)
        {
            try
            {
                await _planeRepo.CreatePlaneAsync(plane);
                return CreatedAtAction(nameof(GetPlane), new { id = plane.PlaneId }, plane);
            }
            catch (Exception ex) 
            {
                throw new Exception("can not create new plane ", ex);
            }
        }

        // PUT - update
        [HttpPut("{id}")]
        public async Task<IActionResult> UpdatePlane(int id, Plane plane)
        {
            if (id != plane.PlaneId)
                return BadRequest();
            if (!await _planeRepo.PlaneExistsAsync(id))
                return NotFound();
            try
            {
                await _planeRepo.UpdatePlaneAsync(plane);
                return NoContent();
            }
            catch (Exception ex)
            {
                throw new Exception($"can not update the plane {id} ", ex);
            }
        }

        // DELETE - delete
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeletePlane(int id)
        {
            var plane = await _planeRepo.GetPlaneByIdAsync(id);
            if (plane == null)
                return NotFound();
            try
            {
                await _planeRepo.DeletePlaneAsync(id);
                return NoContent();
            }
            catch (Exception ex)
            {
                throw new Exception($"can not delete the plane {id} ", ex);
            }
        }

        private Task<bool> PlaneExists(int id)
        {
            return _planeRepo.PlaneExistsAsync(id);
        }
    }
}
