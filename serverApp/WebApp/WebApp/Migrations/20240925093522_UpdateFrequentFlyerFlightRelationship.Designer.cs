﻿// <auto-generated />
using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Metadata;
using Microsoft.EntityFrameworkCore.Migrations;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;
using WebApp.Data;

#nullable disable

namespace WebApp.Migrations
{
    [DbContext(typeof(ApplicationDBContext))]
    [Migration("20240925093522_UpdateFrequentFlyerFlightRelationship")]
    partial class UpdateFrequentFlyerFlightRelationship
    {
        /// <inheritdoc />
        protected override void BuildTargetModel(ModelBuilder modelBuilder)
        {
#pragma warning disable 612, 618
            modelBuilder
                .HasAnnotation("ProductVersion", "8.0.8")
                .HasAnnotation("Relational:MaxIdentifierLength", 128);

            SqlServerModelBuilderExtensions.UseIdentityColumns(modelBuilder);

            modelBuilder.Entity("WebApp.Models.Flight", b =>
                {
                    b.Property<int>("FlightId")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("int");

                    SqlServerPropertyBuilderExtensions.UseIdentityColumn(b.Property<int>("FlightId"));

                    b.Property<string>("ArrivalLocation")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<DateTime>("DepartureDateTime")
                        .HasColumnType("datetime2");

                    b.Property<string>("DepartureLocation")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<DateTime>("EstimatedArrivalDateTime")
                        .HasColumnType("datetime2");

                    b.Property<int>("FrequentFlyerFlyerId")
                        .HasColumnType("int");

                    b.Property<int?>("NumOfTakenSeats1")
                        .HasColumnType("int");

                    b.Property<int?>("NumOfTakenSeats2")
                        .HasColumnType("int");

                    b.Property<int?>("NumOfTakenSeats3")
                        .HasColumnType("int");

                    b.Property<int>("PlaneId")
                        .HasColumnType("int");

                    b.HasKey("FlightId");

                    b.HasIndex("FrequentFlyerFlyerId");

                    b.ToTable("Flights");
                });

            modelBuilder.Entity("WebApp.Models.FrequentFlyer", b =>
                {
                    b.Property<int>("FlyerId")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("int");

                    SqlServerPropertyBuilderExtensions.UseIdentityColumn(b.Property<int>("FlyerId"));

                    b.Property<string>("Email")
                        .HasColumnType("nvarchar(max)");

                    b.Property<string>("FirstName")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<bool>("IsManager")
                        .HasColumnType("bit");

                    b.Property<string>("LastName")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<string>("Password")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<int?>("PhoneNumber")
                        .HasColumnType("int");

                    b.Property<string>("UserName")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.HasKey("FlyerId");

                    b.ToTable("FrequentFlyers");
                });

            modelBuilder.Entity("WebApp.Models.Plane", b =>
                {
                    b.Property<int>("PlaneId")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("int");

                    SqlServerPropertyBuilderExtensions.UseIdentityColumn(b.Property<int>("PlaneId"));

                    b.Property<string>("MadeBy")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<string>("Name")
                        .IsRequired()
                        .HasColumnType("nvarchar(max)");

                    b.Property<int>("NumOfSeats1")
                        .HasColumnType("int");

                    b.Property<int>("NumOfSeats2")
                        .HasColumnType("int");

                    b.Property<int>("NumOfSeats3")
                        .HasColumnType("int");

                    b.Property<byte[]>("Picture")
                        .HasColumnType("varbinary(max)");

                    b.Property<int>("Year")
                        .HasColumnType("int");

                    b.HasKey("PlaneId");

                    b.ToTable("Planes");
                });

            modelBuilder.Entity("WebApp.models.FlightTicket", b =>
                {
                    b.Property<int>("TicketId")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("int");

                    SqlServerPropertyBuilderExtensions.UseIdentityColumn(b.Property<int>("TicketId"));

                    b.Property<int>("FlightId")
                        .HasColumnType("int");

                    b.Property<int>("TicketType")
                        .HasColumnType("int");

                    b.Property<int>("UserId")
                        .HasColumnType("int");

                    b.HasKey("TicketId");

                    b.ToTable("FlightTickets");
                });

            modelBuilder.Entity("WebApp.Models.Flight", b =>
                {
                    b.HasOne("WebApp.Models.FrequentFlyer", "FrequentFlyer")
                        .WithMany("UserFlights")
                        .HasForeignKey("FrequentFlyerFlyerId")
                        .OnDelete(DeleteBehavior.Cascade)
                        .IsRequired();

                    b.Navigation("FrequentFlyer");
                });

            modelBuilder.Entity("WebApp.Models.FrequentFlyer", b =>
                {
                    b.Navigation("UserFlights");
                });
#pragma warning restore 612, 618
        }
    }
}
