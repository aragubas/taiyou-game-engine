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
    public class StringOperation
    {



        public static void Initialize(string[] SplitedString)
        {
            string Agr1 = SplitedString[1]; // String Var Name
            string Agr2 = SplitedString[2]; // Operation Type
            string Agr3 = SplitedString[3]; // Operation Value
            if (SplitedString.Length < 3) { throw new Exception("StringOperation dont take less than 3 arguments."); }

            int StringIndex = TaiyouReader.GlobalVars_String_Names.IndexOf(Agr1);
            string Arg3AllText = "";
            if (StringIndex == -1) { throw new Exception("The string variable [" + Agr1 + "] does not exist."); }

            for (int i = 3; i < SplitedString.Length; i++)
            {
                Arg3AllText += SplitedString[i] + " "; 
            }

            if (Agr2.Equals("ADD"))
            {
                TaiyouReader.GlobalVars_String_Content[StringIndex] += Arg3AllText;
            }
            if (Agr2.Equals("REPLACE"))
            {
                string[] ReplaceCommand = Arg3AllText.Split('|');

                string OldChar = ReplaceCommand[0];
                string NewChar = ReplaceCommand[1];


                TaiyouReader.GlobalVars_String_Content[StringIndex].Replace(OldChar, NewChar);
            }



        }


    }
}
