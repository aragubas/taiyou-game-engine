using System;
namespace TaiyouScriptEngine.Desktop.Taiyou.Command
{
    public static class MathOperation
    {
        public static void call(string[] Args)
        {
            string OperatorVarName = Utils.GetSubstring(Args[0], '"');
            string MathOperation = Utils.GetSubstring(Args[1], '"');
            string ActuatorVarName = Utils.GetSubstring(Args[2], '"');

            int OperatorIndex = Global.VarList_Keys.IndexOf(OperatorVarName);
            int ActuatorIndex = Global.VarList_Keys.IndexOf(ActuatorVarName);
            string OperatorValue = Global.VarList[OperatorIndex].Value;
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


            switch (MathOperation)
            {
                case "+":
                    Global.VarList[OperatorIndex].Value = Convert.ToString(Convert.ToInt32(OperatorValue) + Convert.ToInt32(ActuatorValue));
                    break;
            }

        }

    }
}
