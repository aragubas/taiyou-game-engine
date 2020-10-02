using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Microsoft.Xna.Framework.Input;
using TaiyouScriptEngine.Desktop.Taiyou;

namespace TaiyouScriptEngine.Desktop
{
    public class Global
    {
        // Directories
        public static string RegistryDir = "";
        public static string SpriteDir = "";
        public static string FontDir = "";
        public static string GameFolder = "";
        public static string SourceFolderFilter = "";
        public static string TaiyouDir = "";

        public static int GlobalDelay = 1;

        #region Taiyou Interpreter Variables
        public static List<string> LoadedTaiyouScripts = new List<string>();
        public static List<List<TaiyouLine>> LoadedTaiyouScripts_Data = new List<List<TaiyouLine>>();

        // Global Variables
        public static List<Variable> VarList = new List<Variable>();
        public static List<string> VarList_Keys = new List<string>();
        private static bool DefaultValuesSet = false;
        private static MouseState oldState;

        // Functions List
        public static List<List<TaiyouLine>> Functions_Data = new List<List<TaiyouLine>>();
        public static List<string> Functions_Keys = new List<string>();

        // TSCN and TSUP lists
        static List<string> TSCN = new List<string>();
        static List<string> TSUP = new List<string>();

        // Operation Signals
        public static bool IsOnStopOperation;

