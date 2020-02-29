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
namespace TaiyouGameEngine.Desktop.TaiyouCommands
{
    public class ChangeWindowPropertie
    {
        // Change a Window Propertie



        public static void Initialize(string[] SplitedString)
        {
            string Arg1 = SplitedString[1]; // Propertie Name
            string Arg2 = SplitedString[2]; // Propertie Value
            if (SplitedString.Length < 2) { throw new Exception("ChangeWindowPropertie dont take less than 2 arguments."); }

            string AllText = "";

            for (int i = 2; i < SplitedString.Length; i++)
            {
                AllText += SplitedString[i] + " ";
                 
            }

            WindowManager.ChangeWindowPropertie(Arg1, AllText);
        }
    }
}
