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
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;

namespace TaiyouGameEngine.Desktop
{
    public class WindowManager
    {
        // Vars
        public static string WindowTitle = "Taiyou Game Engine";
        public static int WindowW;
        public static int WindowH;
        public static bool ShowCursor;
        public static bool MaxFPSChanged = true;
        public static bool ResiziableWindow = false;
        public static bool HaveBorders = false;
        public static bool AllowAltF4 = false;
        public static int MaxFPS = 60;
        public static List<string> WindowProperties = new List<string>() { "TITLE", "MAX_FPS" , "RESIZIABLE_WINDOW","HAVE_BORDERS",
                                                                           "ALLOW_ALT_F4", "RESOLUTION", "TOGGLE_FULLSCREEN", "VSYNC",
                                                                           "MULTI_SAMPLE", "CURSOR_OFFSCREEN", "DEPTH_FORMAT", "RENDER_ORDER"  };

        public static void Update()
        {
            // Update Window Properties
            Game1.ThisGameObj.Window.Title = WindowTitle; // Set the Window title
            Game1.ThisGameObj.IsMouseVisible = ShowCursor; // Show/Hide the cursor
            WindowW = Game1.ThisGameObj.Window.ClientBounds.Width; // Get the window W
            WindowH = Game1.ThisGameObj.Window.ClientBounds.Height; // Get the window H

            if (!MaxFPSChanged)
            {
                MaxFPSChanged = true;
                if (MaxFPS > 1000) { throw new Exception("Max FPS is higher than 1000."); };
                Game1.ThisGameObj.TargetElapsedTime = TimeSpan.FromSeconds(1d / Convert.ToDouble(MaxFPS));

            }

            Game1.ThisGameObj.Window.AllowUserResizing = ResiziableWindow;
            Game1.ThisGameObj.Window.IsBorderless = !HaveBorders;
            Game1.ThisGameObj.Window.AllowAltF4 = AllowAltF4;
        }

        public static void ChangeWindowPropertie(string Propertie, string Value)
        {
            int PropertieListID = WindowProperties.IndexOf(Propertie);

            if (PropertieListID == -1) { throw new Exception("The window propertie [" + Propertie + "] does not exist."); }


            if (Propertie == "TITLE")
            {
                WindowTitle = Value;
            }if (Propertie == "MAX_FPS")
            {
                MaxFPSChanged = false;
                MaxFPS = Convert.ToInt32(Value);

            }
            if (Propertie == "RESIZIABLE_WINDOW")
            {
                ResiziableWindow = Convert.ToBoolean(Value);
            }if (Propertie == "HAVE_BORDERS")
            {
                HaveBorders = Convert.ToBoolean(Value);
            }
            if (Propertie == "ALLOW_ALT_F4")
            {
                AllowAltF4 = Convert.ToBoolean(Value);
            }
            if (Propertie == "RESOLUTION")
            {
                string[] SplitedString = Value.Split('x');
                // Values like 800x600


                Game1.ThisGraphicsObj.PreferredBackBufferWidth = Convert.ToInt32(SplitedString[0]);
                Game1.ThisGraphicsObj.PreferredBackBufferHeight = Convert.ToInt32(SplitedString[1]);
                Game1.ThisGraphicsObj.ApplyChanges();

            }
            if (Propertie == "TOGGLE_FULLSCREEN")
            {

                if (Value == "True")
                {
                    int MaxW = Game1.ThisGraphicsObj.GraphicsDevice.DisplayMode.Width;
                    int MaxH = Game1.ThisGraphicsObj.GraphicsDevice.DisplayMode.Height;
                    Game1.ThisGraphicsObj.PreferredBackBufferWidth = MaxW;
                    Game1.ThisGraphicsObj.PreferredBackBufferHeight = MaxH;

                    Game1.ThisGraphicsObj.ApplyChanges();

                    Game1.ThisGraphicsObj.IsFullScreen = true;

                }else if (Value == "False")
                {
                    Game1.ThisGraphicsObj.IsFullScreen = false;
                }
                else
                {
                    Game1.ThisGraphicsObj.ToggleFullScreen();

                    if (Game1.ThisGraphicsObj.IsFullScreen)
                    {
                        int MaxW = Game1.ThisGraphicsObj.GraphicsDevice.DisplayMode.Width;
                        int MaxH = Game1.ThisGraphicsObj.GraphicsDevice.DisplayMode.Height;
                        Game1.ThisGraphicsObj.PreferredBackBufferWidth = MaxW;
                        Game1.ThisGraphicsObj.PreferredBackBufferHeight = MaxH;
                        
                        Game1.ThisGraphicsObj.ApplyChanges();

                    }
                }



            }
            if (Propertie == "VSYNC")
            {
                Game1.ThisGraphicsObj.SynchronizeWithVerticalRetrace = Convert.ToBoolean(Value);
                Game1.ThisGraphicsObj.ApplyChanges();
            }

            if (Propertie == "MULTI_SAMPLE")
            {
                Game1.ThisGraphicsObj.PreferMultiSampling = Convert.ToBoolean(Value);
                Game1.ThisGraphicsObj.ApplyChanges();
            }

            if (Propertie == "CURSOR_OFFSCREEN")
            {
                UserInput.Cursor.PreventOffscreen = !Convert.ToBoolean(Value);
            }

            if (Propertie == "DEPTH_FORMAT")
            {
                string StringDepth = Value;
                DepthFormat NewDepthFormat = DepthFormat.None;

                if (Value == "16") { NewDepthFormat = DepthFormat.Depth16; }
                if (Value == "24") { NewDepthFormat = DepthFormat.Depth24; }
                if (Value == "24Stencil8") { NewDepthFormat = DepthFormat.Depth24Stencil8; }


                Game1.ThisGraphicsObj.PreferredDepthStencilFormat = NewDepthFormat;
                Game1.ThisGraphicsObj.ApplyChanges();

            }

            if (Propertie == "RENDER_ORDER")
            {
                if (Value == "FRONT_TO_BACK")
                {
                    Global.RenderOrder = "FrontToBack";
                }

                if (Value == "BACK_TO_FRONT")
                {
                    Global.RenderOrder = "BackToFront";
                }

                if (Value == "DEFERRED")
                {
                    Global.RenderOrder = "Deferred";
                }

                if (Value == "IMMEDIATE")
                {
                    Global.RenderOrder = "Immediate";
                }

                if (Value == "TEXTURE")
                {
                    Global.RenderOrder = "Texture";
                }

            }





        }


    }
}
