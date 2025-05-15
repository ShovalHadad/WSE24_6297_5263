﻿using System;
using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;
using WebApp.Exceptions;

namespace WebApp.Services
{
    public class HebCalService
    {
        private readonly HttpClient _httpClient;

        public HebCalService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<string> GetShabbatTimesAndParashaAsync(DateTime date)
        {
            try
            {
                string url = $"https://www.hebcal.com/shabbat?cfg=json&geonameid=293397&gy={date.Year}&gm={date.Month}&gd={date.Day}";
                HttpResponseMessage response = await _httpClient.GetAsync(url);
                response.EnsureSuccessStatusCode();
                string jsonResponse = await response.Content.ReadAsStringAsync();
                var json = JObject.Parse(jsonResponse);

                var shabbatStart = json["items"]?.FirstOrDefault(item => item["category"]?.ToString() == "candles")?["date"]?.ToString();
                var shabbatEnd = json["items"]?.FirstOrDefault(item => item["category"]?.ToString() == "havdalah")?["date"]?.ToString();

                if (shabbatStart == null || shabbatEnd == null)
                    throw new HebCalServiceException("Shabbat times not found for the specified date.");

                DateTime shabbatStartTime = DateTime.Parse(shabbatStart);
                DateTime shabbatEndTime = DateTime.Parse(shabbatEnd);

                if (date >= shabbatStartTime && date <= shabbatEndTime)
                    throw new HebCalServiceException("The specified date is during Shabbat. Please provide a date outside of Shabbat.");

                var parasha = json["items"]?.FirstOrDefault(item => item["category"]?.ToString() == "parashat")?["title"]?.ToString();

                if (parasha == null)
                    throw new HebCalServiceException("Parashat not found for the specified date.");

                return $"Shabbat starts at: {shabbatStartTime:yyyy-MM-dd HH:mm}, ends at: {shabbatEndTime:yyyy-MM-dd HH:mm}. Parashat: {parasha}";
            }
            catch (Exception ex)
            {
                throw new HebCalServiceException("Failed to fetch Shabbat times and parasha.", ex);
            }
        }
        public async Task<bool> IsDateInShabbat(DateTime date)  // for flight creation
        {
            string url = $"https://www.hebcal.com/shabbat?cfg=json&geonameid=293397&gy={date.Year}&gm={date.Month}&gd={date.Day}";
            HttpResponseMessage response = await _httpClient.GetAsync(url);
            response.EnsureSuccessStatusCode();

            string jsonResponse = await response.Content.ReadAsStringAsync();
            var json = JObject.Parse(jsonResponse);

            var shabbatStart = json["items"]?.FirstOrDefault(item => item["category"]?.ToString() == "candles")?["date"]?.ToString();
            var shabbatEnd = json["items"]?.FirstOrDefault(item => item["category"]?.ToString() == "havdalah")?["date"]?.ToString();

            if (shabbatStart == null || shabbatEnd == null)
                throw new HebCalServiceException("Shabbat times not found for the specified date.");

            DateTime shabbatStartTime = DateTime.Parse(shabbatStart);
            DateTime shabbatEndTime = DateTime.Parse(shabbatEnd);
           return date >= shabbatStartTime && date <= shabbatEndTime;
        }
        
    }
    
} 
