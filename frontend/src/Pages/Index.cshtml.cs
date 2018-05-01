using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.Extensions.Configuration;
using Microsoft.AspNetCore.Identity;
using frontend.Services;

namespace frontend.Pages
{
    public class IndexModel : PageModel
    {        
        private readonly IChatMessageHandler _handler;
        private class PostMessage
        {
            public string text { get; set; }
        }
        public string EmbedIndexURL { get; set; }   // URL of chat frame to be embedded in the page.

        public IndexModel(IConfiguration configuration, IChatMessageHandler handler)
        {
            _handler = handler;
            EmbedIndexURL = configuration.GetSection("CHAT_EMBED_URL").Value;
        }

        public void OnGet()
        {

        }

        public async Task<IActionResult> OnPostAsync()
        {
            // Get the request text sent from the front-end
            var msg = Utility.getAjaxPostParameter<PostMessage>(this);
            if (msg == null)
                return new StatusCodeResult(500);

            // Transfer the request to the Chat inference component and receive the result.
            var response = await _handler.HandleInferAsync(msg.text);

            return new JsonResult(response);
        }
    }
}
