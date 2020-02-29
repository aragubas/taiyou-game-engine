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
using System.IO;
using System.Windows.Forms;

namespace TaiyouGameEngine.Desktop.TaiyouCommands
{
    public class Goto
    {
        // Jump to a specific region on a specific Taiyou Script

        static string CurrentReadLine = "";
        public static List<string> TaiyouFilesLinesFromMem_Names = new List<string>();
        public static List<string> TaiyouFilesLinesFromMem_Data = new List<string>();


        private static void AddTaiyouScriptCache(string ScriptName, string JumpRegionName)
        {
            // Variables
            List<string> AllCommands = new List<string>();
            bool DataCommandsCanAdd = false;
            string DataCommands = "";

            if (Global.IsLowLevelDebugEnabled) { Console.WriteLine("\n\nGoto : Script[" + ScriptName + "] is being added to the Scripts Cache"); }


            int StringID = TaiyouReader.CustomTaiyouScriptsName.IndexOf(ScriptName);
            if (StringID == -1) { throw new Exception("The script [" + ScriptName + "] does not exist."); }
            foreach (var LinesFromMeM in TaiyouReader.CustomTaiyouScriptsFile[StringID].Split(new string[] { Environment.NewLine }, StringSplitOptions.RemoveEmptyEntries))
            {
                if (LinesFromMeM.Equals("#" + JumpRegionName))
                {
                    DataCommandsCanAdd = true;

                }
                if (LinesFromMeM.Equals("#END"))
                {
                    DataCommandsCanAdd = false;
                }

                if (DataCommandsCanAdd)
                {
                    AllCommands.Add(LinesFromMeM);
                    DataCommands += "\n" + LinesFromMeM;
                }

            }

            if (Global.IsLowLevelDebugEnabled) { Console.WriteLine("\n\nGoto : Data Readed:\n\n### BEGIN SCRIPT DATA ###\n" + DataCommands + "\n\n### END OF SCRIPT DATA ###\n\n"); }


            if (Global.IsLowLevelDebugEnabled) { Console.WriteLine("Goto : Script[" + ScriptName + "] added to the Script Cache.\n\n"); }

            TaiyouFilesLinesFromMem_Names.Add(ScriptName);
            TaiyouFilesLinesFromMem_Data.Add(DataCommands);

    }

        public static void Initialize(string[] SplitedString)
        {
            string Arg1 = SplitedString[1]; // Script Name
            string Arg2 = SplitedString[2]; // Function Name
            if (SplitedString.Length < 2) { throw new Exception("Goto dont take less than 2 arguments."); }


            string TaiyouCommands_Raw = "";
            int NameID = TaiyouFilesLinesFromMem_Names.IndexOf(Arg1);

            if (NameID.Equals(-1))
            {
                AddTaiyouScriptCache(Arg1,Arg2);

                NameID = TaiyouFilesLinesFromMem_Names.IndexOf(Arg1);

                TaiyouCommands_Raw = TaiyouFilesLinesFromMem_Data[NameID];

            }
            else
            {
                TaiyouCommands_Raw = TaiyouFilesLinesFromMem_Data[NameID];

            }


            int Counter = 0;

            try
            {
                string[] TaiyouCommands = TaiyouCommands_Raw.Split(new[] { Environment.NewLine }, StringSplitOptions.RemoveEmptyEntries);

                for (int i = 0; i < TaiyouCommands.Length; i++)
                {
                    Counter += 1;
                    CurrentReadLine = TaiyouCommands[i];

                    TaiyouReader.ReadAsync(TaiyouCommands[i]);

                }

                Counter = 0; // Reset the Counter
            }
            catch (Exception ex)
            {
                string ErrorText = "InstructionNumber: " + Counter + "\n" +
                                   "Line:" + CurrentReadLine + "\n\n" +
                                   "Message: " + ex.Message + "\n\n" +
                                   "HResult: " + ex.HResult + "\n\n" +
                                   "StackTrace: \n" + ex.StackTrace + "\n\n" +
                                   "ScriptID: " + NameID + "\n\n" +
                                   "JumpRegionName: " + Arg2 + "\n\n" +
                                   "ScriptName: " + Arg1 + "\n\n:Goto";


                throw new Exception(ErrorText);
            }


        }
    }
}
