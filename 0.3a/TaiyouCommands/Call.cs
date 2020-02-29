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
using System.Threading.Tasks;
using System.Windows.Forms;

namespace TaiyouGameEngine.Desktop.TaiyouCommands
{
    public class Call
    {
        // Call a taiyou script
        static string CurrentReadLine = "";
        public static List<string> TaiyouFilesLinesFromMem_Names = new List<string>();
        public static List<string> TaiyouFilesLinesFromMem_Data = new List<string>();
      
        private static void AddTaiyouScriptCache(string ScriptName)
        {
            bool LinesCanBeReaded = true;
            string AllCommand = "";

            if (Global.IsLowLevelDebugEnabled) { Console.WriteLine("\n\nCall : Script[" + ScriptName + "] is being added to the Scripts Cache"); }


            int TaiyouScriptID = TaiyouReader.CustomTaiyouScriptsName.IndexOf(ScriptName);
            if (TaiyouScriptID == -1) { throw new Exception("The taiyou script [" + ScriptName + "] does not exist."); }
            foreach (var LinesFromMeM in TaiyouReader.CustomTaiyouScriptsFile[TaiyouScriptID].Split(new string[] { Environment.NewLine }, StringSplitOptions.RemoveEmptyEntries))
            {
                if (LinesFromMeM.StartsWith("#", StringComparison.CurrentCulture)) // Function Instruction
                {
                    LinesCanBeReaded = false;
                }
                if (LinesFromMeM.Equals("#END"))
                {
                    LinesCanBeReaded = true;
                }

                if (LinesCanBeReaded)
                {
                    if (!LinesFromMeM.StartsWith("//", StringComparison.CurrentCulture))
                    { 
                        AllCommand += LinesFromMeM + "\n";
                    }

                }

            }


            if (Global.IsLowLevelDebugEnabled) { Console.WriteLine("\n\nCall : Data Readed:\n\n### BEGIN SCRIPT DATA ###\n" + AllCommand + "\n\n### END OF SCRIPT DATA ###\n\n"); }


            if (Global.IsLowLevelDebugEnabled) { Console.WriteLine("Call : Script[" + ScriptName + "] added to the Script Cache.\n\n" ); }

            TaiyouFilesLinesFromMem_Names.Add(ScriptName);
            TaiyouFilesLinesFromMem_Data.Add(AllCommand);
        }

        public static void Initialize(string Agr1)
        {
            int CurrentTaiyou = TaiyouReader.CustomTaiyouScriptsName.IndexOf(Agr1);

            string TaiyouCommands_Raw = "";

            int NameID = TaiyouFilesLinesFromMem_Names.IndexOf(Agr1);

            if (NameID == -1)
            {
                AddTaiyouScriptCache(Agr1);

                NameID = TaiyouFilesLinesFromMem_Names.IndexOf(Agr1);

                TaiyouCommands_Raw = TaiyouFilesLinesFromMem_Data[NameID];

            }
            else
            {
                TaiyouCommands_Raw = TaiyouFilesLinesFromMem_Data[NameID];

            }


            try
            {
                string[] TaiyouCommands = TaiyouCommands_Raw.Split(new[] { Environment.NewLine }, StringSplitOptions.RemoveEmptyEntries );

                for (int i = 0; i < TaiyouCommands.Length; i++)
                {
                    CurrentReadLine = TaiyouCommands[i];
                    TaiyouReader.ReadAsync(TaiyouCommands[i]);

                }

            }
            catch (Exception ex)
            {
                string ErrorText = "Line:" + CurrentReadLine + "\n\n" + 
                                   "Message: " + ex.Message + "\n\n" + 
                                   "HResult: " + ex.HResult + "\n\n" + 
                                   "StackTrace: \n" + ex.StackTrace + "\n\n" + 
                                   "ScriptID: " + NameID + "\n\n" +
                                   "ScriptName: " + Agr1 + "\n\n:Call";


                throw new Exception(ErrorText);
            }

         
        }
    }
}
