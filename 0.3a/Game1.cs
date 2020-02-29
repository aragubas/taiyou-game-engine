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
using System.IO;
using System.Threading;
using System.Windows.Forms;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;
using TaiyouGameEngine.Desktop.UserInput;

namespace TaiyouGameEngine.Desktop
{
    /// <summary>
    /// This is the main type for your game.
    /// </summary>
    public class Game1 : Game
    {
        GraphicsDeviceManager graphics;
        SpriteBatch spriteBatch;
        public static Game ThisGameObj;
        public static GraphicsDeviceManager ThisGraphicsObj;
        public static bool IsGameUpdateEnabled = false;
        public static bool GameErrorOcorred = false;
        public static KeyboardState previousState;
        public static bool UseRenderOrderMethod = false;
        public static bool RunBackToMenu = false;
        public static bool RunOverlayClose = false;
        public static bool RunOverlayOpen = false;
        public static bool RunAutoStartEvent = false;

        public Game1()
        {
            graphics = new GraphicsDeviceManager(this);
            Content.RootDirectory = Global.ContentFolder;
        }

        /// <summary>
        /// Allows the game to perform any initialization it needs to before starting to run.
        /// This is where it can query for any required services and load any non-graphic
        /// related content.  Calling base.Initialize will enumerate through any components
        /// and initialize them as well.
        /// </summary>
        protected override void Initialize()
        {
            // TODO: Add your initialization logic here
            ThisGameObj = this;
            ThisGraphicsObj = graphics;

            IsFixedTimeStep = true;

            Console.WriteLine("Game : Initialize");

            UserInput.KeyBoard.previousState = Keyboard.GetState();
            base.Initialize();
        }

        /// <summary>
        /// LoadContent will be called once per game and is the place to load
        /// all of your content.
        /// </summary>
        protected override void LoadContent()
        {
            // Create a new SpriteBatch, which can be used to draw textures.
            spriteBatch = new SpriteBatch(GraphicsDevice);
            Console.WriteLine("Game : Load Content");


            ThisGameObj = this;
            ThisGraphicsObj = graphics;

            // Load Sprites
            Sprite.FindAllSprites(this, Environment.CurrentDirectory + "/Taiyou/HOME/SOURCE");

            // Load Sounds
            SoundLoader.FindAllSounds(Environment.CurrentDirectory + "/Taiyou/HOME/SOURCE");
            SoundtrackManager.CreateBGMInstances();

            ////////////////////////////#Login to a Temporary User
            /// Temporary user Login ///#
            ////////////////////////////#
            if (Global.TemporaryUser == true)
            {
                Global.IsUsersExistent = true;
                Global.CurrentLoggedUser = "temp";
                Global.CurrentLoggedPassword = "temp";
                Global.IsLogged = true;
                EngineMenu.Screen_GameSelection.Initialize();
                EngineMenu.Main.MenuCurrentScreen = 1;
                }
            

        }

        /// <summary>
        /// UnloadContent will be called once per game and is the place to unload
        /// game-specific content.
        /// </summary>
        protected override void UnloadContent()
        {
            // TODO: Unload any non ContentManager content here
            Console.WriteLine("Game : Unload Content");


        }

        protected override void OnActivated(object sender, EventArgs args)
        {
            Console.WriteLine("Game : OnActivated");

            if (!Global.IsMenuActivated)
            {
                TriggerEventScript.CheckEvent("GameEngine.WindowActivated");

            }





            base.OnActivated(sender, args);
        }

        protected override void OnDeactivated(object sender, EventArgs args)
        {
            Console.WriteLine("Game : OnDeactivated");

            if (!Global.IsMenuActivated)
            {
                TriggerEventScript.CheckEvent("GameEngine.WindowDeactivated");
            }




            base.OnDeactivated(sender, args);
        }

        protected override void OnExiting(object sender, EventArgs args)
        {
            Console.WriteLine("Game : OnExiting");


            TriggerEventScript.CheckEvent("GameEngine.Exiting");


            base.OnExiting(sender, args);
        }


