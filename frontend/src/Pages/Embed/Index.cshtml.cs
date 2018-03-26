using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.Extensions.Configuration;
using frontend.Model;
using Newtonsoft.Json;

namespace frontend.Pages.Embed
{
    public class PostMessage
    {
        public string text { get; set; }
    }

    public class IndexModel : PageModel
    {
        private readonly ApplicationDbContext _db;
        public string ChatInferURL { get; set; }    // URL of chat inference request to be called by AJAX in the page.

        public IndexModel(IConfiguration configuration, ApplicationDbContext context) 
        {
            ChatInferURL = configuration.GetSection("CHAT_INFER_URL").Value;
            ChatInferURL = "http://localhost:5051/Embed/Index";
            _db = context;
        }

        public void OnGet()
        {

        }

        public async Task<IActionResult> OnPostAsync()
        {
            string text = null;
            MemoryStream stream = new MemoryStream();
            Request.Body.CopyTo(stream);
            stream.Position = 0;
            using (StreamReader reader = new StreamReader(stream))
            {
                string requestBody = reader.ReadToEnd();
                if(requestBody.Length > 0)
                {
                    var obj = JsonConvert.DeserializeObject<PostMessage>(requestBody);
                    if(obj != null)
                    {
                        text = obj.text;
                    }
                }
            }

            var record = new Model.ChatRecord
            {
                UTC = DateTime.UtcNow,
                Input = text
            };
            _db.ChatRecords.Add(record);
            await _db.SaveChangesAsync();
            return new JsonResult(text);
        }
    }
}
