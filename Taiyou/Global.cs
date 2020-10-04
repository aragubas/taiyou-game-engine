using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace TaiyouScriptEngine.Desktop.Taiyou
{
    public static class Global
    {
        public static List<string> LoadedTaiyouScripts = new List<string>();
        public static List<List<TaiyouLine>> LoadedTaiyouScripts_Data = new List<List<TaiyouLine>>();

        // Global Variables
        public static List<Variable> VarList = new List<Variable>();
        public static List<string> VarList_Keys = new List<string>();

        // Functions List
        public static List<List<TaiyouLine>> Functions_Data = new List<List<TaiyouLine>>();
        public static List<string> Functions_Keys = new List<string>();

        // TSCN and TSUP lists
        static List<string> TSCN = new List<string>();
        static List<string> TSUP = new List<string>();

        // Instructions Dictionary Lists
        static List<string> Instructions_TSUP = new List<string>();
        static List<string> Instructions_NumberOfArguments = new List<string>();


        // Operation Signals
        public static bool IsOnStopOperation;
        public static int GlobalDelay = 1;

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

            Console.WriteLine("Dictionary file loaded sucefully.\n### Loading Instructions Arguments Size Dictionary ###");
            string[] IntructionsDictionary = File.ReadAllLines("./Taiyou/taiyou_dict.data");
            // Clear the Lists 
            Instructions_TSUP.Clear();
            Instructions_NumberOfArguments.Clear();

            foreach (var item in TaiyouDictonary)
            {
                string[] Splited = item.Split(';');

                Instructions_TSUP.Add(Splited[0]);
                Instructions_NumberOfArguments.Add(Splited[1]);
            }
            Console.WriteLine("Instructions Arguments Sizes Dictionary loaded.");

            // Find all scripts
            Console.WriteLine("Listing all avaliable scripts in: [" + Path + "]");
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
                            // Do Code Revision for this line
                            EditedLine = LineRevision(EditedLine, KeyNameFiltred, line, index);

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
                        Console.WriteLine("Added Line [" + line + "] to next code revision");
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
                    throw new FileLoadException(TaiyouParserError("ParserStep2: A function has been initialized and not finished properly.\nin Script(" + KeyNameFiltred + ")\nin FunctionName(" + LastFuncLineName + ")\nat Index(" + index + ")."));
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

                    // Final Line
                    string FinalLine = line;

                    // Replace TSCN with TSUP
                    FinalLine = LineRevision(FinalLine, KeyNameFiltred, line, index);

                    Console.WriteLine("Added line: [" + FinalLine + "] to Code Object");
                    ParsedCode.Add(new TaiyouLine(FinalLine));
                }

                Console.WriteLine("\n\n --- Parser Completed ---\n\n");

                LoadedTaiyouScripts_Data.Add(ParsedCode);

            }
            Console.WriteLine("Taiyou.Initialize : Sucefully added all scripts.\n\n\n\n");

        }

        private static string TaiyouParserError(string Message)
        {
            string Result = "Error while parsing the Taiyou Script\n" + Message;

            return Result;
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

        public static string LineRevision(string Input, string KeyNameFiltred, string line, int index)
        {
            string Pass1 = ReplaceWithTSUP(Input);
            string FinalResult = "";

            if (Pass1.Length < 3)
            {
                throw new Exception(TaiyouParserError("LineRevision: Code is less than 3 characters.\nPlease check the code.\nin Script(" + KeyNameFiltred + ")\nin Line(" + line + ")\nat Index(" + index + ")."));
            }

            // If the line does not ends with ';' token, throw an error
            if (!Pass1.EndsWith(";", StringComparison.Ordinal)) { throw new Exception(TaiyouParserError("LineRevision: Line Ending expected.\n\nat Script(" + KeyNameFiltred + ")\nin Line(" + line + ")\nat Index(" + index + ").")); }
            // Remove the ';' token
            string Pass2 = Pass1.Remove(Pass1.Length - 1, 1);
            string Instruction = Pass2.Substring(0, 3);

            /* ### Function Not Working ###
            int InstuctionsArgumentsSizeIndex = Instructions_TSUP.IndexOf(Instruction);
            if (InstuctionsArgumentsSizeIndex == -1) { throw new Exception(TaiyouParserError("LineRevision: Invalid Instruction [" + Instruction + "]")); }
            string CorrectNumberOfInstructions = Instructions_NumberOfArguments[InstuctionsArgumentsSizeIndex];
            int NumberOfInstructions = Pass2.Remove(0, 3).Count(x => x == '"');
            Console.WriteLine(NumberOfInstructions);
            */

            FinalResult = Pass2;

            return FinalResult;

        }

        public static void OptionLine(string[] Input)
        {
            foreach (var option in Input)
            {
                Console.WriteLine("Received Option (" + option + ")");

            }

        }

        /// <summary>
        /// Reloads everthing
        /// </summary>
        public static void Reload()
        {
            IsOnStopOperation = true;
            Console.WriteLine(" -- Taiyou.System --\nReloading everthing...");
            Game1.UpdateThread.Abort();
            Desktop.Global.DefaultValuesSet = false;

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
            Taiyou.Global.LoadTaiyouScripts(Desktop.Global.TaiyouDir);

            // Re-Initialize the Rooms
            GameLogic.RoomSelector.Initialize();

            Game1.RestartUpdateThread();

        }
    }
}
