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

            if (MvAmmountVarIndex != -1)
            {
                MvAmmount = Global.VarList[MvAmmountVarIndex].Value;
            }

            if (RenderQueueIndex == -1)
            {
                Console.WriteLine("-- ERROR -- Cannot find render queue object [" + RqTagName + "].");
                return;
            }

            switch (MvPosition)
            {
                case "x":
                    Game1.RenderQueueList[RenderQueueIndex].destRect.X = Convert.ToInt32(MvAmmount);
                    return;

                case "y":
                    Game1.RenderQueueList[RenderQueueIndex].destRect.Y = Convert.ToInt32(MvAmmount);
                    return;

                case "xy":
                    Game1.RenderQueueList[RenderQueueIndex].destRect.Y = Convert.ToInt32(MvAmmount);
                    Game1.RenderQueueList[RenderQueueIndex].destRect.X = Convert.ToInt32(MvAmmount);
                    return;


                default:
                    throw new ArgumentOutOfRangeException("Invalid move position [" + MvPosition + "]");

            }

        }
    }
}