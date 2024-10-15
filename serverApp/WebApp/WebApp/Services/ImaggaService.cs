using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;
using WebApp.Exceptions;

namespace WebApp.Services
{
    public class ImaggaService
    {
        private readonly HttpClient _httpClient;
        // constructor
        public ImaggaService(HttpClient httpClient)
        {
            _httpClient = httpClient;
            var apiKey = "acc_10e9963589d24bf"; // API key
            var apiSecret = "84512d28c964121b6b0681dec2a116aa"; // API secret
            var byteArray = new System.Text.UTF8Encoding().GetBytes($"{apiKey}:{apiSecret}");
            _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Basic", Convert.ToBase64String(byteArray));
        }

        // AnalyzeImageForPlane returns true if the photo is a plane and false if not
        public async Task<bool> AnalyzeImageForPlane(string imageUrl)
        {
            // URL encode the image URL to ensure it's properly formatted
            string encodedImageUrl = System.Net.WebUtility.UrlEncode(imageUrl);
            string apiUrl = $"https://api.imagga.com/v2/tags?image_url={encodedImageUrl}";

            HttpResponseMessage response = await _httpClient.GetAsync(apiUrl);
            if (response.IsSuccessStatusCode)
            {
                string jsonResponse = await response.Content.ReadAsStringAsync();
                return ContainsPlaneTag(jsonResponse); // return the ContainsPlaneTag private function result 
            }
            else
            {
                string errorResponse = await response.Content.ReadAsStringAsync();  // read response content for more detailed error messages
                throw new ImaggaServiceException($"Failed to analyze image with Imagga API. Status Code: {response.StatusCode}, Response: {errorResponse}");
            }
        }
        
        // private function that returns true if the photo is a plane and false if not
        private bool ContainsPlaneTag(string jsonResponse)
        {
            // Parse the JSON response
            var json = JObject.Parse(jsonResponse);
            var tags = json["result"]["tags"];

            // Check if any of the tags contain the word "plane" (or its variants)
            foreach (var tag in tags)
            {
                string tagName = tag["tag"]["en"].ToString();
                if (tagName.Equals("plane", StringComparison.OrdinalIgnoreCase) ||
                    tagName.Equals("airplane", StringComparison.OrdinalIgnoreCase) ||
                    tagName.Equals("jet", StringComparison.OrdinalIgnoreCase))
                {
                    return true; // Found a plane-related tag
                }
            }
            return false; // No plane-related tags found
        }
    }
}