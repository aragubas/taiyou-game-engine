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
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;

namespace TaiyouGameEngine.Desktop.EngineMenu
{
    public class Screen_GameSelection // The MainMenu
    {
        static Rectangle Rectangle_TopBar = new Rectangle(0, 0, 800, 45);
        static Rectangle Rectangle_BottomBar = new Rectangle(0, 553, 800, 47);
        static Rectangle Rectangle_SelectedGameInfo = new Rectangle(390, 60, 380, 477);
        static Rectangle Rectangle_SelectedGameInfo_GameCover = new Rectangle(395,65,370,210);
        public static int GlobalOpacity = 0;
        public static int GlobalOpacityAnimationSpeed = 1;
        public static bool GlobalOpacity_AnimEnabled = true;
        public static bool AnimationWillClose = false;
        public static bool ChangeGame = false;
        public static bool IsGameOverlay = false;
        public static bool ReInitialize = false;
        public static int GlobalOpacity_AnimMode = 0;

        static Color WhiteColor;
        static string TopMenuText = "Main Menu";
        static string VersionMenuText = Global.GameEngineBuild;
        static CustomListBox InstalledGameList;
        public static string SelectedGame;
        static List<string> AllLoadedGameNames = new List<string>();
        static List<string> AllLoadedGameContentFolders = new List<string>();
        static List<string> AllLoadedGameVersions = new List<string>();
        static List<string> AllLoadedGameID = new List<string>();
        static int SelectedGameInfo_X_Divider = 255;
        static int SelectedGameInfo_X_AnimState = 1;
        static bool SelectedGameInfo_X_AnimEnabled = true;
        static int SelectedGameInfo_X_Divider_Speed = 0;
        static bool SelectecGameHasChanged = false;
        public static string GameDetailsText = "<- Select a game here.";
        static Texture2D SelectedGameTexture;
        static Custom_Button StartGameButton;
        static bool ScreenInitialized = false;
        static int ChangeGameDelay = 0;
        static Custom_Button IsGameOverlay_BackButton;
        static Custom_Button IsGameOverlay_BackToMenu;
        static ColorGenerator ColorGen;
        static int ColorGenTimeout = 0;
        static int PreviuslyTimeOut = 1000;
        static Random ColorGenRnd = new Random();

