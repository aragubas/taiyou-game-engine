using System;
using System.Text.RegularExpressions;

namespace TaiyouScriptEngine.Desktop.Taiyou.Command
{
    public static class IntegerOperation
    {
        public static void call(string[] Args)
        {
            string OperatorVarName = Utils.GetSubstring(Args[0], '"');
            string MathOperation = Utils.GetSubstring(Args[1], '"');
            string ActuatorVarName = Utils.GetSubstring(Args[2], '"');

            // Set the Operator
            int OperatorIndex = Global.VarList_Keys.IndexOf(OperatorVarName);
            if (OperatorIndex == -1) { throw new IndexOutOfRangeException("Cannot find the variable [" + OperatorVarName + "]."); }
            string OperatorValue = Global.VarList[OperatorIndex].Value;

            if (!Regex.IsMatch(OperatorValue, @"\d"))
            {
                Console.WriteLine("-- Invalid Operator Value --");
                Console.WriteLine("OperatorVarName: " + OperatorVarName);
                Console.WriteLine("OperatorIndex: " + OperatorIndex);
                Console.WriteLine("OperatorValue: " + OperatorValue);
                throw new IndexOutOfRangeException("Operator Value is not an number.");
            }

            // Set the Actuator
            int ActuatorIndex = Global.VarList_Keys.IndexOf(ActuatorVarName);
            string ActuatorValue = "";
            if (ActuatorIndex == -1)
            {
                // Check if Actuator is a literal
                if (ActuatorVarName.StartsWith("#", StringComparison.Ordinal))
                {
                    ActuatorValue = ActuatorVarName.Remove(0, 1);
                }

            }
            else { ActuatorValue = Global.VarList[ActuatorIndex].Value; }


            if (!Regex.IsMatch(ActuatorValue, @"\d"))
            {
                throw new IndexOutOfRangeException("Literals must start with '#' token. [" + OperatorVarName + "].");
            }




            switch (MathOperation)
            {
                case "+":
                    Global.VarList[OperatorIndex].Value = Convert.ToString(Convert.ToInt32(OperatorValue) + Convert.ToInt32(ActuatorValue));
                    break;
            }

        }

    }
}
