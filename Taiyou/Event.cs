using System;
using System.Collections.Generic;
using System.Threading;

namespace TaiyouScriptEngine.Desktop.Taiyou
{
    public static class Event
    {
        // Lists
        public static List<EventObject> EventList = new List<EventObject>();
        public static List<string> EventListNames = new List<string>();

        /// Event Dispatcher
        /// <summary>
        /// Triggers an event.
        /// </summary>
        /// <param name="EventName">Event name added to Event Queue</param>
        public static void TriggerEvent(string EventName)
        {
            int EventID = EventListNames.IndexOf(EventName);
            EventList[EventID].InterpreterInstance.Interpret();

        }

        /// <summary>
        /// Renames the event.
        /// </summary>
        /// <param name="EventName">Event name.</param>
        /// <param name="NewName">New name.</param>
        public static void RenameEvent(string EventName, string NewName)
        {
            // Check if event already exists
            int EventID = EventListNames.IndexOf(EventName);

            // If already exists, return
            if (EventID != -1)
            {
                Console.WriteLine("System.Taiyou.RenameEvent : Cannot find the event (" + EventName + ")");
                return;
            }
        }

        /// <summary>
        /// Registers an event.
        /// </summary>
        /// <param name="EventName">Event name.</param>
        /// <param name="EventScript">Event script.</param>
        public static void RegisterEvent(string EventName, string EventScript)
        {
            // Check if event already exists
            int EventID = EventListNames.IndexOf(EventName);
            // If already exists, return
            if (EventID != -1)
            {
                return;
            }


            // Add Event to Event List
            EventListNames.Add(EventName);
            EventList.Add(new EventObject(EventName, EventScript));
        }

        /// <summary>
        /// Removes an event.
        /// </summary>
        /// <param name="EventName">Event name.</param>
        public static void RemoveEvent(string EventName)
        {
            // Check if event already exists
            int EventID = EventListNames.IndexOf(EventName);
            // If already exists, remove it
            if (EventID != -1)
            {
                EventListNames.RemoveAt(EventID);
                EventList.RemoveAt(EventID);
            }
            else
            {
                Console.WriteLine(" -- WARNING -- \nCannot delete an event that does not exists, Event[" + EventName + "].");
            }

        }


    }
}
