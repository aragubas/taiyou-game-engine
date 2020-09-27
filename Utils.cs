using System;
using System.IO;
using System.Text;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;

namespace TaiyouScriptEngine.Desktop
{
    public class Utils
    {
        /// <summary>
        /// Convert strings to rect.
        /// </summary>
        /// <returns>The to rect.</returns>
        /// <param name="StringToConver">String to conver.</param>
        public static Rectangle StringToRect(string StringToConver)
        {
            string[] RectCode = StringToConver.Split(',');

            int RectX = Convert.ToInt32(RectCode[0]);
            int RectY = Convert.ToInt32(RectCode[1]);
            int RectW = Convert.ToInt32(RectCode[2]);
            int RectH = Convert.ToInt32(RectCode[3]);

            return new Rectangle(RectX,RectY,RectW,RectH);
        }

        /// <summary>
        /// Convert string to color
        /// </summary>
        /// <returns>The to color.</returns>
        /// <param name="StringToConver">String to conver.</param>
        /// <param name="ColorAlphaOveride">Color alpha overide.</param>
        public static Color StringToColor(string StringToConver, int ColorAlphaOveride = -255)
        {
            Color ColorToReturn = Color.Magenta;

            int Color_R = 0;
            int Color_G = 0;
            int Color_B = 0;
            int Color_A = 0;

            string[] ColorCodes = StringToConver.Split(',');

            Color_R = Convert.ToInt32(ColorCodes[0]);
            Color_G = Convert.ToInt32(ColorCodes[1]);
            Color_B = Convert.ToInt32(ColorCodes[2]);
            if (ColorAlphaOveride != -255) { Color_A = ColorAlphaOveride; } else { Color_A = Convert.ToInt32(ColorCodes[3]); }

            ColorToReturn = Color.FromNonPremultiplied(Color_R, Color_G, Color_B, Color_A);

            return ColorToReturn;
        }

        /// <summary>
        /// Wraps the text.
        /// </summary>
        /// <returns>The text.</returns>
        /// <param name="spriteFont">Sprite font.</param>
        /// <param name="text">Text.</param>
        /// <param name="maxLineWidth">Max line width.</param>
        public static string WrapText(SpriteFont spriteFont, string text, float maxLineWidth)
        {
            string[] words = text.Split(' ');
            StringBuilder sb = new StringBuilder();
            float lineWidth = 0f;
            float spaceWidth = spriteFont.MeasureString(" ").X;

            foreach (string word in words)
            {
                Vector2 size = spriteFont.MeasureString(word);

                if (lineWidth + size.X < maxLineWidth)
                {
                    sb.Append(word + " ");
                    lineWidth += size.X + spaceWidth;
                }
                else
                {
                    sb.Append("\n" + word + " ");
                    lineWidth = size.X + spaceWidth;
                }
            }

            return sb.ToString();
        }

        /// <summary>
        /// Gets the substring.
        /// </summary>
        /// <returns>The substring.</returns>
        /// <param name="Input">Input.</param>
        /// <param name="Spliter">Spliter.</param>
        public static string GetSubstring(string Input, char Spliter)
        {
            return Input.Substring(Input.IndexOf(Spliter) + 1, Input.LastIndexOf(Spliter) - 1).Replace(Convert.ToString(Spliter), "");
        }

    }
}