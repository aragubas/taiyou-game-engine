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
    public class MathOP
    {


        public static void Intialize(string[] SplitedString)
        {
            string Agr1 = SplitedString[1]; // VarType
            string Agr2 = SplitedString[2]; // VarName
            string Agr3 = SplitedString[3]; // OperationType
            string Agr4 = SplitedString[4]; // Value to Add
            if (SplitedString.Length < 4) { throw new Exception("MathOp dont take less than 4 arguments."); }

            if (Agr1.Equals("INT"))
            {
                int VarNameID = TaiyouReader.GlobalVars_Int_Names.IndexOf(Agr2);
                if (VarNameID == -1) { throw new Exception("The int var [" + Agr2 + "] does not exist."); }

                if (Agr3.Equals("+="))
                {
                    TaiyouReader.GlobalVars_Int_Content[VarNameID] += Convert.ToInt32(Agr4);
                }
                if (Agr3.Equals("-="))
                {
                    TaiyouReader.GlobalVars_Int_Content[VarNameID] -= Convert.ToInt32(Agr4);
                }
                if (Agr3.Equals("*="))
                {
                    TaiyouReader.GlobalVars_Int_Content[VarNameID] *= Convert.ToInt32(Agr4);
                }
                if (Agr3.Equals("/="))
                {
                    TaiyouReader.GlobalVars_Int_Content[VarNameID] /= Convert.ToInt32(Agr4);
                }

            }


            if (Agr1.Equals("FLOAT"))
            {
                int VarNameID = TaiyouReader.GlobalVars_Float_Names.IndexOf(Agr2);
                if (VarNameID == -1) { throw new Exception("The float var [" + Agr2 + "] does not exist."); }

                if (Agr3.Equals("+="))
                {
                    TaiyouReader.GlobalVars_Float_Content[VarNameID] += float.Parse(Agr4, CultureInfo.InvariantCulture.NumberFormat);
                }
                if (Agr3.Equals("-="))
                {
                    TaiyouReader.GlobalVars_Float_Content[VarNameID] -= float.Parse(Agr4, CultureInfo.InvariantCulture.NumberFormat);
                }
                if (Agr3.Equals("*="))
                {
                    TaiyouReader.GlobalVars_Float_Content[VarNameID] *= float.Parse(Agr4, CultureInfo.InvariantCulture.NumberFormat);
                }
                if (Agr3.Equals("/="))
                {
                    TaiyouReader.GlobalVars_Float_Content[VarNameID] /= float.Parse(Agr4, CultureInfo.InvariantCulture.NumberFormat);
                }

            }
            
            if (Agr1.Equals("LIST.INT"))
            {
                int VarNameID = TaiyouReader.GlobalVars_IntList_Names.IndexOf(Agr2);
                if (VarNameID == -1) { throw new Exception("The int list var [" + Agr2 + "] does not exist."); }

                // Argument 3 will act as Index
                // Argument 4 will act as Operation Type
                // Argument 5 will act as Number to Add

                
                int Index = Convert.ToInt32(SplitedString[3]);
                int NumberToAdd = Convert.ToInt32(SplitedString[5]);

                if (Agr4.Equals("+="))
                {

                    TaiyouReader.GlobalVars_IntList_Content[VarNameID][Index] += NumberToAdd;
                }
                if (Agr4.Equals("-="))
                {
                    TaiyouReader.GlobalVars_IntList_Content[VarNameID][Index] -= NumberToAdd;
                }
                if (Agr4.Equals("*="))
                {
                    TaiyouReader.GlobalVars_IntList_Content[VarNameID][Index] *= NumberToAdd;
                }
                if (Agr4.Equals("/="))
                {
                    TaiyouReader.GlobalVars_IntList_Content[VarNameID][Index] /= NumberToAdd;
                }

            }
            
            if (Agr1.Equals("LIST.FLOAT"))
            {
                int VarNameID = TaiyouReader.GlobalVars_FloatList_Names.IndexOf(Agr2);
                if (VarNameID == -1) { throw new Exception("The float list var [" + Agr2 + "] does not exist."); }

                // Argument 3 will act as Index
                // Argument 4 will act as Operation Type
                // Argument 5 will act as Number to Add

                
                int Index = Convert.ToInt32(SplitedString[4]);
                string NumberToAdd = SplitedString[5];


                if (Agr4.Equals("+="))
                {

                    TaiyouReader.GlobalVars_FloatList_Content[VarNameID][Index] += float.Parse(NumberToAdd, CultureInfo.InvariantCulture.NumberFormat);
                }
                if (Agr4.Equals("-="))
                {
                    TaiyouReader.GlobalVars_FloatList_Content[VarNameID][Index] -= float.Parse(NumberToAdd, CultureInfo.InvariantCulture.NumberFormat);
                }
                if (Agr4.Equals("*="))
                {
                    TaiyouReader.GlobalVars_FloatList_Content[VarNameID][Index] *= float.Parse(NumberToAdd, CultureInfo.InvariantCulture.NumberFormat);
                }
                if (Agr4.Equals("/="))
                {
                    TaiyouReader.GlobalVars_FloatList_Content[VarNameID][Index] /= float.Parse(NumberToAdd, CultureInfo.InvariantCulture.NumberFormat);
                }

            }




        }
    }
}