        public static void Draw(SpriteBatch spriteBatch)
        {
            // Draw the Background
            spriteBatch.Draw(Sprite.GetSprite("Base.png"), new Rectangle(0,0,WindowManager.WindowW,WindowManager.WindowH), null, Color.FromNonPremultiplied(0, 0, 0, GlobalOpacity - 20), 0f, Vector2.Zero, SpriteEffects.None, 0.9f);

           
            if (!IsGameOverlay)
            {
                // Draw the Top-Down bar [ with no gradient ]
                spriteBatch.Draw(Sprite.GetSprite("bar_bottom.png"), Rectangle_TopBar, null, Color.FromNonPremultiplied(255, 255, 255, GlobalOpacity - 50), 0f, Vector2.Zero, SpriteEffects.None, 1.0f);
                spriteBatch.Draw(Sprite.GetSprite("bar_top.png"), Rectangle_BottomBar, null, Color.FromNonPremultiplied(255, 255, 255, GlobalOpacity - 50), 0f, Vector2.Zero, SpriteEffects.None, 1.0f);


                // Draw the Game Selection
                #region Game Selection
                InstalledGameList.Draw(spriteBatch);


                spriteBatch.Draw(Sprite.GetSprite("Base.png"), new Rectangle(Rectangle_SelectedGameInfo.X - 2, Rectangle_SelectedGameInfo.Y - 2, Rectangle_SelectedGameInfo.Width + 4, Rectangle_SelectedGameInfo.Height + 4), null, Color.FromNonPremultiplied(255,255,255, GlobalOpacity), 0f, Vector2.Zero, SpriteEffects.None, 0.9f);
                spriteBatch.Draw(Sprite.GetSprite("Base.png"), Rectangle_SelectedGameInfo, null, Color.FromNonPremultiplied(0,0,0, GlobalOpacity), 0f, Vector2.Zero, SpriteEffects.None, 1.0f);

                spriteBatch.Draw(SelectedGameTexture, Rectangle_SelectedGameInfo_GameCover, null, WhiteColor, 0f, Vector2.Zero, SpriteEffects.None, 0.9f);

                if (SelectedGame != "" && IsGameOverlay == false) { StartGameButton.Draw(spriteBatch); }

                spriteBatch.DrawString(Sprite.GetFont("10pt.xnb"), GameDetailsText, new Vector2(Rectangle_SelectedGameInfo.X + 2, Rectangle_SelectedGameInfo.Y + 220), WhiteColor);

                #endregion

                // Render the Username Text on the Top
                // ### Draw the Logged User Text ###
                spriteBatch.DrawString(Sprite.GetFont("10pt.xnb"), Global.CurrentLoggedUser, new Vector2(WindowManager.WindowW - Sprite.GetFont("10pt.xnb").MeasureString(Global.CurrentLoggedUser).X - 5, Rectangle_TopBar.Y + Sprite.GetFont("10pt.xnb").MeasureString(Global.CurrentLoggedUser).Y + 2), WhiteColor);

                spriteBatch.Draw(Sprite.GetSprite("UserButton/1.png"), new Rectangle(Convert.ToInt32(WindowManager.WindowW - Sprite.GetFont("10pt.xnb").MeasureString(Global.CurrentLoggedUser).X - 42), Rectangle_TopBar.Y + 5, 32, 32), Color.White);

            }
            else
            {
                // Draw the Top-Down Bar [ with gradient ]
                spriteBatch.Draw(Sprite.GetSprite("bar_bottom.png"), Rectangle_TopBar, null, Color.FromNonPremultiplied(255, 255, 255, GlobalOpacity - 50), 0f, Vector2.Zero, SpriteEffects.None, 1.0f);
                spriteBatch.Draw(Sprite.GetSprite("bar_top.png"), Rectangle_BottomBar, null, Color.FromNonPremultiplied(255, 255, 255, GlobalOpacity - 50), 0f, Vector2.Zero, SpriteEffects.None, 1.0f);

                // ### Draw the Logged User Text ###
                spriteBatch.DrawString(Sprite.GetFont("10pt.xnb"), Global.CurrentLoggedUser, new Vector2(WindowManager.WindowW - Sprite.GetFont("10pt.xnb").MeasureString(Global.CurrentLoggedUser).X - 5, Rectangle_BottomBar.Y + Sprite.GetFont("10pt.xnb").MeasureString(Global.CurrentLoggedUser).Y + 2), WhiteColor);


                // Render the Close and Back to Menu Buttons
                IsGameOverlay_BackButton.Draw(spriteBatch);
                IsGameOverlay_BackToMenu.Draw(spriteBatch);

                // Render the User Image
                spriteBatch.Draw(Sprite.GetSprite("UserButton/1.png"), new Rectangle(Convert.ToInt32(WindowManager.WindowW - Sprite.GetFont("10pt.xnb").MeasureString(Global.CurrentLoggedUser).X - 42), Rectangle_BottomBar.Y + 5, 32, 32), Color.White);

            }

            // ### Top text ###
            spriteBatch.DrawString(Sprite.GetFont("25pt.xnb"), TopMenuText, new Vector2(7, Rectangle_TopBar.Y + 5), WhiteColor);

            // ### Version Text ###
            spriteBatch.DrawString(Sprite.GetFont("10pt.xnb"), VersionMenuText, new Vector2(7, Rectangle_BottomBar.Y + 17), WhiteColor);



        }




