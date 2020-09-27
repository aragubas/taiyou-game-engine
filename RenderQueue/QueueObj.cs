using System;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework;
using TaiyouScriptEngine.Desktop;

namespace TaiyouScriptEngine.Desktop.RenderQueue
{
    public class QueueObj
    {
        // Public Locals
        public string Tag;

        public string SpriteName;
        public Rectangle destRect;
        public Color BlendColor;

        public Rectangle srcRect;
        public float Rotation;
        public Vector2 Origin;
        public SpriteEffects SpriteEffect;
        public float LayerDepth;

        /// <summary>
        /// An object that will be rendered on screen.
        /// </summary>
        /// <param name="TagName">Tag name.</param>
        /// <param name="ResSprite">Res sprite.</param>
        /// <param name="Dest">Destination.</param>
        /// <param name="blendColor">Blend color.</param>
        /// <param name="SrcRect">Source rect.</param>
        /// <param name="rotation">Rotation.</param>
        /// <param name="origin">Origin.</param>
        /// <param name="Effect">Effect.</param>
        /// <param name="layer_depth">Layer depth.</param>
        public QueueObj(string TagName, string ResSprite, Rectangle Dest, Color blendColor, Rectangle SrcRect, float rotation, Vector2 origin, SpriteEffects Effect, float layer_depth)
        {
            // Required Arguments
            Tag = TagName;
            SpriteName = ResSprite;
            destRect = Dest;
            BlendColor = blendColor;

            // Optional Arguments
            srcRect = SrcRect;
            Rotation = rotation;
            Origin = origin;
            SpriteEffect = Effect;
            LayerDepth = layer_depth;

        }

        /// <summary>
        /// Render the object
        /// </summary>
        /// <param name="spriteBatch">Sprite batch.</param>
        public void Render(SpriteBatch spriteBatch)
        {
            spriteBatch.Draw(Sprites.GetSprite(SpriteName), destRect, srcRect, BlendColor, Rotation, Origin, SpriteEffect, LayerDepth);

        }

        #region Set Dest Rectangle Parameters
        public void Set_destX(int Value)
        {
            destRect.X = Value;
        }

        public void Set_destY(int Value)
        {
            destRect.Y = Value;
        }

        public void Set_destW(int Value)
        {
            destRect.Width = Value;
        }

        public void Set_destH(int Value)
        {
            destRect.Height = Value;
        }

        #endregion

        #region Set Source Rectangle Parameters
        public void Set_srcX(int Value)
        {
           srcRect.X = Value;
        }

        public void Set_srcY(int Value)
        {
            srcRect.Y = Value;
        }

        public void Set_srcW(int Value)
        {
            srcRect.Width = Value;
        }

        public void Set_srcH(int Value)
        {
            srcRect.Height = Value;
        }

        #endregion

        public void Set_BlendColor(Color Value)
        {
            BlendColor = Value;
        }

        public void Set_Rotation(int Value)
        {
            Rotation = Value;
        }

        public void Set_Origin(Vector2 Value)
        {
            Origin = Value;
        }

        public void Set_SpriteEffect(SpriteEffects spriteEffect)
        {

            SpriteEffect = spriteEffect;
        }

        public void Set_LayerDepth(float Value)
        {
            LayerDepth = Value;
        }

    }
}
