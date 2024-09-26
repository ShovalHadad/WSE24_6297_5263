using System.Net.Http.Headers;

namespace WebApp.Services
{
    public class ImaggaService
    {
        private static readonly HttpClient client = new HttpClient();

        public ImaggaService()
        {
            // Replace with your actual Imagga API credentials
            var apiKey = "your_api_key";
            var apiSecret = "your_api_secret";

            var byteArray = new System.Text.UTF8Encoding().GetBytes($"{apiKey}:{apiSecret}");
            client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(byteArray));
        }

        public async Task<string> AnalyzeImage(string imageUrl)
        {
            string apiUrl = $"https://api.imagga.com/v2/tags?image_url={imageUrl}";

            HttpResponseMessage response = await client.GetAsync(apiUrl);
            if (response.IsSuccessStatusCode)
            {
                string jsonResponse = await response.Content.ReadAsStringAsync();
                return jsonResponse;
            }
            else
            {
                throw new Exception("Failed to analyze image with Imagga API.");
            }
        }
    }
}