        public static void Update()
        {
            if (!ScreenInitialized) { ScreenInitialized = true;  Initialize(); }
            WhiteColor = Color.FromNonPremultiplied(255, 255, 255, GlobalOpacity);
            if (!IsGameOverlay) { Game1.ClearScreenColor = Color.FromNonPremultiplied(GlobalOpacity / 5, GlobalOpacity / 8, GlobalOpacity / 3, GlobalOpacity); TopMenuText = "Main Menu"; }
            if (IsGameOverlay) { TopMenuText = "In-Game Overlay"; }

            ColorGen.ColorAnimation();
            ColorGenTimeout += 1;

            if (ColorGenTimeout >= PreviuslyTimeOut)
            {
                ColorGenTimeout = 0;
                ColorGen.ColorRandom();

                PreviuslyTimeOut = ColorGenRnd.Next(0, 2500);
            }

            if (Global.IsLogged == false) { throw new Exception("The current user is not logged."); }

            UpdateLocations();
            UpdateScreenAnimation();
            UpdateSelectedGameInfoAnimation();
            UpdateSelectedGameList();


            #region Update the menu, when is InGame overlay
            if (IsGameOverlay)
            {
                IsGameOverlay_BackButton.Update();
                IsGameOverlay_BackToMenu.Update();

                IsGameOverlay_BackButton.Local_Opacity = GlobalOpacity;
                IsGameOverlay_BackButton.Local_X = Convert.ToInt32(WindowManager.WindowW - Sprite.GetFont("11pt.xnb").MeasureString("Close").X) - 10;
                IsGameOverlay_BackButton.Local_Y = Rectangle_TopBar.Y + 10;

                IsGameOverlay_BackToMenu.Local_Y = Rectangle_TopBar.Y + 10;
                IsGameOverlay_BackToMenu.Local_X = Convert.ToInt32(WindowManager.WindowW - Sprite.GetFont("11pt.xnb").MeasureString("Main Menu").X) - 100;
                IsGameOverlay_BackToMenu.Local_Opacity = GlobalOpacity;


                if (IsGameOverlay_BackButton.Local_ClickState == 2)
                {
                    GlobalOpacity_AnimEnabled = true;

                }

                if (IsGameOverlay_BackToMenu.Local_ClickState == 2)
                {
                    GlobalOpacity_AnimEnabled = true;
                    AnimationWillClose = true;

                    Game1.RunBackToMenu = true;

                }



            }

            #endregion

            #region Load the Selected Game
            if (ChangeGame && IsGameOverlay == false)
            {
                ChangeGameDelay += 1;

                if (ChangeGameDelay >= 75)
                {
                    // Reset some variables
                    EngineMenu.Main.IsDrawAllowed = false; // Disables the menu to draw
                    Global.IsMenuActivated = false; // Desactivate the Menu
                    Game1.UseRenderOrderMethod = true; // Change the Render Order Method to Null


                    // Change the Content Folder
                    Global.ContentFolder = Environment.CurrentDirectory + "/" + SelectedGame;
                    Global.ContentFolderName = SelectedGame;
                    // Load the Game Sprites 
                    Sprite.FindAllSprites(Game1.ThisGameObj, Global.ContentFolder + "/SOURCE");
                    // Change the Background to Black
                    Game1.ClearScreenColor = Color.Black;
                    Global.DrawScreen = true;
                    LanguageSystem.InitializeLangSystem(Global.ContentFolder + "/SOURCE/LANG/");
                    TaiyouReader.Initialize(); // Initialize the Taiyou


                    // Asociate the Default Events
                    Game1.RunAutoStartEvent = true;

                    ChangeGameDelay = 0;
                    ChangeGame = false;

                    Global.CurrentSelectedTitleName = AllLoadedGameNames[AllLoadedGameContentFolders.IndexOf(SelectedGame)];
                    Global.CurrentSelectedTitleID = AllLoadedGameID[AllLoadedGameContentFolders.IndexOf(SelectedGame)];
                    Global.CurrentSelectedTitleVersion = AllLoadedGameVersions[AllLoadedGameContentFolders.IndexOf(SelectedGame)];


                    // Reset the Selected Game Animation
                    GameDetailsText = "< -Select a game here.";
                    SelectedGame = "";


                    EngineMenu.Main.MenuCurrentScreen = -1; // Change the Current MENU screen to -1 [Desactivated]

                }


            }

            if (StartGameButton.Local_ClickState == 2 && SelectedGame != "" && IsGameOverlay == false)
            {
                GlobalOpacity_AnimEnabled = true;
                Global.CurrentSelectedTitleName = AllLoadedGameNames[AllLoadedGameContentFolders.IndexOf(SelectedGame)];
                Global.CurrentSelectedTitleID = AllLoadedGameID[AllLoadedGameContentFolders.IndexOf(SelectedGame)];
                Global.CurrentSelectedTitleVersion = AllLoadedGameVersions[AllLoadedGameContentFolders.IndexOf(SelectedGame)];

            }


        }
        #endregion

        #region Update Objects

