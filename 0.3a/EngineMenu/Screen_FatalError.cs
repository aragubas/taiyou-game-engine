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
using System.Text.RegularExpressions;
using System.Threading;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;

namespace TaiyouGameEngine.Desktop.EngineMenu
{
    public class Screen_FatalError
    {
        public static string MessageText = "null";
        public static int AnimationMode = 0;
        public static bool AnimationEnabled = true;
        static int GlobalOpacity = 0;
        static int GlobalOpacity_AnimationSpeed = 1;
        public static bool AnimationCompleted = false;
        static bool ScreenInitialized = false;
        static int NextScreenDelay = 0;
        public static Exception ExcData;
        static KeyboardState previusState;

        public static void Draw(SpriteBatch spriteBatch)
        {
            // Draw the main text
            spriteBatch.Draw(Sprite.GetSprite("Base.png"), new Rectangle(0, 0, WindowManager.WindowW, WindowManager.WindowH), Color.Black);
            spriteBatch.DrawString(Sprite.GetFont("10pt.xnb"), MessageText, new Vector2(40, 130), Color.FromNonPremultiplied(255, 255, 255, GlobalOpacity));

        }

        public static void Update()
        {
            if (!ScreenInitialized) { ScreenInitialized = true; Initialize(); }
            KeyboardState state = Keyboard.GetState();

            Game1.ClearScreenColor = Color.Black;

            if (AnimationEnabled)
            {
                if (AnimationMode == 0)
                {
                    GlobalOpacity_AnimationSpeed += 1;
                    GlobalOpacity += GlobalOpacity_AnimationSpeed;

                    if (GlobalOpacity >= 255 + GlobalOpacity_AnimationSpeed) { AnimationMode = 1; AnimationEnabled = false; GlobalOpacity_AnimationSpeed = 0; }
                }
                if (AnimationMode == 1)
                {
                    GlobalOpacity_AnimationSpeed += 1;
                    GlobalOpacity -= GlobalOpacity_AnimationSpeed;

                    if (GlobalOpacity <= 0) { AnimationMode = 0; AnimationEnabled = false; Game1.ThisGameObj.Exit(); GlobalOpacity_AnimationSpeed = 0; }
                }

            }

            // Trigger the Enter Key

            if (AnimationMode == 1)
            {
                if (previusState.IsKeyDown(Microsoft.Xna.Framework.Input.Keys.Enter) && state.IsKeyUp(Microsoft.Xna.Framework.Input.Keys.Enter))
                {
                    AnimationEnabled = true;
                }

            }

            if (AnimationCompleted) { NextScreenDelay += 1; if (NextScreenDelay >= 50) { Main.MenuCurrentScreen += 1; NextScreenDelay = 0; }; }

            previusState = state;

        }

        public static void Initialize()
        {
            // Template to fitting the information on the screen
            //            "Taiyou Game Engine is licensed under Apache 2.0 license.\n"
            MessageText = "    A fatal error has been occored on the System Menu   \n\n" +
                          "ErrorCode:" + ExcData.HResult + "                         \n" +
                          "ErrorMessage:" + ExcData.Message + "                    \n\n" +
                          "LastTitleName: " + Global.CurrentSelectedTitleName + "    \n" +
                          "LastTitleVersion: " + Global.CurrentSelectedTitleVersion + "\n\n" +
                          "More detailed information about the error will be saved   \n" +
                          "on [~/Taiyou/HOME/EXC/].                                  \n" + 
                          "\n\n                                                      \n" +
                          "Press [Enter] to exit";

            string ExcFileDir = Environment.CurrentDirectory + "/Taiyou/HOME/EXC/"; 
            string ExFileName = "(" + DateTime.Now.Month + "." + DateTime.Now.Day + "." + DateTime.Now.Year + ")" + DateTime.Now.Hour + "." + DateTime.Now.Minute + "." + DateTime.Now.Second + ".txt";
            string DetailedText = "### EXCEPTION FILE HEAD ###\n\n" +
                                  "//// Infos ////" +
                                  "\nStackTrace:\n\n" + ExcData.StackTrace +
                                  "\n\nHResult:" + ExcData.HResult +
                                  "\nHelpLink:" + ExcData.HelpLink +
                                  "\nTargetSite:" + ExcData.TargetSite +
                                  "\nSource:" + ExcData.Source +
                                  "\nMessage:" + ExcData.Message +
                                  "\nCurrentTitleName:" + Global.CurrentSelectedTitleName +
                                  "\nCurrentTitleID:" + Global.CurrentSelectedTitleID +
                                  "\nCurrentTitleVersion:" + Global.CurrentSelectedTitleVersion +
                                  "\nContentFolder:" + Global.ContentFolder +
                                  "\nContentFolderName:" + Global.ContentFolderName +
                                  "\nDebugRender:" + Global.Engine_DebugRender +
                                  "\nResetKey:" + Global.Engine_ResetKey +
                                  "\nIsLogged:" + Global.IsLogged +
                                  "\nCurrentLoggedUser:" + Global.CurrentLoggedUser +
                                  "\nCurrentOSName:" + Global.CurrentOSName +
                                  "\nCurrentOSIs64Bits:" + Environment.Is64BitOperatingSystem +
                                  "\nIs64BitsProcess:" + Environment.Is64BitProcess +
                                  "\nProcessorCount:" + Environment.ProcessorCount +
                                  "\nTickCount:" + Environment.TickCount +

                                  "\n\n//// Numbers ////" +

                                  "\nAllLoadedSprites:" + Sprite.AllSpritedLoaded_Names.Count +
                                  "\nAllLoadedFonts:" + Sprite.AllFontsLoaded_Names.Count +
                                  "\nFPS_string:" + Global.GameFPSstring +
                                  "\nFPS_raw:" + Global.GameFPSraw +
                                  "\nFPS_int:" + Global.GameFPSint +

                                  "\n\n//// Taiyou Settings ////" +

                                  "\nCodeOptimizationCacheEnabled:" + Global.CreateScriptOptimizationCache +

                                  "\n\n//// Versions ////" +

                                  "\nGameEngineBuild:" + Global.GameEngineBuild +
                                  "\nGamesRuntimeVersion:" + Global.GamesRuntimeVersion +
                                  "\nCurrentOSVersion:" + Environment.OSVersion +


                                  "\n\n### EXCEPTION FILE END ###";

            Directory.CreateDirectory(ExcFileDir); // Create the Directory
            File.WriteAllText(ExcFileDir + ExFileName, DetailedText); // Create the File

            // Reset Variables
            Game1.IsGameUpdateEnabled = false;
            Game1.UseRenderOrderMethod = false;
            Main.IsDrawAllowed = true;
            Global.IsMenuActivated = true;

        }

    }
}
