using System;
namespace TaiyouScriptEngine.Desktop.Taiyou.Command
{
    public static class EventHandler
    {
        public static void call(string[] Args)
        {
            string Operator = Utils.GetSubstring(Args[0], '"');
            string EventName = Utils.GetSubstring(Args[1], '"');
            string EventScript = "null";
            // Optional Argument
            if (Args.Length > 1)
            {
                EventScript = Utils.GetSubstring(Args[2], '"');
            }

            // Check if event already exists
            int EventNameIndex = Event.EventListNames.IndexOf(EventName);

            switch (Operator)
            {
                case "Add":
                    if (EventNameIndex != -1)
                    {
                        Console.WriteLine("Taiyou.EventHandler.Operators.Add : Event already exist [" + EventName + "].\nOperation may not execute.");
                        return;
                    }

                    // Add to the Event Handler
                    Event.EventListNames.Add(EventName);
                    Event.EventList.Add(new EventObject(EventName, EventScript));
                    return;

                case "Remove":
                    if (EventNameIndex == -1)
                    {
                        Console.WriteLine("Taiyou.EventHandler.Operators.Remove : Event does not exist [" + EventName + "].\nOperation may not execute.");
                        return;
                    }

                    Event.EventList.RemoveAt(EventNameIndex);
                    Event.EventListNames.RemoveAt(EventNameIndex);
                    return;

            }



        }




    }
}