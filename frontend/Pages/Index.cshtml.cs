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
        
        public string EmbedIndexURL { get; set; }   // URL of chat frame to be embedded in the page.

        public IndexModel(IConfiguration configuration) 
        {
            EmbedIndexURL = configuration.GetSection("CHAT_EMBED_URL").Value;
        }

        public void OnGet()
        {

        }
    }
}