        public static void LoadTaiyouScripts(string Path)
        {
            // Clear the lists
            LoadedTaiyouScripts.Clear();
            LoadedTaiyouScripts_Data.Clear();
            Functions_Data.Clear();
            Functions_Keys.Clear();

            // Load the Dictionary File
            Console.WriteLine("### Loading Taiyou Dictionary File... ###");
            string[] TaiyouDictonary = File.ReadAllLines("./Taiyou/taiyou_dict.data");
            // Clear the Lists
            TSCN.Clear();
            TSUP.Clear();

            foreach (var item in TaiyouDictonary)
            {
                string[] Splited = item.Split(';');

                TSCN.Add(Splited[0]);
                TSUP.Add(Splited[1]);
            }

            Console.WriteLine("Dictionary file loaded sucefully.\nListing all avaliable scripts...");

            // Find all scripts
            string[] AllScripts = Directory.GetFiles(Path, "*.tiy", SearchOption.AllDirectories);

            // Iterate over every script
            for (int i = 0; i < AllScripts.Length; i++)
            {
                // Set the Script Name
                string KeyNameFiltred = AllScripts[i].Replace(Path, "");
                KeyNameFiltred = KeyNameFiltred.Replace(".tiy", "");
                LoadedTaiyouScripts.Add(KeyNameFiltred);

                Console.WriteLine(" -- Parsing Script: (" + KeyNameFiltred + ") -- ");


                // ##########################################
                // ######### -- Parser Step 1 - #############
                // ##########################################
                Console.WriteLine("\n### Parser : Step 1 ###");

                // Define some variables
                string ReadText = File.ReadAllText(Path + KeyNameFiltred + ".tiy", new System.Text.UTF8Encoding());
                string[] ReadTextLines = ReadText.Split(Convert.ToChar(Environment.NewLine));
                List<string> CorrectTextLines = new List<string>();
                List<TaiyouLine> ParsedCode = new List<TaiyouLine>();

                // Remove every line that is less than 3 Characters
                int index = -1;

                bool IsReadingFunctionLine = false;
                string LastFuncLineName = "";
                var FunctionCode = new List<TaiyouLine>();

                for (int i2 = 0; i2 < ReadTextLines.Length; i2++)
                {
                    string line = ReadTextLines[i2];

                    if (line.Length < 3) { Console.WriteLine("Removed Dead Line"); continue; }
                    if (line.StartsWith("#", StringComparison.Ordinal)) { Console.WriteLine("Removed comment line [" + line + "]"); continue; }

                    // Initialize the Function Read
                    if (line.StartsWith("$FUNCTION", StringComparison.Ordinal))
                    {
                        Console.WriteLine(" -- Found Function Block --");
                        string FunctionName = line.Split('"')[1];

                        IsReadingFunctionLine = true;

                        LastFuncLineName = FunctionName;
                        Console.WriteLine("Function Name:\n" + FunctionName);

                    }
                    
                    // Read the function code
                    if (IsReadingFunctionLine)
                    {
                        // Check if function is not at the end
                        if (line.StartsWith("$END", StringComparison.Ordinal))
                        {
                            // Add the key and the data
                            Functions_Keys.Add(LastFuncLineName);
                            Console.WriteLine(FunctionCode.Count);
                            List<TaiyouLine> Copyied = new List<TaiyouLine>();
                            foreach (var item in FunctionCode)
                            {
                                Copyied.Add(item);
                            }

                            Functions_Data.Add(Copyied);

                            IsReadingFunctionLine = false;
                            FunctionCode.Clear();
                            LastFuncLineName = "";
                            Console.WriteLine(" -- Function Block Completed -- ");

                        }

                        // Count if line a Command Line
                        // If line starts with 1 tab identation, is it valid!
                        if (line.StartsWith("    ", StringComparison.Ordinal))
                        {
                            string EditedLine = line;
                            EditedLine = EditedLine.Remove(0, 4);
                            if (EditedLine.Length < 3)
                            {
                                continue;
                            }
                            EditedLine = ReplaceWithTSUP(EditedLine);

                            FunctionCode.Add(new TaiyouLine(EditedLine));

                            Console.WriteLine("Added Command line: [" + EditedLine + "] to function block.");
                        }

                    }

                    // Add the Line if is not a Function Line
                    if (IsReadingFunctionLine == false)
                    {
                        if (line.StartsWith("$END", StringComparison.Ordinal))
                        {
                            continue;
                        }
                        Console.WriteLine("Added Line [" + line + "]");
                        CorrectTextLines.Add(line);
                    }


                }

                // ##########################################
                // ######### -- Parser Step 2 - #############
                // ##########################################
                Console.WriteLine("\n### Parser : Step 2 ###");

                // Check if a functions start was not left behind
                if (IsReadingFunctionLine)
                {
                    string Error = "Error while parsing Taiyou Script: A function has been initialized and not finished properly." +
                        "\nScriptName: " + KeyNameFiltred +
                        "\nFunctionName: " + LastFuncLineName;

                    throw new FileLoadException(Error);
                }

                // ##########################################
                // ######### -- Parser Step 3 - #############
                // ##########################################
                Console.WriteLine("\n### Parser : Step 3 ###");


                // Convert thr result to Array
                string[] ScriptData = CorrectTextLines.ToArray();

                // Check if line is a valid command
                index = -1;
                foreach (var line in ScriptData)
                {
                    index += 1;

                    // Check if line is a Commented Line
                    if (line.StartsWith("#", StringComparison.Ordinal))
                    {
                        Console.WriteLine(" -- WARNING : Comment line detected, comment line should be removed in step 2. -- ");
                        Console.WriteLine("Line: (" + line + ")");
                        continue;
                    }

                    string EditedLine = line;

                    // Replace TSCN with TSUP
                    EditedLine = ReplaceWithTSUP(EditedLine);

                    if (!EditedLine.EndsWith(";", StringComparison.Ordinal)) { throw new FileLoadException("Error while parsing Taiyou Script Code\nLine Ending expected.\n\nat Script(" + KeyNameFiltred + ")\nin Line(" + line + ")\nat Index(" + index + ")."); }
                    EditedLine = EditedLine.Remove(EditedLine.Length - 1, 1);


                    Console.WriteLine("Added line: [" + EditedLine + "]");
                    ParsedCode.Add(new TaiyouLine(EditedLine));
                }

                Console.WriteLine("\n\n --- Parser Completed ---\n\n");

                LoadedTaiyouScripts_Data.Add(ParsedCode);

            }
            Console.WriteLine("Taiyou.Initialize : Sucefully added all scripts.\n\n\n\n");

        }

