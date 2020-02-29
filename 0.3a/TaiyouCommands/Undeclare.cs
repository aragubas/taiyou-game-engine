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


   12


*/

using System;
namespace TaiyouGameEngine.Desktop.TaiyouCommands
{
    public class Undeclare
    {
        // Undeclare a Variable 


        public static void Initialize(string[] SplitedString)
        {
            string Arg1 = SplitedString[1]; // Variable Type
            string Arg2 = SplitedString[2]; // Variable Name
            if (SplitedString.Length < 2) { throw new Exception("Undeclare dont take less than 2 arguments."); }

            try
            {
                if (Arg1.Equals("INT"))
                {
                    int VarID = TaiyouReader.GlobalVars_Int_Names.IndexOf(Arg2); // Get the Var ID

                    TaiyouReader.GlobalVars_Int_Names.RemoveAt(VarID);
                    TaiyouReader.GlobalVars_Int_Content.RemoveAt(VarID);

                }
                if (Arg1.Equals("STRING"))
                {
                    int VarID = TaiyouReader.GlobalVars_String_Names.IndexOf(Arg2); // Get the Var ID

                    TaiyouReader.GlobalVars_String_Names.RemoveAt(VarID);
                    TaiyouReader.GlobalVars_String_Content.RemoveAt(VarID);

                }
                if (Arg1.Equals("COLOR"))
                {
                    int VarID = TaiyouReader.GlobalVars_Color_Names.IndexOf(Arg2); // Get the Var ID

                    TaiyouReader.GlobalVars_Color_Names.RemoveAt(VarID);
                    TaiyouReader.GlobalVars_Color_Content.RemoveAt(VarID);

                }
                if (Arg1.Equals("BOOL"))
                {
                    int VarID = TaiyouReader.GlobalVars_Bool_Names.IndexOf(Arg2); // Get the Var ID

                    TaiyouReader.GlobalVars_Bool_Names.RemoveAt(VarID);
                    TaiyouReader.GlobalVars_Bool_Content.RemoveAt(VarID);

                }
                if (Arg1.Equals("RECTANGLE"))
                {
                    int VarID = TaiyouReader.GlobalVars_Rectangle_Names.IndexOf(Arg2); // Get the Var ID

                    TaiyouReader.GlobalVars_Rectangle_Names.RemoveAt(VarID);
                    TaiyouReader.GlobalVars_Rectangle_Content.RemoveAt(VarID);

                }
                if (Arg1.Equals("FLOAT"))
                {
                    int VarID = TaiyouReader.GlobalVars_Float_Names.IndexOf(Arg2); // Get the Var ID

                    TaiyouReader.GlobalVars_Float_Names.RemoveAt(VarID);
                    TaiyouReader.GlobalVars_Float_Content.RemoveAt(VarID);

                }
                if (Arg1.Equals("SPRITE"))
                {
                    int VarID = Game1.RenderCommand_Name.IndexOf(Arg2); // Get the Var ID

                    Game1.RenderCommand_Name.RemoveAt(VarID);
                    Game1.RenderCommand_OrigionX.RemoveAt(VarID);
                    Game1.RenderCommand_OrigionY.RemoveAt(VarID);
                    Game1.RenderCommand_RectangleVar.RemoveAt(VarID);
                    Game1.RenderCommand_RenderOrder.RemoveAt(VarID);
                    Game1.RenderCommand_SpriteColor.RemoveAt(VarID);
                    Game1.RenderCommand_RenderRotation.RemoveAt(VarID);
                    Game1.RenderCommand_SpriteResource.RemoveAt(VarID);
                    Game1.RenderCommand_SpriteFlipState.RemoveAt(VarID);

                }
                if (Arg1.Equals("TEXT"))
                {
                    int VarID = Game1.TextRenderCommand_Name.IndexOf(Arg2); // Get the Var ID

                    Game1.TextRenderCommand_X.RemoveAt(VarID);
                    Game1.TextRenderCommand_Y.RemoveAt(VarID);
                    Game1.TextRenderCommand_Name.RemoveAt(VarID);
                    Game1.TextRenderCommand_Text.RemoveAt(VarID);
                    Game1.TextRenderCommand_Color.RemoveAt(VarID);
                    Game1.TextRenderCommand_Scale.RemoveAt(VarID);
                    Game1.TextRenderCommand_Rotation.RemoveAt(VarID);
                    Game1.TextRenderCommand_SpriteFont.RemoveAt(VarID);
                    Game1.TextRenderCommand_RenderOrder.RemoveAt(VarID);
                    Game1.TextRenderCommand_RotationOriginX.RemoveAt(VarID);
                    Game1.TextRenderCommand_RotationOriginY.RemoveAt(VarID);
                    Game1.TextRenderCommand_FlipState.RemoveAt(VarID);

                }
            }
            catch(Exception ex)
            {
                Console.WriteLine("Undeclare : Cannot undeclare an inexistent variable.");
            }


        }
    }
}
