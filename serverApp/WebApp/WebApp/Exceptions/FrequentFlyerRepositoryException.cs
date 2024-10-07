namespace WebApp.Exceptions
{
    public class FrequentFlyerRepositoryException : Exception
    {
        public FrequentFlyerRepositoryException() : base() { }

        public FrequentFlyerRepositoryException(string message) : base(message) { }

        public FrequentFlyerRepositoryException(string message, Exception innerException) : base(message, innerException) { }
    }
}