        private static void UpdateSelectedGameList()
        {
            if (InstalledGameList.Control_ClcikedItem != SelectedGame) { SelectecGameHasChanged = true; SelectedGame = InstalledGameList.Control_ClcikedItem; }

            if (SelectedGame != "" && SelectecGameHasChanged == true)
            {
                SelectedGameInfo_X_AnimEnabled = true;
                int SelectedGameIndex = AllLoadedGameContentFolders.IndexOf(SelectedGame);

                if (SelectedGameInfo_X_AnimState == 1)
                {
                    GameDetailsText = "Game Title:\n" + AllLoadedGameNames[SelectedGameIndex] +
                                  "\n\nVersion:\n" + AllLoadedGameVersions[SelectedGameIndex] +
                                  "\n\nTitleID:\n" + AllLoadedGameID[SelectedGameIndex];


                    SelectedGameTexture = Sprite.GetSprite(AllLoadedGameID[SelectedGameIndex] + ".png");

                    SelectecGameHasChanged = false;
                }

            }
            if (IsGameOverlay == false)
            {
                StartGameButton.Update();
                InstalledGameList.Update();
                StartGameButton.Local_Opacity = GlobalOpacity;
                InstalledGameList.Local_Opacity = GlobalOpacity;
                InstalledGameList.Local_Y = Rectangle_TopBar.Y + 60;
                Rectangle_SelectedGameInfo.Y = Rectangle_TopBar.Y + 60;
                Rectangle_SelectedGameInfo_GameCover.X = Rectangle_SelectedGameInfo.X + 5;
                Rectangle_SelectedGameInfo_GameCover.Y = Rectangle_SelectedGameInfo.Y + 5;
                StartGameButton.Local_Y = Rectangle_SelectedGameInfo.Y + Rectangle_SelectedGameInfo.Height - Convert.ToInt32(Sprite.GetFont("11pt.xnb").MeasureString("Start Game").Y) - 10;

            }


        }

        private static void UpdateLocations()
        {
            // Update Rectangles & Locations
            Rectangle_TopBar = new Rectangle(0, GlobalOpacity - 250, WindowManager.WindowW, 47);
            Rectangle_BottomBar = new Rectangle(0, WindowManager.WindowH - GlobalOpacity + 203, WindowManager.WindowW, 47);
            Rectangle_SelectedGameInfo.X = WindowManager.WindowW - Rectangle_SelectedGameInfo.Width + SelectedGameInfo_X_Divider;
            if (IsGameOverlay == false) { StartGameButton.Local_X = Rectangle_SelectedGameInfo.X + Rectangle_SelectedGameInfo.Width - Convert.ToInt32(Sprite.GetFont("11pt.xnb").MeasureString("Start Game").X) - 10; }

        }

        private static void UpdateSelectedGameInfoAnimation()
        {

            if (SelectedGameInfo_X_AnimEnabled == true)
            {
                if (SelectedGameInfo_X_AnimState == 0) // Cycle Animation 1
                {
                    SelectedGameInfo_X_Divider_Speed += 3;
                    SelectedGameInfo_X_Divider += SelectedGameInfo_X_Divider_Speed;

                    if (SelectedGameInfo_X_Divider >= Rectangle_SelectedGameInfo.Width + 50)
                    {
                        SelectedGameInfo_X_Divider = Rectangle_SelectedGameInfo.Width + 50;
                        SelectedGameInfo_X_AnimState = 1;

                    }
                }
                if (SelectedGameInfo_X_AnimState == 1) // Cycle Animation 2
                {
                    SelectedGameInfo_X_Divider_Speed += 3;
                    SelectedGameInfo_X_Divider -= SelectedGameInfo_X_Divider_Speed;

                    if (SelectedGameInfo_X_Divider <= 0)
                    {
                        SelectedGameInfo_X_Divider_Speed = 0;
                        SelectedGameInfo_X_Divider = 0;
                        SelectedGameInfo_X_AnimState = 0;
                        SelectedGameInfo_X_AnimEnabled = false;
                    }

                }


            }


        }

