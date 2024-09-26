namespace WebApp.Services
{
    public class HebCalService
    {
        private static readonly HttpClient client = new HttpClient();

        public async Task<string> GetHebrewDates(string date)
        {
            // Replace with actual API endpoint and parameters
            string apiUrl = $"https://www.hebcal.com/converter?cfg=json&gy={date}&g2h=1&strict=1";

            HttpResponseMessage response = await client.GetAsync(apiUrl);
            if (response.IsSuccessStatusCode)
            {
                string jsonResponse = await response.Content.ReadAsStringAsync();
                return jsonResponse;
            }
            else
            {
                throw new Exception("Failed to retrieve data from HebCal API.");
            }
        }
    }
}
