namespace WebApp.Exceptions
{
    public class PlaneRepositoryException : Exception
    {
        public PlaneRepositoryException() { }
        public PlaneRepositoryException(string message) : base(message) { }
        public PlaneRepositoryException(string message, Exception innerException) : base(message, innerException) { }
    }
}
