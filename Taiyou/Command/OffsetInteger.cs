using System;
namespace TaiyouScriptEngine.Desktop.Taiyou.Command
{
    public static class OffsetInteger
    {
        // This functions has 3 Arguments
        // All is needed
        // ----------------------------------

        public static void call(string[] Args)
        {
            string OperatorVarName = Utils.GetSubstring(Args[0], '"');
            string OffsetAmount = Utils.GetSubstring(Args[1], '"');
            int iOffsetAmount = 0;

            // Operator Var
            int OperatorVarIndex = Global.VarList_Keys.IndexOf(OperatorVarName);
            Variable OperatorVariable = Global.VarList[OperatorVarIndex];
            int OperatorValue = 0;

            // Check if OperatorVariable is an integer
            if (OperatorVariable.Type != "Int") { throw new Exception("Operator variable is not an integer."); }
            OperatorValue = OperatorVariable.Get_Value();


            // Get the OffsetAmmount from Variable
            if (OffsetAmount.StartsWith("$", StringComparison.Ordinal))
            {
                int OffsetAmountVarIndex = Global.VarList_Keys.IndexOf(OffsetAmount.Remove(0, 1));
                if (Global.VarList[OffsetAmountVarIndex].Type != "Int") { throw new Exception("OffserAmmount variable is not an integer"); }

                iOffsetAmount = Global.VarList[OffsetAmountVarIndex].Get_Value();
            }
            else
            {
                iOffsetAmount = Convert.ToInt32(OffsetAmount);
            }


            OperatorVariable.Set_Value(OperatorValue + iOffsetAmount);

        }


    }
}