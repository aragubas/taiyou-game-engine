using System;
namespace TaiyouScriptEngine.Desktop.Taiyou.Command
{
    public static class SetVarValue
    {
        public static void call(string[] Args)
        {
            string OperatorVarName = Utils.GetSubstring(Args[0], '"');
            string NewValueType = Utils.GetSubstring(Args[1], '"');
            string NewValue = Utils.GetSubstring(Args[2], '"');

            // Get the Operator Variable
            Variable OperatorVariable = Global.VarList[Global.VarList_Keys.IndexOf(OperatorVarName)];

            // Get the NewValueType
            switch (NewValueType)
            {
                case "String":
                    OperatorVariable.Set_Value(Convert.ToString(NewValue));
                    return;

                case "Bool":
                    OperatorVariable.Set_Value(Convert.ToBoolean(NewValue));
                    return;

                case "Float":
                    OperatorVariable.Set_Value(float.Parse(NewValue));
                    return;

                case "Int":
                    OperatorVariable.Set_Value(Convert.ToInt32(NewValue));
                    return;


            }

        }

    }
}
