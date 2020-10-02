using System;
namespace TaiyouScriptEngine.Desktop.Taiyou.Command
{
    public class SetRenderQueuePosition
    {
        public static void call(string[] Args)
        {
            string RqTagName = Utils.GetSubstring(Args[0], '"');
            string MvPosition = Utils.GetSubstring(Args[1], '"');
            string MvAmmount = Utils.GetSubstring(Args[2], '"');

            int RenderQueueIndex = Game1.RenderQueueList_Keys.IndexOf(RqTagName);
            int MvAmmountVarIndex = Global.VarList_Keys.IndexOf(MvAmmount);
            dynamic MvAmmountValue = 0;

            if (MvAmmountVarIndex != -1)
            {
                Variable varWax = Global.VarList[MvAmmountVarIndex];

                if (varWax.GenericVarType != "Number") { throw new Exception("Cannot Set the Operator Value to a non-number variable."); }

                MvAmmountValue = varWax.Value;

            }

            if (RenderQueueIndex == -1)
            {
                Console.WriteLine("-- ERROR -- Cannot find render queue object [" + RqTagName + "].");
                return;
            }

            switch (MvPosition)
            {
                case "x":
                    Game1.RenderQueueList[RenderQueueIndex].destRect.X = MvAmmountValue;
                    return;

                case "y":
                    Game1.RenderQueueList[RenderQueueIndex].destRect.Y = MvAmmountValue;
                    return;

                case "xy":
                    Game1.RenderQueueList[RenderQueueIndex].destRect.Y = MvAmmountValue;
                    Game1.RenderQueueList[RenderQueueIndex].destRect.X = MvAmmountValue;
                    return;

                case "x-":
                    Game1.RenderQueueList[RenderQueueIndex].destRect.X = -MvAmmountValue;
                    return;

                case "y-":
                    Game1.RenderQueueList[RenderQueueIndex].destRect.Y = -MvAmmountValue;
                    return;

                case "x-y-":
                    Game1.RenderQueueList[RenderQueueIndex].destRect.Y = -MvAmmountValue;
                    Game1.RenderQueueList[RenderQueueIndex].destRect.X = -MvAmmountValue;
                    return;


                default:
                    throw new ArgumentOutOfRangeException("Invalid move position [" + MvPosition + "]");

            }

        }
    }
}