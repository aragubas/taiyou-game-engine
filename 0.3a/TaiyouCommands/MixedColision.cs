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
    public class MixedColision
    {
        public static void Initialize(string[] SplitedString)
        {
            string Arg1 = SplitedString[1]; // RenderName1
            string Arg2 = SplitedString[2]; // RectangleVarName
            string Arg3 = SplitedString[3]; // Command to Execute
            string AllText = "";

            int Rect1ID = Game1.RenderCommand_Name.IndexOf(Arg1);
            int Rect2ID = TaiyouReader.GlobalVars_Rectangle_Names.IndexOf(Arg2);

            Rectangle Rect1 = Game1.RenderCommand_Rectangle[Rect1ID];
            Rectangle Rect2 = TaiyouReader.GlobalVars_Rectangle_Content[Rect2ID];


            for (int i = 3; i < TaiyouReader.SplitedString.Length; i++)
            {
                AllText += TaiyouReader.SplitedString[i] + " ";

            }

            string[] AllPieces = AllText.Split('|');

            if (Rect1.Intersects(Rect2)) // If the colision is false
            {
                for (int i = 0; i < AllPieces.Length; i++)
                {
                    TaiyouReader.ReadAsync(AllPieces[i]);
                }

            }
        }

    }
}
