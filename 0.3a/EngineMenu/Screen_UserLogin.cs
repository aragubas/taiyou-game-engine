using System;
using System.IO;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using Microsoft.Xna.Framework.Input;

namespace TaiyouGameEngine.Desktop.EngineMenu
{
    public class Screen_UserLogin
    {
        public static int AnimationMode = 0;
        public static bool AnimationEnabled = true;
        static int GlobalOpacity = 0;
        static int GlobalOpacity_AnimationSpeed = 0;
        public static bool AnimationCompleted = false;
        static KeyboardState previusState;
        static bool ScreenInitialized = false;
        static Rectangle Rectangle_TopBar = new Rectangle(0, 0, 800, 45);
        static Rectangle Rectangle_BottomBar = new Rectangle(0, 553, 800, 47);
        static bool IsUserCreation = false;
        static Color WhiteColor;
        static string TopMenuText;
        static string VersionMenuText = Global.GameEngineBuild;
        static Rectangle Rectangle_SelectedGameInfo = new Rectangle(15, 4, 470, 177);
        static TextBox.TextBox textBox_Username;
        static Rectangle textBox_Username_Rectangle = new Rectangle(1, 1, 230, 20);
        static TextBox.TextBox textBox_Password;
        static Rectangle textBox_Password_Rectangle = new Rectangle(1, 1, 230, 20);
        static Custom_Button OkButton;
        static string CurrentMessage = "Ready.";
        static int ChangeScreenDelay = 0;
        public static bool CanExit = false;
        public static bool IsAlreadyAppered = false;

        public static void Draw(SpriteBatch spriteBatch)
        {
            // Render the Top and Bottom Border
            spriteBatch.Draw(Sprite.GetSprite("bar_bottom.png"), Rectangle_TopBar, null, Color.FromNonPremultiplied(255, 255, 255, GlobalOpacity - 50), 0f, Vector2.Zero, SpriteEffects.None, 1.0f);
            spriteBatch.Draw(Sprite.GetSprite("bar_top.png"), Rectangle_BottomBar, null, Color.FromNonPremultiplied(255, 255, 255, GlobalOpacity - 50), 0f, Vector2.Zero, SpriteEffects.None, 1.0f);

            // Render the Top and Bottom Titles Texts
            spriteBatch.DrawString(Sprite.GetFont("25pt.xnb"), TopMenuText, new Vector2(7, Rectangle_TopBar.Y + 5), WhiteColor);
            spriteBatch.DrawString(Sprite.GetFont("10pt.xnb"), VersionMenuText, new Vector2(7, Rectangle_BottomBar.Y + 17), WhiteColor);


            // Render the page background
            spriteBatch.Draw(Sprite.GetSprite("Base.png"), new Rectangle(Rectangle_SelectedGameInfo.X - 2, Rectangle_SelectedGameInfo.Y - 2, Rectangle_SelectedGameInfo.Width + 4, Rectangle_SelectedGameInfo.Height + 4), null, Color.FromNonPremultiplied(255,255,255, GlobalOpacity));
            spriteBatch.Draw(Sprite.GetSprite("Base.png"), Rectangle_SelectedGameInfo, null, Color.FromNonPremultiplied(0, 0, 0, GlobalOpacity));


            // Draw the Username Section
            #region Username Section
            spriteBatch.DrawString(Sprite.GetFont("15pt.xnb"), "Name:", new Vector2(Rectangle_SelectedGameInfo.X + 15, Rectangle_SelectedGameInfo.Y + 15), WhiteColor);
            // Draw the Username TextBox
            textBox_Username.Draw(spriteBatch);

            #endregion


            #region Password Section
            // Draw the Password Section
            spriteBatch.DrawString(Sprite.GetFont("15pt.xnb"), "Password:", new Vector2(Rectangle_SelectedGameInfo.X + 15, Rectangle_SelectedGameInfo.Y + 50), WhiteColor);
            // Draw the Password TextBox
            textBox_Password.Draw(spriteBatch);

            #endregion



            OkButton.Draw(spriteBatch);

            spriteBatch.DrawString(Sprite.GetFont("10pt.xnb"), CurrentMessage, new Vector2(Rectangle_SelectedGameInfo.X + 15, Rectangle_SelectedGameInfo.Y + Rectangle_SelectedGameInfo.Height - Sprite.GetFont("10pt.xnb").MeasureString(CurrentMessage).Y - 13), WhiteColor);
        
        }

