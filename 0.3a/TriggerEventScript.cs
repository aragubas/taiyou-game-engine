/*
   ####### BEGIN APACHE 2.0 LICENSE #######
   Copyright 2019 Parallex Software

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

   ####### END APACHE 2.0 LICENSE #######




   ####### BEGIN MONOGAME LICENSE #######
   THIS GAME-ENGINE WAS CREATED USING THE MONOGAME FRAMEWORK
   Github: https://github.com/MonoGame/MonoGame#license 

   MONOGAME WAS CREATED BY MONOGAME TEAM

   THE MONOGAME LICENSE IS IN THE MONOGAME_License.txt file on the root folder. 

   ####### END MONOGAME LICENSE ####### 





*/

using System;
using System.Collections.Generic;

namespace TaiyouGameEngine.Desktop
{
    public class TriggerEventScript
    {
        public static List<string> AllEventsNames = new List<string>();
        public static List<string> AllEventsScripts = new List<string>();


        public static void CheckEvent(string EventName)
        {
            int EventID = AllEventsNames.IndexOf(EventName);

            if (EventID == -1)
            {
                Console.WriteLine("CheckEvent : There is no event associated with [{0}].", EventName);
                return;
            }

            int ScriptID = TaiyouReader.CustomTaiyouScriptsName.IndexOf(AllEventsScripts[EventID]);

            if (ScriptID == -1)
            {
                Console.WriteLine("CheckEvent : ERROR , Script [" + AllEventsScripts[EventID] + "] does not exist.");
                return;
            }
        

            TaiyouReader.ReadAsync("Call " + AllEventsScripts[EventID]);

        }

        public static void AddEvent(string EventName, string EventScript)
        {
            Console.WriteLine("AddEvent : EventName[{0}], EventScript[{1}]", EventName, EventScript);
            AllEventsNames.Add(EventName); // Add the event name
            AllEventsScripts.Add(EventScript); // Add the event script

        }
    }
}
