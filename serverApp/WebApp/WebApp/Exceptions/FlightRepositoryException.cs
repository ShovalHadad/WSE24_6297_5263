using System;

namespace WebApp.Exceptions; // Use your application's namespace

public class FlightRepositoryException : Exception
{
    public FlightRepositoryException() : base() { }

    public FlightRepositoryException(string message) : base(message) { }

    public FlightRepositoryException(string message, Exception innerException) : base(message, innerException) { }
}