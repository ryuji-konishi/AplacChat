using System;
using System.IO;
using System.Text;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.Extensions.Configuration;
using frontend.Data;
using Newtonsoft.Json;
using System.Net.Http;

namespace frontend.Services
{
    public class ChatMessageHandler : IChatMessageHandler
    {
        private readonly ApplicationDbContext _db;
        private readonly string _chatInferURL;

        public ChatMessageHandler(IConfiguration configuration, ApplicationDbContext context)
        {
            _db = context;
            // URL of chat inference request to be called by AJAX in the page.
            _chatInferURL = configuration.GetSection("CHAT_INFER_URL").Value;
            if (string.IsNullOrEmpty(_chatInferURL))
                throw new Exception("Environment variable 'CHAT_INFER_URL' is invalid.");
        }

        public async Task<string> HandleInferAsync(string input, int userId = 0)
        {
            // Transfer the request to the Chat inference component and receive the result.
            var output = await sendPostChatInferAsync(input);

            // Store the chat conversation.
            await saveChatRecordAsync(userId, input, output);

            return output;
        }

        private async Task saveChatRecordAsync(int userId, string input, string output)
        {
            var record = new Data.ChatRecord
            {
                UTC = DateTime.UtcNow,
                UserId = userId,
                Input = input,
                Output = output
            };
            _db.ChatRecords.Add(record);
            await _db.SaveChangesAsync();
        }

        private async Task<string> sendPostChatInferAsync(string send)
        {
            HttpClient client = new HttpClient();
            var content = new StringContent(send, Encoding.UTF8, "text/plain");
            var response = await client.PostAsync(_chatInferURL, content);
            var responseString = response.Content.ReadAsStringAsync().Result;
            return JsonConvert.DeserializeObject<string>(responseString);
        }
    }
}
