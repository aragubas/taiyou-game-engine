using System;
namespace TaiyouScriptEngine.Desktop.Taiyou.Command
{
    public class CreateVar
    {

        public static void call(string[] Args)
        {
            string VarType = Utils.GetSubstring(Args[0], '"');
            string VarTag = Utils.GetSubstring(Args[1], '"');
            string VarDefaultValue = Utils.GetSubstring(Args[2], '"');
            int VarID = Global.VarList_Keys.IndexOf(VarTag);

            if (VarID != -1) { return; }


            Global.VarList.Add(new Variable(VarType, VarDefaultValue, VarTag));
            Global.VarList_Keys.Add(VarTag);


        }

    }
}
