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
        // Constructor
        public FrequentFlyerController(ApplicationDBContext context, IFrequentFlyerRepository frequentFlyerRepo) // Inject the repository interface
        {
            _context = context;
            _frequentFlyerRepo = frequentFlyerRepo;
        }

        // GET - read all
        [HttpGet]
        public async Task<ActionResult<IEnumerable<FrequentFlyer>>> GetFrequentFlyers()
        {
            try
            {
                var frequentFlyers = await _frequentFlyerRepo.GetFrequentFlyersAsync();
                return Ok(frequentFlyers);
            }
            catch (Exception ex) 
            {
                throw new Exception("can not read all frequent flyers ", ex);
            }
        }

        // GET - read
        [HttpGet("{id}")]
        public async Task<ActionResult<FrequentFlyer>> GetFrequentFlyer(int id)
        {
            try
            {
                var frequentFlyer = await _frequentFlyerRepo.GetFrequentFlyerByIdAsync(id);
                if (frequentFlyer == null)
                {
                    return NotFound();
                }
                return frequentFlyer;
            }
            catch (Exception ex) 
            {
                throw new Exception($"can not read the frequent flyer {id} ", ex);
            }
        }

        // POST - create
        [HttpPost]
        public async Task<ActionResult<FrequentFlyer>> CreateFrequentFlyer(FrequentFlyer frequentFlyer)
        {
            try
            {
                await _frequentFlyerRepo.CreateFrequentFlyerAsync(frequentFlyer);
                return CreatedAtAction(nameof(GetFrequentFlyer), new { id = frequentFlyer.FlyerId }, frequentFlyer);
            }
            catch(Exception ex)
            {
                throw new Exception("can not create new frequent flyer ", ex);
            }
        }

        // PUT - update
        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateFrequentFlyer(int id, FrequentFlyer frequentFlyer)
        {
            if (id != frequentFlyer.FlyerId)
                return BadRequest();
            if (!await _frequentFlyerRepo.FrequentFlyerExistsAsync(id))
                return NotFound();
            try
            {
                await _frequentFlyerRepo.UpdateFrequentFlyerAsync(frequentFlyer);
                return NoContent();
            }
            catch (Exception ex)
            {
                throw new Exception($"can not update the frequent flyer {id} ", ex);
            }
        }

        // DELETE - delete
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteFrequentFlyer(int id)
        {
            var frequentFlyer = await _frequentFlyerRepo.GetFrequentFlyerByIdAsync(id);
            if (frequentFlyer == null)
                return NotFound();
            try
            {
                await _frequentFlyerRepo.DeleteFrequentFlyerAsync(id);
                return NoContent();
            }
            catch (Exception ex)
            {
                throw new Exception($"can not delete the frequent flyer {id} ", ex);
            }
        }

        private Task<bool> FrequentFlyerExists(int id)
        {
            return _frequentFlyerRepo.FrequentFlyerExistsAsync(id);
        }
    }
}