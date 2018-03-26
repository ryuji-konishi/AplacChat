using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.Extensions.Configuration;

namespace frontend.Pages
{
    public class IndexModel : PageModel
    {
        private readonly Model.ApplicationDbContext _db;
        
        public string EmbedIndexURL { get; set; }   // URL of chat frame to be embedded in the page.

        public IndexModel(IConfiguration configuration, Model.ApplicationDbContext context) 
        {
            EmbedIndexURL = configuration.GetSection("CHAT_EMBED_URL").Value;
            _db = context;
        }

        public void OnGet()
        {
            // this is a test for EF loading
            var records = _db.ChatRecords.Where(p => p.Id == 0);
            foreach (var r in records)
            {
                Console.WriteLine(r.Id);
            }

        }
    }
}
