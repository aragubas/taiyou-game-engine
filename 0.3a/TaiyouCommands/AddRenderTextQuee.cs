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
using System.Globalization;

namespace TaiyouGameEngine.Desktop.TaiyouCommands
{
    public class AddRenderTextQuee
    {
        // Add a text to Render

        public static void Initialize(string[] SplitedString)
        {
            // Required Arguments
            string Arg1 = SplitedString[1]; // Render Tag Name
            string Arg2 = SplitedString[2]; // Font Resource Name
            string Arg3 = SplitedString[3]; // Font Color
            string Arg4 = SplitedString[4]; // Font X
            string Arg5 = SplitedString[5]; // Font Y
            string Arg6 = SplitedString[6]; // Font RenderOrder
            string Arg7 = SplitedString[7]; // String Var Text

            if (SplitedString.Length < 7) { throw new Exception("AddRenderTextQuee dont take less than 7 arguments."); }


            // Optional Arguments
            string Arg8 = "1"; // Font Scale
            string Arg9 = "0"; // Font Rotation
            string Arg10 = "0"; // Font RotationOriginX
            string Arg11 = "0"; // Font RotationOriginY
            string Arg12 = "NONE"; // Flip State

            try
            {
                Arg8 = SplitedString[8]; // Font Scale
                Arg9 = SplitedString[9]; // Font Rotation
                Arg10 = SplitedString[10]; // Font RotationOriginX
                Arg11 = SplitedString[11]; // Font RotationOriginY
                Arg12 = SplitedString[12]; // Flip State

            }
            catch (Exception ex) { }

            int StringVarIndex = TaiyouReader.GlobalVars_String_Names.IndexOf(Arg7);
            string AllText = TaiyouReader.GlobalVars_String_Content[StringVarIndex];

            int ColorCodeID = TaiyouReader.GlobalVars_Color_Names.IndexOf(Arg3);
            float RenderOrder = float.Parse(Arg6, CultureInfo.InvariantCulture.NumberFormat);
            float RenderScale = float.Parse(Arg8, CultureInfo.InvariantCulture.NumberFormat);
            float RenderRotation = float.Parse(Arg9, CultureInfo.InvariantCulture.NumberFormat);
            int RotationOriginX = Convert.ToInt32(Arg10);
            int RotationOriginY = Convert.ToInt32(Arg11);
            //Arg4 = "-" + Arg4;
            //Arg5 = "-" + Arg5;


            Game1.AddTextRenderQuee(Arg1, AllText, Arg2, TaiyouReader.GlobalVars_Color_Content[ColorCodeID], Convert.ToInt32(Arg4), Convert.ToInt32(Arg5) ,RenderOrder,RenderRotation,RotationOriginX,RotationOriginY,RenderScale,Arg12);
        }
    }
}
