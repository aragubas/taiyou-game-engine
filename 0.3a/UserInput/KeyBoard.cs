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
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Xna.Framework.Input;

namespace TaiyouGameEngine.Desktop.UserInput
{
    public class KeyBoard
    {
        // Update the keyboard input

        // Variables
        public static KeyboardState previousState;
        public static string PressedKeyString = "";
        public static List<Keys> VerifyKeyPressed_Key = new List<Keys>();
        public static List<bool> VerifyKeyPressed_Values = new List<bool>();
        public static List<string> VerifyKeyPressed_TaiyouCommandsToRun = new List<string>();
        public static List<string> VerifyKeyPressed_PressType = new List<string>();

        public static void Update()
        {
            KeyboardState state = Keyboard.GetState();

            for (int i = 0; i < VerifyKeyPressed_Key.Count; i++)
            {

                if (VerifyKeyPressed_PressType[i] == "DOWN")
                {
                    if (previousState.IsKeyDown(VerifyKeyPressed_Key[i]) && state.IsKeyDown(VerifyKeyPressed_Key[i]))
                    {
                        VerifyKeyPressed_Values[i] = true;

                        string[] AllComas = VerifyKeyPressed_TaiyouCommandsToRun[i].Split('|');
                        for (int i2 = 0; i2 < AllComas.Length; i2++)
                        {
                            TaiyouReader.ReadAsync(AllComas[i2]);
                        }


                    }

                }
                if (VerifyKeyPressed_PressType[i] == "UP")
                {
                    if (previousState.IsKeyUp(VerifyKeyPressed_Key[i]) && state.IsKeyDown(VerifyKeyPressed_Key[i]))
                    {
                        VerifyKeyPressed_Values[i] = true;

                        string[] AllComas = VerifyKeyPressed_TaiyouCommandsToRun[i].Split('|');
                        for (int i2 = 0; i2 < AllComas.Length; i2++)
                        {
                            TaiyouReader.ReadAsync(AllComas[i2]);
                        }

                    }
                }


            }

            VerifyKeyPressed_Key.Clear();
            VerifyKeyPressed_Values.Clear();
            VerifyKeyPressed_TaiyouCommandsToRun.Clear();
            VerifyKeyPressed_PressType.Clear();

            previousState = state;
        }
    }
}


/*
 public string jsButton = "JoystickButton9" ;
 public KeyCode kc ;
 
 void Awake()
 {
    kc = (KeyCode)System.Enum.Parse(typeof(KeyCode), jsButton) ;
 }

*/