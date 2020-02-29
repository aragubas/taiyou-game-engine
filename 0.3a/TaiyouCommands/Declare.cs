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
using System.Globalization;
using Microsoft.Xna.Framework;

namespace TaiyouGameEngine.Desktop.TaiyouCommands
{
    public class Declare
    {
        static List<string> ValidVariablesType = new List<string>() { "STRING", "BOOL", "INT", "COLOR", "RECTANGLE", "FLOAT", "LIST.STRING", "LIST.INT", "LIST.COLOR", "LIST.FLOAT","LIST.RECTANGLE" };

        public static void Initialize(string[] SplitedString)
        {
            string Agr1 = SplitedString[1]; // Var Type
            string Agr2 = SplitedString[2]; // Var Name
            string Agr3 = SplitedString[3]; // Default Value
            if (SplitedString.Length < 3) { throw new Exception("Declare dont take less than 3 arguments."); }

            int ValidVarID = ValidVariablesType.IndexOf(Agr1);
            if (ValidVarID == -1) { throw new Exception("The variable type '" + Agr1 + "' is invalid."); }


            if (Agr1.Equals("STRING"))
            {
                if (TaiyouReader.GlobalVars_String_Names.Contains(Agr2))
                {
                    return;
                }
                TaiyouReader.GlobalVars_String_Names.Add(Agr2);

                string AllText = "";

                for (int i = 3; i < SplitedString.Length; i++)
                {
                    if (i < SplitedString.Length)
                    {
                        AllText += SplitedString[i] + " ";
                    }


                }


                TaiyouReader.GlobalVars_String_Content.Add(AllText);
            }

            if (Agr1.Equals("BOOL"))
            {
                if (TaiyouReader.GlobalVars_Bool_Names.Contains(Agr2))
                {
                    return;
                }
                TaiyouReader.GlobalVars_Bool_Names.Add(Agr2);

                TaiyouReader.GlobalVars_Bool_Content.Add(Convert.ToBoolean(Agr3));

            }

            if (Agr1.Equals("INT"))
            {
                if (TaiyouReader.GlobalVars_Int_Names.Contains(Agr2))
                {
                    return;
                }
                TaiyouReader.GlobalVars_Int_Names.Add(Agr2);

                TaiyouReader.GlobalVars_Int_Content.Add(Convert.ToInt32(Agr3));

            }

            if (Agr1.Equals("COLOR"))
            {
                if (TaiyouReader.GlobalVars_Color_Names.Contains(Agr2))
                {
                    return;
                }
                TaiyouReader.GlobalVars_Color_Names.Add(Agr2);

                string[] ColorArguments = Agr3.Split(',');
                if (ColorArguments.Length < 3) { throw new Exception("The RGBA color code is invalid."); };

                TaiyouReader.GlobalVars_Color_Content.Add(Color.FromNonPremultiplied(Convert.ToInt32(ColorArguments[0]), Convert.ToInt32(ColorArguments[1]), Convert.ToInt32(ColorArguments[2]), Convert.ToInt32(ColorArguments[3])));

            }

            if (Agr1.Equals("RECTANGLE"))
            {
                if (TaiyouReader.GlobalVars_Rectangle_Names.Contains(Agr2))
                {
                    return;
                }
                TaiyouReader.GlobalVars_Rectangle_Names.Add(Agr2);

                string[] RectangleArguments = Agr3.Split(',');
                if (RectangleArguments.Length < 3) { throw new Exception("The Rectangle Arguments is invalid."); };

                TaiyouReader.GlobalVars_Rectangle_Content.Add(new Rectangle(Convert.ToInt32(RectangleArguments[0]), Convert.ToInt32(RectangleArguments[1]), Convert.ToInt32(RectangleArguments[2]), Convert.ToInt32(RectangleArguments[3])));

            }

            if (Agr1.Equals("FLOAT"))
            {
                if (TaiyouReader.GlobalVars_Float_Names.Contains(Agr2))
                {
                    return;
                }
                TaiyouReader.GlobalVars_Float_Names.Add(Agr2);

                TaiyouReader.GlobalVars_Float_Content.Add(float.Parse(Agr3, CultureInfo.InvariantCulture.NumberFormat));

            }

            if (Agr1.Equals("LIST.STRING"))
            {
                if (TaiyouReader.GlobalVars_StringList_Names.Contains(Agr2))
                {
                    return;
                }


                TaiyouReader.GlobalVars_StringList_Names.Add(Agr2);
                string[] DefaultItems = Agr3.Split('|');
                TaiyouReader.GlobalVars_StringList_Content.Add(new List<string>());

                for (int i = 0; i < DefaultItems.Length; i++)
                {
                    int ListListIndex = TaiyouReader.GlobalVars_StringList_Names.IndexOf(Agr2);

                    TaiyouReader.GlobalVars_StringList_Content[ListListIndex].Add(DefaultItems[i]);

                }

            }

            if (Agr1.Equals("LIST.INT"))
            {
                if (TaiyouReader.GlobalVars_IntList_Names.Contains(Agr2))
                {
                    return;
                }


                TaiyouReader.GlobalVars_IntList_Names.Add(Agr2);
                string[] DefaultItems = Agr3.Split('|');
                TaiyouReader.GlobalVars_IntList_Content.Add(new List<int>());

                for (int i = 0; i < DefaultItems.Length; i++)
                {
                    int ListListIndex = TaiyouReader.GlobalVars_IntList_Names.IndexOf(Agr2);

                    TaiyouReader.GlobalVars_IntList_Content[ListListIndex].Add(Convert.ToInt32(DefaultItems[i]));

                }

            }

            if (Agr1.Equals("LIST.COLOR"))
            {
                if (TaiyouReader.GlobalVars_ColorList_Names.Contains(Agr2))
                {
                    return;
                }


                TaiyouReader.GlobalVars_ColorList_Names.Add(Agr2);
                string[] DefaultItems = Agr3.Split('|');
                TaiyouReader.GlobalVars_ColorList_Content.Add(new List<Color>());

                for (int i = 0; i < DefaultItems.Length; i++)
                {
                    int ListListIndex = TaiyouReader.GlobalVars_ColorList_Names.IndexOf(Agr2);

                    string[] ColorCodeSplit = DefaultItems[i].Split(',');
                    Color NewColor = Color.White;
                    NewColor.R = (byte)Convert.ToInt32(ColorCodeSplit[0]);
                    NewColor.G = (byte)Convert.ToInt32(ColorCodeSplit[1]);
                    NewColor.B = (byte)Convert.ToInt32(ColorCodeSplit[2]);
                    NewColor.A = (byte)Convert.ToInt32(ColorCodeSplit[3]);


                    TaiyouReader.GlobalVars_ColorList_Content[ListListIndex].Add(NewColor);

                }

            }

            if (Agr1.Equals("LIST.RECTANGLE"))
            {
                if (TaiyouReader.GlobalVars_RectangleList_Names.Contains(Agr2))
                {
                    return;
                }
                TaiyouReader.GlobalVars_RectangleList_Names.Add(Agr2);
                TaiyouReader.GlobalVars_RectangleList_Content.Add(new List<Rectangle>());
                string[] DefaultItems = Agr3.Split('|');
                int ListListIndex = TaiyouReader.GlobalVars_RectangleList_Names.IndexOf(Agr2);

                for (int i = 0; i < DefaultItems.Length; i++)
                {
                    string[] RectangleCodeSplit = DefaultItems[i].Split(',');
                    Rectangle newRectangle = Rectangle.Empty;
                    newRectangle.X = (byte)Convert.ToInt32(RectangleCodeSplit[0]);
                    newRectangle.Y = (byte)Convert.ToInt32(RectangleCodeSplit[1]);
                    newRectangle.Width = (byte)Convert.ToInt32(RectangleCodeSplit[2]);
                    newRectangle.Height = (byte)Convert.ToInt32(RectangleCodeSplit[3]);


                    TaiyouReader.GlobalVars_RectangleList_Content[ListListIndex].Add(newRectangle);


                }




            }






        }
    }
}