        public static void Update()
        {
            // Chnage the Background Color
            Game1.ClearScreenColor = Color.FromNonPremultiplied(20,30,27, GlobalOpacity);
            WhiteColor = Color.FromNonPremultiplied(255, 255, 255, GlobalOpacity);
            if (!ScreenInitialized) { ScreenInitialized = true; Initialize(); } // Initialize the Objects


            UpdateGlobalAnimation();
            UpdateChangeWhenCompleted_Logic();
            UpdateObjects();
            UpdateLocations();


            // Skip the Login Screen if the user is already logged
            if (IsAlreadyAppered && AnimationCompleted)
            {
                Main.MenuCurrentScreen = 1;
            }


            // The Main "OK" Login button
            UpdateOkButtonLogic();


        }


        #region Updates Logic

        public static void UpdateGlobalAnimation()
        {
            if (AnimationEnabled)
            {
                if (AnimationMode == 0)
                {
                    GlobalOpacity_AnimationSpeed += 1;
                    GlobalOpacity += GlobalOpacity_AnimationSpeed;

                    if (GlobalOpacity >= 255 - GlobalOpacity_AnimationSpeed) { AnimationMode = 1; AnimationEnabled = false; GlobalOpacity_AnimationSpeed = 0; }
                }
                if (AnimationMode == 1)
                {
                    GlobalOpacity_AnimationSpeed += 1;
                    GlobalOpacity -= GlobalOpacity_AnimationSpeed;

                    if (GlobalOpacity <= 0) { AnimationMode = 0; AnimationEnabled = false; AnimationCompleted = true; GlobalOpacity_AnimationSpeed = 0; }
                }

            }
        }

        public static void UpdateObjects()
        {
            TextBox.KeyboardInput.Update();
            // Update the Username TextBox
            textBox_Username.Update();
            textBox_Username.Active = textBox_Username_Rectangle.Intersects(UserInput.Cursor.CursorPosition_Rect);
            textBox_Username.Area = textBox_Username_Rectangle;
            textBox_Username.Renderer.Color = Color.GhostWhite;
            // Update the Password TextBox
            textBox_Password.Update();
            textBox_Password.Active = textBox_Password_Rectangle.Intersects(UserInput.Cursor.CursorPosition_Rect);
            textBox_Password.Area = textBox_Password_Rectangle;
            textBox_Password.Renderer.Color = Color.GhostWhite;
            // Update the OK Button
            OkButton.Update();
            OkButton.Local_Opacity = GlobalOpacity;

        }

        public static void UpdateLocations()
        {
            Rectangle_TopBar = new Rectangle(0, GlobalOpacity - 250, WindowManager.WindowW, 47);
            Rectangle_BottomBar = new Rectangle(0, WindowManager.WindowH - GlobalOpacity + 203, WindowManager.WindowW, 47);
            Rectangle_SelectedGameInfo.Y = Rectangle_TopBar.Y + Rectangle_SelectedGameInfo.Height;
            textBox_Username_Rectangle = new Rectangle(Rectangle_SelectedGameInfo.X + 120, Rectangle_SelectedGameInfo.Y + 15, 230, 20);
            textBox_Password_Rectangle = new Rectangle(Rectangle_SelectedGameInfo.X + 210, Rectangle_SelectedGameInfo.Y + 50, 230, 20);


            OkButton.Local_X = Rectangle_SelectedGameInfo.X + Rectangle_SelectedGameInfo.Width - Convert.ToInt32(Sprite.GetFont("15pt.xnb").MeasureString("OK").X + 15);
            OkButton.Local_Y = Rectangle_SelectedGameInfo.Y + Rectangle_SelectedGameInfo.Height - Convert.ToInt32(Sprite.GetFont("15pt.xnb").MeasureString("OK").Y + 15);
            OkButton.Local_Opacity = GlobalOpacity;
            textBox_Password.Opacity = GlobalOpacity;
            textBox_Username.Opacity = GlobalOpacity;

            Rectangle_SelectedGameInfo.X = WindowManager.WindowW / 2 - Rectangle_SelectedGameInfo.Width / 2;

        }

        public static void UpdateChangeWhenCompleted_Logic()
        {
            if (AnimationCompleted)
            {
                if (CanExit)
                {
                    ChangeScreenDelay += 1;

                    if (ChangeScreenDelay >= 50)
                    {
                        ChangeScreenDelay = 0;
                        CanExit = false;
                        AnimationMode = 0;
                        AnimationEnabled = true;
                        CurrentMessage = "Ready.";
                        textBox_Username.Text.String = "";
                        textBox_Password.Text.String = "";
                        IsAlreadyAppered = true;

                        Main.IsDrawAllowed = false;
                        Screen_GameSelection.Initialize();
                        Main.MenuCurrentScreen = 1;
                        Main.IsDrawAllowed = true;


                    }

                }
            }
        }

