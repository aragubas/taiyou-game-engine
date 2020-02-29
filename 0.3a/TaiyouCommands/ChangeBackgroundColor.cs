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
using Microsoft.Xna.Framework;

namespace TaiyouGameEngine.Desktop.TaiyouCommands
{
    public class ChangeBackgroundColor
    {
        // Change the ClearScreen color


        public static void Initialize(string[] SplitedString)
        {
            try
            {
                string Arg1 = SplitedString[1]; // Color
                if (SplitedString.Length < 1) { throw new Exception("ChangeBackgroundColor dont take less than 1 argument."); }

                string[] ArgCommands = Arg1.Split(',');

                int ColorR = Convert.ToInt32(ArgCommands[0]);
                int ColorG = Convert.ToInt32(ArgCommands[1]);
                int ColorB = Convert.ToInt32(ArgCommands[2]);
                int ColorA = Convert.ToInt32(ArgCommands[3]);

                Color newColor = Color.FromNonPremultiplied(ColorR, ColorG, ColorB, ColorA);

                Game1.ClearScreenColor = newColor;


            }catch (Exception ex)
            {
                throw new Exception("Some argument is missing : ChangeBackgroundColor");
            }

        }
    }
}

