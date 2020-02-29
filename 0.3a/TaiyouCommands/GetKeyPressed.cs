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
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Xna.Framework.Input;
using TaiyouGameEngine.Desktop.UserInput;

namespace TaiyouGameEngine.Desktop.TaiyouCommands
{
    public class GetKeyPressed
    {
        // Get the pressed key
        static KeyboardState previousState;
        


        public static void Initialize(string[] SplitedString)
        {
            string Arg1 = SplitedString[1]; // Key to Check
            string Arg2 = SplitedString[2]; // Press Type
            string Arg3 = SplitedString[3]; // Command to Execute
            if (SplitedString.Length < 3) { throw new Exception("GetKeyPressed dont take less than 3 arguments."); }

            Keys KeysTCK = (Keys)Enum.Parse(typeof(Keys), Arg1);


            string AllText = "";

            for (int i = 3; i < TaiyouReader.SplitedString.Length; i++)
            {
                AllText += TaiyouReader.SplitedString[i] + " ";
                 
            }


            KeyBoard.VerifyKeyPressed_Key.Add(KeysTCK);
            KeyBoard.VerifyKeyPressed_Values.Add(false);
            KeyBoard.VerifyKeyPressed_TaiyouCommandsToRun.Add(AllText);
            KeyBoard.VerifyKeyPressed_PressType.Add(Arg2);




        }

        private static void ThenRunOtherCommand(string CommandString)
        {
            string[] CommandsToRun = CommandString.Split('|');

            for (int i = 0; i < CommandsToRun.Length; i++)
            {
                TaiyouReader.ReadAsync(CommandsToRun[i]);

            }
        }

    }
    
}
