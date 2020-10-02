using System;
using System.Collections.Generic;

namespace TaiyouScriptEngine.Desktop.Taiyou.Command
{
    public static class FunctionHandler
    {
        public static void call(string[] Args)
        {
            string FunctionName = Utils.GetSubstring(Args[0], '"');

            int FunctionIndex = Global.Functions_Keys.IndexOf(FunctionName);

            if (FunctionIndex == -1) { throw new IndexOutOfRangeException(" -- ERROR Cannot find function [" + FunctionName + "] -- "); }

            List<TaiyouLine> AllCode = Global.Functions_Data[FunctionIndex];

            // Create an Interpreter Instance
            Interpreter RunFunction = new Interpreter("",  true, Global.Functions_Data[FunctionIndex]);

            // Run the Function
            RunFunction.Interpret();

        }


    }
}
