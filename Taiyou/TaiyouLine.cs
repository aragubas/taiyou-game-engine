using System;
namespace TaiyouScriptEngine.Desktop.Taiyou
{
    public class TaiyouLine
    {
        public Action<string[]> FunctionCall;
        public string[] Arguments;
        public string OriginalTSUP;

        public TaiyouLine(string Line)
        {
            string CommandCode = Line.Substring(0, 3);
            // Set the Arguments string
            Arguments = Line.Remove(0, 3).Split(',');

            OriginalTSUP = CommandCode;

            // Switch Case the TGEUC Interpretation
            switch (CommandCode)
            {
                case "001":
                    FunctionCall = Command.WriteLine.call;
                    break;

                case "002":
                    FunctionCall = Command.CreateVar.call;
                    break;

                case "003":
                    FunctionCall = Command.AddRenderQueue.call;
                    break;

                case "004":
                    FunctionCall = Command.MoveRenderQueueObject.call;
                    break;

                case "005":
                    FunctionCall = Command.SetRenderQueuePosition.call;
                    break;

                case "006":
                    FunctionCall = Command.IntegerOperation.call;
                    break;

                case "007":
                    FunctionCall = Command.EventHandler.call;
                    break;

                case "008":
                    FunctionCall = Command.FunctionHandler.call;
                    break;

                case "009":
                    FunctionCall = Command.SetOption.call;
                    break;


                default:
                    Console.WriteLine("Taiyou.Interpreter : Unknow TSUP (" + CommandCode + ")");
                    throw new ArgumentOutOfRangeException("Taiyou.Interpreter : Unknow TSUP (" + CommandCode + ")");

            }


        }

        public void call()
        {
            FunctionCall.Invoke(Arguments);
        }

        public string[] GetArguments()
        {
            return Arguments;
        }

    }
}
