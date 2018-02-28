using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.Extensions.Configuration;

namespace frontend.Pages.Embed
{
    public class IndexModel : PageModel
    {
        public string ChatInferURL { get; set; }    // URL of chat inference request to be called by AJAX in the page.

        public IndexModel(IConfiguration configuration) 
        {
            ChatInferURL = configuration.GetSection("CHAT_INFER_URL").Value;
        }

        public void OnGet()
        {

        }
    }
}
