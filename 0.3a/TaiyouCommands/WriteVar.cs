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
    public class WriteVar
    {
        // Write a value to a var



        public static void Initialize(string[] SplitedString)
        {
            string Agr1 = SplitedString[1]; // Var Type
            string Agr2 = SplitedString[2]; // Var Name
            string Agr3 = SplitedString[3]; // New Content
            if (SplitedString.Length < 3) { throw new Exception("WriteVar dont take less than 3 arguments."); }

            if (Agr1.Equals("STRING"))
            {
                int VarNameID = TaiyouReader.GlobalVars_String_Names.IndexOf(Agr2);
                if (VarNameID == -1) { throw new Exception("The string variable [" + Agr2 + "] does not exist."); }


                string AllText = "";

                for (int i = 3; i < SplitedString.Length; i++)
                {

                    AllText += SplitedString[i] + " ";

                }


                TaiyouReader.GlobalVars_String_Content[VarNameID] = AllText;

            }

            if (Agr1.Equals("BOOL"))
            {
                int VarNameID = TaiyouReader.GlobalVars_Bool_Names.IndexOf(Agr2);
                if (VarNameID == -1) { throw new Exception("The boolean variable [" + Agr2 + "] does not exist."); }

                TaiyouReader.GlobalVars_Bool_Content[VarNameID] = Convert.ToBoolean(Agr3);

            }
            if (Agr1.Equals("INT"))
            {
                int VarNameID = TaiyouReader.GlobalVars_Int_Names.IndexOf(Agr2);
                if (VarNameID == -1) { throw new Exception("The int variable [" + Agr2 + "] does not exist."); }

                TaiyouReader.GlobalVars_Int_Content[VarNameID] = Convert.ToInt32(Agr3);

            }
            if (Agr1.Equals("FLOAT"))
            {
                int VarNameID = TaiyouReader.GlobalVars_Float_Names.IndexOf(Agr2);
                if (VarNameID == -1) { throw new Exception("The float variable [" + Agr2 + "] does not exist."); }


                TaiyouReader.GlobalVars_Float_Content[VarNameID] = float.Parse(Agr3, CultureInfo.InvariantCulture.NumberFormat);

            }
            if (Agr1.Equals("COLOR"))
            {
                int VarNameID = TaiyouReader.GlobalVars_Color_Names.IndexOf(Agr2); // Get the name of the Var
                if (VarNameID == -1) { throw new Exception("The color variable [" + Agr2 + "] does not exist."); }

                string[] ColorArgument = Agr3.Split(',');


                Color NewColor = Color.FromNonPremultiplied(Convert.ToInt32(ColorArgument[0]), Convert.ToInt32(ColorArgument[1]), Convert.ToInt32(ColorArgument[2]), Convert.ToInt32(ColorArgument[3]));


                TaiyouReader.GlobalVars_Color_Content[VarNameID] = NewColor;
            }

            //////////////////////////
            /// Rectangle Modfiers ///
            //////////////////////////

            if (Agr1.Equals("RECTANGLE"))
            {
                int VarNameID = TaiyouReader.GlobalVars_Rectangle_Names.IndexOf(Agr2); // Get the name of the Var
                if (VarNameID == -1) { throw new Exception("The rectangle variable [" + Agr2 + "] does not exist."); }

                string[] RectangleArgument = Agr3.Split(',');



                Rectangle NewRectangle = new Rectangle(Convert.ToInt32(RectangleArgument[0]), Convert.ToInt32(RectangleArgument[1]), Convert.ToInt32(RectangleArgument[2]), Convert.ToInt32(RectangleArgument[3]));



                TaiyouReader.GlobalVars_Rectangle_Content[VarNameID] = NewRectangle;
            }

            if (Agr1.Equals("RECTANGLE.X"))
            {
                int VarNameID = TaiyouReader.GlobalVars_Rectangle_Names.IndexOf(Agr2); // Get the name of the Var
                if (VarNameID == -1) { throw new Exception("The rectangle variable [" + Agr2 + "] does not exist."); }

                int NewXValue = Convert.ToInt32(Agr3);


                Rectangle oldRectangle = TaiyouReader.GlobalVars_Rectangle_Content[VarNameID];

                Rectangle NewRectangle = new Rectangle(NewXValue, oldRectangle.Y, oldRectangle.Width, oldRectangle.Height);



                TaiyouReader.GlobalVars_Rectangle_Content[VarNameID] = NewRectangle;
            }

            if (Agr1.Equals("RECTANGLE.Y"))
            {
                int VarNameID = TaiyouReader.GlobalVars_Rectangle_Names.IndexOf(Agr2); // Get the name of the Var
                if (VarNameID == -1) { throw new Exception("The rectangle variable [" + Agr2 + "] does not exist."); }

                int NewYValue = Convert.ToInt32(Agr3);


                Rectangle oldRectangle = TaiyouReader.GlobalVars_Rectangle_Content[VarNameID];

                Rectangle NewRectangle = new Rectangle(oldRectangle.X, NewYValue, oldRectangle.Width, oldRectangle.Height);



                TaiyouReader.GlobalVars_Rectangle_Content[VarNameID] = NewRectangle;
            }

            if (Agr1.Equals("RECTANGLE.W"))
            {
                int VarNameID = TaiyouReader.GlobalVars_Rectangle_Names.IndexOf(Agr2); // Get the name of the Var
                if (VarNameID == -1) { throw new Exception("The rectangle variable [" + Agr2 + "] does not exist."); }

                int NewWValue = Convert.ToInt32(Agr3);


                Rectangle oldRectangle = TaiyouReader.GlobalVars_Rectangle_Content[VarNameID];

                Rectangle NewRectangle = new Rectangle(oldRectangle.X, oldRectangle.Y, NewWValue, oldRectangle.Height);



                TaiyouReader.GlobalVars_Rectangle_Content[VarNameID] = NewRectangle;
            }

            if (Agr1.Equals("RECTANGLE.H"))
            {
                int VarNameID = TaiyouReader.GlobalVars_Rectangle_Names.IndexOf(Agr2); // Get the name of the Var
                if (VarNameID == -1) { throw new Exception("The rectangle variable [" + Agr2 + "] does not exist."); }

                int NewHValue = Convert.ToInt32(Agr3);


                Rectangle oldRectangle = TaiyouReader.GlobalVars_Rectangle_Content[VarNameID];

                Rectangle NewRectangle = new Rectangle(oldRectangle.X, oldRectangle.Y, oldRectangle.Width, NewHValue);



                TaiyouReader.GlobalVars_Rectangle_Content[VarNameID] = NewRectangle;
            }

            ////////////////////////////////
            /// Rectangle Modfiers _ End ///
            ////////////////////////////////




            ///////////////////////////////
            /// List.Rectangle Modfiers ///
            ///////////////////////////////

            if (Agr1.Equals("LIST.RECTANGLE.WRITE"))
            {
                int VarNameID = TaiyouReader.GlobalVars_RectangleList_Names.IndexOf(Agr2); // Get the name of the Var
                if (VarNameID == -1) { throw new Exception("The list.rectangle variable [" + Agr2 + "] does not exist."); }

                int Index = Convert.ToInt32(Agr3);
                string[] RectCode = SplitedString[4].Split(','); // New Content


                Rectangle NewRectangle = new Rectangle(Convert.ToInt32(RectCode[0]), Convert.ToInt32(RectCode[1]), Convert.ToInt32(RectCode[2]), Convert.ToInt32(RectCode[3]));



                TaiyouReader.GlobalVars_RectangleList_Content[VarNameID][Index] = NewRectangle;
            }

            if (Agr1.Equals("LIST.RECTANGLE.ADD"))
            {
                int VarNameID = TaiyouReader.GlobalVars_RectangleList_Names.IndexOf(Agr2); // Get the name of the Var
                if (VarNameID == -1) { throw new Exception("The list.rectangle variable [" + Agr2 + "] does not exist."); }

                string[] RectCode = Agr3.Split(','); // New Content


                Rectangle NewRectangle = new Rectangle(Convert.ToInt32(RectCode[0]), Convert.ToInt32(RectCode[1]), Convert.ToInt32(RectCode[2]), Convert.ToInt32(RectCode[3]));



                TaiyouReader.GlobalVars_RectangleList_Content[VarNameID].Add(NewRectangle);
            }
            
            ///////////////////////////////////
            /// List.Rectangle_END Modfiers ///
            ///////////////////////////////////




            /////////////////////////
            /// List.INT Modfiers ///
            /////////////////////////
            if (Agr1.Equals("LIST.INT.WRITE"))
            {
                int VarNameID = TaiyouReader.GlobalVars_IntList_Names.IndexOf(Agr2); // Get the name of the Var
                if (VarNameID == -1) { throw new Exception("The list.int variable [" + Agr2 + "] does not exist."); }

                int Index = Convert.ToInt32(Agr3);
                int NewNumber = Convert.ToInt32(SplitedString[4]); // New Content



                TaiyouReader.GlobalVars_IntList_Content[VarNameID][Index] = NewNumber;
            }

            if (Agr1.Equals("LIST.INT.ADD"))
            {
                int VarNameID = TaiyouReader.GlobalVars_IntList_Names.IndexOf(Agr2); // Get the name of the Var
                if (VarNameID == -1) { throw new Exception("The list.int variable [" + Agr2 + "] does not exist."); }

                int NewNumber = Convert.ToInt32(Agr3); // New Content



                TaiyouReader.GlobalVars_IntList_Content[VarNameID].Add(NewNumber);
            }
            


        }
    }
}
