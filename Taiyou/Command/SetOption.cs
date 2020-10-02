using System;
namespace TaiyouScriptEngine.Desktop.Taiyou.Command
{
    public static class SetOption
    {
        public static void call(string[] Args)
        {
            string OptionName = Utils.GetSubstring(Args[0], '"');
            string OptionValue = Utils.GetSubstring(Args[1], '"');

            switch (OptionName)
            {
                case "FixedTimeStep":
                    Game1.Reference.IsFixedTimeStep = Convert.ToBoolean(OptionValue);
                    return;

                case "MouseVisible":
                    Game1.Reference.IsMouseVisible = Convert.ToBoolean(OptionValue);
                    return;

                case "WindowTitle":
                    Game1.Reference.Window.Title = OptionValue;
                    return;

                case "WindowBorderless":
                    Game1.Reference.Window.IsBorderless = Convert.ToBoolean(OptionValue);
                    return;


                default:
                    throw new ArgumentOutOfRangeException("Invalid argument: [" + OptionName + "]");

            }

        }


    }
}