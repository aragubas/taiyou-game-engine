using System;
using System.Threading;

namespace TaiyouScriptEngine.Desktop.Taiyou
{
    public class EventObject
    {
        public string Name;
        public string ScriptName;
        public Interpreter InterpreterInstance;
        public bool EventEnabled;

        public EventObject(string name, string scriptname)
        {
            // Define some variables
            Name = name;
            ScriptName = scriptname;

            // Create an Interpreter Instance
            InterpreterInstance = new Interpreter(ScriptName);

        }

        public void run()
        {
            InterpreterInstance.Interpret();
        }

    }
}
