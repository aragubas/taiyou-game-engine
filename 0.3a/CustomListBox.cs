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
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;

namespace TaiyouGameEngine.Desktop
{
    public class CustomListBox
    {
        // Variaveis
        Rectangle Local;
        public int Local_X;
        public int Local_Y;
        public int Local_Width;
        public int Local_Height;
        public int Local_Opacity = 255;
        List<string> Control_Items;
        List<Rectangle> Control_ItemsRect = new List<Rectangle>();
        List<int> Control_ItemsRect_X = new List<int>();
        List<int> Control_ItemsRect_Y = new List<int>();
        List<int> Control_ItemsRect_Width = new List<int>();
        List<int> Control_ItemsRect_Height = new List<int>();
        List<int> Control_ItemsOpacity = new List<int>();
        List<int> Control_ItemsState = new List<int>();
        List<bool> Control_ItemsIsVisible = new List<bool>();
        public string Control_SelectedItem = "";
        public string Control_ClcikedItem = "";
        int RolagemY = 0;
        KeyboardState previusState;

        public CustomListBox(Rectangle Location, List<string> Items)
        {
            Local = Location;

            Local_X = Local.X;
            Local_Y = Local.Y;
            Local_Width = Local.Width;
            Local_Height = Local.Height;
            Control_Items = Items;

            for (int i = 0; i < Control_Items.Count; i++)
            {
                Control_ItemsRect.Add(new Rectangle(Local_X, Local_Y + i * 16, Control_Items[i].Length * 20, 14));
                Control_ItemsState.Add(3);
                Control_ItemsRect_X.Add(Local_X);
                Control_ItemsRect_Y.Add(Convert.ToInt32(Sprite.GetFont("10pt.xnb").MeasureString(Control_Items[i]).Y) + 5);
                Control_ItemsRect_Width.Add(Convert.ToInt32(Sprite.GetFont("10pt.xnb").MeasureString(Control_Items[i]).X));
                Control_ItemsRect_Height.Add(14);
                Control_ItemsOpacity.Add(255);
                Control_ItemsIsVisible.Add(true);
            }

        }
        int WaitLoop = 0;
        int ScrollAdder = 0;
        public void Update()
        {
            // The Key State
            KeyboardState state = Keyboard.GetState();

            // Update Rectangles
            Local = new Rectangle(Local_X, Local_Y, Local_Width, Local_Height);



            // Trigger the Key Event
            UserInput.KeyBoard keyTest = new UserInput.KeyBoard();

            if (state.IsKeyDown(Keys.Down) && previusState.IsKeyDown(Keys.Down))
            {
                if (ScrollAdder <= 10) { ScrollAdder += 1; };
                RolagemY += ScrollAdder;

            }
            else if (state.IsKeyDown(Keys.Up) && previusState.IsKeyDown(Keys.Up))
            {

                if (ScrollAdder <= 10) { ScrollAdder += 1; };
                RolagemY -= ScrollAdder;

            }
            else
            {
                if (ScrollAdder >= 1) { ScrollAdder -= 1; };
            }



            // Update Each Item
            for (int i = 0; i < Control_Items.Count; i++)
            {
                // Update the List Y
                int Spacer = Control_ItemsRect_Height[i] + 4;
                Control_ItemsRect_Y[i] = Local_Y + i * Spacer + RolagemY;



                // Trigger the Click of each item
                if (Control_ItemsIsVisible[i])
                {
                    if (Control_ItemsRect[i].Intersects(UserInput.Cursor.CursorPosition_Rect))
                    {
                        if (Control_ItemsRect[i].Intersects(UserInput.Cursor.Left_Cursor_ClickDown))
                        {
                            Control_ItemsState[i] = 2;
                            Control_ClcikedItem = Control_Items[i];

                        }
                        else
                        {
                            Control_ItemsState[i] = 1;
                            Control_SelectedItem = Control_Items[i];

                        }
                    }
                    else
                    {
                        Control_ItemsState[i] = 0;
                    }

                }



                Control_ItemsRect[i] = new Rectangle(Control_ItemsRect_X[i], Control_ItemsRect_Y[i], Control_ItemsRect_Width[i], Control_ItemsRect_Height[i]);

                // Update the Out-screen animation
                if (Control_ItemsRect[i].Y >= Local.Y && Control_ItemsRect[i].Y <= Local.Height)
                {
                    Control_ItemsIsVisible[i] = true;

                    if (Control_ItemsOpacity[i] <= 255)
                    {
                        Control_ItemsOpacity[i] += 25;
                        Control_ItemsRect_X[i] += 5;

                    }

                }
                else
                {
                    Control_ItemsState[i] = 3;
                    Control_ItemsIsVisible[i] = false;

                    if (Control_ItemsOpacity[i] >= 10)
                    {
                        Control_ItemsOpacity[i] -= 25;
                        Control_ItemsRect_X[i] -= 5;

                    }

                }




            }

            previusState = state;
        }




