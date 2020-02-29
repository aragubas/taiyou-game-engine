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
namespace TaiyouGameEngine.Desktop.TaiyouCommands
{
    public class LanguageSystemManager
    {
        // Language System

        public static void Initialize(string[] SplitedArgs)
        {
            string Arg1 = SplitedArgs[1]; // Operation
            string Arg2 = SplitedArgs[2]; // Operation Arg 1

            if (Arg1.Equals("GET"))
            {
                // Arg2 == LangFileName
                // Arg3 == StringVarToReturn
                string Arg3 = SplitedArgs[3];

                string ValueToRetun = LanguageSystem.GetLangTranslation(Arg2);
                int StringVarReturnIndex = TaiyouReader.GlobalVars_String_Names.IndexOf(Arg3);
                TaiyouReader.GlobalVars_String_Content[StringVarReturnIndex] = ValueToRetun;

            }
            if (Arg1.Equals("SET_LANGUAGE"))
            {
                // Arg2 = LanguageCode
                LanguageSystem.CurrentLanguage = Arg2;
            }


        }


    }
}