        private static void UpdateScreenAnimation()
        {
            if (GlobalOpacity_AnimEnabled)
            {
                if (GlobalOpacity_AnimMode == 0)
                {
                    GlobalOpacityAnimationSpeed += 1;
                    GlobalOpacity += GlobalOpacityAnimationSpeed;

                    if (GlobalOpacity >= 255 - GlobalOpacityAnimationSpeed) { GlobalOpacity_AnimMode = 1; GlobalOpacity_AnimEnabled = false; GlobalOpacityAnimationSpeed = 0; }
                }
                if (GlobalOpacity_AnimMode == 1)
                {
                    GlobalOpacityAnimationSpeed += 1;
                    GlobalOpacity -= GlobalOpacityAnimationSpeed;

                    if (GlobalOpacity <= -GlobalOpacityAnimationSpeed)
                    {
                        GlobalOpacityAnimationSpeed = 0;
                        GlobalOpacity = -1;
                        GlobalOpacity_AnimMode = 0;
                        GlobalOpacity_AnimEnabled = false;
                        ChangeGame = true;

                        if (IsGameOverlay)
                        {
                            // Reset some Variables
                            Global.IsMenuActivated = false;
                            Main.IsDrawAllowed = false;
                            Game1.UseRenderOrderMethod = true;

                            Game1.RunOverlayClose = true;

                        }

                        if (AnimationWillClose && IsGameOverlay)
                        {
                            AnimationWillClose = false;

                            string[] SplitedString = { "Reload", "REMOVE" };
                            TaiyouCommands.Reload.Initialize(SplitedString);
                            Main.MenuCurrentScreen = 0;
                            Main.IsDrawAllowed = true;
                            Main.IsMenuActiaved = true;
                            Main.StartDelay = 0;
                            Main.InitializationCompleted = false;
                            EngineMenu.Screen_LicenseWarning.AnimationMode = 0;
                            EngineMenu.Screen_LicenseWarning.AnimationEnabled = true;
                            EngineMenu.Screen_LicenseWarning.AnimationCompleted = false;

                            IsGameOverlay = false;
                            ChangeGame = false;
                            GlobalOpacity_AnimEnabled = true;
                            GlobalOpacity = 0;
                            Game1.UseRenderOrderMethod = false;


                        }
                    }
                }

            }


        }

        #endregion


        #region Initialization Steps
        public static void Initialize()
        {

            ListGamesInstalled();
            InitializeObjects();
        }

        private static bool ValidateGameFolder(string GameFolder)
        {
            bool BooleanToReturn = true;

            Console.WriteLine("\nValidateGameFolder : Validating [" + GameFolder + "]...");

            string MetadataFileLocation = Environment.CurrentDirectory + "/" + GameFolder + "/metadata.cfg";
            if (!File.Exists(MetadataFileLocation)) { BooleanToReturn = false; return false; }
            Console.WriteLine("ValidateGameFolder : Metadata file exists.");

            var MetadataFileNumberLines = File.ReadAllLines(MetadataFileLocation).Length;
            Console.WriteLine("ValidateGameFolder : Metadata file has [" + MetadataFileNumberLines + "] lines.");

            if (MetadataFileNumberLines < 4) { BooleanToReturn = false;  return false; }

            if (!Directory.Exists(GameFolder + "/SCRIPTS/")) { BooleanToReturn = false; return false; };
            if (!Directory.Exists(GameFolder + "/SOURCE/")) { BooleanToReturn = false; return false; };
            if (!Directory.Exists(GameFolder + "/SOURCE/SPRITE/")) { BooleanToReturn = false; return false; };
            if (!Directory.Exists(GameFolder + "/SOURCE/LANG/")) { BooleanToReturn = false; return false; };
            if (!Directory.Exists(GameFolder + "/SOURCE/SOUND/")) { BooleanToReturn = false; return false; };
            if (!Directory.Exists(GameFolder + "/SOURCE/FONT/")) { BooleanToReturn = false; return false; };

            Console.WriteLine("ValidadeGameFolder : GameFolder [" + GameFolder + "] has been aproved.\n");
            return BooleanToReturn;
        }

        // Lists
        static List<string> AllInstalledGames = new List<string>();

