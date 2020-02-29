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
    public class DirectoryExists
    {
        // Verify if a Directory Exists

        public static void Initialize(string[] SplitedString)
        {
            string Arg1 = SplitedString[1]; // Directory to Check
            string Arg2 = SplitedString[2]; // Boolean Var to return value
            if (SplitedString.Length < 2) { throw new Exception("DirectoryExists dont take less than 2 arguments."); }

            string DirectoryOfData = Global.GameDataFolder;

            // IF the game is trying to write to the .reserved directory
            if (Arg1.StartsWith(".reserved", StringComparison.CurrentCulture)) { throw new Exception("Access to the [.reserved] is denied."); }


            int VarToReturn = TaiyouReader.GlobalVars_Bool_Names.IndexOf(Arg2);
            if (VarToReturn == -1) { throw new Exception("The boolean var [" + Arg2 + "] does not exist."); }

            TaiyouReader.GlobalVars_Bool_Content[VarToReturn] = Directory.Exists(DirectoryOfData);


        }
    }
}
