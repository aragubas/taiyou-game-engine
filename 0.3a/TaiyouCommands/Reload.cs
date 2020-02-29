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

namespace TaiyouGameEngine.Desktop.TaiyouCommands
{
    public class Reload
    {
        // Reload all Taiyou Scripts



        public static void Initialize(string[] SplitedString)
        {
            // No arguments is required
            string Arg1 = "";
            try
            {
                Arg1 = SplitedString[1];

            }catch (Exception ex2) { }

            // Clear all Defined Variables
            TaiyouReader.GlobalVars_Int_Names.Clear();
            TaiyouReader.GlobalVars_Bool_Names.Clear();
            TaiyouReader.GlobalVars_Color_Names.Clear();
            TaiyouReader.GlobalVars_Int_Content.Clear();
            TaiyouReader.GlobalVars_Bool_Content.Clear();
            TaiyouReader.GlobalVars_String_Names.Clear();
            TaiyouReader.GlobalVars_Color_Content.Clear();
            TaiyouReader.GlobalVars_String_Content.Clear();
            TaiyouReader.GlobalVars_Rectangle_Names.Clear();
            TaiyouReader.GlobalVars_Rectangle_Content.Clear();
            TaiyouReader.GlobalVars_Float_Names.Clear();
            TaiyouReader.GlobalVars_Float_Content.Clear();
            TaiyouReader.AllTIYScriptOnScriptFolder.Clear();
            TaiyouReader.CustomTaiyouScriptsDescription.Clear();
            TaiyouReader.CustomTaiyouScriptsFile.Clear();
            TaiyouReader.CustomTaiyouScriptsName.Clear();
            TaiyouReader.GlobalVars_IntList_Names.Clear();
            TaiyouReader.GlobalVars_IntList_Content.Clear();
            TaiyouReader.GlobalVars_StringList_Names.Clear();
            TaiyouReader.GlobalVars_StringList_Content.Clear();
            TaiyouReader.GlobalVars_RectangleList_Names.Clear();
            TaiyouReader.GlobalVars_RectangleList_Content.Clear();
            TaiyouReader.GlobalVars_ColorList_Names.Clear();
            TaiyouReader.GlobalVars_ColorList_Content.Clear();
            TaiyouReader.GlobalVars_FloatList_Names.Clear();
            TaiyouReader.GlobalVars_FloatList_Content.Clear();

            // Clear the Sprite Render Quee
            Game1.RenderCommand_Name.Clear();
            Game1.RenderCommand_RectangleVar.Clear();
            Game1.RenderCommand_SpriteColor.Clear();
            Game1.RenderCommand_SpriteResource.Clear();
            Game1.RenderCommand_RenderOrder.Clear();
            Game1.RenderCommand_RenderRotation.Clear();
            Game1.RenderCommand_OrigionX.Clear();
            Game1.RenderCommand_OrigionY.Clear();
            Game1.RenderCommand_SpriteFlipState.Clear();

            // Clear the Text Render Quee
            Game1.TextRenderCommand_X.Clear();
            Game1.TextRenderCommand_Y.Clear();
            Game1.TextRenderCommand_Name.Clear();
            Game1.TextRenderCommand_Text.Clear();
            Game1.TextRenderCommand_Color.Clear();
            Game1.TextRenderCommand_SpriteFont.Clear();
            Game1.TextRenderCommand_RenderOrder.Clear();
            Game1.TextRenderCommand_RotationOriginX.Clear();
            Game1.TextRenderCommand_RotationOriginY.Clear();
            Game1.TextRenderCommand_Scale.Clear();
            Game1.TextRenderCommand_Rotation.Clear();
            Game1.TextRenderCommand_FlipState.Clear();

            // Clear All Events
            TriggerEventScript.AllEventsNames.Clear();
            TriggerEventScript.AllEventsScripts.Clear();

            // Stop all musics being played
            for (int i = 0; i < SoundtrackManager.Current_BGM_Name.Count; i++)
            {
                SoundtrackManager.Current_BGM_Instances[i].Stop();
            }

            SoundtrackManager.Current_BGM_Name.Clear();
            SoundtrackManager.Current_BGM_Command.Clear();
            SoundtrackManager.Current_BGM_Instances.Clear();

            // Clear some variables
            Game1.GameErrorOcorred = false;
            WindowManager.ShowCursor = false;
            Overlay_Error.ErrorListX = 0;
            Overlay_Error.ErrorListY = 0;
            Overlay_Error.ErrorListTextScale = 1f;
            Overlay_Error.ErrorListTextSize = 7;
            Overlay_Error.ErrorListMovSpeed = 5;
            Global.GameDataFolder = "";
            Global.RenderOrder = "BackToFront";
            LanguageSystem.LanguageFilesDirectory = "";
            LanguageSystem.AvaliableLangFiles.Clear();
            LanguageSystem.LanguageFilesContent.Clear();
            Global.TaiyouInitialized = false;
            Call.TaiyouFilesLinesFromMem_Data.Clear();
            Call.TaiyouFilesLinesFromMem_Names.Clear();
            Goto.TaiyouFilesLinesFromMem_Data.Clear();
            Goto.TaiyouFilesLinesFromMem_Names.Clear();

            try
            {
                // Just reload the Game
                if (Arg1 == "")
                {
                    TaiyouReader.Initialize(); // Re-Initialize Taiyou
                    Game1.RunAutoStartEvent = true;
                    Sprite.FindAllSprites(Game1.ThisGameObj, Global.ContentFolder + "/SOURCE");
                    SoundLoader.FindAllSounds(Global.ContentFolder + "/SOURCE");
                    SoundtrackManager.CreateBGMInstances();
                    LanguageSystem.InitializeLangSystem(Global.ContentFolder + "/SOURCE/LANG/");


                } 
                // Remove everthing related to the game, and go to menu
                if (Arg1 == "REMOVE")
                {
                    // Unload all sprites
                    //Game1.ThisGameObj.Content.Unload();
                    // Not Working

                    // Clear Variables
                    Global.ContentFolder = "";
                    Global.ContentFolderName = "";
                    Global.IsMenuActivated = true;
                    Game1.IsGameUpdateEnabled = true;
                    WindowManager.ChangeWindowPropertie("RESOLUTION", "800x600");

                }

            }
            catch (Exception ex)
            {
                string ExFileName = "(" + DateTime.Now.Month + "." + DateTime.Now.Day + "." + DateTime.Now.Year + ")" + DateTime.Now.Hour + "." + DateTime.Now.Minute + "." + DateTime.Now.Second + ".txt";
                string ErrTxt = "An exception has been created on AutoStart\nMessage: " + ex.Message + "\nHResult:" + ex.HResult + "\nSource: " + ex.Source + "\n\nPress Pause|Break key to restart.\n\n\nStackTrace:\n=== BEGIN STACK TRACE ===\n" + ex.StackTrace + "\n=== END STRACK TRACE ===" + "\n\nThis text has been saved on '" + Global.ContentFolderName + "/OPT/EXC/UPDATE/" + ExFileName + ")";


                try
                {
                    File.WriteAllText(Global.ContentFolderName + "/OPT/EXC/UPDATE/" + ExFileName, ErrTxt, new System.Text.ASCIIEncoding());
                    ErrTxt += "\nException report file created.";
                }
                catch (Exception ex2) { ErrTxt += "\nError while writing exception report file.\nMessage:" + ex2.Message + "\nHResult:" + ex2.HResult; }

                Overlay_Error.ErrorText = ErrTxt;
               
            }
            Game1.IsGameUpdateEnabled = true;
            Global.DrawScreen = true;

        }
    }
}
