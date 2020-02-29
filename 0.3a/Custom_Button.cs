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
using Microsoft.Xna.Framework.Graphics;

namespace TaiyouGameEngine.Desktop
{
    public class Custom_Button
    {
        // Variaveis
        Rectangle Local_Rectangle;
        public int Local_X;
        public int Local_Y;
        int Local_W;
        int Local_H;
        public Color Local_BGCOLOR;
        public Color Local_FGCOLOR;
        public Color Local_TextCOLOR;
        public int Local_ClickState;
        public string Local_Text;
        public int Local_Opacity;
        public SpriteFont spriteFont = Sprite.GetFont("11pt.xnb");


        public Custom_Button(int PositionX, int PositionY, string ButtonText, Color ButtonBGColor, Color ButtonFGColor, Color TextColor)
        {
            Local_Rectangle = new Rectangle(0, 0, 0, 0);
            Local_X = PositionX;
            Local_Y = PositionY;
            Local_W = 0;
            Local_H = 0;
            Local_ClickState = 0;
            Local_Text = ButtonText;
            Local_Opacity = 255;
            Local_BGCOLOR = ButtonBGColor;
            Local_FGCOLOR = ButtonFGColor;
            Local_TextCOLOR = TextColor;
        }

        public void Draw(SpriteBatch spriteBatch)
        {

            if (Local_ClickState == 0)
            {
                spriteBatch.Draw(Sprite.GetSprite("Base.png"), new Rectangle(Local_X - 4, Local_Y - 4, Local_W + 8, Local_H + 8), Color.FromNonPremultiplied(Local_FGCOLOR.R, Local_FGCOLOR.G, Local_FGCOLOR.B, Local_Opacity - 50));


                spriteBatch.Draw(Sprite.GetSprite("Base.png"), new Rectangle(Local_X - 2, Local_Y - 2,Local_W + 4 ,Local_H + 4), Color.FromNonPremultiplied(Local_BGCOLOR.R, Local_BGCOLOR.G, Local_BGCOLOR.B, Local_Opacity));


                spriteBatch.DrawString(spriteFont, Local_Text, new Vector2(Local_X + 1, Local_Y + 2), Color.FromNonPremultiplied(Local_TextCOLOR.R, Local_TextCOLOR.G, Local_TextCOLOR.B, Local_Opacity));
            }
            if (Local_ClickState == 1 || Local_ClickState == 2)
            {
                spriteBatch.Draw(Sprite.GetSprite("Base.png"), new Rectangle(Local_X - 4, Local_Y - 4, Local_W + 8, Local_H + 8), Color.FromNonPremultiplied(Local_FGCOLOR.R + 10, Local_FGCOLOR.G + 10, Local_FGCOLOR.B + 10, Local_Opacity - 50));

                spriteBatch.Draw(Sprite.GetSprite("Base.png"), new Rectangle(Local_X - 1, Local_Y - 1, Local_W + 2, Local_H + 2), Color.FromNonPremultiplied(Local_BGCOLOR.R, Local_BGCOLOR.G, Local_BGCOLOR.B, Local_Opacity));

                spriteBatch.DrawString(spriteFont, Local_Text, new Vector2(Local_X + 1, Local_Y + 1), Color.FromNonPremultiplied(Local_TextCOLOR.R, Local_TextCOLOR.G, Local_TextCOLOR.B, Local_Opacity));
            }


        }

        public void Update()
        {

            Local_Rectangle = new Rectangle(Local_X, Local_Y, Local_W, Local_H);

            Local_W = Convert.ToInt32(spriteFont.MeasureString(Local_Text).X + 1);
            Local_H = Convert.ToInt32(spriteFont.MeasureString(Local_Text).Y);


                if (Local_Rectangle.Intersects(UserInput.Cursor.Left_Cursor_ClickDown))
                {
                    Local_ClickState = 1;
                }
                else if (Local_Rectangle.Intersects(UserInput.Cursor.Left_Cursor_ClickUp))
                {
                    Local_ClickState = 2;
                }
                else
                {
                    Local_ClickState = 0;
                }

          
        }

    }
}
