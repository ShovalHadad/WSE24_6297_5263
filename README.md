<h1>IsraFlight – Distributed Flight Management System</h1>

A client–server system for managing flights, aircraft, tickets, and user access for two roles: Administrators (Managers) and Frequent Flyers. The project demonstrates a distributed architecture built for the Windows Systems Engineering course, using a Python desktop UI (PySide6) and an ASP.NET Core backend with SQL Server hosted on Somee.com.

<h2>Key Features</h2>

Python (PySide6) GUI for Managers & Frequent Flyers with custom navigation.

ASP.NET Core 6 (C#) REST API backed by SQL Server on Somee.com (Entity Framework Core).

Authentication: username/password for Frequent Flyers.

Flight & Aircraft Management: CRUD for planes and flights, including scheduling (departure/arrival date/time, aircraft assignment, routes).

Ticketing: purchase, view, and print tickets as PDF.

Real-time seat tracking for flights.

External integrations:

Imagga API – validate that uploaded image URLs are airplane images (via tagging) when adding/updating aircraft.

HebCal API – detect Shabbat times & Torah portion; warn if selected landing time intersects with Shabbat.

Landing board: query scheduled landings at Ben Gurion for the next 1–5 hours.
