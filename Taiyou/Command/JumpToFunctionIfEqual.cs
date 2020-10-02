using System;
namespace TaiyouScriptEngine.Desktop.Taiyou.Command
{
    public static class JumpToFunctionIfEqual
    {
        public static void call(string[] Args)
        {
            string Operator = Utils.GetSubstring(Args[0], '"');
            string Comparator = Utils.GetSubstring(Args[1], '"');
            string JumpFunction = Utils.GetSubstring(Args[2], '"');
            string JumpElseFunction = "";

            // Optional Else
            try
            {
                JumpElseFunction = Utils.GetSubstring(Args[3], '"');
            }
            catch { }


            // Get the Operator Variable
            Variable OperatorVariable = Global.VarList[Global.VarList_Keys.IndexOf(Operator)];
            // Check if Operator is a Number Variable
            if (OperatorVariable.GenericVarType != "Number") { throw new Exception("Operator variable is not an Number"); }
            dynamic OperatorValue = OperatorVariable.Get_Value();

            // Get the Comparator Variable
            Variable ComparatorVariable = Global.VarList[Global.VarList_Keys.IndexOf(Comparator)];
            if (ComparatorVariable.GenericVarType != "Number") { throw new Exception("Comparator variable is not an Number"); }
            dynamic ComparatorValue = ComparatorVariable.Get_Value();


            if (OperatorValue == ComparatorValue)
            {
                FunctionHandler.call(new string[] { JumpFunction });
                return;
            }
            if (JumpElseFunction == "") { return; }
            // Else, call else function
            FunctionHandler.call(new string[] { JumpElseFunction });
            return;


        }
    }
}