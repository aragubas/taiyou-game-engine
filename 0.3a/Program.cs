/*
   ####### BEGIN APACHE 2.0 LICENSE #######
   Copyright 2019 Parallex Software

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

   ####### END APACHE 2.0 LICENSE #######




   ####### BEGIN MONOGAME LICENSE #######
   THIS GAME-ENGINE WAS CREATED USING THE MONOGAME FRAMEWORK
   Github: https://github.com/MonoGame/MonoGame#license 

   MONOGAME WAS CREATED BY MONOGAME TEAM

   THE MONOGAME LICENSE IS IN THE MONOGAME_License.txt file on the root folder. 

   ####### END MONOGAME LICENSE ####### 





*/

using System;
using System.Collections.Generic;
using System.IO;
using System.Threading;
using System.Windows.Forms;

namespace TaiyouGameEngine.Desktop
{
    /// <summary>
    /// The main class.
    /// </summary>
    public static class Program
    {
        public static string[] ArgumentsDeclared;
        [STAThread]
        static void Main(string[] args)
        {
          
            for (int i = 0; i < args.Length; i++)
            {
                Console.WriteLine("Arg: " + args[i]);

                if (args[i] == "--resetKey")
                {
                    Global.Engine_ResetKey = true;
                }

                if (args[i] == "--debug")
                {
                    Global.Engine_DebugRender = true;
                }

                if (args[i] == "--help")
                {
                    ArgumentsHelp();
                }

                if (args[i] == "--tempUser")
                {
                    Global.TemporaryUser = true;
                }




            }

            ArgumentsDeclared = args;

            if (!Directory.Exists(Environment.CurrentDirectory + "/Taiyou/"))
            {
                MessageBox.Show("Error while initializating the Taiyou Game Engine:\nCannot find the Taiyou directory. [~/Taiyou/]", "Initialization Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                Thread.CurrentThread.Abort();

            }

            if (!Directory.Exists(Environment.CurrentDirectory + "/x64/") && !Directory.Exists(Environment.CurrentDirectory + "/x86/"))
            {
                MessageBox.Show("Error while initializating the Taiyou Game Engine:\nCannot find the x64 and x86 directories.", "Initialization Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                Thread.CurrentThread.Abort();

            }


            using (var game = new Game1())
                game.Run();



        }

        public static void InitializationError(string ErrorName)
        {

        }

        public static void ArgumentsHelp()
        {
            Console.WriteLine("Usage: " + AppDomain.CurrentDomain.FriendlyName + " [OPTION]:[VALUE]");
            Console.WriteLine("Run games writted in Taiyou Programming Language");

            Console.WriteLine("\n");
            Console.WriteLine("\n --resetKey           press pause|break key to restart");
            Console.WriteLine("\n --debug              draw debug information on screen");
            Console.WriteLine("\n --help               show this help screen");
            Console.WriteLine("\n --tempUser           login to a temporary user");
            Console.WriteLine("\n");

            Console.Read();
            Console.Clear();
            Thread.CurrentThread.Abort();
        }
    }
}
