/*
   ####### BEGIN APACHE 2.0 LICENSE #######
   Copyright 2019 Aragubas

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


namespace TaiyouScriptEngine.Desktop
{
    public static class Sprites
    {

        // Sprites Variables
        public static List<string> AllSpritedLoaded_Names = new List<string>();
        public static List<Texture2D> AllSpritedLoaded_Content = new List<Texture2D>();

        public static List<string> AllFontsLoaded_Names = new List<string>();
        public static List<SpriteFont> AllFontsLoaded_Content = new List<SpriteFont>();


        #region Load Functions
        // Load Sprite From File
        private static Texture2D LoadTexture2D_FromFile(Game gameObj, string FileLocation)
        {
            FileStream fileStream = new FileStream(FileLocation, FileMode.Open);
            Texture2D ValToReturn = Texture2D.FromStream(gameObj.GraphicsDevice, fileStream);
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

            AllSpritedLoaded_Content.Add(LoadTexture2D_FromFile(Game1.Reference, FileLocation));
            AllSpritedLoaded_Names.Add(SpriteFiltedName);

        
        }
        #endregion


        public static void FindAllSprites(Game gameObj, string SourceFolder, string FontsSourceFolder)
        {
            // First, we need to list all files on SPRITES directory
            string[] AllSprites = Directory.GetFiles(SourceFolder, "*.png", SearchOption.AllDirectories);
            Console.WriteLine("Sprite.FindAllSprites : Started");

             foreach (var file in AllSprites){
             FileInfo info = new FileInfo(file);
                string FileFullName = info.FullName;
                string SpriteFiltedName = FileFullName.Replace(Environment.CurrentDirectory, "").Replace(Global.SourceFolderFilter + "img/", "");

                int SpriteID = AllSpritedLoaded_Names.IndexOf(SpriteFiltedName);
                 
                if (SpriteID == -1 && info.Extension == ".png")
                {
                    Console.WriteLine(SpriteFiltedName);

                    AllSpritedLoaded_Content.Add(LoadTexture2D_FromFile(gameObj, FileFullName));
                    AllSpritedLoaded_Names.Add(SpriteFiltedName);

                    Console.WriteLine("FindAllSprites : Found[" + SpriteFiltedName + "]");


                }

            }

            // Load the Fonts
            string[] AllFonts = Directory.GetFiles(FontsSourceFolder);
            Console.WriteLine("Sprite.FindAllSprites : Finding Compiled FontFile...");

            foreach (var fontfile in AllFonts)
            {
                FileInfo inf = new FileInfo(fontfile);
                string FontFiltredName = inf.FullName.Replace(FontsSourceFolder, "");
                int FontID = AllFontsLoaded_Names.IndexOf(FontFiltredName);

                if (FontID == -1)
                {
                    if (inf.Extension == ".xnb")
                    {
                        AllFontsLoaded_Names.Add(FontFiltredName);

                        AllFontsLoaded_Content.Add(LoadSpriteFont(Game1.Reference, FontsSourceFolder + FontFiltredName.Replace(".xnb", "")));

                        Console.WriteLine("FindFont : Found[" + FontFiltredName + "]");

                    }
                }
            }

            Console.WriteLine("Sprite.FindAllSprites : Operation Completed.");


        }


        public static Texture2D GetSprite(string SpriteName)
        {
            if (AllSpritedLoaded_Names.IndexOf(SpriteName) == -1)
            {
                return LoadTexture2D_FromFile(Game1.Reference, Registry.ReadKeyValue("ERROR/MissingTexture"));
            }
            return AllSpritedLoaded_Content[AllSpritedLoaded_Names.IndexOf(SpriteName)]; // Return the correct sprite

        }

        public static SpriteFont GetFont(string FontName)
        {
            SpriteFont ValToReturn;
            int FontID = AllFontsLoaded_Names.IndexOf(FontName);

            if(FontID == -1) { throw new FileNotFoundException("The requested font(" + FontName + ") does not exist."); };

            ValToReturn = AllFontsLoaded_Content[FontID];


            return ValToReturn;
        }


    }
}
