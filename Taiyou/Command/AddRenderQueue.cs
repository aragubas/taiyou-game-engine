using System;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;

namespace TaiyouScriptEngine.Desktop.Taiyou.Command
{
    public class AddRenderQueue
    {
        // This functions has 8 Arguments
        // Only 4 is needed
        // ----------------------------------

        public static void call(string[] Arguments)
        {
            // Required Arguments
            string RqTagName = Utils.GetSubstring(Arguments[0], '"');
            string RqResSprite = Utils.GetSubstring(Arguments[1], '"');
            string RqRectangle = Utils.GetSubstring(Arguments[2], '"');
            string RqBlendColor = Utils.GetSubstring(Arguments[3], '"');


            // Required Variables
            Rectangle Dst = new Rectangle(0, 0, 0, 0);
            Rectangle SrcRect = Rectangle.Empty;
            Color RqColor = Color.FromNonPremultiplied(255, 255, 255, 255);

            // Optional Variables
            float Rotation = 0.0f;
            Vector2 Origin = Vector2.Zero;
            SpriteEffects spriteEffects = SpriteEffects.None;
            float LayerDepth = 0.0f;


            // Destination Rectangle is a Literal
            if (RqRectangle.StartsWith("#", StringComparison.Ordinal))
            {
                string[] AllRectCode = RqRectangle.Remove(0, 1).Split(';');

                // Set the Correct Dest Rectangle
                Dst.X = Convert.ToInt32(AllRectCode[0]);
                Dst.Y = Convert.ToInt32(AllRectCode[1]);
                Dst.Width = Convert.ToInt32(AllRectCode[2]);
                Dst.Height = Convert.ToInt32(AllRectCode[3]);
            }
            else
            {
                int VarIndex = Global.VarList_Keys.IndexOf(RqRectangle);
                // Check if variable exists



            }

            // Destination Color is a Literal
            if (RqBlendColor.StartsWith("#", StringComparison.Ordinal))
            {
                string[] AllColorCode = RqBlendColor.Remove(0, 1).Split(';');

                int R = Convert.ToInt32(AllColorCode[0]);
                int G = Convert.ToInt32(AllColorCode[1]);
                int B = Convert.ToInt32(AllColorCode[2]);
                int A = Convert.ToInt32(AllColorCode[3]);


                RqColor = Color.FromNonPremultiplied(R, G, B, A);
            }

            // Add Optional Arguments
            if (Arguments.Length > 4)
            {
                string RqRotation = Utils.GetSubstring(Arguments[4], '"');
                string RqOrigin = Utils.GetSubstring(Arguments[5], '"');
                string RqSpriteEffect = Utils.GetSubstring(Arguments[6], '"');
                string RqLayerDepth = Utils.GetSubstring(Arguments[7], '"');
                string RqSrcRect = Utils.GetSubstring(Arguments[8], '"');


                // RqRotation is a Literal
                if (RqRotation.StartsWith("#", StringComparison.Ordinal))
                {
                    Rotation = float.Parse(RqRotation.Remove(0, 1));
                }else if(RqRotation.Length > 3)
                {
                    int VarIndex = Global.VarList_Keys.IndexOf(RqRotation);
                    if (VarIndex == -1) { throw new IndexOutOfRangeException("Variable [" + RqRotation + "] does not exist."); }
                    string VarValue = Convert.ToString(Global.VarList[VarIndex].Value);



                    Rotation = float.Parse(VarValue);

                }


                // RqOrigin is a Literal
                if (RqOrigin.StartsWith("#", StringComparison.Ordinal))
                {
                    string[] Splited = RqOrigin.Remove(0, 1).Split(';');

                    Origin = new Vector2(float.Parse(Splited[0]), float.Parse(Splited[1]));
                }

                // RqSpriteEffects is a Literal
                if (RqSpriteEffect.StartsWith("#", StringComparison.Ordinal))
                {
                    switch (RqSpriteEffect.Remove(0, 1))
                    {
                        case "FlipVertical":
                            spriteEffects = SpriteEffects.FlipVertically;
                            break;

                        case "FlipHorizontal":
                            spriteEffects = SpriteEffects.FlipHorizontally;
                            break;

                        default:
                            spriteEffects = SpriteEffects.None;
                            break;

                    }
                }

                // RqLayerDepth is a Literal
                if (RqLayerDepth.StartsWith("#", StringComparison.Ordinal))
                {
                    LayerDepth = float.Parse(RqLayerDepth.Remove(0, 1));
                }

                // Source Rectangle is a Literal
                if (RqSrcRect.StartsWith("#", StringComparison.Ordinal))
                {
                    string[] AllRectCode = RqSrcRect.Remove(0, 1).Split(';');

                    // Set the Correct Dest Rectangle
                    SrcRect.X = Convert.ToInt32(AllRectCode[0]);
                    SrcRect.Y = Convert.ToInt32(AllRectCode[1]);
                    SrcRect.Width = Convert.ToInt32(AllRectCode[2]);
                    SrcRect.Height = Convert.ToInt32(AllRectCode[3]);
                }


            }


            if (SrcRect == Rectangle.Empty)
            {
                SrcRect = Sprites.GetSprite(RqResSprite).Bounds;
            }

            // Finnaly, add everthing to the render queue
            Game1.RenderQueueList.Add(new RenderQueue.QueueObj(RqTagName, RqResSprite, Dst, RqColor, SrcRect, Rotation, Origin, spriteEffects, LayerDepth));
            Game1.RenderQueueList_Keys.Add(RqTagName);

        }
    }
}
