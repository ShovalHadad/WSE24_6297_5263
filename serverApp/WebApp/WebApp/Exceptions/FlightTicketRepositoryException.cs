namespace WebApp.Exceptions
{
    public class FlightTicketRepositoryException : Exception
    {
        public FlightTicketRepositoryException() : base() { }

        public FlightTicketRepositoryException(string message) : base(message) { }

        public FlightTicketRepositoryException(string message, Exception innerException) : base(message, innerException) { }
    }
}
