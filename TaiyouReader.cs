/*
   ####### BEGIN APACHE 2.0 LICENSE #######
   Copyright 2019 Aragubas

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
using System.Net;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Xna.Framework;
using System.Security;
using System.Globalization;

namespace TaiyouGameEngine
{
    public class TaiyouReader
    {
        // Global Vars

        /// <summary>
        /// Initialize this instance.
        /// </summary>
        public static void Initialize()
        {
            Console.WriteLine("Taiyou : Initialize");


            // Verify if the TaiyouLang directory Exists
            if (!Directory.Exists(Environment.CurrentDirectory + "/Taiyou/OPT/TaiyouLang/"))
            {
                throw new DirectoryNotFoundException("The Taiyou Language files does not exist.");
            }

            // Read the Config File
            TaiyouConfigFile();



            // Lista all taiyou Scripts
            ListTaiyouSCRIPTS(); // List all SCRIPTS on SCRIPTS folder.

            Console.WriteLine("Taiyou : Loading Scripts to Memory");
            // Read All Taiyou scripts to memory
            for (int i = 0; i < CustomTaiyouScriptsName.Count; i++)
            {
                string ScriptNameFilted = CustomTaiyouScriptsName[i];

                if (ScriptNameFilted.Contains("."))
                {
                    ScriptNameFilted = ScriptNameFilted.Replace(".", "/");
                }

                string FileDir = Global.ContentFolder + "/SCRIPTS/" + ScriptNameFilted + Registry.ReadKeyValue("FILE_EXTENSIONS/Taiyou");
                    CustomTaiyouScriptsFile.Add(TranslateTaiyouScript(File.ReadAllText(FileDir), ScriptNameFilted.Replace("/",".")));

            }

            // Load the Enviroment Variables
            LoadDefaultVars();



            // When the operation is Completed.
            Console.WriteLine("Taiyou : Ready!");

        
        }

        private static void TaiyouConfigFile(bool AlwaysWriteDefaults = false)
        {
            
            if (File.Exists(Environment.CurrentDirectory + Registry.ReadKeyValue("TAIYOU_OPTIONS/OptionsFile")) && AlwaysWriteDefaults == false)
            {
                Console.WriteLine("\n\nReadTaiyouConfigFile : Config file detected.");

                try
                {
                    var lines = File.ReadLines(Environment.CurrentDirectory + Registry.ReadKeyValue("TAIYOU_OPTIONS/OptionsFile"));
                    foreach (var line in lines)
                    {
                        bool IsLineValid = true;

                        if (line.StartsWith("//"))
                        {
                            IsLineValid = false;

                            Console.WriteLine("ReadTaiyouConfigFile : Commentary Line Detected");
                            
                        }

                        if (IsLineValid)
                        {
                            string[] SplitedParameters = line.Split(':');
                            bool ParameterIgnored = false;

                            if (SplitedParameters[0] == "ScriptOptimizationCache")
                            {
                                Global.CreateScriptOptimizationCache = Convert.ToBoolean(SplitedParameters[1]);
                                ParameterIgnored = true;
                            }


                            Console.WriteLine("ReadTaiyouConfigFile : Line[" + SplitedParameters[0] + "] ParameterIgnored[" + ParameterIgnored + "]");
                        }

                    }
                    Console.WriteLine("ReadTaiyouConfigFile : Config file read complete.");

                }catch (Exception ex)
                {
                    Console.WriteLine("ReadTaiyouConfigFile : ReadConfFile ERROR;" + ex.Message + "\nWritting new Config File...");
                    TaiyouConfigFile(true);
                }


            }
            else // Set the Default Parameters & Create the Taiyou Config File
            {
                Console.WriteLine("ReadTaiyouConfigFile : Config file not detected.");

                string FileContent = "// #################################################\n " +
                                     "// # This file contains the Game Taiyou Language   #\n" +
                                     "// # Interpreter Options, if this file is deleted  #\n" +
                                     "// # The Taiyou Language Interpreter will recreate #\n" +
                                     "// # it with the Default values.                   #\n" +
                                     "// #################################################\n" +
                                     "// File Created at:" + DateTime.Now.ToShortDateString() + " | In:" + DateTime.Now.ToShortTimeString() + ".\n" + 
                                     "ScriptOptimizationCache:True";


                File.WriteAllText(Environment.CurrentDirectory + Registry.ReadKeyValue("TAIYOU_OPTIONS/OptionsFile"),FileContent);

                // Set the Default Parameters
                Global.CreateScriptOptimizationCache = true;

                Console.WriteLine("ReadTaiyouConfigFile : Default parameters has been defined.");

            }

            Console.WriteLine("ReadTaiyouConfigFile : End\n\n");
        }

        private static void ListTaiyouSCRIPTS()
        {
            Console.WriteLine("ListTaiyouScripts : Initialize");
           
            string[] AllTIYScripts = Directory.GetFiles(Global.ContentFolder + Registry.ReadKeyValue("ENGINE/GAMES_VALIDATION/ScriptsDir"), "*" + Registry.ReadKeyValue("FILE_EXTENSIONS/Taiyou"), SearchOption.AllDirectories);


             foreach (var file in AllTIYScripts){
             FileInfo info = new FileInfo(file);
                // Do something with the Folder or just add them to a list via nameoflist.add();
                string ScriptNameWitoutDir = info.FullName.Replace(Global.ContentFolder + Registry.ReadKeyValue("ENGINE/GAMES_VALIDATION/ScriptsDir"),"");
                string ScriptCorrectName = info.FullName.Replace(Global.ContentFolder + Registry.ReadKeyValue("ENGINE/GAMES_VALIDATION/ScriptsDir"), "").Replace("/", ".").Replace(Registry.ReadKeyValue("FILE_EXTENSIONS/Taiyou"),"");

                AllTIYScriptOnScriptFolder.Add(ScriptNameWitoutDir);
                CustomTaiyouScriptsName.Add(ScriptCorrectName);
                Console.WriteLine("Found Script: " + ScriptCorrectName);


            }
            
           Console.WriteLine("ListTaiyouScripts : Ready!");
          
        }

        static bool TaiyouDictionaryInitialized = false;
        public static List<string> TaiyouDictionary_FullCmd = new List<string>();
        public static List<string> TaiyouDictionary_TGEUCCmd = new List<string>();
        public static List<string> TaiyouDictionary_VarTypeFull = new List<string>();
        public static List<string> TaiyouDictionary_VarTypeTGEUC = new List<string>();


        // Dictionary File Backup
        /*
            List<string> FullComma = new List<string>() { "Clear", "Call","Write","WriteLine","WriteFile","IF",
                                                          "Abort", "Declare","WriteVar","MathOp","Goto","FileExists",
                                                          "ReadFile","DirectoryExists","DownloadServerString","CopyFile",
                                                          "MoveFile","DeleteFile","AddRenderQuee","AddEvent","CheckEvent",
                                                          "ChangeWindowProp","Colision","Reload","GetPressedKey","AddRenderTextQuee",
                                                          "ChangeRenderProp","ChangeBackgroundColor","Undeclare","SendBGMCommand",
                                                          "MasterVolume","LanguageSystem" };
            List<string> EncurtedComma = new List<string>() { "0x0", "0x1", "0x2","0x3","0x4","0x5","0x6","0x7","0x8","0x9","1x0","1x1",
                                                              "1x2", "1x3", "1x4", "1x5","1x6","1x7", "1x8","1x9","2x0","2x1",
                                                              "2x2","2x3","2x4","2x5","2x6","2x7","2x8","2x9","3x0","3x1" };

        */


        private static void ReadTaiyouDictionaryFile()
        {
            string TaiyouDictionaryFileLocation = Environment.CurrentDirectory + Registry.ReadKeyValue("TAIYOU_OPTIONS/DictionaryFile");
            var lines2 = File.ReadLines(TaiyouDictionaryFileLocation);
            foreach (var line in lines2)
            {
                bool IsLineValid = true;

                if (line.StartsWith("//", StringComparison.CurrentCulture))
                {
                    IsLineValid = false;

                    Console.WriteLine("TranslateTaiyouScript : ReadDictionaryFile;Commentary Line Detected.");

                }

                if (IsLineValid)
                {
                    string[] SplitedParameters = line.Split(':');
                    bool IsLineCorrect = true;
                    if (SplitedParameters.Length < 2)
                    {
                        IsLineCorrect = false;
                    }

                    if (IsLineCorrect)
                    {
                        TaiyouDictionary_FullCmd.Add(SplitedParameters[0]);
                        TaiyouDictionary_TGEUCCmd.Add(SplitedParameters[1]);

                        Console.WriteLine("Command:" + SplitedParameters[0] + ",TGEUC: " + SplitedParameters[1]);

                    }


                }

            }

        }

        private static void ReadTaiyouVariablesDictionaryFile()
        {
            string TaiyouDictionaryFileLocation = Environment.CurrentDirectory + Registry.ReadKeyValue("TAIYOU_OPTIONS/VariablesDictionaryFile");
            var lines2 = File.ReadLines(TaiyouDictionaryFileLocation);
            foreach (var line in lines2)
            {
                bool IsLineValid = true;

                if (line.StartsWith("//", StringComparison.CurrentCulture))
                {
                    IsLineValid = false;

                    Console.WriteLine("TranslateTaiyouScript : ReadVariableDictionaryFile;Commentary Line Detected.");

                }

                if (IsLineValid)
                {
                    string[] SplitedParameters = line.Split(':');
                    bool IsLineCorrect = true;
                    if (SplitedParameters.Length < 2)
                    {
                        IsLineCorrect = false;
                    }

                    if (IsLineCorrect)
                    {
                        TaiyouDictionary_VarTypeFull.Add(SplitedParameters[0]);
                        TaiyouDictionary_VarTypeTGEUC.Add(SplitedParameters[1]);

                        Console.WriteLine("Command:" + SplitedParameters[0] + ",TGEUC: " + SplitedParameters[1]);

                    }


                }

            }

        }

        public static string TranslateTaiyouScript(string TaiyouScriptData, string TaiyouScriptName)
        {
            // Read the Taiyou Dictionary File
            if (!TaiyouDictionaryInitialized)
            {
                Console.WriteLine("\n\nTranslateTaiyouScript : Reading Taiyou Dictionary File...");
                ReadTaiyouDictionaryFile();
                ReadTaiyouVariablesDictionaryFile();
                Console.WriteLine("TranslateTaiyouScript : ReadDictionaryFile; End");


                TaiyouDictionaryInitialized = true;

            }

            Console.WriteLine("\n\n\nTranslateTaiyouScript : Translate Script;" + TaiyouScriptName);

            // Optimization Variables
            string TemporaryScriptsDataDir = Environment.CurrentDirectory + Registry.ReadKeyValue("TAIYOU_OPTIONS/ScriptOptimizationDir") + Global.CurrentSelectedTitleName + "/" + Global.CurrentSelectedTitleID + "/" + Global.CurrentSelectedTitleVersion + "/";
            string TemporaryScriptsFileName = TemporaryScriptsDataDir + TaiyouScriptName + Registry.ReadKeyValue("FILE_EXTENSIONS/NotOptimizedTaiyouScript");
            string OptimizedCode = "";
            string IfCommas = "";
            int IfMode = 0;

            // Directorys
            Directory.CreateDirectory(TemporaryScriptsDataDir);
            File.WriteAllText(TemporaryScriptsFileName, TaiyouScriptData); // Write the Temporary Taiyou File

            var lines = File.ReadLines(TemporaryScriptsFileName);
            foreach (var line in lines)
            {
                string[] SplitedEachCommand = line.Split(' ');
                bool IsLineValid = true;
                bool IgnoreLine = false;
                bool IsIfLine = false;

                if (SplitedEachCommand[0] == "") { IsLineValid = false; }
                if (SplitedEachCommand[0].StartsWith("//", StringComparison.CurrentCulture)) { IsLineValid = false; }
                if (SplitedEachCommand[0].StartsWith("#", StringComparison.CurrentCulture)) { IgnoreLine = true; }
                if (SplitedEachCommand[0].StartsWith("@", StringComparison.CurrentCulture)) { IsIfLine = true; }

                if (IsLineValid && IgnoreLine == false && IsIfLine == false) 
                {
                    int EncurtedCommaIndex = TaiyouDictionary_FullCmd.IndexOf(SplitedEachCommand[0]);
                    bool IsCommaValid = true;
                    if (EncurtedCommaIndex == -1) { IsCommaValid = false; }

                    if (IsCommaValid)
                    {
                        string AllLine = "";
                        for (int i = 1; i < SplitedEachCommand.Length; i++)
                        {
                            int EncurtedCommaIndexInsideComma = TaiyouDictionary_FullCmd.IndexOf(SplitedEachCommand[i]);
                            if (EncurtedCommaIndexInsideComma != -1) { SplitedEachCommand[i] = TaiyouDictionary_TGEUCCmd[EncurtedCommaIndexInsideComma]; }

                            AllLine += " " + SplitedEachCommand[i];
         
                        }

                        OptimizedCode += "\n" + TaiyouDictionary_TGEUCCmd[EncurtedCommaIndex] + AllLine;

                    }
                    else
                    {
                        OptimizedCode += "\n" + TaiyouDictionary_TGEUCCmd[TaiyouDictionary_FullCmd.IndexOf("WriteLine")] + " ERROR: Command[" + SplitedEachCommand[0] + "] does not exist.";
                    }


                }
                if (IgnoreLine && IsLineValid) // Regions Line has to be ignored
                {
                    string AllLine = "";
                    for (int i = 0; i < SplitedEachCommand.Length; i++)
                    {
                        if (i > 0)
                        {
                            AllLine += " " + SplitedEachCommand[i];
                        }
                        else
                        {
                            AllLine += SplitedEachCommand[i];
                        }

                    }


                    OptimizedCode += "\n" + AllLine;
                }if (IsIfLine && IsLineValid)
                {
                    for (int i = 0; i < SplitedEachCommand.Length; i++)
                    {
                        if (IfMode == 0)
                        {
                            if (SplitedEachCommand[i] == "@IF")
                            {
                                IfCommas += TaiyouDictionary_TGEUCCmd[TaiyouDictionary_FullCmd.IndexOf("IF")] + " ";

                            }if(SplitedEachCommand[i] != "@THEN")
                            {
                                IfCommas += SplitedEachCommand[i] + " ";

                            }if (SplitedEachCommand[i] == "@THEN")
                            {
                                IfMode += 1;
                            }
                            IfCommas = IfCommas.Replace("@IF ", "");

                        }if (IfMode == 1)
                        {
                            if (SplitedEachCommand[i] != "@END")
                            {
                                if (SplitedEachCommand[i].StartsWith("@", StringComparison.CurrentCulture))
                                {
                                    if (SplitedEachCommand[i] != "@THEN")
                                    {
                                        string CorrectCMD = SplitedEachCommand[i].Replace("@", "");
                                        bool IsCommaValid = true;
                                        int ThisCommand = TaiyouDictionary_FullCmd.IndexOf(CorrectCMD);
                                        if (ThisCommand == -1) { IsCommaValid = false; }

                                        if (IsCommaValid)
                                        {
                                            IfCommas += TaiyouDictionary_TGEUCCmd[ThisCommand];

                                        }
                                        else
                                        {
                                            OptimizedCode += "\n" + TaiyouDictionary_TGEUCCmd[TaiyouDictionary_FullCmd.IndexOf("WriteLine")] + " ERROR: Command[" + CorrectCMD + "] is invalid.";

                                        }

                                    }

                                }else if (SplitedEachCommand[i].EndsWith(";", StringComparison.CurrentCulture))
                                {
                                    IfCommas += " " + SplitedEachCommand[i].Replace(";","") + "|";
                                }
                                else
                                {
                                    IfCommas += " " + SplitedEachCommand[i];
                                }

                            }
                            else
                            {
                                OptimizedCode += "\n" + IfCommas;
                                IfCommas = "";
                                IfMode = 0;

                            }

                        }

                    }
                }

                string[] VarsLine = line.Split(' ');
                for (int i = 0; i < VarsLine.Length; i++)
                {
                    Console.WriteLine("ReplaceVarCode : " + VarsLine[i]);

                    int ProbalyTheIndex = TaiyouDictionary_VarTypeFull.IndexOf(VarsLine[i]);

                    if (ProbalyTheIndex == -1)
                    {
                        Console.WriteLine("ReplaceVarCode : No valid codes detected.");
                    }
                    else
                    {
                        string CorrectVarCode = TaiyouDictionary_VarTypeTGEUC[ProbalyTheIndex];
                        Console.WriteLine("ReplaceVarCode : " + CorrectVarCode);


                        OptimizedCode = OptimizedCode.Replace(VarsLine[i], CorrectVarCode);

                    }

                    

                }
        
            }// Script Optimization End

            Console.WriteLine("TranslateTaiyouScript : Code Translation Cache is setted to:" + Global.CreateScriptOptimizationCache);


            if (Global.CreateScriptOptimizationCache)
            {
                Console.WriteLine("TranslateTaiyouScript : Creating TGEUC Output File...");

                File.WriteAllText(TemporaryScriptsDataDir + TaiyouScriptName + Registry.ReadKeyValue("FILE_EXTENSIONS/TaiyouGameEngineUpCodes"), OptimizedCode);

                Console.WriteLine("TranslateTaiyouScript : TGEUC file created.");
            }
            else
            {
                Console.WriteLine("TranslateTaiyouScript : Delete Script Translation Cache...");
                Directory.Delete(TemporaryScriptsDataDir, true);

            }

            Console.WriteLine("TranslateTaiyouScript : End");




            return OptimizedCode;
        }




        // Taiyou Scripts Lists
        public static List<string> AllTIYScriptOnScriptFolder = new List<string>();
        public static List<string> CustomTaiyouScriptsName = new List<string>();
        public static List<string> CustomTaiyouScriptsDescription = new List<string>();
        public static List<string> CustomTaiyouScriptsFile = new List<string>();

        // String Vars
        public static List<string> GlobalVars_String_Names = new List<string>();
        public static List<string> GlobalVars_String_Content = new List<string>();

        // Integer Vars
        public static List<string> GlobalVars_Int_Names = new List<string>();
        public static List<int> GlobalVars_Int_Content = new List<int>();

        // Boolean Vars
        public static List<string> GlobalVars_Bool_Names = new List<string>();
        public static List<bool> GlobalVars_Bool_Content = new List<bool>();

        // Color Vars
        public static List<string> GlobalVars_Color_Names = new List<string>();
        public static List<Color> GlobalVars_Color_Content = new List<Color>();

        // Rectangle Vars
        public static List<string> GlobalVars_Rectangle_Names = new List<string>();
        public static List<Rectangle> GlobalVars_Rectangle_Content = new List<Rectangle>();

        // Float Vars
        public static List<string> GlobalVars_Float_Names = new List<string>();
        public static List<float> GlobalVars_Float_Content = new List<float>();


        ///////////////////
        //   List Vars   //
        ///////////////////

        // String List Vars
        public static List<string> GlobalVars_StringList_Names = new List<string>();
        public static List<List<string>> GlobalVars_StringList_Content = new List<List<string>>();

        // Integer List Vars
        public static List<string> GlobalVars_IntList_Names = new List<string>();
        public static List<List<int>> GlobalVars_IntList_Content = new List<List<int>>();

        // Boolean List Vars
        public static List<string> GlobalVars_BooleanList_Names = new List<string>();
        public static List<List<bool>> GlobalVars_BooleanList_Content = new List<List<bool>>();

        // Color List Vars
        public static List<string> GlobalVars_ColorList_Names = new List<string>();
        public static List<List<Color>> GlobalVars_ColorList_Content = new List<List<Color>>();

        // Rectangle List Vars
        public static List<string> GlobalVars_RectangleList_Names = new List<string>();
        public static List<List<Rectangle>> GlobalVars_RectangleList_Content = new List<List<Rectangle>>();

        // Float List Vars
        public static List<string> GlobalVars_FloatList_Names = new List<string>();
        public static List<List<float>> GlobalVars_FloatList_Content = new List<List<float>>();



        private static void LoadDefaultVars()
        {
            ReadAsync("WriteLine TAIYOU : Declaring default vars...");
            int DeclareTGEUCIndex = TaiyouDictionary_FullCmd.IndexOf("Declare");
            if (DeclareTGEUCIndex == -1) { throw new Exception("The taiyou dictionary is missing the command: Declare."); }
            string DeclareTGUC = TaiyouDictionary_TGEUCCmd[DeclareTGEUCIndex];

            string StringVarTGEUC = TaiyouDictionary_VarTypeTGEUC[TaiyouDictionary_VarTypeFull.IndexOf("!STRING")];
            string BoolVarTGEUC = TaiyouDictionary_VarTypeTGEUC[TaiyouDictionary_VarTypeFull.IndexOf("!BOOL")];
            string IntVarTGEUC = TaiyouDictionary_VarTypeTGEUC[TaiyouDictionary_VarTypeFull.IndexOf("!INT")];
            string FloatVarTGEUC = TaiyouDictionary_VarTypeTGEUC[TaiyouDictionary_VarTypeFull.IndexOf("!FLOAT")];

            // Enviroment Variables
            ReadAsync(DeclareTGUC + " " + StringVarTGEUC + " ENVIROMENT_USERNAME " + Environment.UserName);
            ReadAsync(DeclareTGUC + " " + StringVarTGEUC + " ENVIROMENT_USERDOMAIN_NAME " + Environment.UserDomainName);
            ReadAsync(DeclareTGUC + " " + StringVarTGEUC + " ENVIROMENT_OSPLATFORM " + Environment.OSVersion.Platform);
            ReadAsync(DeclareTGUC + " " + StringVarTGEUC + " ENVIROMENT_OSVERSION " + Environment.OSVersion.Version);
            ReadAsync(DeclareTGUC + " " + StringVarTGEUC + " ENVIROMENT_OSSERVICEPACK " + Environment.OSVersion.ServicePack);
            ReadAsync(DeclareTGUC + " " + BoolVarTGEUC + " ENVIROMENT_IS64BITS " + Environment.Is64BitProcess);
            ReadAsync(DeclareTGUC + " " + StringVarTGEUC + " ENVIROMENT_WORKINGSET " + Environment.WorkingSet);
            ReadAsync(DeclareTGUC + " " + StringVarTGEUC + " ENVIROMENT_DIR " + Global.ContentFolder);
            ReadAsync(DeclareTGUC + " " + StringVarTGEUC + " ENVIROMENT_CONTENT_DIR " + Global.ContentFolder + "");
            ReadAsync(DeclareTGUC + " " + StringVarTGEUC + " ENVIROMENT_MACHINE_NAME " + Environment.MachineName);
            ReadAsync(DeclareTGUC + " " + StringVarTGEUC + " ENVIROMENT_SYSTEM_PATH " + Environment.SystemDirectory);
            ReadAsync(DeclareTGUC + " " + IntVarTGEUC + " WINDOW_WIDTH " + WindowManager.WindowW);
            ReadAsync(DeclareTGUC + " " + IntVarTGEUC + " WINDOW_HEIGHT " + WindowManager.WindowH);
            ReadAsync(DeclareTGUC + " " + BoolVarTGEUC + " DEBUG_MODE " + Global.Engine_DebugRender);

            // Cursor Vars
            ReadAsync(DeclareTGUC + " " + IntVarTGEUC + " CURSOR_X " + UserInput.Cursor.Cursor_X);
            ReadAsync(DeclareTGUC + " " + IntVarTGEUC + " CURSOR_Y " + UserInput.Cursor.Cursor_Y);
            ReadAsync(DeclareTGUC + " " + IntVarTGEUC + " CURSOR_LEFT_DOWN_X " + UserInput.Cursor.Left_Cursor_ClickDown.X);
            ReadAsync(DeclareTGUC + " " + IntVarTGEUC + " CURSOR_LEFT_DOWN_Y " + UserInput.Cursor.Left_Cursor_ClickDown.Y);
            ReadAsync(DeclareTGUC + " " + IntVarTGEUC + " CURSOR_LEFT_UP_X " + UserInput.Cursor.Left_Cursor_ClickUp.X);
            ReadAsync(DeclareTGUC + " " + IntVarTGEUC + " CURSOR_LEFT_UP_Y " + UserInput.Cursor.Left_Cursor_ClickUp.Y);
            ReadAsync(DeclareTGUC + " " + IntVarTGEUC + " CURSOR_RIGHT_DOWN_X " + UserInput.Cursor.Right_Cursor_ClickDown.X);
            ReadAsync(DeclareTGUC + " " + IntVarTGEUC + " CURSOR_RIGHT_DOWN_Y " + UserInput.Cursor.Right_Cursor_ClickDown.Y);
            ReadAsync(DeclareTGUC + " " + IntVarTGEUC + " CURSOR_RIGHT_UP_X " + UserInput.Cursor.Right_Cursor_ClickUp.X);
            ReadAsync(DeclareTGUC + " " + IntVarTGEUC + " CURSOR_RIGHT_UP_Y " + UserInput.Cursor.Right_Cursor_ClickUp.Y);

            // FPS values
            ReadAsync(DeclareTGUC + " " + IntVarTGEUC + " FPS_INT " + Global.GameFPSint);
            ReadAsync(DeclareTGUC + " " + FloatVarTGEUC + " FPS_RAW " + Global.GameFPSraw);
            ReadAsync(DeclareTGUC + " " + StringVarTGEUC + " FPS_STRING " + Global.GameFPSstring);

            // User variables
            ReadAsync(DeclareTGUC + " " + StringVarTGEUC + " USER_NAME " + Global.CurrentLoggedUser);


            ReadAsync("WriteLine TAIYOU : Default Vars Declared.");

        }

        public static void UpdateGlobalVars()
        {
            // Window Variables
            WriteToIntVar("WINDOW_WIDTH", WindowManager.WindowW);
            WriteToIntVar("WINDOW_HEIGHT", WindowManager.WindowH);


            // Write the Cursor Vars
            WriteToIntVar("CURSOR_X", UserInput.Cursor.Cursor_X);
            WriteToIntVar("CURSOR_Y", UserInput.Cursor.Cursor_Y);


            // Cursor Left Up/Down
            WriteToIntVar("CURSOR_LEFT_DOWN_X", UserInput.Cursor.Left_Cursor_ClickDown.X);
            WriteToIntVar("CURSOR_LEFT_DOWN_Y", UserInput.Cursor.Left_Cursor_ClickDown.Y);
            WriteToIntVar("CURSOR_LEFT_UP_X", UserInput.Cursor.Left_Cursor_ClickUp.X);
            WriteToIntVar("CURSOR_LEFT_UP_Y", UserInput.Cursor.Left_Cursor_ClickUp.Y);

            // Cursor Right Up/Down
            WriteToIntVar("CURSOR_RIGHT_DOWN_X", UserInput.Cursor.Right_Cursor_ClickDown.X);
            WriteToIntVar("CURSOR_RIGHT_DOWN_Y", UserInput.Cursor.Right_Cursor_ClickDown.Y);
            WriteToIntVar("CURSOR_RIGHT_UP_X", UserInput.Cursor.Right_Cursor_ClickUp.X);
            WriteToIntVar("CURSOR_RIGHT_UP_Y", UserInput.Cursor.Right_Cursor_ClickUp.Y);

            // Update the FPS Vars
            WriteToIntVar("FPS_INT", Global.GameFPSint);
            WriteToFloatVar("FPS_RAW", Global.GameFPSraw);
            WriteToStringVar("FPS_STRING", Global.GameFPSstring);


        }


        private static void WriteToStringVar(string VarName, string NewValue)
        {
            int NewVarID = GlobalVars_String_Names.IndexOf(VarName);

            GlobalVars_String_Content[NewVarID] = NewValue;

        }


        private static void WriteToFloatVar(string VarName, float NewValue)
        {
            int NewVarID = GlobalVars_Float_Names.IndexOf(VarName);

            GlobalVars_Float_Content[NewVarID] = NewValue;

        }

        private static void WriteToIntVar(string VarName, int NewValue)
        {
            int NewVarID = GlobalVars_Int_Names.IndexOf(VarName);

            GlobalVars_Int_Content[NewVarID] = NewValue;

        }

        private static bool ReturnBooleanVarValue(string VarName)
        {
            bool ValToReturn = false;

            var VarNameIndex = GlobalVars_Bool_Names.IndexOf(VarName);
            ValToReturn = GlobalVars_Bool_Content[VarNameIndex];

            return ValToReturn;
        }

        private static int ReturnIntVarValue(string VarName)
        {
            int ValToReturn = 0;

            var VarNameIndex = GlobalVars_Int_Names.IndexOf(VarName);
            ValToReturn = GlobalVars_Int_Content[VarNameIndex];

            return ValToReturn;
        }




        /// <summary>
        /// Read the specified Command.
        /// </summary>
        /// <param name="Command">Command.</param>
        public static string[] SplitedString; // The Splited String
        public static void ReadAsync(string Command)
        {
            SplitedString = Command.Split(' '); // The Splited String

            // Format the current Taiyou Line
            for (int i = 0; i < SplitedString.Length; i++)
            {

                // FORMATATION
                SplitedString[i] = SplitedString[i].Replace("%N", Environment.NewLine); // New Line

                for (int i2 = 0; i2 < GlobalVars_String_Names.Count; i2++)
                {
                    SplitedString[i] = SplitedString[i].Replace("$STRING_" + GlobalVars_String_Names[i2] + "$", GlobalVars_String_Content[i2].Replace(" ", ""));
               
                }
                for (int i2 = 0; i2 < GlobalVars_Bool_Names.Count; i2++)
                {
                    SplitedString[i] = SplitedString[i].Replace("$BOOL_" + GlobalVars_Bool_Names[i2] + "$", Convert.ToString(GlobalVars_Bool_Content[i2]));

                }
                for (int i2 = 0; i2 < GlobalVars_Int_Names.Count; i2++)
                {
                    SplitedString[i] = SplitedString[i].Replace("$INT_" + GlobalVars_Int_Names[i2] + "$", Convert.ToString(GlobalVars_Int_Content[i2]));

                }
                for (int i2 = 0; i2 < GlobalVars_Float_Names.Count; i2++)
                {
                    SplitedString[i] = SplitedString[i].Replace("$FLOAT_" + GlobalVars_Float_Names[i2] + "$", Convert.ToString(GlobalVars_Float_Content[i2]));

                }




                if (SplitedString[i].Contains("%RANDOM%"))
                {
                    string[] SubSplitedString = SplitedString[i].Split('%');
                    string Arg1 = SubSplitedString[2]; // Number 1
                    string Arg2 = SubSplitedString[3]; // Number 2
                    Random RND = new Random();

                    SplitedString[i] = SplitedString[i].Replace("%RANDOM%" + Arg1 + "%" + Arg2 + "%", Convert.ToString(RND.Next(Convert.ToInt32(Arg1),Convert.ToInt32(Arg2))));

                }

                if (SplitedString[i].Contains("%ADD%"))
                {
                    string[] SubSplitedString = SplitedString[i].Split('%');

                    string Arg1 = SubSplitedString[2]; // Number 1
                    string Arg2 = SubSplitedString[3]; // Number 2
                    int MathResult = Convert.ToInt32(Arg1) + Convert.ToInt32(Arg2);

                    SplitedString[i] = SplitedString[i].Replace("%ADD%" + Arg1 + "%" + Arg2 + "%", Convert.ToString(MathResult));

                }

                if (SplitedString[i].Contains("%DECREASE%"))
                {
                    string[] SubSplitedString = SplitedString[i].Split('%');
                    string Arg1 = SubSplitedString[2]; // Number 1
                    string Arg2 = SubSplitedString[3]; // Number 2
                    int MathResult = Convert.ToInt32(Arg1) - Convert.ToInt32(Arg2);

                    SplitedString[i] = SplitedString[i].Replace("%DECREASE%" + Arg1 + "%" + Arg2 + "%", Convert.ToString(MathResult));

                }

                if (SplitedString[i].Contains("%MULTIPLY%"))
                {
                    string[] SubSplitedString = SplitedString[i].Split('%');
                    string Arg1 = SubSplitedString[2]; // Number 1
                    string Arg2 = SubSplitedString[3]; // MultiplyTimes
                    int MathResult = Convert.ToInt32(Arg1) * Convert.ToInt32(Arg2);

                    SplitedString[i] = SplitedString[i].Replace("%MULTIPLY%" + Arg1 + "%" + Arg2 + "%", Convert.ToString(MathResult));

                }

                if (SplitedString[i].Contains("%DIVIDE%"))
                {
                    string[] SubSplitedString = SplitedString[i].Split('%');
                    string Arg1 = SubSplitedString[2]; // Number 1
                    string Arg2 = SubSplitedString[3]; // Number 2
                    int MathResult = Convert.ToInt32(Arg1) / Convert.ToInt32(Arg2);

                    SplitedString[i] = SplitedString[i].Replace("%DIVIDE%" + Arg1 + "%" + Arg2 + "%", Convert.ToString(MathResult));

                }

                if (SplitedString[i].Contains("%DIFERENCE%"))
                {
                    string[] SubSplitedString = SplitedString[i].Split('%');
                    string Arg1 = SubSplitedString[2]; // Number 1
                    string Arg2 = SubSplitedString[3]; // Number 2
                    int MathResult = Math.Abs(Convert.ToInt32(Arg1) - Convert.ToInt32(Arg2));


                    SplitedString[i] = SplitedString[i].Replace("%DIFERENCE%" + Arg1 + "%" + Arg2 + "%", Convert.ToString(MathResult));

                }

                if (SplitedString[i].Contains("%PERCENTAGE%"))
                {
                    string[] SubSplitedString = SplitedString[i].Split('%');
                    string Arg1 = SubSplitedString[2]; // Number 1
                    string Arg2 = SubSplitedString[3]; // Number 2
                    int MathResult = (int)Math.Round((double)(100 * Convert.ToInt32(Arg1)) / Convert.ToInt32(Arg2));


                    SplitedString[i] = SplitedString[i].Replace("%PERCENTAGE%" + Arg1 + "%" + Arg2 + "%", Convert.ToString(MathResult));

                }

                if (SplitedString[i].Contains("%LOCATION_OF%"))
                {
                    string[] SubSplitedString = SplitedString[i].Split('%');
                    string Arg1 = SubSplitedString[2]; // Render Type
                    string Arg2 = SubSplitedString[3]; // Render Name
                    string Arg3 =  SubSplitedString[4]; // Value Type
                    Rectangle RectObject = GlobalVars_Rectangle_Content[RenderQuee.Main.RenderCommand_RectangleVar.IndexOf(Arg2)];

                    int RenderNameIndex = -1;
                    if (Arg1 == "SPRITE") { RenderNameIndex = RenderQuee.Main.RenderCommand_Name.IndexOf(Arg2); };
                    if (Arg1 == "TEXT") { RenderNameIndex = RenderQuee.Main.TextRenderCommand_Name.IndexOf(Arg2); };
                    int ValToReturn = 0;
                    if (Arg3 == "X" && Arg1 == "SPRITE") { ValToReturn = RectObject.X; };
                    if (Arg3 == "X" && Arg1 == "TEXT") { ValToReturn = RenderQuee.Main.TextRenderCommand_X[RenderNameIndex]; }

                    if (Arg3 == "Y" && Arg1 == "SPRITE") { ValToReturn = RectObject.Y; };
                    if (Arg3 == "Y" && Arg1 == "TEXT") { ValToReturn = RenderQuee.Main.TextRenderCommand_Y[RenderNameIndex]; };

                    if (Arg3 == "W" && Arg1 == "SPRITE") { ValToReturn = RectObject.Width; };
                    if (Arg3 == "H" && Arg1 == "SPRITE") { ValToReturn = RectObject.Height; };


                    SplitedString[i] = SplitedString[i].Replace("%LOCATION_OF%" + Arg1 + "%" + Arg2 + "%" + Arg3 + "%", Convert.ToString(ValToReturn));

                }

                if (SplitedString[i].Contains("%COLOR_VALUE%"))
                {
                    string[] SubSplitedString = SplitedString[i].Split('%');
                    string Arg1 = SubSplitedString[2]; // ColorVarName
                    string Arg2 = SubSplitedString[3]; // CodeName
                    int ColorVarIndex = GlobalVars_Color_Names.IndexOf(Arg1);
                    string ValToReturn = "0";
                    if (ColorVarIndex == -1) { throw new Exception("Color Variable [" + Arg1 + "] does not exist."); }

                    if (Arg2.Equals("R")) { ValToReturn = Convert.ToString(GlobalVars_Color_Content[ColorVarIndex].R); };
                    if (Arg2.Equals("G")) { ValToReturn = Convert.ToString(GlobalVars_Color_Content[ColorVarIndex].G); };
                    if (Arg2.Equals("B")) { ValToReturn = Convert.ToString(GlobalVars_Color_Content[ColorVarIndex].B); };
                    if (Arg2.Equals("A")) { ValToReturn = Convert.ToString(GlobalVars_Color_Content[ColorVarIndex].A); };
                    if (Arg2.Equals("ALL")) { ValToReturn = GlobalVars_Color_Content[ColorVarIndex].R + "," + GlobalVars_Color_Content[ColorVarIndex].G + "," + GlobalVars_Color_Content[ColorVarIndex].B + "," + GlobalVars_Color_Content[ColorVarIndex].A; };


                    SplitedString[i] = SplitedString[i].Replace("%COLOR_VALUE%" + Arg1 + "%" + Arg2 + "%", Convert.ToString(ValToReturn));

                }


                if (SplitedString[i].Contains("%LIST_VALUE%"))
                {
                    string[] SubSplitedString = SplitedString[i].Split('%');
                    string ValToReturn = "null_or_incorrect";
                    string Arg1 = SubSplitedString[2]; // ListType
                    string Arg2 = SubSplitedString[3]; // ListName
                    string Arg3 = SubSplitedString[4]; // Index

                    if (Arg1.Equals("STRING"))
                    {
                        int ListNameIndex = GlobalVars_StringList_Names.IndexOf(Arg2);
                        int Index = Convert.ToInt32(Arg3);

                        ValToReturn = GlobalVars_StringList_Content[ListNameIndex][Index];

                    }

                    if (Arg1.Equals("INT"))
                    {
                        int ListNameIndex = GlobalVars_IntList_Names.IndexOf(Arg2);
                        int Index = Convert.ToInt32(Arg3);

                        ValToReturn = Convert.ToString(GlobalVars_IntList_Content[ListNameIndex][Index]);
                    }

                    if (Arg1.Equals("COLOR"))
                    {
                        int ListNameIndex = GlobalVars_ColorList_Names.IndexOf(Arg2);
                        int Index = Convert.ToInt32(Arg3);

                        Color ColorGetted = GlobalVars_ColorList_Content[ListNameIndex][Index];
                        string ColorCodeToReturn = ColorGetted.R + "," + ColorGetted.G + "," + ColorGetted.B + "," + ColorGetted.A;

                        ValToReturn = ColorCodeToReturn;
                    }

                    if (Arg1.Equals("FLOAT"))
                    {
                        int ListNameIndex = GlobalVars_FloatList_Names.IndexOf(Arg2);
                        int Index = Convert.ToInt32(Arg3);

                        ValToReturn = Convert.ToString(GlobalVars_FloatList_Content[ListNameIndex][Index]);

                    }

                    if (Arg1.Equals("RECTANGLE"))
                    {
                        int ListNameIndex = GlobalVars_RectangleList_Names.IndexOf(Arg2);
                        int Index = Convert.ToInt32(Arg3);

                        Rectangle RectGetted = GlobalVars_RectangleList_Content[ListNameIndex][Index];
                        string RectangleCode = RectGetted.X + "," + RectGetted.Y + "," + RectGetted.Width + "," + RectGetted.Height;

                        ValToReturn = Convert.ToString(RectangleCode);

                    }


                    SplitedString[i] = SplitedString[i].Replace("%LIST_VALUE%" + Arg1 + "%" + Arg2 + "%" + Arg3 + "%", Convert.ToString(ValToReturn));

                }


            }


            // Begin Command Interpretation
            if (SplitedString[0].Equals("0x0"))
            {
                Clear.Initialize();

            }
            if (SplitedString[0].Equals("0x1"))
            {
                Call.Initialize(SplitedString[1]);

            }
            if (SplitedString[0].Equals("0x2"))
            {
                Write.Initialize(SplitedString[1]);


            }
            if (SplitedString[0].Equals("0x3"))
            {
                WriteLine.Initialize(SplitedString[1]);


            }
            if (SplitedString[0].Equals("0x4"))
            {
                WriteFile.Initialize(SplitedString[1], SplitedString[2]);


            }
            if (SplitedString[0].Equals("0x5"))
            {

                TaiyouIF.Initialize(SplitedString);

            }
            if (SplitedString[0].Equals("0x6"))
            {
                Abort.Initialize();

            }
            if (SplitedString[0].Equals("0x7"))
            {
                Declare.Initialize(SplitedString);


            }
            if (SplitedString[0].Equals("0x8"))
            {
                WriteVar.Initialize(SplitedString);


            }
            if (SplitedString[0].Equals("0x9"))
            {
                MathOP.Intialize(SplitedString);


            }
            if (SplitedString[0].Equals("1x0"))
            {
                Goto.Initialize(SplitedString);


            }
            if (SplitedString[0].Equals("1x1"))
            {
                FileExists.Initialize(SplitedString);


            }
            if (SplitedString[0].Equals("1x2"))
            {
                ReadFile.Intialize(SplitedString);

            }
            if (SplitedString[0].Equals("1x3"))
            {
                DirectoryExists.Initialize(SplitedString);

            }
            if (SplitedString[0].Equals("1x4"))
            {
                DownloadServerString.Initialize(SplitedString);

            }
            if (SplitedString[0].Equals("1x5"))
            {
                CopyFile.Initialize(SplitedString);

            }
            if (SplitedString[0].Equals("1x6"))
            {
                MoveFile.Initialize(SplitedString);

            }
            if (SplitedString[0].Equals("1x7"))
            {
                DeleteFile.Initialize(SplitedString);

            }
            if (SplitedString[0].Equals("1x8"))
            {
                AddRenderQuee.Initialize(SplitedString);


            }
            if (SplitedString[0].Equals("1x9"))
            {
                AddEvent.Initialize(SplitedString);


            }
            if (SplitedString[0].Equals("2x0"))
            {
                CheckEvent.Initialize(SplitedString);


            }
            if (SplitedString[0].Equals("2x1"))
            {
                ChangeWindowPropertie.Initialize(SplitedString);


            }
            if (SplitedString[0].Equals("2x2"))
            {
                Colision.Initialize(SplitedString);


            }
            if (SplitedString[0].Equals("2x3"))
            {
                Reload.Initialize(SplitedString);


            }
            if (SplitedString[0].Equals("2x4"))
            {
                GetKeyPressed.Initialize(SplitedString);


            }
            if (SplitedString[0].Equals("2x5"))
            {
                AddRenderTextQuee.Initialize(SplitedString);


            }
            if (SplitedString[0].Equals("2x6"))
            {
                ChangeRenderProp.Initialize(SplitedString);


            }

            if (SplitedString[0].Equals("2x7"))
            {
                ChangeBackgroundColor.Initialize(SplitedString);


            }

            if (SplitedString[0].Equals("2x8"))
            {
                Undeclare.Initialize(SplitedString);

            }

            if (SplitedString[0].Equals("2x9"))
            {
                SendBGMCommand.Initialize(SplitedString);
            }

            if (SplitedString[0].Equals("3x0"))
            {
                MasterVolume.Initialize(SplitedString);
            }

            if (SplitedString[0].Equals("3x1"))
            {
                LanguageSystemManager.Initialize(SplitedString);
            }

            if (SplitedString[0].Equals("3x2"))
            {
                // FIXME Not Working
                //VarMath.Initialize(SplitedString);

            }



            if (Global.IsLowLevelDebugEnabled)
            {
                for (int i = 0; i < SplitedString.Length; i++)
                {
                    Console.Write(SplitedString[i] + " ");
                }
                Console.Write("\n");
            }


        }


    }
}