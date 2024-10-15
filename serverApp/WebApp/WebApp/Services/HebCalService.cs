using System;
using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;
using WebApp.Exceptions;

namespace WebApp.Services
{
    public class HebCalService
    {
        private readonly HttpClient _httpClient;
        // constructor
        public HebCalService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        // Method to get Shabbat times for a specific city and week
        // if flight Arrived in Shabbat then throw exception
        public async Task<string> GetShabbatTimesAsync(string city, DateTime date)
        {
            try
            {
                // Construct the API URL using the city and the week's start and end dates
                DateTime startOfWeek = date.StartOfWeek(); // Get the start of the week for the given date
                DateTime endOfWeek = startOfWeek.AddDays(6); // End of the week (7 days later)

                string url = $"https://www.hebcal.com/hebcal?cfg=json&v=1&maj=on&geo=city&city={Uri.EscapeDataString(city)}&start={startOfWeek:yyyy-MM-dd}&end={endOfWeek:yyyy-MM-dd}";

                // Make the HTTP request
                HttpResponseMessage response = await _httpClient.GetAsync(url);
                response.EnsureSuccessStatusCode();

                // Parse the JSON response
                string jsonResponse = await response.Content.ReadAsStringAsync();
                var json = JObject.Parse(jsonResponse);

                // Extract Shabbat times
                var shabbatStart = json["shabbat"]?["start"]?.ToString();
                var shabbatEnd = json["shabbat"]?["end"]?.ToString();

                if (shabbatStart == null || shabbatEnd == null)
                {
                    throw new HebCalServiceException("Shabbat times not found for the specified location.");
                }
                DateTime shabbatStartTime = DateTime.Parse(shabbatStart);
                DateTime shabbatEndTime = DateTime.Parse(shabbatEnd);

                // Check if the specified date is during Shabbat
                if (date >= shabbatStartTime && date <= shabbatEndTime)
                {
                    throw new HebCalServiceException("The specified date is during Shabbat. Please provide a date outside of Shabbat.");
                }
                return $"Shabbat starts at: {shabbatStartTime:yyyy-MM-dd HH:mm}, ends at: {shabbatEndTime:yyyy-MM-dd HH:mm}"; // Return Shabbat times in a single string
            }
            catch (Exception ex)
            {
                throw new HebCalServiceException("Failed to fetch Shabbat times.", ex);
            }
        }
    }

    // Extension method to get the start of the week
    public static class DateTimeExtensions
    {
        public static DateTime StartOfWeek(this DateTime dt)
        {
            // Calculate the difference in days between the current day and Sunday
            int diff = (7 + (dt.DayOfWeek - DayOfWeek.Sunday)) % 7; // Make sure it's non-negative
            return dt.AddDays(-diff).Date; // Move back to the previous Sunday
        }
    }
}