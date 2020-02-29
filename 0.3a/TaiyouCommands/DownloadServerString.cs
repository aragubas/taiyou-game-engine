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
using System.Net;

namespace TaiyouGameEngine.Desktop.TaiyouCommands
{
    public class DownloadServerString
    {
        // Download a string from a server



        public static void Initialize(string[] SplitedString)
        {
            string Arg1 = SplitedString[1]; // DownloadLink
            string Arg2 = SplitedString[2]; // Return Var Type
            string Arg3 = SplitedString[3]; // Return Var Name
            if (SplitedString.Length < 3) { throw new Exception("DownloadServerString dont take less than 3 arguments."); }

            int ReturnVarID = -1;

            try
            {
                WebClient webCl = new WebClient();

                string FlDat = webCl.DownloadString("https://" + Arg1);

                if (Arg2 == "STRING")
                {
                    ReturnVarID = TaiyouReader.GlobalVars_String_Names.IndexOf(Arg3);
                    if (ReturnVarID == -1) { throw new Exception("The string var [" + Arg3 + "] does not exist."); }

                    TaiyouReader.GlobalVars_String_Content[ReturnVarID] = FlDat;
                }
                if (Arg2 == "INT")
                {
                    ReturnVarID = TaiyouReader.GlobalVars_Int_Names.IndexOf(Arg3);
                    if (ReturnVarID == -1) { throw new Exception("The int var [" + Arg3 + "] does not exist."); }

                    TaiyouReader.GlobalVars_Int_Content[ReturnVarID] = Convert.ToInt32(FlDat);
                }
                if (Arg2 == "BOOL")
                {
                    ReturnVarID = TaiyouReader.GlobalVars_Bool_Names.IndexOf(Arg3);
                    if (ReturnVarID == -1) { throw new Exception("The boolean var [" + Arg3 + "] does not exist."); }

                    TaiyouReader.GlobalVars_Bool_Content[ReturnVarID] = Convert.ToBoolean(FlDat);
                }
                if (Arg2 == "FLOAT")
                {
                    ReturnVarID = TaiyouReader.GlobalVars_Float_Names.IndexOf(Arg3);
                    if (ReturnVarID == -1) { throw new Exception("The float var [" + Arg3 + "] does not exist."); }

                    TaiyouReader.GlobalVars_Float_Content[ReturnVarID] = float.Parse(FlDat, CultureInfo.InvariantCulture.NumberFormat);
                }


            }
            catch (Exception ex)
            {
                Console.WriteLine("Error while processing the Server File request:\nMessage: " + ex.Message + "\n\nArg1[" + Arg1 + "]\nArg2[" + Arg2 + "]");
            }


        }
    }
}
