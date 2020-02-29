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

namespace TaiyouGameEngine.Desktop
{
    public class Global
    {
        #region Game Options / Others
        // Options
        public static string GameName;
        public static string CurrentOSName = Convert.ToString(Environment.OSVersion);
        public static string CurrentLanguage = "en-US";
        public static bool TaiyouInitialized = false;
        public static string GameEngineBuild = "Pre-Alpha 0.3a";
        public static string GamesRuntimeVersion = "0.3a";
        public static bool Engine_ResetKey = false;
        public static bool Engine_DebugRender = false;
        public static bool DrawScreen = true;
        public static string GameFPSstring = "0.00";
        public static float GameFPSraw = 0.00f;
        public static int GameFPSint = 0;
        public static string UpdateFPSstring = "0.00";
        public static float UpdateFPSraw = 0.00f;

        public static string RenderOrder = "BackToFront";
        public static bool IsMenuActivated = true;
        public static bool IsLowLevelDebugEnabled = false;

        #endregion

        #region Taiyou Options
        public static bool CreateScriptOptimizationCache = true;

        #endregion

        #region Menu Options
        public static bool PauseWhenInactive = false;
        public static bool PreventOffscrenCursor = false;
        public static bool TemporaryUser = false;
        public static int MenuMaxFPS = 60;


        #endregion

        #region Current Selected Game Variables
        public static string CurrentSelectedTitleID = "";
        public static string CurrentSelectedTitleName = "";
        public static string CurrentSelectedTitleVersion = "";
        public static string ContentFolder = "";
        public static string ContentFolderName = "";
        public static string GameDataFolder = "";
        public static string GameCompilation = "";


        #endregion

        #region User Variables
        public static bool IsUsersExistent = false;
        public static bool IsLogged = false;
        public static string CurrentLoggedUser = "";
        public static string CurrentLoggedPassword = "";


        #endregion

    }
}