        /// <summary>
        /// Allows the game to run logic such as updating the world,
        /// checking for collisions, gathering input, and playing audio.
        /// </summary>
        /// <param name="gameTime">Provides a snapshot of timing values.</param>
        protected override void Update(GameTime gameTime)
        {
            // TODO: Update the global variables
            ThisGameObj = this;
            ThisGraphicsObj = graphics;
            KeyboardState state = Keyboard.GetState();

            // Main Engine update Function
            try
            {
                // Update the Menu
                EngineMenu.Main.Update();
                // Update the user input
                UserInput.Cursor.Update();
                KeyBoard.Update();

                if (IsGameUpdateEnabled)
                {
                    // Run the AutoStart script first
                    if (RunAutoStartEvent)
                    {
                        RunAutoStartEvent = false;

                        TaiyouCommands.Call.Initialize("AutoStart");


                    }

                    if (!Global.IsMenuActivated)
                    {

                        // Update the Game Code
                        TaiyouCommands.Call.Initialize("GameUpdate");

                        // Update global Vars
                        TaiyouReader.UpdateGlobalVars();


                        // Update the Soundtrack                
                        SoundtrackManager.Update();

                    }

                    // Update Menu Events
                    #region Update Menu Events
                    if (RunOverlayClose)
                    {
                        RunOverlayClose = false;

                        TriggerEventScript.CheckEvent("GameOverlay.Close");
                    }
                    if (RunOverlayOpen)
                    {
                        RunOverlayOpen = false;

                        TriggerEventScript.CheckEvent("GameOverlay.Open");
                    }
                    if (RunBackToMenu)
                    {
                        RunBackToMenu = false;

                        TriggerEventScript.CheckEvent("GameOverlay.BackToMenu");
                    }
                    #endregion

                    // If true, restart everthing when pressed Pause/Break
                    if (Global.Engine_ResetKey)
                    {
                        if (previousState.IsKeyDown(Microsoft.Xna.Framework.Input.Keys.Pause) && state.IsKeyUp(Microsoft.Xna.Framework.Input.Keys.Pause))
                        {
                            TaiyouReader.ReadAsync("Reload");
                        }

                    }


                }

            }
            catch (Exception ex)
            {
                ThrowGameException(ex, "GameUpdate");

            }

            // Trigger the Scroll Key to Open Menu
            if (previousState.IsKeyDown(Microsoft.Xna.Framework.Input.Keys.Scroll) && state.IsKeyUp(Microsoft.Xna.Framework.Input.Keys.Scroll) && Global.ContentFolder != "" && Global.IsMenuActivated == false && IsGameUpdateEnabled == true)
            {
                TriggerEventScript.CheckEvent("GameOverlay.Open");

                Global.IsMenuActivated = true;
                EngineMenu.Main.StartDelay = 0;
                EngineMenu.Main.MenuCurrentScreen = 1;
                EngineMenu.Main.IsMenuActiaved = true;
                EngineMenu.Main.IsDrawAllowed = true;
                UseRenderOrderMethod = false;

                EngineMenu.Screen_GameSelection.SelectedGame = "";

                EngineMenu.Screen_GameSelection.GlobalOpacity = 0;
                EngineMenu.Screen_GameSelection.GlobalOpacity_AnimMode = 0;
                EngineMenu.Screen_GameSelection.GlobalOpacity_AnimEnabled = true;
                EngineMenu.Screen_GameSelection.IsGameOverlay = true;

                WindowManager.ChangeWindowPropertie("MAX_FPS", Convert.ToString(Global.MenuMaxFPS));

            }

            // Back to Menu when a error occours
            if (previousState.IsKeyDown(Microsoft.Xna.Framework.Input.Keys.Scroll) && state.IsKeyUp(Microsoft.Xna.Framework.Input.Keys.Scroll) && GameErrorOcorred == true && Global.IsMenuActivated == false)
            {
                string[] SplitedString = { "Reload", "REMOVE" };
                TaiyouCommands.Reload.Initialize(SplitedString);
                EngineMenu.Main.WindowProps();

                WindowManager.ChangeWindowPropertie("RESOLUTION", "800x600");
                WindowManager.ChangeWindowPropertie("TOGGLE_FULLSCREEN", "False");


                Global.ContentFolder = "";
                Global.ContentFolderName = "";

                Global.IsMenuActivated = true;
                EngineMenu.Main.MenuCurrentScreen = 0;
                EngineMenu.Main.Initialize();
                EngineMenu.Main.StartDelay = 0;
                EngineMenu.Main.IsMenuActiaved = true;
                EngineMenu.Main.IsDrawAllowed = true;
                EngineMenu.Screen_GameSelection.SelectedGame = "";
                EngineMenu.Screen_GameSelection.GlobalOpacity = 0;
                EngineMenu.Screen_GameSelection.GlobalOpacity_AnimMode = 0;
                EngineMenu.Screen_GameSelection.GlobalOpacity_AnimEnabled = true;
                EngineMenu.Screen_GameSelection.IsGameOverlay = false;
                EngineMenu.Screen_LicenseWarning.AnimationMode = 0;
                EngineMenu.Screen_LicenseWarning.AnimationEnabled = true;
                EngineMenu.Screen_LicenseWarning.AnimationCompleted = false;
                UseRenderOrderMethod = false;
                GameErrorOcorred = false;
                Global.DrawScreen = true;
                IsGameUpdateEnabled = true;
                RunBackToMenu = false;
                RunOverlayOpen = false;
                RunOverlayClose = false;
                RunAutoStartEvent = false;
                

            }

            if (!IsGameUpdateEnabled && Global.IsMenuActivated == false)
            {
                if (previousState.IsKeyDown(Microsoft.Xna.Framework.Input.Keys.Pause) && state.IsKeyUp(Microsoft.Xna.Framework.Input.Keys.Pause))
                {
                    TaiyouReader.ReadAsync("Reload");
                }

            }

            // Update the Windows Properties
            WindowManager.Update();

            #region Calculate the FPS
            float frameRate = 1 / (float)gameTime.ElapsedGameTime.TotalSeconds; //Calculate the FPS
            if (frameRate <= 10)
            {
                Global.UpdateFPSstring = frameRate.ToString("0.00");
            }
            if (frameRate <= 100 && frameRate >= 10)
            {
                Global.UpdateFPSstring = frameRate.ToString("00.00");
            }
            if (frameRate >= 100 && frameRate <= 1000)
            {
                Global.UpdateFPSstring = frameRate.ToString("000.00");
            }
            if (frameRate >= 1000)
            {
                Global.UpdateFPSstring = frameRate.ToString("0000.00");
            }
            Global.UpdateFPSraw = frameRate;

            #endregion


            if (GameErrorOcorred) { Overlay_Error.Update(); }
            previousState = state;
            base.Update(gameTime);
        }

