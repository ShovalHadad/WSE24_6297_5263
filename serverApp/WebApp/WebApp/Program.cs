using Microsoft.EntityFrameworkCore;
using System;
using WebApp.Data;
using WebApp.Interfaces;
using WebApp.Repositories;
using WebApp.Repository;
using WebApp.Services;



var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();


// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Configure Entity Framework with SQL Server
builder.Services.AddDbContext<ApplicationDBContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// Register the services
builder.Services.AddHttpClient<ImaggaService>();
builder.Services.AddHttpClient<HebCalService>();

// Add the repositories to Server
builder.Services.AddScoped<IPlaneRepository, PlaneRepository>();
builder.Services.AddScoped<IFlightRepository, FlightRepository>();
builder.Services.AddScoped<IFlightTicketRepository, FlightTicketRepository>();
builder.Services.AddScoped<IFrequentFlyerRepository, FrequentFlyerRepository>();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseAuthorization();

app.MapControllers();

app.Run();
