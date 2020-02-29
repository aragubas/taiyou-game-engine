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
    public class ChangeRenderProp
    {
        // Change a render propertie


        public static void Initialize(string[] SplitedString)
        {
            string Arg1 = SplitedString[1]; // RenderType
            string Arg2 = SplitedString[2]; // RenderObjName
            string Arg3 = SplitedString[3]; // PropertieName
            string Arg4 = SplitedString[4]; // PropertieValue
            int ObjRenderID = -1;
            if (SplitedString.Length < 4) { throw new Exception("ChangeRenderProp dont take less than 4 arguments."); }

            if (Arg1.Equals("SPRITE"))
            {
                ObjRenderID = Game1.RenderCommand_Name.IndexOf(Arg2);

            }if (Arg1.Equals("TEXT"))
            {
                ObjRenderID = Game1.TextRenderCommand_Name.IndexOf(Arg2);
            }

            if (ObjRenderID == -1)
            {
                throw new Exception("The [" + Arg1 + "] Render Object [" + Arg2 + "] does not exist.");
            }

            if (Arg3.Equals("COLOR"))
            {
                string[] Parms = Arg4.Split(',');

                int ColorR = Convert.ToInt32(Parms[0]);
                int ColorG = Convert.ToInt32(Parms[1]);
                int ColorB = Convert.ToInt32(Parms[2]);
                int ColorA = Convert.ToInt32(Parms[3]);

                Color RtnClr = Color.FromNonPremultiplied(ColorR, ColorG, ColorB, ColorA);

                if (Arg1.Equals("SPRITE"))
                {
                    Game1.RenderCommand_SpriteColor[ObjRenderID] = RtnClr;
                }
                if (Arg1.Equals("TEXT"))
                {
                    Game1.TextRenderCommand_Color[ObjRenderID] = RtnClr;
                }

            }
            if (Arg3.Equals("RENDER_ORDER"))
            {
                string[] Parms = Arg4.Split(',');

                float RenderOrder = float.Parse(Arg4, CultureInfo.InvariantCulture.NumberFormat);

                if (Arg1.Equals("SPRITE"))
                {
                    Game1.RenderCommand_RenderOrder[ObjRenderID] = RenderOrder;
                }
                if (Arg1.Equals("TEXT"))
                {
                    Game1.TextRenderCommand_RenderOrder[ObjRenderID] = RenderOrder;
                }

            }
            if (Arg3.Equals("ROTATION"))
            {
                float RenderRotation = float.Parse(Arg4, CultureInfo.InvariantCulture.NumberFormat);

                if (Arg1.Equals("SPRITE"))
                {
                    Game1.RenderCommand_RenderRotation[ObjRenderID] = RenderRotation;
                }
                if (Arg1.Equals("TEXT"))
                {
                    Game1.TextRenderCommand_Rotation[ObjRenderID] = RenderRotation;
                }
            }

            if (Arg3.Equals("X"))
            {
                int NewXValue = Convert.ToInt32(Arg4);

                if (Arg1.Equals("TEXT"))
                {
                    Game1.TextRenderCommand_X[ObjRenderID] = NewXValue;
                }
                if (Arg1.Equals("SPRITE"))
                {
                    int RectVarID = Game1.RenderCommand_Name.IndexOf(Arg2);
                    if (RectVarID == -1) { throw new Exception("The rectangle variable [" + Arg2 + "] does not exist."); }
                    string RectName = Game1.RenderCommand_RectangleVar[RectVarID];
                    int VarRectObj = TaiyouReader.GlobalVars_Rectangle_Names.IndexOf(RectName);
                    Rectangle OldRectangle = TaiyouReader.GlobalVars_Rectangle_Content[VarRectObj];

                    Rectangle NewRectangle = new Rectangle(NewXValue, OldRectangle.Y, OldRectangle.Width, OldRectangle.Height);

                    TaiyouReader.GlobalVars_Rectangle_Content[VarRectObj] = NewRectangle;

                }

            }

            if (Arg3.Equals("X_SCALE"))
            {
                int NewXScaleValue = Convert.ToInt32(Arg4);

                if (Arg1.Equals("SPRITE"))
                {
                    int RectVarID = Game1.RenderCommand_Name.IndexOf(Arg2);
                    if (RectVarID == -1) { throw new Exception("The rectangle variable [" + Arg2 + "] does not exist."); }
                    string RectName = Game1.RenderCommand_RectangleVar[RectVarID];
                    int VarRectObj = TaiyouReader.GlobalVars_Rectangle_Names.IndexOf(RectName);
                    Rectangle OldRectangle = TaiyouReader.GlobalVars_Rectangle_Content[VarRectObj];

                    Rectangle NewRectangle = new Rectangle(OldRectangle.X, OldRectangle.Y, OldRectangle.Width * NewXScaleValue, OldRectangle.Height);

                    TaiyouReader.GlobalVars_Rectangle_Content[VarRectObj] = NewRectangle;


                }

            }

            if (Arg3.Equals("Y_SCALE"))
            {
                int NewYScaleValue = Convert.ToInt32(Arg4);

                if (Arg1.Equals("SPRITE"))
                {
                    int RectVarID = Game1.RenderCommand_Name.IndexOf(Arg2);
                    if (RectVarID == -1) { throw new Exception("The rectangle variable [" + Arg2 + "] does not exist."); }
                    string RectName = Game1.RenderCommand_RectangleVar[RectVarID];
                    int VarRectObj = TaiyouReader.GlobalVars_Rectangle_Names.IndexOf(RectName);
                    Rectangle OldRectangle = TaiyouReader.GlobalVars_Rectangle_Content[VarRectObj];

                    Rectangle NewRectangle = new Rectangle(OldRectangle.X, OldRectangle.Y, OldRectangle.Width, OldRectangle.Height * NewYScaleValue);

                    TaiyouReader.GlobalVars_Rectangle_Content[VarRectObj] = NewRectangle;

                }

            }

            if (Arg3.Equals("XY_SCALE"))
            {
                int ScaleValue = Convert.ToInt32(Arg4);

                if (Arg1.Equals("SPRITE"))
                {
                    int RectVarID = Game1.RenderCommand_Name.IndexOf(Arg2);
                    if (RectVarID == -1) { throw new Exception("The rectangle variable [" + Arg2 + "] does not exist."); }
                    string RectName = Game1.RenderCommand_RectangleVar[RectVarID];
                    int VarRectObj = TaiyouReader.GlobalVars_Rectangle_Names.IndexOf(RectName);
                    Rectangle OldRectangle = TaiyouReader.GlobalVars_Rectangle_Content[VarRectObj];

                    Rectangle NewRectangle = new Rectangle(OldRectangle.X, OldRectangle.Y, OldRectangle.Width * ScaleValue, OldRectangle.Height * ScaleValue);

                    TaiyouReader.GlobalVars_Rectangle_Content[VarRectObj] = NewRectangle;

                }

            }



            if (Arg3.Equals("Y"))
            {
                int NewYValue = Convert.ToInt32(Arg4);

                if (Arg1.Equals("TEXT"))
                {
                    Game1.TextRenderCommand_Y[ObjRenderID] = NewYValue;
                }
                if (Arg1.Equals("SPRITE"))
                {
                    int RectVarID = Game1.RenderCommand_Name.IndexOf(Arg2);
                    if (RectVarID == -1) { throw new Exception("The rectangle variable [" + Arg2 + "] does not exist."); }
                    string RectName = Game1.RenderCommand_RectangleVar[RectVarID];
                    int VarRectObj = TaiyouReader.GlobalVars_Rectangle_Names.IndexOf(RectName);
                    Rectangle OldRectangle = TaiyouReader.GlobalVars_Rectangle_Content[VarRectObj];

                    Rectangle NewRectangle = new Rectangle(OldRectangle.X, NewYValue, OldRectangle.Width, OldRectangle.Height);

                    TaiyouReader.GlobalVars_Rectangle_Content[VarRectObj] = NewRectangle;


                }

            }
            if (Arg3.Equals("X_ORIGIN"))
            {
                int NewXValue = Convert.ToInt32(Arg4);

                if (Arg1.Equals("TEXT"))
                {
                    Game1.TextRenderCommand_RotationOriginX[ObjRenderID] = NewXValue;
                }
                if (Arg1.Equals("SPRITE"))
                {
                    Game1.RenderCommand_OrigionX[ObjRenderID] = NewXValue;
                }

            }
            if (Arg3.Equals("Y_ORIGIN"))
            {
                int NewYValue = Convert.ToInt32(Arg4);

                if (Arg1.Equals("TEXT"))
                {
                    Game1.TextRenderCommand_RotationOriginY[ObjRenderID] = NewYValue;
                }
                if (Arg1.Equals("SPRITE"))
                {
                    Game1.RenderCommand_OrigionY[ObjRenderID] = NewYValue;
                }

            }

            if (Arg3.Equals("W"))
            {
                int NewWValue = Convert.ToInt32(Arg4);

                if (Arg1.Equals("SPRITE"))
                {
                    int RectVarID = Game1.RenderCommand_Name.IndexOf(Arg2);
                    if (RectVarID == -1) { throw new Exception("The rectangle variable [" + Arg2 + "] does not exist."); }
                    string RectName = Game1.RenderCommand_RectangleVar[RectVarID];
                    int VarRectObj = TaiyouReader.GlobalVars_Rectangle_Names.IndexOf(RectName);
                    Rectangle OldRectangle = TaiyouReader.GlobalVars_Rectangle_Content[VarRectObj];

                    Rectangle NewRectangle = new Rectangle(OldRectangle.X, OldRectangle.Y, NewWValue, OldRectangle.Height);

                    TaiyouReader.GlobalVars_Rectangle_Content[VarRectObj] = NewRectangle;

                }

            }
            if (Arg3.Equals("H"))
            {
                int NewHValue = Convert.ToInt32(Arg4);

                if (Arg1.Equals("SPRITE"))
                {
                    int RectVarID = Game1.RenderCommand_Name.IndexOf(Arg2);
                    if (RectVarID == -1) { throw new Exception("The rectangle variable [" + Arg2 + "] does not exist."); }
                    string RectName = Game1.RenderCommand_RectangleVar[RectVarID];
                    int VarRectObj = TaiyouReader.GlobalVars_Rectangle_Names.IndexOf(RectName);
                    Rectangle OldRectangle = TaiyouReader.GlobalVars_Rectangle_Content[VarRectObj];

                    Rectangle NewRectangle = new Rectangle(OldRectangle.X, OldRectangle.Y, OldRectangle.Width, NewHValue);

                    TaiyouReader.GlobalVars_Rectangle_Content[VarRectObj] = NewRectangle;

                }

            }
            if (Arg3.Equals("SCALE"))
            {
                float newScale = float.Parse(Arg4, CultureInfo.InvariantCulture.NumberFormat);

                if (Arg1.Equals("TEXT"))
                {
                    Game1.TextRenderCommand_Scale[ObjRenderID] = newScale;
                }

            }

            if (Arg3.Equals("TEXT"))
            {
                string AllText = "";

                for (int i = 4; i < SplitedString.Length; i++)
                {

                    AllText += SplitedString[i] + " ";

                }

                if (Arg1.Equals("TEXT"))
                {
                    Game1.TextRenderCommand_Text[ObjRenderID] = AllText;
                }

            }
            if (Arg3.Equals("SPRITE"))
            {
                string newText = Convert.ToString(Arg4);

                if (Arg1.Equals("TEXT"))
                {
                    Game1.TextRenderCommand_SpriteFont[ObjRenderID] = newText;
                }
                if (Arg1.Equals("SPRITE"))
                {
                    Game1.RenderCommand_SpriteResource[ObjRenderID] = newText;
                }

            }
            if (Arg3.Equals("FLIP_STATE"))
            {
                string newText = Convert.ToString(Arg4);

                if (Arg1.Equals("TEXT"))
                {
                    Game1.TextRenderCommand_FlipState[ObjRenderID] = newText;
                }
                if (Arg1.Equals("SPRITE"))
                {
                    Game1.RenderCommand_SpriteFlipState[ObjRenderID] = newText;
                }

            }







        }
    }
}
