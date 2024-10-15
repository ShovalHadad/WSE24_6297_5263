namespace WebApp.Exceptions
{
    public class ImaggaServiceException : Exception
    {
        public ImaggaServiceException() : base() { }

        public ImaggaServiceException(string message) : base(message) { }

        public ImaggaServiceException(string message, Exception innerException) : base(message, innerException) { }
    }
}
