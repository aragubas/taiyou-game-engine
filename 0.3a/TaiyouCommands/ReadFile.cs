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
using System.IO;

namespace TaiyouGameEngine.Desktop.TaiyouCommands
{
    public class ReadFile
    {


        public static void Intialize(string[] SplitedString)
        {
            string Agr1 = SplitedString[1]; // File Directory
            string Agr2 = SplitedString[2]; // VarReturn Type
            string Agr3 = SplitedString[3]; // ReturnVar name
            if (SplitedString.Length < 3) { throw new Exception("ReadFile dont take less than 3 arguments."); }

            string DirectoryOfData = "";
            DirectoryOfData = Global.GameDataFolder;

            // IF the game is trying to write to the .reserved directory
            if (Agr1.StartsWith(".reserved", StringComparison.CurrentCulture)) { throw new Exception("Access to the [.reserved] is denied."); }


            string UncryptedText = PassCryptografy.DecryptString(File.ReadAllText(DirectoryOfData), Global.CurrentLoggedPassword);

            if (File.Exists(DirectoryOfData))
                {
            
                    if (Agr2 == "STRING")
                    {
                        int ReturnVarID = TaiyouReader.GlobalVars_String_Names.IndexOf(Agr3);
                        if (ReturnVarID == -1) { throw new Exception("The string variable [" + ReturnVarID + "] does not exsit."); }

            
                        TaiyouReader.GlobalVars_String_Content[ReturnVarID] = UncryptedText;

                    }

                    if (Agr2 == "INT")
                    {
                        int ReturnVarID = TaiyouReader.GlobalVars_Int_Names.IndexOf(Agr3);
                        if (ReturnVarID == -1) { throw new Exception("The int variable [" + ReturnVarID + "] does not exsit."); }


                        TaiyouReader.GlobalVars_Int_Content[ReturnVarID] = Convert.ToInt32(UncryptedText);

                    }

                    if (Agr2 == "FLOAT")
                    {
                        int ReturnVarID = TaiyouReader.GlobalVars_Float_Names.IndexOf(Agr3);
                        if (ReturnVarID == -1) { throw new Exception("The float variable [" + ReturnVarID + "] does not exsit."); }

                        float newValue = float.Parse(UncryptedText, CultureInfo.InvariantCulture.NumberFormat);

                        TaiyouReader.GlobalVars_Float_Content[ReturnVarID] = newValue;

                    }


                    if (Agr2 == "BOOLEAN")
                    {
                        int ReturnVarID = TaiyouReader.GlobalVars_Bool_Names.IndexOf(Agr3);
                        if (ReturnVarID == -1) { throw new Exception("The boolean variable [" + ReturnVarID + "] does not exsit."); }

            
                        TaiyouReader.GlobalVars_Bool_Content[ReturnVarID] = Convert.ToBoolean(UncryptedText);

                    }


                }
                else
                {
                    throw new FileNotFoundException("ERROR : The requested file does not exist.");
                }




            }
        }
    }