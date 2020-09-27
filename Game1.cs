using System;
using System.Collections.Generic;
using System.IO;
using System.Threading;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;

namespace TaiyouScriptEngine.Desktop
{
    /// <summary>
    /// This is the main type for your game.
    /// </summary>
    public class Game1 : Game
    {
        GraphicsDeviceManager graphics;
        SpriteBatch spriteBatch;
        public static bool StartScriptToggle;
        public static KeyboardState oldState;

        public static Game1 Reference;
        public static Thread UpdateThread;
        public static List<RenderQueue.QueueObj> RenderQueueList = new List<RenderQueue.QueueObj>();
        public static List<string> RenderQueueList_Keys = new List<string>();

        public Game1()
        {
            graphics = new GraphicsDeviceManager(this);
            Content.RootDirectory = "Content";
            Reference = this;
        }

        protected override void Initialize()
        {
            // TODO: Add your initialization logic here
            // Load Game Assets
            string CurrentGameName = "";

            CurrentGameName = File.ReadAllText("./CurrentGame.txt").Replace(Environment.NewLine, "");

            string TaiyouDir = CurrentGameName + "/tiy/";
            string CurrentSourceFolder = CurrentGameName + "/res/";
            string SpriteDir = CurrentSourceFolder + "img/";
            string FontDir = CurrentSourceFolder + "font/";
            string RegDir = CurrentSourceFolder + "reg/";
            string SoundDir = CurrentSourceFolder + "sound/";


            // Set Global Directories
            Global.SpriteDir = SpriteDir.Replace(Environment.CurrentDirectory + CurrentSourceFolder,"");
            Global.FontDir = FontDir;
            Global.RegistryDir = RegDir;
            Global.GameFolder = CurrentGameName;
            Global.SourceFolderFilter = CurrentGameName + "/res/";
            Global.TaiyouDir = TaiyouDir;

            Sprites.FindAllSprites(this, SpriteDir, FontDir);
            Registry.Initialize(RegDir);
            Global.LoadTaiyouScripts(TaiyouDir);
            SoundLoader.FindAllSounds(SoundDir);
            SoundtrackManager.CreateBGMInstances();



            base.Initialize();
        }

        protected override void LoadContent()
        {
            // Create a new SpriteBatch, which can be used to draw textures.
            spriteBatch = new SpriteBatch(GraphicsDevice);

            // TODO: use this.Content to load your game content here
        }

        
        protected override void OnExiting(object sender, EventArgs args)
        {
            // Stop the Update Thread
            Taiyou.LoopEvent.UpdateEnable = false;
            UpdateThread.Abort();

            base.OnExiting(sender, args);
        }

        protected override void Update(GameTime gameTime)
        {
            KeyboardState newState = Keyboard.GetState();

            if (newState.IsKeyDown(Keys.F12) && oldState.IsKeyUp(Keys.F12))
            {
                Global.Reload();
            }


            // Start the AutoStart Script
            if (!StartScriptToggle)
            {
                StartScriptToggle = true;
                RestartUpdateThread();
            }

            oldState = newState;
            base.Update(gameTime);

        }

        public static void RestartUpdateThread()
        {
            // Add Default Taiyou Events
            Taiyou.Event.RegisterEvent("AutoStart", "start");
            Taiyou.Event.TriggerEvent("AutoStart");

            Taiyou.LoopEvent.RegisterEvent("Update", "update");

            UpdateThread = new Thread(new ParameterizedThreadStart((obj) => Taiyou.LoopEvent.RunEvents()))
            {
                Name = "TaiyouUpdateThread"
            };

            UpdateThread.Start();
            Taiyou.LoopEvent.UpdateEnable = true;

        }


        protected override void Draw(GameTime gameTime)
        {
            GraphicsDevice.Clear(Color.CornflowerBlue);
            spriteBatch.Begin();

            foreach (var sprite in RenderQueueList)
            {
                sprite.Render(spriteBatch);
            }

            spriteBatch.End();
            base.Draw(gameTime);
        }
    }
}