        public static void ThrowGameException(Exception ex, string ErrorPartString)
        {
            string ExcFileDir = Environment.CurrentDirectory + "/Taiyou/OPT/EXC/" + Global.ContentFolderName + "/" + Global.CurrentSelectedTitleID + "/" + Global.CurrentSelectedTitleVersion + "/" + ErrorPartString;
            string ExFileName = "(" + DateTime.Now.Month + "." + DateTime.Now.Day + "." + DateTime.Now.Year + ")" + DateTime.Now.Hour + "." + DateTime.Now.Minute + "." + DateTime.Now.Second + ".txt";
            string ErrTxt = "An exception has been created on " + ErrorPartString + "\nMessage: " + ex.Message + "\nHResult:" + ex.HResult + "\nSource: " + ex.Source + "\n\nPress Pause|Break key to restart.\nPress SCROLL_LOCK to back to Menu\n\n\nStackTrace:\n=== BEGIN STACK TRACE ===\n" + ex.StackTrace + "\n=== END STRACK TRACE ===" + "\n\nThis text has been saved on [" + ExcFileDir + "]";
            Console.WriteLine(ErrTxt);

            if (!Global.IsMenuActivated)
            {

                try
                {
                    Directory.CreateDirectory(ExcFileDir);
                    File.WriteAllText(ExcFileDir + "/" + ExFileName, ErrTxt, new System.Text.ASCIIEncoding());
                    ErrTxt += "\nException report file created.";
                }
                catch (Exception ex2) { ErrTxt += "\nError while writing exception report file.\nMessage:" + ex2.Message + "\nHResult:" + ex2.HResult; }

                Overlay_Error.ErrorText = ErrTxt;
                IsGameUpdateEnabled = false;
                GameErrorOcorred = true;
                UseRenderOrderMethod = true;

            }

        }

