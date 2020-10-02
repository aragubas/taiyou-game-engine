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
        private List<TaiyouLine> Code;

        public Interpreter(string ScriptName, bool DirectCode = false, List<TaiyouLine> taiyouLines = null)
        {
            scriptName = ScriptName;

            // Find the script on Script List
            if (DirectCode)
            {
                Code = taiyouLines;
                return;
            }
            int ScriptIndex = Global.LoadedTaiyouScripts.IndexOf(ScriptName);
            if (ScriptIndex == -1) { throw new EntryPointNotFoundException("the Taiyou Script (" + ScriptName + ") does not exist."); }

            Code = Global.LoadedTaiyouScripts_Data[ScriptIndex];

        }

        public void Interpret()
        {
            if (Global.IsOnStopOperation) { return; }
            Global.UpdateGlobalVariables();

            foreach (var line in Code)
            {
                line.call();
            }


        }



    }
}