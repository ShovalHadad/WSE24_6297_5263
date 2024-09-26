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
        public PlaneController(ApplicationDBContext context, IPlaneRepository planeRepo) //add the interface
        {
            _planeRepo = planeRepo;
            _context = context;
        }

        //GET - read
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Plane>>> GetPlanes()
        {
            //return await _planeRepo.GetPlanesAsync();
            var planes = await _planeRepo.GetPlanesAsync();
            return Ok(planes);
        }

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


        //POST - create
        [HttpPost]
        public async Task<ActionResult<Flight>> CreatePlane(Plane plane)
        {
            //_context.Planes.Add(plane);
           // await _context.SaveChangesAsync();
            await _planeRepo.CreatePlaneAsync(plane);
            return CreatedAtAction(nameof(GetPlane), new { id = plane.PlaneId }, plane);
        }


        //PUT- update
        [HttpPut("{id}")]
        public async Task<IActionResult> UpdatePlane(int id, Plane plane)
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




        //DELETE
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

        private Task<bool> PlaneExists(int id)
        {
            //return _context.Planes.Any(e => e.PlaneId == id);
            return _planeRepo.PlaneExistsAsync(id);
        }

    }
}