        // Render _image_ Quee
        public static List<string> RenderCommand_Name = new List<string>();
        public static List<string> RenderCommand_RectangleVar = new List<string>();
        public static List<string> RenderCommand_SpriteResource = new List<string>();
        public static List<string> RenderCommand_SpriteFlipState = new List<string>();
        public static List<Color> RenderCommand_SpriteColor = new List<Color>();
        public static List<float> RenderCommand_RenderOrder = new List<float>();
        public static List<float> RenderCommand_RenderRotation = new List<float>();
        public static List<int> RenderCommand_OrigionX = new List<int>();
        public static List<int> RenderCommand_OrigionY = new List<int>();

        // Render _text_ Quee
        public static List<string> TextRenderCommand_Name = new List<string>();
        public static List<string> TextRenderCommand_SpriteFont = new List<string>();
        public static List<string> TextRenderCommand_FlipState = new List<string>();
        public static List<int> TextRenderCommand_X = new List<int>();
        public static List<int> TextRenderCommand_Y = new List<int>();
        public static List<Color> TextRenderCommand_Color = new List<Color>();
        public static List<string> TextRenderCommand_Text = new List<string>();
        public static List<float> TextRenderCommand_RenderOrder = new List<float>();
        public static List<float> TextRenderCommand_Rotation = new List<float>();
        public static List<int> TextRenderCommand_RotationOriginX = new List<int>();
        public static List<int> TextRenderCommand_RotationOriginY = new List<int>();
        public static List<float> TextRenderCommand_Scale = new List<float>();


        // RenderProperties
        public static Color ClearScreenColor = Color.Black;

        public static void AddRenderQuee(string Name, string RectVarName, string SpriteResource, Color SpriteColor, float RenderOrder, float RenderRotation, int RotationOrigionX = 0, int RotationOrigionY = 0, string SpriteFlip = "NONE")
        {
            int IsObjectExistent = RenderCommand_Name.IndexOf(Name);

            if (IsObjectExistent != -1) { return; };

            RenderCommand_Name.Add(Name);
            RenderCommand_RectangleVar.Add(RectVarName);
            RenderCommand_SpriteResource.Add(SpriteResource);
            RenderCommand_SpriteColor.Add(SpriteColor);
            RenderCommand_RenderOrder.Add(RenderOrder);
            RenderCommand_RenderRotation.Add(RenderRotation);
            RenderCommand_OrigionX.Add(RotationOrigionX);
            RenderCommand_OrigionY.Add(RotationOrigionY);
            RenderCommand_SpriteFlipState.Add(SpriteFlip);



        }

        public static void AddTextRenderQuee(string Name, string Text, string FontResource, Color Color, int X, int Y, float RenderOrder, float Rotation = 0f,int RotationOriginX = 0, int RotationOriginY = 0, float Scale = 1.0f, string FlipState = "NONE")
        {
            int IsObjectExistent = TextRenderCommand_Name.IndexOf(Name);

            if (IsObjectExistent != -1) { return; };

            TextRenderCommand_Name.Add(Name);
            TextRenderCommand_Text.Add(Text);
            TextRenderCommand_Color.Add(Color);
            TextRenderCommand_SpriteFont.Add(FontResource);
            TextRenderCommand_X.Add(X);
            TextRenderCommand_Y.Add(Y);
            TextRenderCommand_RenderOrder.Add(RenderOrder);
            TextRenderCommand_Rotation.Add(Rotation);
            TextRenderCommand_Scale.Add(Scale);
            TextRenderCommand_RotationOriginX.Add(RotationOriginX);
            TextRenderCommand_RotationOriginY.Add(RotationOriginY);
            TextRenderCommand_FlipState.Add(FlipState);

        }

