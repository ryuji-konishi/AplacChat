using System.IO;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Newtonsoft.Json;

namespace frontend
{
    public class Utility 
    {
        /**
            This method returns the argument parameter value that is sent via AJAX POST request.
            If it's not via AJAX, but the Razor Pages forms submit, you can use the BindProperty attribute instead.
         */
        public static T getAjaxPostParameter<T>(PageModel page)
        {
            T result = default(T);
            MemoryStream stream = new MemoryStream();
            page.Request.Body.CopyTo(stream);
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