        public static string ReplaceWithTSUP(string Input)
        {
            string LineInstruction = Input.Split(' ')[0];

            // Replace TSCN with TSUP
            int IntructionNameIndex = TSCN.IndexOf(LineInstruction);
            if (IntructionNameIndex == -1)
            {
                Console.WriteLine(" -- WARNING : Unknow TSUP (" + LineInstruction + ") -- ");
                return Input;
            }

            string InstructionUpcode = TSUP[IntructionNameIndex];

            Console.WriteLine("Renamed Command-Name(" + LineInstruction + ") to TSUP(" + InstructionUpcode + ")");
            return Input.Replace(LineInstruction, InstructionUpcode);



        }

        public static void OptionLine(string[] Input)
        {
            foreach (var option in Input)
            {
                Console.WriteLine("Received Option (" + option + ")");

            }

        }

        public static void Reload()
        {
            IsOnStopOperation = true;
            Console.WriteLine(" -- Taiyou.System --\nReloading everthing...");
            Game1.UpdateThread.Abort();
            DefaultValuesSet = false;

            LoopEvent.UpdateEnable = false;

            LoadedTaiyouScripts.Clear();
            LoadedTaiyouScripts_Data.Clear();
            VarList.Clear();
            VarList_Keys.Clear();
            Event.EventList.Clear();
            Event.EventListNames.Clear();
            LoopEvent.EventEnables.Clear();
            LoopEvent.EventListNames.Clear();
            LoopEvent.EventList.Clear();
            Game1.RenderQueueList.Clear();
            Game1.RenderQueueList_Keys.Clear();
            Functions_Keys.Clear();
            Functions_Data.Clear();

            // Re-Load all scripts
            LoadTaiyouScripts(TaiyouDir);

            // Re-Initialize the Rooms
            GameLogic.RoomSelector.Initialize();

            Game1.RestartUpdateThread();

        }

        public static void UpdateGlobalVariables()
        {
            MouseState state = Mouse.GetState();

            ChangeVar("M.X", Convert.ToString(state.X));
            ChangeVar("M.Y", Convert.ToString(state.Y));

            if (!DefaultValuesSet)
            {
                DefaultValuesSet = true;
                ChangeVar("MLP.X", "0");
                ChangeVar("MLP.Y", "0");
                ChangeVar("MLR.X", "0");
                ChangeVar("MLR.Y", "0");
                ChangeVar("MRP.X", "0");
                ChangeVar("MRP.Y", "0");
                ChangeVar("MRR.X", "0");
                ChangeVar("MRR.Y", "0");
            }

            switch (state.LeftButton)
            {
                case ButtonState.Pressed:
                    ChangeVar("MLP.X", Convert.ToString(state.X));
                    ChangeVar("MLP.Y", Convert.ToString(state.Y));
                    break;

                case ButtonState.Released:
                    if (oldState.LeftButton == ButtonState.Pressed)
                    {
                        ChangeVar("MLR.X", Convert.ToString(state.X));
                        ChangeVar("MLR.Y", Convert.ToString(state.Y));
                    }

                    break;
            }
             
            switch (state.RightButton)
            {
                case ButtonState.Pressed:
                    ChangeVar("MRP.X", Convert.ToString(state.X));
                    ChangeVar("MRP.Y", Convert.ToString(state.Y));
                    break;

                case ButtonState.Released:
                    if (oldState.RightButton == ButtonState.Pressed)
                    {
                        ChangeVar("MRR.X", Convert.ToString(state.X));
                        ChangeVar("MRR.Y", Convert.ToString(state.Y));
                    }
                    break;
            }

            oldState = state;
        }

        public static void ChangeVar(string VarName, string VarValue)
        {
            int VarIndex = VarList_Keys.IndexOf(VarName);

            // If it does not exist, add the variable
            if (VarIndex == -1)
            {
                VarList.Add(new Variable("Int", VarValue, VarName));
                VarList_Keys.Add(VarName);

            } // If exist, update it's value
            else
            {
                VarList[VarIndex].Value = VarValue;
            }

        }

        #endregion

    }
}
