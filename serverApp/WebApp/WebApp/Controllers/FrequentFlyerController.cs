using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using WebApp.Data;
using WebApp.Interfaces;
using WebApp.Models;



namespace WebApp.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class FrequentFlyerController : ControllerBase
    {
        private readonly ApplicationDBContext _context;
      
        private readonly IFrequentFlyerRepository _frequentFlyerRepo;


        public FrequentFlyerController(ApplicationDBContext context, IFrequentFlyerRepository frequentFlyerRepo) // Inject the repository interface
        {
            _context = context;
            _frequentFlyerRepo = frequentFlyerRepo;
        }

        // GET: api/FrequentFlyer
        [HttpGet]
        public async Task<ActionResult<IEnumerable<FrequentFlyer>>> GetFrequentFlyers()
        {
            var frequentFlyers = await _frequentFlyerRepo.GetFrequentFlyersAsync();
            return Ok(frequentFlyers);
        }

        // GET: api/FrequentFlyer/5
        [HttpGet("{id}")]
        public async Task<ActionResult<FrequentFlyer>> GetFrequentFlyer(int id)
        {
            var frequentFlyer = await _frequentFlyerRepo.GetFrequentFlyerByIdAsync(id);

            if (frequentFlyer == null)
            {
                return NotFound();
            }

            return frequentFlyer;
        }

        // POST: api/FrequentFlyer
        [HttpPost]
        public async Task<ActionResult<FrequentFlyer>> CreateFrequentFlyer(FrequentFlyer frequentFlyer)
        {
            await _frequentFlyerRepo.CreateFrequentFlyerAsync(frequentFlyer);
            return CreatedAtAction(nameof(GetFrequentFlyer), new { id = frequentFlyer.FlyerId }, frequentFlyer);
        }

        // PUT: api/FrequentFlyer/5
        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateFrequentFlyer(int id, FrequentFlyer frequentFlyer)
        {
            if (id != frequentFlyer.FlyerId)
            {
                return BadRequest();
            }

            try
            {
                await _frequentFlyerRepo.UpdateFrequentFlyerAsync(frequentFlyer);
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!await _frequentFlyerRepo.FrequentFlyerExistsAsync(id))
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
            var frequentFlyer = await _frequentFlyerRepo.GetFrequentFlyerByIdAsync(id);
            if (frequentFlyer == null)
            {
                return NotFound();
            }

            await _frequentFlyerRepo.DeleteFrequentFlyerAsync(id);
            return NoContent();
        }

        private Task<bool> FrequentFlyerExists(int id)
        {
            return _frequentFlyerRepo.FrequentFlyerExistsAsync(id);
        }

    }
}