        public void Draw(SpriteBatch spriteBatch)
        {


            // Render the Background
            spriteBatch.Draw(Sprite.GetSprite("Base.png"), new Rectangle(Local_X - 2, Local_Y - 2, Local_Width + 4, Local_Height + 4),
                              Color.FromNonPremultiplied(255, 255, 255, Local_Opacity));
            spriteBatch.Draw(Sprite.GetSprite("Base.png"), new Rectangle(Local_X, Local_Y, Local_Width, Local_Height),
                              Color.FromNonPremultiplied(0,0,0, Local_Opacity));

            // Render the items
            for (int i = 0; i < Control_Items.Count; i++)
            {
                if (Control_ItemsState[i] == 0)
                {
                    spriteBatch.Draw(Sprite.GetSprite("Base.png"), new Rectangle(Control_ItemsRect_X[i] - 4, Control_ItemsRect_Y[i] - 4, Control_ItemsRect[i].Width + 8, Control_ItemsRect[i].Height + 8),
                                           Color.FromNonPremultiplied(255, 255, 255, Local_Opacity));

                    spriteBatch.Draw(Sprite.GetSprite("Base.png"), new Rectangle(Control_ItemsRect_X[i] - 2, Control_ItemsRect_Y[i] - 2, Control_ItemsRect[i].Width + 4, Control_ItemsRect[i].Height + 4), Color.FromNonPremultiplied(0, 0, 0, Local_Opacity));

                    spriteBatch.DrawString(Sprite.GetFont("10pt.xnb"), Control_Items[i], new Vector2(Control_ItemsRect[i].X, Control_ItemsRect[i].Y),
                                            Color.FromNonPremultiplied(200, 200, 200, Local_Opacity));

                }
                if (Control_ItemsState[i] == 1)
                {
                    spriteBatch.Draw(Sprite.GetSprite("Base.png"), new Rectangle(Control_ItemsRect_X[i] - 2, Control_ItemsRect_Y[i] - 2, Control_ItemsRect[i].Width + 4, Control_ItemsRect[i].Height + 4),
                                           Color.FromNonPremultiplied(255, 255, 255, Local_Opacity));

                    spriteBatch.Draw(Sprite.GetSprite("Base.png"), new Rectangle(Control_ItemsRect_X[i] - 1, Control_ItemsRect_Y[i] - 1, Control_ItemsRect[i].Width + 2, Control_ItemsRect[i].Height + 2), Color.FromNonPremultiplied(0, 0, 0, Local_Opacity));

                    spriteBatch.DrawString(Sprite.GetFont("10pt.xnb"), Control_Items[i], new Vector2(Control_ItemsRect[i].X, Control_ItemsRect[i].Y),
                                            Color.FromNonPremultiplied(200, 200, 200, Local_Opacity));

                }
                if (Control_ItemsState[i] == 2)
                {
                    spriteBatch.Draw(Sprite.GetSprite("Base.png"), new Rectangle(Control_ItemsRect_X[i] - 1, Control_ItemsRect_Y[i] - 1, Control_ItemsRect[i].Width + 2, Control_ItemsRect[i].Height + 2),
                                           Color.FromNonPremultiplied(255, 255, 255, Local_Opacity));

                    spriteBatch.Draw(Sprite.GetSprite("Base.png"), new Rectangle(Control_ItemsRect_X[i], Control_ItemsRect_Y[i], Control_ItemsRect[i].Width, Control_ItemsRect[i].Height), Color.FromNonPremultiplied(0, 0, 0, Local_Opacity));

                    spriteBatch.DrawString(Sprite.GetFont("10pt.xnb"), Control_Items[i], new Vector2(Control_ItemsRect[i].X, Control_ItemsRect[i].Y),
                                            Color.FromNonPremultiplied(200, 200, 200, Local_Opacity));

                }


                if (Control_ItemsState[i] == 3)
                {
                    spriteBatch.Draw(Sprite.GetSprite("Base.png"), new Rectangle(Control_ItemsRect_X[i] - 5, Control_ItemsRect_Y[i] - 5, Control_ItemsRect[i].Width, Control_ItemsRect[i].Height),
                                           Color.FromNonPremultiplied(0, 0, 0, Control_ItemsOpacity[i]));


                    spriteBatch.Draw(Sprite.GetSprite("Base.png"), Control_ItemsRect[i], Color.FromNonPremultiplied(30 + i, 40 + i, 37 + i, Control_ItemsOpacity[i]));


                    spriteBatch.DrawString(Sprite.GetFont("10pt.xnb"), Control_Items[i], new Vector2(Control_ItemsRect[i].X, Control_ItemsRect[i].Y),
                                                                     Color.FromNonPremultiplied(255,255,255, Control_ItemsOpacity[i]));

                }



            }
        }


        public void ClearList()
        {
            for (int i = 0; i < Control_Items.Count; i++)
            {
                Control_Items.Remove(Control_Items[i]);
                Control_ItemsRect.Remove(Control_ItemsRect[i]);
                Control_ItemsState.Remove(Control_ItemsState[i]);
                Control_ItemsRect_X.Remove(Control_ItemsRect_X[i]);
                Control_ItemsRect_Y.Remove(Control_ItemsRect_Y[i]);
                Control_ItemsRect_Width.Remove(Control_ItemsRect_Width[i]);
                Control_ItemsRect_Height.Remove(Control_ItemsRect_Height[i]);
                Control_ItemsOpacity.Remove(Control_ItemsOpacity[i]);
                Control_ItemsIsVisible.Remove(Control_ItemsIsVisible[i]);


            }
        }
    }
}
