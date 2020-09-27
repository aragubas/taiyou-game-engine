using System;
namespace TaiyouScriptEngine.Desktop.Taiyou.Command
{
    public class CallEvent
    {
        public static void call(string[] Args)
        {
            string EventName = Utils.GetSubstring(Args[0], '"');
            int EventIndex = Event.EventListNames.IndexOf(EventName);

            if (EventIndex == -1)
            {
                Console.WriteLine("-- ERROR --\nCannot call event [" + EventName + "] because it does not exist.");
                return;
            }

            Event.TriggerEvent(EventName);

        }


    }
}