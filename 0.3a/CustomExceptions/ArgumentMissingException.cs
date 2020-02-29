using System;
namespace TaiyouGameEngine.CustomExceptions
{
    public class ArgumentMissingException : Exception
    {
        public ArgumentMissingException()
    {

    }

    public ArgumentMissingException(string message)
        : base(message)
    {
            WriteHelpText();
    }

    public ArgumentMissingException(string message, Exception inner)
        : base(message, inner)
    {
            WriteHelpText();
    }

    private void WriteHelpText()
    {
        Console.WriteLine("Exception Help:\n");
        Console.WriteLine("This exception is called when a command is missing an Argument.");

    }

    }
}
