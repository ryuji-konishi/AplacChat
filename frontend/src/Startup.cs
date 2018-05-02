using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using frontend.Data;
using frontend.Services;

namespace frontend
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            // This is required to accept AJAX post requests with anti cross site request forgery token in the header.
            services.AddAntiforgery(o => o.HeaderName = "XSRF-TOKEN");
            services.AddDbContext<ApplicationDbContext>();

            services.AddIdentity<ApplicationUser, IdentityRole>()
                .AddEntityFrameworkStores<ApplicationDbContext>()
                .AddDefaultTokenProviders();

            // services.AddAuthentication().AddGoogle(googleOptions =>
            // {
            //     googleOptions.ClientId = Configuration["Authentication_Google_ClientId"];
            //     googleOptions.ClientSecret = Configuration["Authentication_Google_ClientSecret"];
            // });
            // services.AddAuthentication().AddFacebook(facebookOptions =>
            // {
            //     facebookOptions.AppId = Configuration["Authentication_Facebook_AppID"];
            //     facebookOptions.AppSecret = Configuration["Authentication_Facebook_AppSecret"];
            // });

            // services.ConfigureApplicationCookie(options =>
            // {
            //     options.LoginPath = "/Account/Login";   // Account/Login is called if the user is not authenticated.
            // });

            services.AddMvc();
                // .AddRazorPagesOptions(options =>
                // {
                //     options.Conventions.AuthorizePage("/Index");     // To access to /Index the user authentication is required.
                // });

            services.AddTransient<IChatMessageHandler, ChatMessageHandler>();
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IHostingEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }
            else
            {
                app.UseExceptionHandler("/Error");
            }

            app.UseStaticFiles();

            app.UseAuthentication();

            app.UseMvc();
        }
    }
}
