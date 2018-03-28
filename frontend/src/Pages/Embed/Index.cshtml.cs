using System;
using System.IO;
using System.Text;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.Extensions.Configuration;
using frontend.Model;
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
            var msg = getRequestParameter<PostMessage>();
            if (msg == null)
                return new StatusCodeResult(500);

            string text = msg.text;

            HttpClient client = new HttpClient();
            var content = new StringContent(text, Encoding.UTF8, "text/plain");
            var response = await client.PostAsync(_chatInferURL, content);
            var responseString = response.Content.ReadAsStringAsync().Result;
            var res = JsonConvert.DeserializeObject<string>(responseString);

            var record = new Model.ChatRecord
            {
                UTC = DateTime.UtcNow,
                Input = text,
                Output = res
            };
            _db.ChatRecords.Add(record);
            _db.SaveChanges();
            return new JsonResult(res);
        }

        /**
            This method returns the argument parameter value that is sent via AJAX POST request.
            If it's not via AJAX, but the Razor Pages forms submit, you can use the BindProperty attribute instead.
         */
        private T getRequestParameter<T>()
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
