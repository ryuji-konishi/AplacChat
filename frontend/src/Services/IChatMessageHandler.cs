using System;
using System.Threading.Tasks;

namespace frontend.Services
{
    public interface IChatMessageHandler
    {
        Task<string> HandleInferAsync(string input, int userId = 0);
    }
}
