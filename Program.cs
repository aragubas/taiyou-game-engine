using System;

namespace TaiyouScriptEngine.Desktop
{
    /// <summary>
    /// The main class.
    /// </summary>
    public static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main(string[] Args)
        {
            int index = -1;
            foreach (var arg in Args)
            {
                index += 1;
                Console.WriteLine("Reading argument id(" + index + ")");

                if (arg.StartsWith("-thread_wait", StringComparison.Ordinal))
                {
                    Taiyou.Global.GlobalDelay = Convert.ToInt32(Args[index]);
                    Console.WriteLine("Thread Wait was set to : " + Taiyou.Global.GlobalDelay);
                }

            }

            using (var game = new Game1())
                game.Run();

        }

    }
}