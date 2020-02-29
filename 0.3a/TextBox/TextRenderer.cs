﻿// *************************************************************************** 
// This is free and unencumbered software released into the public domain.
// 
// Anyone is free to copy, modify, publish, use, compile, sell, or
// distribute this software, either in source code form or as a compiled
// binary, for any purpose, commercial or non-commercial, and by any
// means.
// 
// In jurisdictions that recognize copyright laws, the author or authors
// of this software dedicate any and all copyright interest in the
// software to the public domain. We make this dedication for the benefit
// of the public at large and to the detriment of our heirs and
// successors. We intend this dedication to be an overt act of
// relinquishment in perpetuity of all present and future rights to this
// software under copyright law.
// 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
// EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
// MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
// IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
// OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
// ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
// OTHER DEALINGS IN THE SOFTWARE.
// 
// For more information, please refer to <http://unlicense.org>
// ***************************************************************************
// Source Link: https://github.com/UnterrainerInformatik/MonoGame-Textbox


using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;

namespace TaiyouGameEngine.Desktop.TextBox
{

    public class TextRenderer
    {
        public Rectangle Area { get; set; }
        public SpriteFont Font { get; set; }
        public Color Color { get; set; }

        private readonly TextBox box;
        private RenderTarget2D target;
        private SpriteBatch batch;

        // Cached texture that has all of the characters.
        private Texture2D text;

        // Location of the character.
        internal readonly short[] X;
        internal readonly short[] Y;

        // With of the character.
        internal readonly byte[] Width;

        // Row the character is on.
        private readonly byte[] row;

        public void Dispose()
        {
            text?.Dispose();
            text = null;
            target?.Dispose();
            target = null;
            Font = null;
            batch?.Dispose();
            batch = null;
        }

        public TextRenderer(TextBox box)
        {
            this.box = box;

            X = new short[this.box.Text.MaxLength];
            Y = new short[this.box.Text.MaxLength];
            Width = new byte[this.box.Text.MaxLength];

            row = new byte[this.box.Text.MaxLength];
        }

        public void Update()
        {
            if (!box.Text.IsDirty)
            {
                return;
            }

            MeasureCharacterWidths();
            text = RenderText();
        }

        public void Draw(SpriteBatch spriteBatch)
        {
            if (text != null)
            {
                spriteBatch.Draw(text, Area, Color.White);
            }
        }

        public int CharAt(Point localLocation)
        {
            Rectangle charRectangle = new Rectangle(0, 0, 0, Font.LineSpacing);

            int r = localLocation.Y / (Font.LineSpacing);

            for (short i = 0; i < box.Text.Length; i++)
            {
                if (row[i] != r)
                {
                    continue;
                }

                // Rectangle that encompasses the current character.
                charRectangle.X = X[i];
                charRectangle.Y = Y[i];
                charRectangle.Width = Width[i];

                // Click on a character so put the cursor in front of it.
                if (charRectangle.Contains(localLocation))
                {
                    return i;
                }

                // Next character is not on the correct row so this is the last character for this row so select it.
                if (i < box.Text.Length - 1 && row[i + 1] != r)
                {
                    return i;
                }
            }

            // Missed a character so return the end.
            return box.Text.Length;
        }

        private void MeasureCharacterWidths()
        {
            for (int i = 0; i < box.Text.Length; i++)
            {
                Width[i] = MeasureCharacter(i);
            }
        }

        private byte MeasureCharacter(int location)
        {
            string value = box.Text.String;
            float front = Font.MeasureString(value.Substring(0, location)).X;
            float end = Font.MeasureString(value.Substring(0, location + 1)).X;

            return (byte)(end - front);
        }

        private Texture2D RenderText()
        {
            if (batch == null)
            {
                batch = new SpriteBatch(box.GraphicsDevice);
            }
            if (target == null)
            {
                target = new RenderTarget2D(box.GraphicsDevice, Area.Width, Area.Height);
            }

            box.GraphicsDevice.SetRenderTarget(target);

            box.GraphicsDevice.Clear(Color.Transparent);

            int start = 0;
            float height = 0.0f;

            batch.Begin(SpriteSortMode.Immediate, BlendState.AlphaBlend);

            while (true)
            {
                start = RenderLine(batch, start, height);

                if (start >= box.Text.Length)
                {
                    batch.End();
                    box.GraphicsDevice.SetRenderTarget(null);

                    return target;
                }

                height += Font.LineSpacing;
            }
        }

        private int RenderLine(SpriteBatch spriteBatch, int start, float height)
        {
            int breakLocation = start;
            float lineLength = 0.0f;
            byte r = (byte)(height / Font.LineSpacing);

            string t = box.Text.String;
            string tempText;

            // Starting from end of last line loop though the characters.
            for (int iCount = start; iCount < box.Text.Length; iCount++)
            {
                // Calculate screen location of current character.
                X[iCount] = (short)lineLength;
                Y[iCount] = (short)height;
                row[iCount] = r;

                // Calculate the width of the current line.
                lineLength += Width[iCount];

                // Current line is too long need to split it.
                if (lineLength > Area.Width)
                {
                    if (breakLocation == start)
                    {
                        // Have to split a word.
                        // Render line and return start of new line.
                        tempText = t.Substring(start, iCount - start);
                        spriteBatch.DrawString(Font, tempText, new Vector2(0.0f, height), Color);
                        return iCount + 1;
                    }

                    // Have a character we can split on.
                    // Render line and return start of new line.
                    tempText = t.Substring(start, breakLocation - start);
                    spriteBatch.DrawString(Font, tempText, new Vector2(0.0f, height), Color);
                    return breakLocation + 1;
                }

                // Handle characters that force/allow for breaks.
                switch (box.Text.Characters[iCount])
                {
                    // These characters force a line break.
                    case '\r':
                    case '\n':
                        //Render line and return start of new line.
                        tempText = t.Substring(start, iCount - start);
                        spriteBatch.DrawString(Font, tempText, new Vector2(0.0f, height), Color);
                        return iCount + 1;
                    // These characters are good break locations.
                    case '-':
                    case ' ':
                        breakLocation = iCount + 1;
                        break;
                }
            }

            // We hit the end of the text box render line and return
            // _textData.Length so RenderText knows to return.
            tempText = t.Substring(start, box.Text.Length - start);
            spriteBatch.DrawString(Font, tempText, new Vector2(0.0f, height), Color);
            return box.Text.Length;
        }
    }
}
