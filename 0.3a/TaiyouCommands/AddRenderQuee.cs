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
using Microsoft.Xna.Framework;

namespace TaiyouGameEngine.Desktop.TaiyouCommands
{
    public class AddRenderQuee
    {
        // Add a sprite to Render Quee

        public static void Initialize(string[] SplitedString)
        {
            string Arg1 = SplitedString[1]; // The SpriteName
            string Arg2 = SplitedString[2]; // Var Rectangle
            string Arg3 = SplitedString[3]; // TextureName
            string Arg4 = SplitedString[4]; // Var Color
            string Arg5 = SplitedString[5]; // Render Order
            string Arg6 = "0"; // Render Rotation
            string Arg7 = "0"; // Rotation Origin X
            string Arg8 = "0"; // Rotation Origin Y
            string Arg9 = "NONE"; // FlipState

            if (SplitedString.Length < 5) { throw new Exception("AddRenderQuee dont take less than 5 arguments."); }

            try
            {
                Arg6 = SplitedString[6];
                Arg7 = SplitedString[7];
                Arg8 = SplitedString[8];
                Arg9 = SplitedString[9];

            }
            catch (Exception ex) { }

            // Get the correct ID's
            int ColorVarID = TaiyouReader.GlobalVars_Color_Names.IndexOf(Arg4);
            float RenderOrder = float.Parse(Arg5, CultureInfo.InvariantCulture.NumberFormat);
            float RenderRotation = float.Parse(Arg6, CultureInfo.InvariantCulture.NumberFormat);
            int RotationOriginX = Convert.ToInt32(Arg7);
            int RotationOriginY = Convert.ToInt32(Arg8);
            Rectangle RectToReturn = new Rectangle(0, 0, 1, 1);

            // Verify if rectangle var exist
            int RectVarID = TaiyouReader.GlobalVars_Rectangle_Names.IndexOf(Arg2);
            if (RectVarID == -1) { throw new Exception("The rectangle var [" + Arg2 + "] does not exist."); }


            // And Finally, add to Render Quee
            Game1.AddRenderQuee(Arg1, Arg2, Arg3, TaiyouReader.GlobalVars_Color_Content[ColorVarID],RenderOrder, RenderRotation, RotationOriginX,RotationOriginY,Arg9);

        }



    }
}
