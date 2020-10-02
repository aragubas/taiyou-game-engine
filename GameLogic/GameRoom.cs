namespace TaiyouScriptEngine.Desktop.GameLogic
{
    public class GameRoom
    {
        // Public Statements
        public string scriptClass;
        public int RoomID;
        public bool IsActive;

        // Private Statements
        private bool StartScriptToggle;
        private string StartScriptCallName;
        private string UpdateScriptCallName;
        private string StartScriptEventName;
        private string UpdateScriptEventName;


        public GameRoom(int roomID)
        {
            scriptClass = "Rooms/" + roomID + "/";
            RoomID = roomID;
            IsActive = true;

            // Add the UpdateScript for this room
            StartScriptCallName = scriptClass + "auto-start";
            UpdateScriptCallName = scriptClass + "update";
            StartScriptEventName = "room_" + roomID + "_auto-start";
            UpdateScriptEventName = "room_" + roomID + "_update";

            // Register the Main ROOM Events
            Taiyou.Event.RegisterEvent(StartScriptEventName, StartScriptCallName);
            Taiyou.LoopEvent.RegisterEvent(UpdateScriptEventName, UpdateScriptCallName, false);
            
        }


        public void Update()
        {
            // Toggle StartScript
            if (!StartScriptToggle)
            {
                StartScriptToggle = true;
                Taiyou.Event.TriggerEvent(StartScriptEventName);

            }

            // Set the Enable State for the Update Script
            Taiyou.LoopEvent.SetEventEnable(UpdateScriptEventName, IsActive);


        }

    }
}
