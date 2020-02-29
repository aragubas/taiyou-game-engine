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
using System.Globalization;

namespace TaiyouGameEngine.Desktop.TaiyouCommands
{
    public class TaiyouIF
    {
        // IF...


        public static void Initialize(string[] SplitedString)
        {
            string Arg1 = SplitedString[1]; // ConvertToCompare Type
            string Arg2 = SplitedString[2]; // Compare String 1
            string Arg3 = SplitedString[3]; // Compare Type
            string Arg4 = SplitedString[4]; // Compare String 2
            string Arg5 = SplitedString[5]; // Next Instruction
            if (SplitedString.Length < 5) { throw new Exception("TaiyouIF dont take less than 5 arguments."); }



            string NextCommandToExecute = "";

            /////////////////////////
            /// Float Comparators ///
            /////////////////////////

            if (Arg1.Equals("FLOAT"))
            {
                if (Arg3.Equals("=="))
                {
                    if (float.Parse(Arg2, CultureInfo.InvariantCulture.NumberFormat) == float.Parse(Arg4, CultureInfo.InvariantCulture.NumberFormat))
                    {
                        ThenRunOtherCommands();
                    }
                }
                if (Arg3.Equals("!="))
                {
                    if (float.Parse(Arg2, CultureInfo.InvariantCulture.NumberFormat) != float.Parse(Arg4, CultureInfo.InvariantCulture.NumberFormat))
                    {
                        ThenRunOtherCommands();
                    }
                }
                if (Arg3.Equals(">="))
                {
                    if (float.Parse(Arg2, CultureInfo.InvariantCulture.NumberFormat) >= float.Parse(Arg4, CultureInfo.InvariantCulture.NumberFormat))
                    {
                        ThenRunOtherCommands();
                    }
                }
                if (Arg3.Equals("<="))
                {
                    if (float.Parse(Arg2, CultureInfo.InvariantCulture.NumberFormat) <= float.Parse(Arg4, CultureInfo.InvariantCulture.NumberFormat))
                    {
                        ThenRunOtherCommands();
                    }
                }
                if (Arg3.Equals(">"))
                {
                    if (float.Parse(Arg2, CultureInfo.InvariantCulture.NumberFormat) > float.Parse(Arg4, CultureInfo.InvariantCulture.NumberFormat))
                    {
                        ThenRunOtherCommands();
                    }
                }
                if (Arg3.Equals("<"))
                {
                    if (float.Parse(Arg2, CultureInfo.InvariantCulture.NumberFormat) < float.Parse(Arg4, CultureInfo.InvariantCulture.NumberFormat))
                    {
                        ThenRunOtherCommands();
                    }
                }


            }


            //////////////////////
            /// Int Comparators //
            //////////////////////

            if (Arg1.Equals("INT"))
            {
                if (Arg3.Equals("=="))
                {
                    if (Convert.ToInt32(Arg2) == Convert.ToInt32(Arg4))
                    {
                        ThenRunOtherCommands();
                    }
                }
                if (Arg3.Equals("!="))
                {
                    if (Convert.ToInt32(Arg2) != Convert.ToInt32(Arg4))
                    {
                        ThenRunOtherCommands();
                    }
                }
                if (Arg3.Equals(">="))
                {
                    if (Convert.ToInt32(Arg2) >= Convert.ToInt32(Arg4))
                    {
                        ThenRunOtherCommands();
                    }
                }
                if (Arg3.Equals("<="))
                {
                    if (Convert.ToInt32(Arg2) <= Convert.ToInt32(Arg4))
                    {
                        ThenRunOtherCommands();
                    }
                }
                if (Arg3.Equals(">"))
                {
                    if (Convert.ToInt32(Arg2) > Convert.ToInt32(Arg4))
                    {
                        ThenRunOtherCommands();
                    }
                }
                if (Arg3.Equals("<"))
                {
                    if (Convert.ToInt32(Arg2) < Convert.ToInt32(Arg4))
                    {
                        ThenRunOtherCommands();
                    }
                }


            }


            //////////////////////////
            /// String Comparators ///
            //////////////////////////

            if (Arg1.Equals("STRING"))
            {
                if (Arg3.Equals("=="))
                {
                    if (Arg2 == Arg4)
                    {
                        ThenRunOtherCommands();
                    }
                }
                if (Arg3.Equals("!="))
                {
                    if (Arg2 != Arg4)
                    {
                        ThenRunOtherCommands();
                    }
                }



            }


            ///////////////////////////
            /// Boolean Comparators ///
            ///////////////////////////

            if (Arg1.Equals("BOOL"))
            {
                if (Arg3.Equals("=="))
                {
                    if (Convert.ToBoolean(Arg2) == Convert.ToBoolean(Arg4))
                    {
                        ThenRunOtherCommands();
                    }
                }
                if (Arg3.Equals("!="))
                {
                    if (Convert.ToBoolean(Arg2) != Convert.ToBoolean(Arg4))
                    {
                        ThenRunOtherCommands();
                    }
                }


            }


        }

        public static void ThenRunOtherCommands()
        {
            string AllText = "";

            for (int i = 5; i < TaiyouReader.SplitedString.Length; i++)
            {
                if (i < TaiyouReader.SplitedString.Length)
                {
                    AllText += TaiyouReader.SplitedString[i] + " ";
                }


            }


            string[] AllPieces = AllText.Split('|');

            for (int i = 0; i < AllPieces.Length; i++)
            {
                TaiyouReader.ReadAsync(AllPieces[i]);

            }

        }


    }


}
