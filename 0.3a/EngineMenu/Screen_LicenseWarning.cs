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
using System.IO;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;
using TaiyouGameEngine.Desktop.UserInput;

namespace TaiyouGameEngine.Desktop.EngineMenu
{
    public class Screen_LicenseWarning // License Screen
    {
        static string LicenseText = "";
        public static int AnimationMode = 0;
        public static bool AnimationEnabled = true;
        static int GlobalOpacity = 0;
        static int GlobalOpacity_AnimationSpeed = 1;
        public static bool AnimationCompleted = false;
        static KeyboardState previusState;
        static bool ScreenInitialized = false;
        static int NextScreenDelay = 0;

        public static void Draw(SpriteBatch spriteBatch)
        {
            spriteBatch.DrawString(Sprite.GetFont("10pt.xnb"), LicenseText, new Vector2(40, 130), Color.FromNonPremultiplied(255,255,255, GlobalOpacity));

        }

        public static void Update()
        {
            if (!ScreenInitialized) { ScreenInitialized = true;  Initialize(); }

            KeyboardState state = Keyboard.GetState();

            Game1.ClearScreenColor = Color.Black;


            if (AnimationEnabled)
            {
                if (AnimationMode == 0)
                {
                    GlobalOpacity_AnimationSpeed += 1;
                    GlobalOpacity += GlobalOpacity_AnimationSpeed;

                    if (GlobalOpacity >= 255) { AnimationMode = 1; AnimationEnabled = false; GlobalOpacity_AnimationSpeed = 0; }
                }
                if (AnimationMode == 1)
                {
                    GlobalOpacity_AnimationSpeed += 1;
                    GlobalOpacity -= GlobalOpacity_AnimationSpeed;

                    if (GlobalOpacity <= 0) { AnimationMode = 0; AnimationEnabled = false; AnimationCompleted = true; GlobalOpacity_AnimationSpeed = 0; }
                }

            }

            if (AnimationMode == 1)
            {
                if (previusState.IsKeyDown(Keys.Enter) && state.IsKeyUp(Keys.Enter))
                {
                    AnimationEnabled = true;
                }

            }

            if (AnimationCompleted) { NextScreenDelay += 1; if (NextScreenDelay >= 50) { Main.MenuCurrentScreen = 2; NextScreenDelay = 0; }; }


            previusState = state;
        }

        public static void Initialize()
        {
            // Default License Text
            string LicenseTextFile = Environment.CurrentDirectory + "/Taiyou/HOME/license_text.txt";
            if (File.Exists(LicenseTextFile))
            {
                LicenseText = File.ReadAllText(LicenseTextFile, new System.Text.UTF8Encoding());
                Console.WriteLine("SCREEN_LICENSE : License Text was detected.");


            }
            else
            {
                Console.WriteLine("SCREEN_LICENSE : License Text was not detected.");

                LicenseText += "         [ERROR: License text was not detected.]      \n\n" +
                               "Please verify if the file [license_text.txt] exists on\n" +
                               "the directory [~/Taiyou/HOME/].                       \n\n";

            }


            if (Global.Engine_DebugRender == true)
            {
                Console.WriteLine("SCREEN_LICENSE : Debug Mode Detected");

                LicenseText += "Debug Mode Detected, this mode is only for help games \n" +
                               "develop, if you dont know what you're doing, exit this\n" +
                               "mode.                                                 \n";

            }
            LicenseText += "\n\nPress [Enter] to continue";


        }


    }
}
