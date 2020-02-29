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
using System.Threading;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;

namespace TaiyouGameEngine.Desktop.EngineMenu
{
    public class Main
    {
        // Global Menu Variables
        public static bool IsDrawAllowed = false;
        public static bool IsMenuActiaved = false;
        public static bool InitializationCompleted = false;
        public static int MenuCurrentScreen = 0;
        public static int StartDelay = 0;
        public static bool IsFatalErrorOcorred = false;
        public static string CursorResourceName = "Cursor.png";

        public static void Draw(SpriteBatch spriteBatch)
        {
            if (IsDrawAllowed)
            {
                // Draw the Selected Menu Screen
                if (IsFatalErrorOcorred == true) { Screen_FatalError.Draw(spriteBatch); }

                try
                {
                    if (!IsFatalErrorOcorred)
                    {
                        if (MenuCurrentScreen == 0)
                        {
                            Screen_LicenseWarning.Draw(spriteBatch);
                        }

                        if (MenuCurrentScreen == 1)
                        {
                            Screen_GameSelection.Draw(spriteBatch);
                        }

                        if (MenuCurrentScreen == 2)
                        {
                            Screen_UserLogin.Draw(spriteBatch);
                        }

                        spriteBatch.Draw(Sprite.GetSprite(CursorResourceName), UserInput.Cursor.Cursor_Rect, Color.White);

                    }

                }
                catch (Exception ex)
                {
                    Screen_FatalError.ExcData = ex;
                    MenuCurrentScreen = -1;

                    IsFatalErrorOcorred = true;

                }

            }

        }

        public static void Update()
        {
            try
            {
                if (InitializationCompleted == false) { Initialize(); InitializationCompleted = true; };
            }
            catch (Exception ex) { throw new Exception("Error while initializating the Taiyou Game Engine Menu\n" + ex.Message); }
            if (IsFatalErrorOcorred == true) { Screen_FatalError.Update(); }


            if (StartDelay <= 50) { StartDelay += 1; }

            // Update Screens
            if (StartDelay >= 50)
            {
                try
                {
                    if (!IsFatalErrorOcorred)
                    {
                        if (MenuCurrentScreen == 0)
                        {
                            Screen_LicenseWarning.Update();
                        }
                        if (MenuCurrentScreen == 1)
                        {
                            Screen_GameSelection.Update();
                        }
                        if (MenuCurrentScreen == 2)
                        {
                            Screen_UserLogin.Update();
                        }

                    }


                }
                catch (Exception ex)
                {
                    Screen_FatalError.ExcData = ex;
                    MenuCurrentScreen = -1;

                    IsFatalErrorOcorred = true;

                }

            }

        }

        public static void Initialize()
        {
            if (Global.ContentFolder != "") { MenuCurrentScreen = 1; Game1.UseRenderOrderMethod = true; EngineMenu.Screen_GameSelection.IsGameOverlay = true; Screen_GameSelection.GlobalOpacity = 0; Screen_GameSelection.GlobalOpacity_AnimEnabled = false; StartDelay = 50; }
            if (Global.ContentFolder == "") { IsDrawAllowed = true; IsMenuActiaved = true; };


            WindowProps(); // Update the Window Properties

            // If there is no user, Set Variable
            Global.IsUsersExistent = Directory.Exists(Environment.CurrentDirectory + "/Taiyou/HOME/Users/");

            WindowManager.ChangeWindowPropertie("RESOLUTION", "800x600");


        }

        public static void WindowProps()
        {
            // Load the Engine Menu Windows Parameters file
            if (File.Exists(Environment.CurrentDirectory + "/Taiyou/HOME/window.cfg"))
            {
                LoadMenuWindowProps();
            }
            else
            {
                string FileContent = "MAX_FPS:60\n" +
                                     "VSYNC:False\n" +
                                     "ALLOW_ALT_F4:False\n" +
                                     "CURSOR_OFFSCREEN:False\n" +
                                     "HAVE_BORDERS:True\n" +
                                     "RESIZIABLE_WINDOW:False\n" +
                                     "TOGGLE_FULLSCREEN:False\n";
                
                File.WriteAllText(Environment.CurrentDirectory + "/Taiyou/HOME/window.cfg", FileContent);
                LoadMenuWindowProps();
            }


        }

        private static void LoadMenuWindowProps()
        {
            string fileName = Environment.CurrentDirectory + "/Taiyou/HOME/window.cfg";
            Console.WriteLine("LoadMenuWindowProps : Start");

            var lines = File.ReadLines(fileName);
            foreach (var line in lines)
            {
                string[] SplitedParameters = line.Split(':');

                WindowManager.ChangeWindowPropertie(SplitedParameters[0], SplitedParameters[1]);

                if (SplitedParameters[0] == "MAX_FPS") { Global.MenuMaxFPS = Convert.ToInt32(SplitedParameters[1]); };

                Console.WriteLine("LoadMenuWindowProps : Propertie [" + SplitedParameters[0] + "] applyed with value [" + SplitedParameters[1] + "].");

            }

            Console.WriteLine("LoadMenuWindowProps : End");

        }



    }
}
