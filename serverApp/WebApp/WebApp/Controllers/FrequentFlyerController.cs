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
        private readonly ApplicationDBContext _context; // _context = list of FrequentFlyers
        // constractor
        public FrequentFlyerController(ApplicationDBContext context)
        {
            _context = context;
        }

        /// <summary>
        /// GET ALL - read all
        /// returns the FrequentFlyers from _context in a list
        /// </summary>
        /// <returns> list of FrequentFlyers </returns>
        [HttpGet]
        public async Task<ActionResult<IEnumerable<FrequentFlyer>>> GetFrequentFlyers()
        {
            return await _context.FrequentFlyers.Include(f => f.FlightsIds).ToListAsync();
        }

        /// <summary>
        /// GET - read
        /// returns a FrequentFlyer from _context that match the id
        /// </summary>
        /// <param name="id"> id of wanted FrequentFlyer </param>
        /// <returns> FrequentFlyer </returns>
        [HttpGet("{id}")]
        public async Task<ActionResult<FrequentFlyer>> GetFrequentFlyer(int id)
        {
            var frequentFlyer = await _context.FrequentFlyers.Include(f => f.FlightsIds).FirstOrDefaultAsync(f => f.FlyerId == id);

            if (frequentFlyer == null)
            {
                return NotFound();
            }

            return frequentFlyer;
        }

        /// <summary>
        /// POST - create
        /// creates a new FrequentFlyer and add to _context
        /// </summary>
        /// <param name="frequentFlyer"> the new FrequentFlyer </param>
        /// <returns> result of CreatedAtAction </returns>
        [HttpPost]
        public async Task<ActionResult<FrequentFlyer>> PostFrequentFlyer(FrequentFlyer frequentFlyer)
        {
            _context.FrequentFlyers.Add(frequentFlyer);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetFrequentFlyer), new { id = frequentFlyer.FlyerId }, frequentFlyer);
        }

        /// <summary>
        /// PUT- update ??
        /// updates the FrequentFlyer that match the id with the input FrequentFlyer
        /// </summary>
        /// <param name="id"> id if FrequentFlyer we need to update </param>
        /// <param name="frequentFlyer"> the FrequentFlyer with the updated details </param>
        /// <returns> NoContent if update was successful </returns>
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

        /// <summary>
        /// DELETE - delete
        /// deletes the FrequentFlyer that match the id
        /// </summary>
        /// <param name="id"> id of the FrequentFlyer we need to delete </param>
        /// <returns> NoContent if delete was successful </returns>
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

        // private function for Update function
        private bool FrequentFlyerExists(int id)
        {
            return _context.FrequentFlyers.Any(e => e.FlyerId == id);
        }

    }
}
