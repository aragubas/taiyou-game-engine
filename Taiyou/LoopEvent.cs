using System;
using System.Collections.Generic;
using System.Threading;

namespace TaiyouScriptEngine.Desktop.Taiyou
{
    public static class LoopEvent
    {
        // Lists
        public static List<EventObject> EventList = new List<EventObject>();
        public static List<string> EventListNames = new List<string>();
        public static List<bool> EventEnables = new List<bool>();
        public static bool UpdateEnable = true;


        /// <summary>
        /// Runs the events on event queue
        /// </summary>
        public static void RunEvents()
        {
            while (UpdateEnable) // Make the thread loop forever and ever
            {
                // Pause the thread for 1 milisecounds, to make it not CRASH the pc
                Thread.Sleep(Global.GlobalDelay);

                // Run update for every thread here
                int id = -1;

                foreach (var Event in EventList)
                {
                    id += 1;

                    if (!EventEnables[id])
                    {
                        EventList.RemoveAt(id);
                        EventListNames.RemoveAt(id);
                        EventEnables.RemoveAt(id);
                        continue;
                    }

                    // Dispatch the Event
                    Event.run();

                }
            }

        }

        /// <summary>
        /// Registers an event on event queue.
        /// </summary>
        /// <param name="EventName">Event name.</param>
        /// <param name="EventScript">Event script.</param>
        /// <param name="AutoEnable">If set to <c>true</c> auto enable.</param>
        public static void RegisterEvent(string EventName, string EventScript, bool AutoEnable = true)
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
            EventEnables.Add(true);
           
            if (AutoEnable)
            {
                EventID = EventList.Count - 1;
                EventList[EventID].EventEnabled = true;
            }


        }

        /// <summary>
        /// Remove an event on event queue
        /// </summary>
        /// <param name="EventName">Event name.</param>
        public static void RemoveEvent(string EventName)
        {
            // Check if event already exists
            int EventID = EventListNames.IndexOf(EventName);
            // If already exists, remove it
            if (EventID != -1)
            {
                EventEnables[EventID] = true;
                EventList[EventID].EventEnabled = false;

            }
            else
            {
                Console.WriteLine("Cannot delete an loop event that does not exists.\nEventName(" + EventName + ").");
            }

        }

        /// <summary>
        /// Set the EnableState of event
        /// </summary>
        /// <param name="EventName">Event name.</param>
        public static void SetEventEnable(string EventName, bool EnableState)
        {
            // Check if event already exists
            int EventID = EventListNames.IndexOf(EventName);
            // If already exists, remove it
            if (EventID != -1)
            {
                EventList[EventID].EventEnabled = EnableState;

            }
            else
            {
                Console.WriteLine("Cannot update an loop event that does not exists.\nEventName(" + EventName + ").");
            }

        }


    }
}
