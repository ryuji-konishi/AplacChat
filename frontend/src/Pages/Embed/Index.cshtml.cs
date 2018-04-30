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

namespace frontend.Pages.Embed
{
    public class PostMessage
    {
        public string text { get; set; }
    }

    public class IndexModel : PageModel
    {
        private readonly ApplicationDbContext _db;
        private readonly string _chatInferURL;

        public IndexModel(IConfiguration configuration, ApplicationDbContext context) 
        {
            _db = context;
            // URL of chat inference request to be called by AJAX in the page.
            _chatInferURL = configuration.GetSection("CHAT_INFER_URL").Value;
            if (string.IsNullOrEmpty(_chatInferURL))
                throw new Exception("Environment variable 'CHAT_INFER_URL' is invalid.");
        }

        public void OnGet()
        {

        }

        public async Task<IActionResult> OnPostAsync()
        {
            // Get the request text sent from the front-end
            var msg = getAjaxPostParameter<PostMessage>();
            if (msg == null)
                return new StatusCodeResult(500);

            // Transfer the request to the Chat inference component and receive the result.
            var response = await sendPostChatInferAsync(msg.text);

            // Store the chat conversation.
            await saveChatRecordAsync(msg.text, response);

            return new JsonResult(response);
        }

        private async Task saveChatRecordAsync(string input, string output)
        {
            var record = new Data.ChatRecord
            {
                UTC = DateTime.UtcNow,
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

        /**
            This method returns the argument parameter value that is sent via AJAX POST request.
            If it's not via AJAX, but the Razor Pages forms submit, you can use the BindProperty attribute instead.
         */
        private T getAjaxPostParameter<T>()
        {
            T result = default(T);
            MemoryStream stream = new MemoryStream();
            Request.Body.CopyTo(stream);
            stream.Position = 0;
            using (StreamReader reader = new StreamReader(stream))
            {
                string requestBody = reader.ReadToEnd();
                if(requestBody.Length > 0)
                {
                    result = JsonConvert.DeserializeObject<T>(requestBody);
                }
            }
            return result;
        }
    }
}