        protected override void Draw(GameTime gameTime)
        {
            GraphicsDevice.Clear(ClearScreenColor);
            
            if (UseRenderOrderMethod)
            {
                SpriteSortMode CurrentSortMode = SpriteSortMode.BackToFront;

                if (Global.RenderOrder == "BackToFront")
                {
                    CurrentSortMode = SpriteSortMode.BackToFront;

                }
                if (Global.RenderOrder == "FrontToBack")
                {
                    CurrentSortMode = SpriteSortMode.FrontToBack;
                }

                if (Global.RenderOrder == "Deferred")
                {
                    CurrentSortMode = SpriteSortMode.Deferred;
                }

                if (Global.RenderOrder == "Immediate")
                {
                    CurrentSortMode = SpriteSortMode.Immediate;
                }

                if (Global.RenderOrder == "Texture")
                {
                    CurrentSortMode = SpriteSortMode.Texture;
                }

                spriteBatch.Begin(CurrentSortMode, null, null, null, null, null);
            }
            else
            {
                spriteBatch.Begin(SpriteSortMode.Immediate,null,null,null,null,null);
            }

            // Draw everthing on the Render/Text Quee
            #region Draw everthing on the Render/Text Quee
            try
            {
                if (Global.DrawScreen)
                {
                    for (int i = 0; i < RenderCommand_Name.Count; i++)
                    {
                        string SpriteResourceName = RenderCommand_Name[i]; // Get the sprite resource
                        Rectangle SpriteRectangle = TaiyouReader.GlobalVars_Rectangle_Content[TaiyouReader.GlobalVars_Rectangle_Names.IndexOf(RenderCommand_RectangleVar[i])]; ; // Get the sprite resource
                        Texture2D SpriteTexture = Sprite.GetSprite(RenderCommand_SpriteResource[i]);
                        Color SpriteColor = RenderCommand_SpriteColor[i];
                        float RenderOrder = RenderCommand_RenderOrder[i]; // de 0.0 a 1.0
                        float RenderRotation = RenderCommand_RenderRotation[i]; // de 0.0 a 1.0
                        Vector2 RotationOrigin = new Vector2(RenderCommand_OrigionX[i], RenderCommand_OrigionY[i]);
                        SpriteEffects SpriteFlipState = SpriteEffects.None;

                        if (RenderCommand_SpriteFlipState[i].Equals("FLIP_HORIZONTALLY"))
                        {
                            SpriteFlipState = SpriteEffects.FlipHorizontally;
                        }
                        else if (RenderCommand_SpriteFlipState[i].Equals("FLIP_VERTICALLY"))
                        {
                            SpriteFlipState = SpriteEffects.FlipVertically;
                        }
                        else if (!RenderCommand_SpriteFlipState[i].Equals("NONE"))
                        {
                            throw new Exception("Error while rendering the Sprite Element [" + SpriteResourceName + "]:\nThe flip state [" + RenderCommand_SpriteFlipState[i] + "] is invalid.");

                        }

                        if (DrawSquaresDebug)
                        {
                            int SpriteLocX = SpriteRectangle.X - 2;
                            int SpriteLocY = SpriteRectangle.Y - 2;
                            int SpriteLocW = SpriteRectangle.Width + 4;
                            int SpriteLocH = SpriteRectangle.Height + 4;
                            int BoxBorderSize = 2;
                            int DebugTextFontSize = 5;

                            spriteBatch.Draw(Sprite.GetSprite("Base.png"), new Rectangle(SpriteLocX, SpriteLocY, SpriteLocW, BoxBorderSize), Color.Red);
                            spriteBatch.Draw(Sprite.GetSprite("Base.png"), new Rectangle(SpriteLocX + SpriteRectangle.Width, SpriteLocY, BoxBorderSize, SpriteLocH), Color.Red);
                            spriteBatch.Draw(Sprite.GetSprite("Base.png"), new Rectangle(SpriteLocX, SpriteLocY + SpriteLocH, SpriteLocW, BoxBorderSize), Color.Red);
                            spriteBatch.Draw(Sprite.GetSprite("Base.png"), new Rectangle(SpriteLocX, SpriteLocY, BoxBorderSize, SpriteLocH), Color.Red);
                            spriteBatch.DrawString(Sprite.GetFont(DebugTextFontSize + "pt.xnb"), SpriteResourceName, new Vector2(SpriteLocX, SpriteLocY - Sprite.GetFont(DebugTextFontSize + "pt.xnb").MeasureString(SpriteResourceName).Y + 5), Color.White);
                        }
                        spriteBatch.Draw(SpriteTexture, SpriteRectangle, SpriteTexture.Bounds, SpriteColor, RenderRotation, RotationOrigin, SpriteFlipState, RenderOrder); // And Finally, render the sprite.
                                                                                                                                                                              //texture, position, null, Color.White, 0, Vector2.Zero, SpriteEffects.None, 0.1f
                    }

                    for (int i = 0; i < TextRenderCommand_Name.Count; i++)
                    {
                        string TextRenderName = TextRenderCommand_Name[i];
                        int Xlocation = TextRenderCommand_X[i];
                        int Ylocation = TextRenderCommand_Y[i];
                        Color TextColor = TextRenderCommand_Color[i];
                        string TextString = TextRenderCommand_Text[i];
                        SpriteFont TextSpriteFont = Sprite.GetFont(TextRenderCommand_SpriteFont[i]);
                        float RenderRotation = TextRenderCommand_Rotation[i];
                        Vector2 RotationOrigin = new Vector2(TextRenderCommand_RotationOriginX[i], TextRenderCommand_RotationOriginY[i]);
                        float Scale = TextRenderCommand_Scale[i];
                        float RenderOrder = TextRenderCommand_RenderOrder[i];
                        SpriteEffects SpriteFlipState = SpriteEffects.None;
                        if (TextRenderCommand_FlipState[i].Equals("FLIP_HORIZONTALLY"))
                        {
                            SpriteFlipState = SpriteEffects.FlipHorizontally;
                        }
                        else if (TextRenderCommand_FlipState[i].Equals("FLIP_VERTICALLY"))
                        {
                            SpriteFlipState = SpriteEffects.FlipVertically;
                        }
                        else if (!TextRenderCommand_FlipState[i].Equals("NONE"))
                        {
                            throw new Exception("Error while rendering the Text Element [" + TextRenderName + "]:\nThe flip state [" + TextRenderCommand_FlipState[i] + "] is invalid.");

                        }


                        spriteBatch.DrawString(TextSpriteFont, TextString, new Vector2(Xlocation, Ylocation), TextColor, RenderRotation, RotationOrigin, Scale, SpriteFlipState, RenderOrder);
                    }


                }

            }
            catch (Exception ex)
            {
                Global.DrawScreen = false;

                ThrowGameException(ex, "GameUpdate");

            }

            #endregion

            if (GameErrorOcorred) { Overlay_Error.Draw(spriteBatch); }  // Draw the error overlay

            // Draw the Menu
            EngineMenu.Main.Draw(spriteBatch);


            // Debug Render
            if (Global.Engine_DebugRender)
            {
                RenderDebugHUD(spriteBatch);

            }

            spriteBatch.End();

            #region Calculate the Render FPS
            float frameRate = 1 / (float)gameTime.ElapsedGameTime.TotalSeconds; //Calculate the Render FPS
            if (frameRate <= 10)
            {
                Global.GameFPSstring = frameRate.ToString("0.00");
            }
            if (frameRate <= 100 && frameRate >= 10)
            {
                Global.GameFPSstring = frameRate.ToString("00.00");
            }
            if (frameRate >= 100 && frameRate <= 1000)
            {
                Global.GameFPSstring = frameRate.ToString("000.00");
            }
            if (frameRate >= 1000)
            {
                Global.GameFPSstring = frameRate.ToString("0000.00");
            }
            Global.GameFPSraw = frameRate;
            Global.GameFPSint = Convert.ToInt32(frameRate);

            #endregion


            base.Draw(gameTime);
        }







