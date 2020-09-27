using System;
using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;
using System.Threading;

namespace TaiyouScriptEngine.Desktop.Taiyou
{
    public class Interpreter
    {

        private string scriptName;
        private int scriptID;
        private List<TaiyouLine> Code;

        public Interpreter(string ScriptName)
        {
            scriptName = ScriptName;

            // Find the script on Script List
            int ScriptIndex = Global.LoadedTaiyouScripts.IndexOf(ScriptName);
            if (ScriptIndex == -1) { throw new EntryPointNotFoundException("the Taiyou Script (" + ScriptName + ") does not exist."); }

            scriptID = ScriptIndex;
            Code = Global.LoadedTaiyouScripts_Data[scriptID];

        }

        public void Interpret()
        {
            Global.UpdateGlobalVariables();

            int lineIndex = -1;
            foreach (var line in Code)
            {
                lineIndex++;
                string[] arguments = line.Arguments;

                for (int i = 0; i < arguments.Length; i++)
                {
                    foreach (var Var in Global.VarList)
                    {
                        arguments[i] = arguments[i].Replace(Var.SearchPattern, Var.Value);

                    }
                }


                line.call(arguments);
            }


        }



    }
}