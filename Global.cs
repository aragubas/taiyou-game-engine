using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Microsoft.Xna.Framework.Input;
using TaiyouScriptEngine.Desktop.Taiyou;

namespace TaiyouScriptEngine.Desktop
{
    public class Global
    {
        // Directories
        public static string RegistryDir = "";
        public static string SpriteDir = "";
        public static string FontDir = "";
        public static string GameFolder = "";
        public static string SourceFolderFilter = "";
        public static string TaiyouDir = "";

        public static MouseState oldState;
        public static bool DefaultValuesSet = false;

        public static void UpdateGlobalVariables()
        {
            MouseState state = Mouse.GetState();

            ChangeVar("M.X", state.X, "Int");
            ChangeVar("M.Y", state.Y, "Int");

            if (!DefaultValuesSet)
            {
                DefaultValuesSet = true;
                ChangeVar("MLP.X", 0, "Int");
                ChangeVar("MLP.Y", 0, "Int");
                ChangeVar("MLR.X", 0, "Int");
                ChangeVar("MLR.Y", 0, "Int");
                ChangeVar("MRP.X", 0, "Int");
                ChangeVar("MRP.Y", 0, "Int");
                ChangeVar("MRR.X", 0, "Int");
                ChangeVar("MRR.Y", 0, "Int");
            }

            switch (state.LeftButton)
            {
                case ButtonState.Pressed:
                    ChangeVar("MLP.X", state.X, "Int");
                    ChangeVar("MLP.Y", state.Y, "Int");
                    break;

                case ButtonState.Released:
                    if (oldState.LeftButton == ButtonState.Pressed)
                    {
                        ChangeVar("MLR.X", state.X, "Int");
                        ChangeVar("MLR.Y", state.Y, "Int");
                    }

                    break;
            }
             
            switch (state.RightButton)
            {
                case ButtonState.Pressed:
                    ChangeVar("MRP.X", state.X, "Int");
                    ChangeVar("MRP.Y", state.Y, "Int");
                    break;

                case ButtonState.Released:
                    if (oldState.RightButton == ButtonState.Pressed)
                    {
                        ChangeVar("MRR.X", state.X, "Int");
                        ChangeVar("MRR.Y", state.Y, "Int");
                    }
                    break;
            }

            oldState = state;
        }

        public static void ChangeVar(string VarName, dynamic VarValue, string VarType)
        {
            int VarIndex = Taiyou.Global.VarList_Keys.IndexOf(VarName);

            // If it does not exist, add the variable
            if (VarIndex == -1)
            {
                Taiyou.Global.VarList.Add(new Variable(VarType, VarValue, VarName));
                Taiyou.Global.VarList_Keys.Add(VarName);

            } // If exist, update it's value
            else
            {
                Taiyou.Global.VarList[VarIndex].Set_Value(VarValue);
            }

        }



    }
}