        static bool DrawVariablesDebug = false;
        static bool DrawSquaresDebug = false;
        static bool RenderQueeDebug = true;

        static KeyboardState oldState = Keyboard.GetState();
        private static void RenderDebugHUD(SpriteBatch spriteBatch)
        {
            KeyboardState thisState = Keyboard.GetState();

            // Draw the Infos Text
            if (RenderQueeDebug)
            {
                string DebugText = "##[FPS]##" + "\n" +
                                   "RenderFPS: " +  Global.GameFPSstring + "\n" +
                                   "UpdateFPS: " + Global.UpdateFPSstring + "\n" +
                                   "##[RenderQuee]##" + "\n" +
                                   "ActiveSpriteRenderObjs: " + RenderCommand_Name.Count + "\n" +
                                   "ActiveTextRenderObjs: " + TextRenderCommand_Name.Count + "\n\n##[SpriteRes]##\n" +
                                   "AllSpritesLoaded:" + Sprite.AllSpritedLoaded_Names.Count + "\n" +
                                   "AllFontsLoaded:" + Sprite.AllFontsLoaded_Names.Count + "\n\n##[SoundsRes]##\n" +
                                   "AllSoundsLoaded:" + SoundLoader.AllLoadedSounds_Names.Count + "\n\n##[LangRes]##\n" +
                                   "AllLangFilesLoaded:" + LanguageSystem.AvaliableLangFiles.Count + "\n\n##[DebugsEnables]##\n" +
                                   "VariablesDebug(F10):" + DrawVariablesDebug + "\n" +
                                   "SquaresDebug(F11)" + DrawSquaresDebug + "\n" +
                                   "LowLevelDebug(F12):" + Global.IsLowLevelDebugEnabled + "\n\n##[Taiyou]##\n" +
                                   "TaiyouInitialized:" + Global.TaiyouInitialized + "\n" +
                                   "AllScriptsLoaded:" + TaiyouReader.AllTIYScriptOnScriptFolder.Count;

                spriteBatch.DrawString(Sprite.GetFont("7pt.xnb"), DebugText, new Vector2(3, 3), Color.Black, 0f, Vector2.Zero, 1f, SpriteEffects.None, 0.0f);
                spriteBatch.DrawString(Sprite.GetFont("7pt.xnb"), DebugText, new Vector2(2, 2), Color.White, 0f, Vector2.Zero, 1f, SpriteEffects.None, 0.0f);

            }

            // Debug Keys
            if (thisState.IsKeyUp(Microsoft.Xna.Framework.Input.Keys.F9) && oldState.IsKeyDown(Microsoft.Xna.Framework.Input.Keys.F9))
            {
                if (RenderQueeDebug == false) { RenderQueeDebug = true; } else { RenderQueeDebug = false; }
            }
            if (thisState.IsKeyUp(Microsoft.Xna.Framework.Input.Keys.F10) && oldState.IsKeyDown(Microsoft.Xna.Framework.Input.Keys.F10))
            {
                if (DrawVariablesDebug == false) { DrawVariablesDebug = true; } else { DrawVariablesDebug = false; }
            }
            if (thisState.IsKeyUp(Microsoft.Xna.Framework.Input.Keys.F11) && oldState.IsKeyDown(Microsoft.Xna.Framework.Input.Keys.F11))
            {
                if (DrawSquaresDebug == false) { DrawSquaresDebug = true; } else { DrawSquaresDebug = false; }
            }
            if (thisState.IsKeyUp(Microsoft.Xna.Framework.Input.Keys.F12) && oldState.IsKeyDown(Microsoft.Xna.Framework.Input.Keys.F12))
            {
                if (Global.IsLowLevelDebugEnabled == false) { Global.IsLowLevelDebugEnabled = true; } else { Global.IsLowLevelDebugEnabled = false; }
            }


            if (DrawVariablesDebug)
            {
                string DebugText_Variables = "StringVars:" + TaiyouReader.GlobalVars_String_Names.Count + "\n" +
                                           "\nBoolVars:" + TaiyouReader.GlobalVars_Bool_Names.Count + "\n" +
                                           "\nIntVariables:" + TaiyouReader.GlobalVars_Int_Names.Count + "\n" +
                                           "\nFloatVariables:" + TaiyouReader.GlobalVars_Float_Names.Count + "\n" +
                                           "\nRectangleVariables:" + TaiyouReader.GlobalVars_Rectangle_Names.Count + "\n" +
                                           "\nColorVariables:" + TaiyouReader.GlobalVars_Color_Names.Count + "\n" +
                                           "\n##List Variables##" + "\n" +
                                           "\nStringLists:" + TaiyouReader.GlobalVars_StringList_Names.Count + "\n" +
                                           "\nBoolLists:" + TaiyouReader.GlobalVars_BooleanList_Names.Count + "\n" +
                                           "\nIntLists:" + TaiyouReader.GlobalVars_IntList_Names.Count + "\n" +
                                           "\nFloatLists:" + TaiyouReader.GlobalVars_FloatList_Names.Count + "\n" +
                                           "\nRectangleLists:" + TaiyouReader.GlobalVars_RectangleList_Names.Count + "\n" +
                                           "\nColorLists:" + TaiyouReader.GlobalVars_ColorList_Names.Count;

                spriteBatch.DrawString(Sprite.GetFont("7pt.xnb"), DebugText_Variables, new Vector2(WindowManager.WindowW - Sprite.GetFont("7pt.xnb").MeasureString(DebugText_Variables).X - 2, 2), Color.Red, 0f, Vector2.Zero, 1f, SpriteEffects.None, 0f);

            }

            oldState = thisState;
        }




    }
}

