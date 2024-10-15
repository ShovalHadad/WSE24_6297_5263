namespace WebApp.Exceptions
{
    public class HebCalServiceException : Exception
    {
        public HebCalServiceException() : base() { }

        public HebCalServiceException(string message) : base(message) { }

        public HebCalServiceException(string message, Exception innerException) : base(message, innerException) { }
    }
}
