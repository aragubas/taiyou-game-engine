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
using Microsoft.Xna.Framework.Input;

namespace TaiyouGameEngine.Desktop
{
    public class Overlay_Error
    {

        public static int ErrorListX;
        public static int ErrorListY;
        public static int ErrorListTextSize = 7;
        public static int ErrorListMovSpeed = 5;
        public static float ErrorListTextScale = 1;
        public static string ErrorText = "Exception Screen.";
        public static KeyboardState Keyboard_previousState;


        public static void Update()
        {
            KeyboardState state = Keyboard.GetState();

            #region Text Movement
            if (Keyboard_previousState.IsKeyDown(Keys.Up) && state.IsKeyDown(Keys.Up))
            {
                ErrorListY -= ErrorListMovSpeed;
            }

            if (Keyboard_previousState.IsKeyDown(Keys.Down) && state.IsKeyDown(Keys.Down))
            {
                ErrorListY += ErrorListMovSpeed;
            }
            
            if (Keyboard_previousState.IsKeyDown(Keys.Left) && state.IsKeyDown(Keys.Left))
            {
                ErrorListX -= ErrorListMovSpeed;
            }

            if (Keyboard_previousState.IsKeyDown(Keys.Right) && state.IsKeyDown(Keys.Right))
            {
                ErrorListX += ErrorListMovSpeed;
            }
            #endregion

            if (Keyboard_previousState.IsKeyDown(Keys.PageUp) && state.IsKeyUp(Keys.Insert))
            {
                if (ErrorListTextSize <= 20) { ErrorListTextSize += 1; };
            }

            if (Keyboard_previousState.IsKeyDown(Keys.PageDown) && state.IsKeyUp(Keys.Delete))
            {
                if (ErrorListTextSize >= 5) { ErrorListTextSize -= 1; };
            }

            if (Keyboard_previousState.IsKeyDown(Keys.Home) && state.IsKeyUp(Keys.PageUp))
            {
                if (ErrorListTextScale <= 20f) { ErrorListTextScale += 0.1f; };
            }

            if (Keyboard_previousState.IsKeyDown(Keys.End) && state.IsKeyUp(Keys.PageDown))
            {
                if (ErrorListTextScale >= 0.5f) { ErrorListTextScale -= 0.1f; };
            }

            // Remove all sprite on the same layers as the Exception Text
            try
            {
                for (int i = 0; i < Game1.RenderCommand_Name.Count; i++)
                {
                    if (Game1.RenderCommand_RenderOrder[i] <= 0.001f)
                    {
                        Game1.RenderCommand_Name.RemoveAt(i);
                        Game1.RenderCommand_OrigionX.RemoveAt(i);
                        Game1.RenderCommand_OrigionY.RemoveAt(i);
                        Game1.RenderCommand_RectangleVar.RemoveAt(i);
                        Game1.RenderCommand_RenderOrder.RemoveAt(i);
                        Game1.RenderCommand_SpriteColor.RemoveAt(i);
                        Game1.RenderCommand_RenderRotation.RemoveAt(i);
                        Game1.RenderCommand_SpriteResource.RemoveAt(i);

                    }
                }

                for (int i = 0; i < Game1.TextRenderCommand_Name.Count; i++)
                {
                    if (Game1.TextRenderCommand_RenderOrder[i] <= 0.001f)
                    {
                        Game1.TextRenderCommand_X.RemoveAt(i);
                        Game1.TextRenderCommand_Y.RemoveAt(i);
                        Game1.TextRenderCommand_Name.RemoveAt(i);
                        Game1.TextRenderCommand_Text.RemoveAt(i);
                        Game1.TextRenderCommand_Color.RemoveAt(i);
                        Game1.TextRenderCommand_Scale.RemoveAt(i);
                        Game1.TextRenderCommand_Rotation.RemoveAt(i);
                        Game1.TextRenderCommand_SpriteFont.RemoveAt(i);
                        Game1.TextRenderCommand_RenderOrder.RemoveAt(i);
                        Game1.TextRenderCommand_RotationOriginX.RemoveAt(i);
                        Game1.TextRenderCommand_RotationOriginY.RemoveAt(i);

                    }
                }
            } catch (Exception ex) { Console.WriteLine("Error while removing sprites from Render Quee:\n" + ex.Message); }


            WindowManager.ShowCursor = true;

            Keyboard_previousState = state;
        }

        public static void Draw(SpriteBatch spriteBatch)
        {
            // Render the Error text
            spriteBatch.DrawString(Sprite.GetFont(ErrorListTextSize + "pt.xnb"), ErrorText, new Vector2(ErrorListX, ErrorListY), Color.White,0f, Vector2.Zero, ErrorListTextScale, SpriteEffects.None, 0f);

            // Render the Background Box
            spriteBatch.Draw(Sprite.GetSprite("Base.png"), new Rectangle(ErrorListX - 2, ErrorListY - 2, Convert.ToInt32(Sprite.GetFont(ErrorListTextSize + "pt.xnb").MeasureString(ErrorText).X) + 4, Convert.ToInt32(Sprite.GetFont(ErrorListTextSize + "pt.xnb").MeasureString(ErrorText).Y) + 4),Rectangle.Empty, Color.Black,0f,Vector2.Zero,SpriteEffects.None,0.001f);

        }
    }
}
