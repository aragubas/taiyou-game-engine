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
using Microsoft.Xna.Framework.Audio;

namespace TaiyouScriptEngine.Desktop
{
    public class SoundLoader
    {
        public static List<string> AllLoadedSounds_Names = new List<string>();
        public static List<SoundEffect> AllLoadedSounds_Content = new List<SoundEffect>();


        public static void FindAllSounds(string SoundFolder)
        {
            // First, we need to list all files on SPRITES directory
            string[] AllSounds = Directory.GetFiles(SoundFolder, "*.wav*", SearchOption.AllDirectories);
            Console.WriteLine("FindAllSounds : Start");

            foreach (var file in AllSounds)
            {
                FileInfo info = new FileInfo(file);
                // Do something with the Folder or just add them to a list via nameoflist.add();
                string SoundFiltedName = info.FullName;
                SoundFiltedName = SoundFiltedName.Replace(Environment.CurrentDirectory + "/" + SoundFolder, "/");



                int SoundID = AllLoadedSounds_Names.IndexOf(SoundFiltedName);

                if (SoundID == -1)
                {
                    if (info.Extension == ".wav")
                    {
                        Console.WriteLine("FiltredName is: " + SoundFiltedName);

                        AllLoadedSounds_Content.Add(LoadSoundFromFile(SoundFolder + SoundFiltedName));
                        AllLoadedSounds_Names.Add(SoundFiltedName);

                        Console.WriteLine("FindAllSounds : Found[" + SoundFiltedName + "]");

                    }

                }

            }

        }

        public static SoundEffect LoadSoundFromFile(string FileName)
        {
            SoundEffect SoundToReturn;

            FileStream fileStream = null;
            fileStream = new FileStream(FileName, FileMode.Open);

            byte[] data = new byte[fileStream.Length];
            fileStream.Read(data, 0, data.Length);

            Stream stream = new MemoryStream(data);

            SoundToReturn = SoundEffect.FromStream(stream);
            fileStream.Dispose();

            return SoundToReturn;
        }






    }
}
