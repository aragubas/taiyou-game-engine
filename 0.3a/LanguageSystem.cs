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

namespace TaiyouGameEngine.Desktop
{
    public class LanguageSystem
    {
        public static List<string> AvaliableLangFiles = new List<string>() { };
        public static List<string> LanguageFilesContent = new List<string>() { };

        public static string LanguageFilesDirectory = "";
        public static string CurrentLanguage = "en";

        public static void InitializeLangSystem(string LanguageFilesDir)
        {
            LanguageFilesDirectory = LanguageFilesDir;
            AvaliableLangFiles.Clear();
            LanguageFilesContent.Clear();

            // Initialize the Lang Files

            string Dir = LanguageFilesDirectory;
            Directory.CreateDirectory(Dir); // Creates the Directory, if not exists

            DirectoryInfo d = new DirectoryInfo(Dir); // Get Directory Info
            FileInfo[] Files = d.GetFiles("*.lang"); //Getting LangData files

            foreach (FileInfo file in Files)
            {
                string str = "";

                str = file.Name;
                string ReadedData = File.ReadAllText(LanguageFilesDirectory + str);
                string CorrectString = ReadedData.Replace(Environment.NewLine, "");

                AvaliableLangFiles.Add(str.Replace(".lang", ""));
                LanguageFilesContent.Add(CorrectString);


            }

        }

        public static string GetLangTranslation(string LangFile)
        {
            string ValueToReturn = LangFile;
            int FileNameIndex = 0;
            string FileNameString = "";
            string FileDirectory = "";
            string LangCode = CurrentLanguage;


            try
            {
                FileNameIndex = AvaliableLangFiles.IndexOf(LangFile);
                FileNameString = AvaliableLangFiles[FileNameIndex];
                FileDirectory = LanguageFilesDirectory + FileNameString + ".lang";
                LangCode = CurrentLanguage;


                string ReadedData = LanguageFilesContent[FileNameIndex];
                string[] SliptedData = ReadedData.Split('|');
                List<string> AllFileContents = new List<string>();

                for (int i = 0; i < SliptedData.Length; i++)
                {
                    AllFileContents.Add(SliptedData[i]);
                }

                int LangCodeIndexOf = AllFileContents.IndexOf(LangCode);

                // Character Replacements

                ValueToReturn = AllFileContents[LangCodeIndexOf + 1].Replace("%N", Environment.NewLine);


            }
            catch (Exception ex)
            {
                ValueToReturn = LangFile;

            }


            return ValueToReturn;
        }


    }
}
