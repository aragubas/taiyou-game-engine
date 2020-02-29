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
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;

namespace TaiyouGameEngine.Desktop
{
    public class Sprite
    {

        // Sprites Variables
        public static List<string> AllSpritedLoaded_Names = new List<string>();
        public static List<Texture2D> AllSpritedLoaded_Content = new List<Texture2D>();

        public static List<string> AllFontsLoaded_Names = new List<string>();
        public static List<SpriteFont> AllFontsLoaded_Content = new List<SpriteFont>();


        #region Load Functions
        // Load Sprite From File
        private static Texture2D LoadTexture2D_FromFile(Game gameObj,string FileLocation)
        {
            Texture2D ValToReturn = new Texture2D(gameObj.GraphicsDevice,5,5);

            FileStream fileStream = new FileStream(FileLocation, FileMode.Open);
            ValToReturn = Texture2D.FromStream(gameObj.GraphicsDevice, fileStream);
            fileStream.Dispose();
           
            return ValToReturn;
        }

        // Load SpriteFont from File
        private static SpriteFont LoadSpriteFont(Game gameObj, string FileName)
        {
            SpriteFont ToLoad;

            ToLoad = gameObj.Content.Load<SpriteFont>(FileName);



            return ToLoad;
        }

        // Load Custom Sprite
        public static void LoadCustomSprite(string FileLocation)
        {
            string SpriteFiltedName = Path.GetFileName(FileLocation);
            Console.WriteLine(SpriteFiltedName);

            if (!File.Exists(FileLocation)) { return; }

            AllSpritedLoaded_Content.Add(LoadTexture2D_FromFile(Game1.ThisGameObj, FileLocation));
            AllSpritedLoaded_Names.Add(SpriteFiltedName);

        
        }
        #endregion


        public static void FindAllSprites(Game gameObj, string SourceFolder)
        {
            Game1.IsGameUpdateEnabled = false;
            Global.DrawScreen = false;
            // First, we need to list all files on SPRITES directory
            string[] AllSprites = Directory.GetFiles(SourceFolder + "/SPRITE/", "*.png*", SearchOption.AllDirectories);
            Console.WriteLine("FindAllSprites : Start");

             foreach (var file in AllSprites){
             FileInfo info = new FileInfo(file);
                // Do something with the Folder or just add them to a list via nameoflist.add();
                string SpriteFiltedName = info.FullName.Replace(SourceFolder + "/SPRITE/", "");
                int SpriteID = AllSpritedLoaded_Names.IndexOf(SpriteFiltedName);

                if (SpriteID == -1)
                {
                    if (info.Extension == ".png")
                    {
                     
                        AllSpritedLoaded_Content.Add(LoadTexture2D_FromFile(gameObj, SourceFolder + "/SPRITE/" + SpriteFiltedName));
                        AllSpritedLoaded_Names.Add(SpriteFiltedName);
                    
                        Console.WriteLine("FindAllSprites : Found[" + SpriteFiltedName + "]");

                    }

                }

            }

            // Load the Fonts
            string[] AllFonts = Directory.GetFiles(SourceFolder + "/FONT/");
            Console.WriteLine("FindAllSprites : FindAllFonts");

            foreach (var fontfile in AllFonts)
            {
                FileInfo inf = new FileInfo(fontfile);
                string FontFiltredName = inf.FullName.Replace(SourceFolder + "/FONT/", "");
                int FontID = AllFontsLoaded_Names.IndexOf(FontFiltredName);

                if (FontID == -1)
                {
                    if (inf.Extension == ".xnb")
                    {
                        AllFontsLoaded_Names.Add(FontFiltredName);

                        AllFontsLoaded_Content.Add(LoadSpriteFont(Game1.ThisGameObj, SourceFolder + "/FONT/" + FontFiltredName.Replace(".xnb","")));

                        Console.WriteLine("FindFont : Found[" + FontFiltredName + "]");

                    }
                }

                
            }


            Game1.IsGameUpdateEnabled = true;
            Global.DrawScreen = true;

        }


        public static Texture2D GetSprite(string SpriteName)
        {
            Texture2D SpriteToReturn;
            int SpriteID = AllSpritedLoaded_Names.IndexOf(SpriteName);

            if (SpriteID == -1)
            {
                SpriteToReturn = LoadTexture2D_FromFile(Game1.ThisGameObj, "Taiyou/HOME/SOURCE/SPRITE/MissingTexture.png");
            }
            else
            {
                SpriteToReturn = AllSpritedLoaded_Content[SpriteID]; // Return the correct sprite

            }


            return SpriteToReturn;
        }

        public static SpriteFont GetFont(string FontName)
        {
            SpriteFont ValToReturn;
            int FontID = AllFontsLoaded_Names.IndexOf(FontName);

            if(FontID == -1) { throw new FileNotFoundException("The requested font(" + FontName + ") does not exist."); };

            ValToReturn = AllFontsLoaded_Content[FontID];


            return ValToReturn;
        }


        // TODO Not Working Function
        public static void UnloadAllSprites()
        {
            Console.WriteLine("UnloadAllSprites : Initialize");
            bool IsAllContentUnloaded = false;

            Console.WriteLine(Game1.ThisGameObj.GraphicsDevice.Indices.BufferUsage);
            

            for (int i = 0; i < AllSpritedLoaded_Content.Count; i++)
            {
                if (AllSpritedLoaded_Content[i] != null)
                {
                    Console.WriteLine("UnloadAllSprites : Sprite [" + AllSpritedLoaded_Names[i] + "]");

                    AllSpritedLoaded_Content[i].Dispose();
                    AllSpritedLoaded_Content[i].GraphicsDevice.Dispose();
                    AllSpritedLoaded_Content[i].GraphicsDevice.PlatformClear(ClearOptions.Target,Vector4.Zero,0.0f,0);
                    AllSpritedLoaded_Content[i] = null;

                }
            }

            Console.WriteLine("UnloadAllSprites : Unloading Fonts...");

            for (int i = 0; i < AllFontsLoaded_Content.Count; i++)
            {
                if (AllFontsLoaded_Content[i] != null)
                {
                    Console.WriteLine("UnloadAllSprites : Font [" + AllSpritedLoaded_Names[i] + "]");

                    AllFontsLoaded_Content[i].Texture.Dispose();
                    AllFontsLoaded_Content[i].Texture.GraphicsDevice.Dispose();
                    AllFontsLoaded_Content[i] = null;

                }

            }

            Console.WriteLine("UnloadAllSprites : Clearing Lists...");

            AllSpritedLoaded_Names.Clear();
            AllFontsLoaded_Names.Clear();
            AllSpritedLoaded_Content.Clear();
            AllFontsLoaded_Content.Clear();

            Console.WriteLine("UnloadAllSprites : Loading Default Sprite Set...");

            FindAllSprites(Game1.ThisGameObj,Environment.CurrentDirectory + "/Taiyou/HOME/Source/");


        }


    }
}
