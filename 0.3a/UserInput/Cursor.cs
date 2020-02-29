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
using Microsoft.Xna.Framework.Input;

namespace TaiyouGameEngine.Desktop.UserInput
{
    public class Cursor
    {
        // Variaveis
        public static int CursorSelected = 0;
        public static ButtonState Left_ButtonState;
        public static ButtonState Right_ButtonState;
        public static int Cursor_Prescision = 1;
        public static int Cursor_X = 50;
        public static int Cursor_Y = 50;
        static MouseState CurrentState;
        public static Rectangle Left_Cursor_ClickDown;
        public static Rectangle Left_Cursor_ClickUp;
        public static Rectangle Right_Cursor_ClickDown;
        public static Rectangle Right_Cursor_ClickUp;
        public static Rectangle Cursor_Rect;
        public static Rectangle CursorPosition_Rect;
        public static bool PreventOffscreen = true;
        public static int CursorOffset = 0;

        static int TimePassed_Cursor = 0;
        public static void Update()
        {
            // Atualiza posição do cursor
            MouseState newState = Mouse.GetState();

            Cursor_X = CurrentState.X;
            Cursor_Y = CurrentState.Y;

            if (PreventOffscreen)
            {
                if (Cursor_X <= 0) { Cursor_X = 0; };
                if (Cursor_X >= WindowManager.WindowW) { Cursor_X = WindowManager.WindowW; };
                if (Cursor_Y <= 0) { Cursor_Y = 0; };
                if (Cursor_Y >= WindowManager.WindowH) { Cursor_Y = WindowManager.WindowH; };

            }
            Cursor_Rect = new Rectangle(Cursor_X + CursorOffset, Cursor_Y + CursorOffset, 36, 44);
            CursorPosition_Rect = new Rectangle(Cursor_X, Cursor_Y, Cursor_Prescision, Cursor_Prescision);

            Detect_LeftClick(newState);
            Detect_RightClick(newState);

            CurrentState = newState;
        }

        /// <summary>
        /// Refresh the Left-Click State
        /// </summary>
        /// <param name="newState">New state.</param>
        private static void Detect_LeftClick(MouseState newState)
        {
            if (newState.LeftButton == ButtonState.Released && CurrentState.LeftButton == ButtonState.Released)
            {
                Left_Cursor_ClickUp = new Rectangle(0, 0, 0, 0);
                Left_Cursor_ClickDown = new Rectangle(0, 0, 0, 0);

            }
            if (newState.LeftButton == ButtonState.Pressed && CurrentState.LeftButton == ButtonState.Released)
            {
                Left_Cursor_ClickUp = new Rectangle(0, 0, 0, 0);

                Left_Cursor_ClickDown = new Rectangle(Cursor_X, Cursor_Y, Cursor_Prescision, Cursor_Prescision);

            }
            if (newState.LeftButton == ButtonState.Released && CurrentState.LeftButton == ButtonState.Pressed)
            {
                Left_Cursor_ClickUp = new Rectangle(Cursor_X, Cursor_Y, Cursor_Prescision, Cursor_Prescision);

                Left_Cursor_ClickDown = new Rectangle(0, 0, 0, 0);

            }


        }

        /// <summary>
        /// Refresh the Right-Click State.
        /// </summary>
        /// <param name="newState">New state.</param>
        private static void Detect_RightClick(MouseState newState)
        {
            if (newState.RightButton == ButtonState.Released && CurrentState.RightButton == ButtonState.Released)
            {
                Right_Cursor_ClickUp = new Rectangle(0, 0, 0, 0);
                Right_Cursor_ClickDown = new Rectangle(0, 0, 0, 0);

            }
            if (newState.RightButton == ButtonState.Pressed && CurrentState.RightButton == ButtonState.Released)
            {
                Right_Cursor_ClickUp = new Rectangle(0, 0, 0, 0);

                Right_Cursor_ClickDown = new Rectangle(Cursor_X, Cursor_Y, Cursor_Prescision, Cursor_Prescision);

            }
            if (newState.RightButton == ButtonState.Released && CurrentState.RightButton == ButtonState.Pressed)
            {
                Right_Cursor_ClickUp = new Rectangle(Cursor_X, Cursor_Y, Cursor_Prescision, Cursor_Prescision);

                Right_Cursor_ClickDown = new Rectangle(0, 0, 0, 0);



            }


        }




    }
}