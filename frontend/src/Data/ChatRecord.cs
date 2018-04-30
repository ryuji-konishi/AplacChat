using System;
using Microsoft.EntityFrameworkCore;

namespace frontend.Data
{
    public class ChatRecord
    {
        public int Id { get; set; }
        public int UserId { get; set; }
        public DateTime UTC { get; set; }
        public string Input { get; set; }
        public string Output { get; set; }
    }
}