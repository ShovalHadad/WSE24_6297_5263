using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using WebApp.Data;
using WebApp.Models;


namespace WebApp.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class FrequentFlyerController : ControllerBase
    {
        private readonly ApplicationDBContext _context;

        public FrequentFlyerController(ApplicationDBContext context)
        {
            _context = context;
        }

        // GET: api/FrequentFlyer
        [HttpGet]
        public async Task<ActionResult<IEnumerable<FrequentFlyer>>> GetFrequentFlyers()
        {
            return await _context.FrequentFlyers.Include(f => f.UserFlights).ToListAsync();
        }

        // GET: api/FrequentFlyer/5
        [HttpGet("{id}")]
        public async Task<ActionResult<FrequentFlyer>> GetFrequentFlyer(int id)
        {
            var frequentFlyer = await _context.FrequentFlyers.Include(f => f.UserFlights).FirstOrDefaultAsync(f => f.FlyerId == id);

            if (frequentFlyer == null)
            {
                return NotFound();
            }

            return frequentFlyer;
        }

        // POST: api/FrequentFlyer
        [HttpPost]
        public async Task<ActionResult<FrequentFlyer>> PostFrequentFlyer(FrequentFlyer frequentFlyer)
        {
            _context.FrequentFlyers.Add(frequentFlyer);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetFrequentFlyer), new { id = frequentFlyer.FlyerId }, frequentFlyer);
        }

        // PUT: api/FrequentFlyer/5
        [HttpPut("{id}")]
        public async Task<IActionResult> PutFrequentFlyer(int id, FrequentFlyer frequentFlyer)
        {
            if (id != frequentFlyer.FlyerId)
            {
                return BadRequest();
            }

            _context.Entry(frequentFlyer).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!FrequentFlyerExists(id))
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

        // DELETE: api/FrequentFlyer/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteFrequentFlyer(int id)
        {
            var frequentFlyer = await _context.FrequentFlyers.FindAsync(id);
            if (frequentFlyer == null)
            {
                return NotFound();
            }

            _context.FrequentFlyers.Remove(frequentFlyer);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        private bool FrequentFlyerExists(int id)
        {
            return _context.FrequentFlyers.Any(e => e.FlyerId == id);
        }



    }
}