        public static void UpdateOkButtonLogic()
        {
            if (OkButton.Local_ClickState == 2)
            {
                if (!CanExit)
                {
                    // If the boxes is empity, warn to fill all of then
                    if (textBox_Password.Text.String == "" || textBox_Username.Text.String == "")
                    {
                        CurrentMessage = "Fill all boxes to continue";
                    }
                    else
                    {
                        // If is user creation, create a user
                        if (IsUserCreation)
                        {
                            CurrentMessage = "Creating User...";

                            string Response = CreateUser(textBox_Username.Text.String, textBox_Password.Text.String);

                            CurrentMessage = Response;

                            if (Response == "Done.")
                            {
                                IsUserCreation = false;
                            }

                        }
                        else
                        {
                            // Else, Login
                            if (IsUserCreation == false)
                            {
                                CurrentMessage = "Loading...";

                                string TryResponse = LogAUser(textBox_Username.Text.String, textBox_Password.Text.String);

                                CurrentMessage = TryResponse;

                                if (TryResponse == "Done.")
                                {

                                    CanExit = true;
                                    AnimationEnabled = true;
                                }


                            }
                        }

                    }


                }

            }
        }

        #endregion

        /// <summary>
        /// Logs a User
        /// </summary>
        /// <returns>Function Return (returns "Done." when completed)</returns>
        /// <param name="Username">Username.</param>
        /// <param name="Password">Password.</param>
        public static string LogAUser(string Username, string Password)
        {
            string UserNameFolder = Username.Replace(" ", "_");
            string UserFolder = Environment.CurrentDirectory + "/Taiyou/HOME/Users/" + UserNameFolder + "/";
            string MetaDataFileContent = "";

            if (!Directory.Exists(UserFolder)) { return "This user does not exist."; }

            try
            {
                MetaDataFileContent = File.ReadAllText(UserFolder + "data/meta.data");

            }
            catch (Exception)
            {
                return "Read Data Error!";
            }

            string[] DataReadSplit = MetaDataFileContent.Split('|');

            // If the password cannot be decrypted, it is incorrect.
            try
            {
                if (Password != PassCryptografy.DecryptString(DataReadSplit[1], Password)) { return "Incorrect Password."; }
            }
            catch (Exception ex) { return "Incorrect Password."; }

            // Fill the Variables
            Global.CurrentLoggedUser = Username;
            Global.CurrentLoggedPassword = Password;
            Global.IsLogged = true;


            return "Done.";
        }

        /// <summary>
        /// Create a User
        /// </summary>
        /// <returns>Function Return (returns "Done." when completed)</returns>
        /// <param name="Username">Username.</param>
        /// <param name="Password">Password.</param>
        public static string CreateUser(string Username, string Password)
        {
            string UsernameFolderName = Username.Replace(" ", "_");
            string ReturnMessage = "";

            string FileDir = Environment.CurrentDirectory + "/Taiyou/HOME/Users/" + UsernameFolderName + "/"; // User Directory

            if (Directory.Exists(FileDir)) { return "This user already exist!"; }; // Return if user already exist

            // Create the Data Folder
            string MetadataFileLocation = Environment.CurrentDirectory + "/Taiyou/HOME/Users/" + UsernameFolderName + "/data/meta.data";

            // Create Directorys
            try
            {
                Directory.CreateDirectory(FileDir + "data"); // Data Folder
                Directory.CreateDirectory(FileDir + "cache"); // Web Cache Folder
                Directory.CreateDirectory(FileDir + "screenshots"); // Screenshots

                // Write the user Information File
                File.WriteAllText(MetadataFileLocation, Username + "|" + PassCryptografy.EncryptString(Password, Password) + "|");

            }
            catch (Exception ex)
            {
                return "Data Write Error";
            }


            return "Done.";
        }

        public static void Initialize()
        {
            IsUserCreation = !Global.IsUsersExistent;
            if (IsUserCreation) 
            { 
                TopMenuText = "Create a user";
            } 
            else 
            { 
                TopMenuText = "Login"; 

            }

            textBox_Username = new TextBox.TextBox(textBox_Username_Rectangle, 11, "", Game1.ThisGraphicsObj.GraphicsDevice, Sprite.GetFont("15pt.xnb"), Color.Red, Color.FromNonPremultiplied(150, 150, 150, 255), 5);
            textBox_Password = new TextBox.TextBox(textBox_Password_Rectangle, 11, "", Game1.ThisGraphicsObj.GraphicsDevice, Sprite.GetFont("15pt.xnb"), Color.Red, Color.FromNonPremultiplied(150, 150, 150, 255), 5);
            TextBox.KeyboardInput.Initialize(Game1.ThisGameObj, 500f, 20);
            OkButton = new Custom_Button(-500, -500, "OK", Color.Black, Color.White, Color.White);
            OkButton.spriteFont = Sprite.GetFont("15pt.xnb"); // Change the Font

        }

    }
}