        private static void ListGamesInstalled()
        {
            string[] Directories = Directory.GetDirectories(Environment.CurrentDirectory);

            // Clear all variables
            AllInstalledGames.Clear();
            AllLoadedGameID.Clear();
            AllLoadedGameNames.Clear();
            AllLoadedGameVersions.Clear();
            AllLoadedGameContentFolders.Clear();

            for (int i = 0; i < Directories.Length; i++)
            {
                string CurrentElement = Directories[i].Replace(Environment.CurrentDirectory + "/", "");

                if (CurrentElement != "Taiyou" && CurrentElement != "x64" && CurrentElement != "x86")
                {
                    if (ValidateGameFolder(CurrentElement) == true)
                    {
                        AllInstalledGames.Add(CurrentElement);
                    }
                    else
                    {
                        Console.WriteLine("The game [" + CurrentElement + "] was not aproved.");
                    }

                }
            }

            for (int i = 0; i < AllInstalledGames.Count; i++)
            {
                string GameTitle = "undefined";
                string GameVersion = "0.00a";
                string GameTitleID = "undefined";
                int Counter = 0;
                bool IsGameValid = true;
                string MetadataFileLocation = Environment.CurrentDirectory + "/" + AllInstalledGames[i] + "/metadata.cfg";

                // Load the metadata file
                var lines = File.ReadLines(MetadataFileLocation);
                foreach (var line in lines)
                {
                    Counter += 1;

                    if (Counter == 1) // Game Title
                    {
                        string[] SplitedArgs = line.Split(':');

                        GameTitle = SplitedArgs[1];

                        if (GameTitle.Length > 25)
                        {
                            GameTitle = GameTitle.Remove(25, GameTitle.Length - 25);
                            GameTitle += "...";
                        }
                    }
                    if (Counter == 2) // Game Title ID
                    {
                        string[] SplitedArgs = line.Split(':');

                        GameTitleID = SplitedArgs[1];
                    }
                    if (Counter == 3) // Game Version
                    {
                        string[] SplitedArgs = line.Split(':');

                        GameVersion = SplitedArgs[1];
                    }
                    if (Counter == 4) // Taiyou Runtime version
                    {
                        string[] SplitedArgs = line.Split(':');

                        if (SplitedArgs[1] == Global.GamesRuntimeVersion)
                        {
                            IsGameValid = true;
                        }
                    }

                    if (Counter < 4)
                    {
                        IsGameValid = false;
                    }


                }

                if (IsGameValid)
                {
                    Console.WriteLine("The Game ({0}) has been added to the GameList\nGameTitleID: {1}\nGameVersion: {2}", GameTitle, GameTitleID, GameVersion);

                    AllLoadedGameContentFolders.Add(AllInstalledGames[i]);
                    AllLoadedGameVersions.Add(GameVersion);
                    AllLoadedGameNames.Add(GameTitle);
                    AllLoadedGameID.Add(GameTitleID);

                    // Get the Game Cover
                    Sprite.LoadCustomSprite(Environment.CurrentDirectory + "/" + AllLoadedGameContentFolders[i] + "/" + AllLoadedGameID[i] + ".png");

                }

            }

        }

        private static void InitializeObjects()
        {
            SelectedGameTexture = Sprite.GetSprite("Base.png");
            StartGameButton = new Custom_Button(Rectangle_SelectedGameInfo.X + Rectangle_SelectedGameInfo.Width - Convert.ToInt32(Sprite.GetFont("11pt.xnb").MeasureString("Start Game").X) - 10, Rectangle_SelectedGameInfo.Y + Rectangle_SelectedGameInfo.Height - Convert.ToInt32(Sprite.GetFont("11pt.xnb").MeasureString("Start Game").Y) - 10, "Start Game", Color.Black, Color.White, Color.White);
            IsGameOverlay_BackButton = new Custom_Button(Convert.ToInt32(WindowManager.WindowW - Sprite.GetFont("11pt.xnb").MeasureString("Close").X) - 10, 10, "Close", Color.Black, Color.White, Color.White);
            IsGameOverlay_BackToMenu = new Custom_Button(Convert.ToInt32(WindowManager.WindowW - Sprite.GetFont("11pt.xnb").MeasureString("Main Menu").X) - 100, 10, "Main Menu", Color.Black, Color.White, Color.White);
            IsGameOverlay_BackButton.Local_Opacity = 0;
            IsGameOverlay_BackToMenu.Local_Opacity = 0;
            ColorGen = new ColorGenerator();

            InstalledGameList = new CustomListBox(new Rectangle(15, 60, 350, 477), AllInstalledGames);

        }


        #endregion


    }
}





