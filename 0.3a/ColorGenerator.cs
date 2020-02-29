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
using Microsoft.Xna.Framework;

namespace TaiyouGameEngine.Desktop
{
    public class ColorGenerator
    {
        // Variaveis
        int ColorAnim_R = 5;
        int ColorAnim_G = 5;
        int ColorAnim_B = 5;
        string ColorAnim_R_State = "ADD";
        string ColorAnim_G_State = "ADD";
        string ColorAnim_B_State = "ADD";
        public Color ColorToReturn;

        int ColorAnimR_RanNum = 0;
        int ColorAnimG_RanNum = 0;
        int ColorAnimB_RanNum = 0;

        string ColorAnimR_RanState = "ADD";
        string ColorAnimG_RanState = "ADD";
        string ColorAnimB_RanState = "ADD";

        public void ColorRandom()
        {
            int ColorAnim_RanMod = RandomNumber(1, 6);

            if (ColorAnimR_RanNum >= 5) { ColorAnimR_RanState = "ADD"; }
            if (ColorAnimR_RanNum <= 5) { ColorAnimR_RanState = "DECREASE"; };

            if (ColorAnimG_RanNum >= 5) { ColorAnimG_RanState = "ADD"; }
            if (ColorAnimG_RanNum <= 5) { ColorAnimG_RanState = "DECREASE"; };

            if (ColorAnimB_RanNum >= 5) { ColorAnimB_RanState = "ADD"; }
            if (ColorAnimB_RanNum <= 5) { ColorAnimB_RanState = "DECREASE"; };


            ColorAnimR_RanNum = RandomNumber(0, 20);
            ColorAnimG_RanNum = RandomNumber(0, 20);
            ColorAnimB_RanNum = RandomNumber(0, 20);



            ColorAnim_R_State = ColorAnimR_RanState;
            ColorAnim_G_State = ColorAnimG_RanState;
            ColorAnim_B_State = ColorAnimB_RanState;





        }

        public void ColorAnimation()
        {
            if (ColorAnim_R >= 250) { ColorAnim_R = 250; };
            if (ColorAnim_G >= 250) { ColorAnim_G = 250; };
            if (ColorAnim_B >= 250) { ColorAnim_B = 250; };

            if (ColorAnim_R <= 10) { ColorAnim_R = 10; };
            if (ColorAnim_G <= 10) { ColorAnim_G = 10; };
            if (ColorAnim_B <= 10) { ColorAnim_B = 10; };

            if (ColorAnim_R_State == "ADD") { ColorAnim_R++; };
            if (ColorAnim_R_State == "DECREASE") { ColorAnim_R--; };

            if (ColorAnim_G_State == "ADD") { ColorAnim_G++; };
            if (ColorAnim_G_State == "DECREASE") { ColorAnim_G--; };

            if (ColorAnim_B_State == "ADD") { ColorAnim_B++; };
            if (ColorAnim_B_State == "DECREASE") { ColorAnim_B--; };

            ColorToReturn.R = Convert.ToByte(ColorAnim_R);
            ColorToReturn.G = Convert.ToByte(ColorAnim_G);
            ColorToReturn.B = Convert.ToByte(ColorAnim_B);
        }


        public int RandomNumber(int min, int max)
        {
            Random random = new Random();
            return random.Next(min, max);
        }


    }

}
