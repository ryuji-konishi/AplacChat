using System;
using Microsoft.EntityFrameworkCore;

namespace frontend.Model
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