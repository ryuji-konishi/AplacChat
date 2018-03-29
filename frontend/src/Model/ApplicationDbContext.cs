using Microsoft.Extensions.Configuration;
using Microsoft.EntityFrameworkCore;

namespace frontend.Model
{
    public class ApplicationDbContext : DbContext
    {
        public DbSet<ChatRecord> ChatRecords { get; set; }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            // This method is called in both run-time and design-time (by dotnet ef command),
            // When design-time, since the assembly is executed from a different method (BuildWebHost),
            // the configuration object isn't initialized in the Startup class and DI is not available.
            // Thus, create the ConfigurationBuilder youself and load the configuration here.
            IConfigurationRoot configuration = new ConfigurationBuilder()
                .AddEnvironmentVariables()
                .Build();
            var sqlConnection = configuration.GetSection("CONNECTION_APPDB").Value;
            optionsBuilder.UseSqlite(sqlConnection);
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            modelBuilder.Entity<ChatRecord>(b =>
            {
                b.Metadata.Relational().TableName = "ChatRecords";
            });
        }
    }
}


