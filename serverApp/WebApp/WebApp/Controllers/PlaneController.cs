using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using WebApp.Data;
using WebApp.Models;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace WebApp.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class PlaneController : ControllerBase
    {
        private readonly ApplicationDBContext _context;

        public PlaneController(ApplicationDBContext context)
        {
            _context = context;
        }

        //GET - read
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Plane>>> GetPlanes()
        {
            return await _context.Planes.ToListAsync();
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<Plane>> GetPlane(int id)
        {
            var plane = await _context.Planes.FindAsync(id);
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
            _context.Planes.Add(plane);
            await _context.SaveChangesAsync();
            return CreatedAtAction(nameof(GetPlane), new { id = plane.PlaneId }, plane);
        }


        //PUT- update
        [HttpPut("{id}")]
        public async Task<IActionResult> PutPlane(int id, Plane plane)
        {

            _context.Entry(plane).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!PlaneExists(id))
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
            var plane = await _context.Planes.FindAsync(id);
            if (plane == null)
            {
                return NotFound();
            }

            _context.Planes.Remove(plane);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        private bool PlaneExists(int id)
        {
            return _context.Planes.Any(e => e.PlaneId == id);
        }

    }
}
