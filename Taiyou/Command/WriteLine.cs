using System;

namespace TaiyouScriptEngine.Desktop.Taiyou.Command
{
    public static class WriteLine
    {

        public static void call(string[] Arguments)
        {
            string TextToDisplay = Utils.GetSubstring(Arguments[0], '"');

            Console.WriteLine(TextToDisplay);
        }

    }
}
