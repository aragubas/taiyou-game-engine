using System;
using System.Collections.Generic;

namespace TaiyouScriptEngine.Desktop.GameLogic
{
    public static class RoomSelector
    {
        public static List<GameRoom> RoomColection = new List<GameRoom>();
        public static List<int> RoomIDCollection = new List<int>();
        public static int CurrentRoom = 0;

        public static void Update()
        {
            Global.ChangeVar("SYS.CSR", Convert.ToString(CurrentRoom), "Int");

            // Update the current selected room
            RoomColection[CurrentRoom].Update();

        }

        public static void Initialize()
        {
            // Clear the Lists
            RoomColection.Clear();
            RoomIDCollection.Clear();
            CurrentRoom = 0;

            // Create the DefaultRoom [ID 0]
            AddRoom(new GameRoom(0));


        }

        public static void AddRoom(GameRoom RoomObj)
        {
            // Check if room already exists
            foreach (var roomID in RoomIDCollection)
            {
                if (RoomObj.RoomID == roomID)
                {
                    Console.WriteLine("Cannot Add room [" + RoomObj.RoomID + "]\nA room with the same ID already exist.");
                    return;
                }
            }


            RoomColection.Add(RoomObj);
            RoomIDCollection.Add(RoomObj.RoomID);
            Console.WriteLine("Added Room: [" + RoomObj.RoomID + "]");

        }

    }
}
