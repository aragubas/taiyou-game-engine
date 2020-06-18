#!/usr/bin/python3.7
#   Copyright 2020 Aragubas
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#
import pygame
from ENGINE import SPRITE as sprite
from ENGINE.TaiyouUI import UIGTK as gtk
from ENGINE import REGISTRY as reg
from ENGINE import SOUND as sound
from ENGINE.TaiyouUI import DeveloperConsole as developWindow
import ENGINE as tge
from ENGINE import UTILS as utils
from ENGINE import TaiyouUI as UiHandler
from ENGINE.TaiyouUI.GameOverlay import WarnDialog as warnDialog
from ENGINE.TaiyouUI.GameOverlay import SystemVolumeSlider as volumeSlider

TopBarRectangle = pygame.Rect(0, 0, 0, 0)
DownBarRectangle = pygame.Rect(0, 0, 0, 0)
UIObjectsSurface = pygame.Surface((5, 5))
DarkerBackgroundSurface = pygame.Surface((5, 5))
CopyOfTheScreen = pygame.Surface((5, 5))
DISPLAYObject = pygame.Surface((5, 5))
TopMenu_BackToGame_Button = gtk.Button
TopMenu_DeveloperConsoleButton = gtk.Button
TopMenu_RestartGame = gtk.Button
TopMenu_MainMenu = gtk.Button

# -- Animation -- #
UIOpacity = 0
UIOpacityAnimSpeed = 15
UIOpacityAnimEnabled = True
UIOpacityAnimState = 0
UIOpacityPauseGame = True
UIOpacityAnim_InSoundPlayed = False
UIOpacityAnim_OutSoundPlayed = False
UIOpacityAnim_InGameErrorSoundPlayed = False
AnimationNumb = 0

# -- Console Window -- #
ConsoleWindowEnabled = False

# -- Boolean -- #
UIObjectsSurfaceUpdated = False
ExitToInitializeGame = False
OpenedInGameError = False
ObjectsInitialized = False

# -- Copy of Screen -- #
CopyOfScreen_Last = False
CopyOfScreen_Result = pygame.Surface
CopyOfScreen_BlurAmount = 0


# -- Exit to Main Menu Anim -- #
ExitToMainMenuAnim = False
ExitToMainMenuAnimOpacity = 0
ExitTOMainMenuSurfaceCreated = False
ExitToMainMenuOpacityAnimBG = pygame.Surface((0, 0))


def Initialize():
    global TopMenu_BackToGame_Button
    global TopMenu_DeveloperConsoleButton
    global TopMenu_RestartGame
    global TopMenu_MainMenu

    # -- Top Menu Buttons -- #
    TopMenu_BackToGame_Button = gtk.Button(pygame.Rect(3, 1, 5, 5), gtk.GetLangText("back", "overlay"), 18)
    TopMenu_DeveloperConsoleButton = gtk.Button(pygame.Rect(3, 1, 5, 5), gtk.GetLangText("console", "overlay"), 18)
    TopMenu_RestartGame = gtk.Button(pygame.Rect(3, 1, 3, 3), gtk.GetLangText("restart", "overlay"), 18)
    TopMenu_MainMenu = gtk.Button(pygame.Rect(3, 1, 1, 3), gtk.GetLangText("exit", "overlay"), 18)

    warnDialog.Initialize()
    volumeSlider.Initialize()
    developWindow.Initialize()


def Draw(Display):
    global UIObjectsSurface
    global TopBarRectangle
    global TopMenu_BackToGame_Button
    global TopMenu_DeveloperConsoleButton
    global TopMenu_RestartGame
    global UIOpacity
    global UIOpacityAnimEnabled
    global UIOpacityAnimState
    global DarkerBackgroundSurface
    global DISPLAYObject
    global CopyOfTheScreen
    global DownBarRectangle
    global ConsoleWindowEnabled
    global AnimationNumb
    global UIObjectsSurfaceUpdated
    global OpenedInGameError
    global TopMenu_MainMenu
    global ExitToMainMenuAnim
    global ExitTOMainMenuSurfaceCreated
    global ExitToMainMenuOpacityAnimBG
    global ObjectsInitialized
    global CopyOfScreen_BlurAmount

    DISPLAYObject = Display

    # -- Initialize the UIObjectSurface -- #
    if not UIObjectsSurfaceUpdated:
        UIObjectsSurface = pygame.Surface((Display.get_width(), Display.get_height()), pygame.SRCALPHA)
        print("Surface Created")
        UIObjectsSurfaceUpdated = True


    # -- Draw the Screenshot of Screen -- #
    Draw_ScreenshotOfGameScreen(UIObjectsSurface)

    # -- Set Surface Alpha -- #
    UIObjectsSurface.set_alpha(UIOpacity)

    # -- Draw the Top Bar -- #
    gtk.Draw_Panel(UIObjectsSurface, TopBarRectangle, "DOWN")

    # -- Draw the Down Bar -- #
    gtk.Draw_Panel(UIObjectsSurface, DownBarRectangle, "UP")

    # -- Draw Buttons -- #
    TopMenu_BackToGame_Button.Render(UIObjectsSurface)
    TopMenu_DeveloperConsoleButton.Render(UIObjectsSurface)
    TopMenu_RestartGame.Render(UIObjectsSurface)
    TopMenu_MainMenu.Render(UIObjectsSurface)

    # -- Draw Taiyou Version -- #
    sprite.FontRender(UIObjectsSurface, "/Ubuntu_Bold.ttf", 18, "v" + str(utils.FormatNumber(tge.TaiyouGeneralVersion)),
                      (240, 240, 240), 5, DownBarRectangle[1] + 3)

    # -- Draw the Developer Console -- #
    if ConsoleWindowEnabled:
        developWindow.Draw(UIObjectsSurface)

    # -- Draw Volume Slider -- #
    volumeSlider.Draw(UIObjectsSurface)


    # -- Warn Dialog -- #
    warnDialog.Render(UIObjectsSurface)

    Display.blit(UIObjectsSurface, (0, 0))

    # -- Render the Exit to Main Menu Animation -- #
    if ExitToMainMenuAnim and ExitTOMainMenuSurfaceCreated:
        ExitToMainMenuOpacityAnimBG.fill((0, 0, 0))
        ExitToMainMenuOpacityAnimBG.set_alpha(ExitToMainMenuAnimOpacity * 2)

        Display.blit(ExitToMainMenuOpacityAnimBG, (0, 0))

    if not ObjectsInitialized:
        ObjectsInitialized = True

def Draw_ScreenshotOfGameScreen(Display):
    global CopyOfScreen_Result
    global CopyOfScreen_Last
    global CopyOfScreen_BlurAmount

    # -- Blur Amount Value -- #
    if not CopyOfScreen_Last:
        CopyOfScreen_BlurAmount = max(1.0, UIOpacity - reg.ReadKey_int("/TaiyouSystem/CONF/blur_amount"))

    if UIOpacityAnimEnabled:  # -- Draw the Animation -- #
        CopyOfScreen_Last = False
        if reg.ReadKey_bool("/TaiyouSystem/CONF/blur_enabled"):
            # -- Pixalizate if Overlay Pixalizate is True -- #
            if not reg.ReadKey_bool("/TaiyouSystem/CONF/overlay_pixelizate"):
                # -- Blur the Copy of Screen -- #
                Display.blit(sprite.Surface_Blur(CopyOfTheScreen, CopyOfScreen_BlurAmount), (0, 0))
            else:
                # -- Pixalizate Copy of Screen -- #
                Display.blit(sprite.Surface_Blur(CopyOfTheScreen, CopyOfScreen_BlurAmount, True), (0, 0))

        else:
            Display.blit(CopyOfTheScreen, (0, 0))

    # -- Draw the Last Frame -- #
    if not CopyOfScreen_Last and not UIOpacityAnimEnabled:
        CopyOfScreen_Result = sprite.Surface_Blur(CopyOfTheScreen, CopyOfScreen_BlurAmount)
        CopyOfScreen_Last = True

    # -- Render the Last Frame -- #
    if CopyOfScreen_Last and not UIOpacityAnimEnabled:  # -- Render the last frame of animation -- #
        Display.blit(CopyOfScreen_Result, (0, 0))


def Update():
    global TopBarRectangle
    global UIObjectsSurface
    global TopMenu_DeveloperConsoleButton
    global TopMenu_BackToGame_Button
    global UIOpacityAnimEnabled
    global AnimationNumb
    global UIOpacityAnimSpeed
    global TopMenu_RestartGame
    global DownBarRectangle
    global ConsoleWindowEnabled
    global ExitToInitializeGame
    global UIOpacityAnim_OutSoundPlayed
    global TopMenu_MainMenu
    global ExitTOMainMenuSurfaceCreated
    global ExitToMainMenuAnim
    global ExitToMainMenuOpacityAnimBG
    global ObjectsInitialized

    if ObjectsInitialized:
        volumeSlider.Update()
        volumeSlider.ObjX = UIObjectsSurface.get_width() - 40
        volumeSlider.ObjY = TopBarRectangle[1] + 2

    # -- Exit to Main Menu Anim -- #
    if ExitToMainMenuAnim:
        if not ExitTOMainMenuSurfaceCreated:
            ExitToMainMenuOpacityAnimBG = pygame.Surface((DISPLAYObject.get_width(), DISPLAYObject.get_height()))
            ExitTOMainMenuSurfaceCreated = True

    # -- Restart Game Dialog -- #
    warnDialog.Update()

    AnimationNumb = UIOpacity - 255 + UIOpacityAnimSpeed

    TopBarRectangle = pygame.Rect(0, AnimationNumb, UIObjectsSurface.get_width(), 34)
    DownBarRectangle = pygame.Rect(0, UIObjectsSurface.get_height() - AnimationNumb - 25, UIObjectsSurface.get_width(),
                                   34)

    # -- Set Objects X -- #
    TopMenu_MainMenu.Set_X(TopMenu_RestartGame.Rectangle[0] + TopMenu_RestartGame.Rectangle[2] + 2)
    TopMenu_DeveloperConsoleButton.Set_X(
        TopMenu_BackToGame_Button.Rectangle[0] + TopMenu_BackToGame_Button.Rectangle[2] + 2)
    TopMenu_RestartGame.Set_X(
        TopMenu_DeveloperConsoleButton.Rectangle[0] + TopMenu_DeveloperConsoleButton.Rectangle[2] + 2)
    TopMenu_BackToGame_Button.Set_X(AnimationNumb + 2)

    # -- Set Objects Y -- #
    TopMenu_BackToGame_Button.Set_Y(AnimationNumb + 2)
    TopMenu_DeveloperConsoleButton.Set_Y(TopMenu_BackToGame_Button.Rectangle[1])
    TopMenu_RestartGame.Set_Y(TopMenu_BackToGame_Button.Rectangle[1])
    TopMenu_MainMenu.Set_Y(TopMenu_BackToGame_Button.Rectangle[1])

    if TopMenu_BackToGame_Button.ButtonState == "UP" and not warnDialog.Enabled:
        UIOpacityAnim_OutSoundPlayed = False
        if not UIOpacityAnimEnabled:
            UIOpacityAnimEnabled = True
            tge.devel.PrintToTerminalBuffer("TaiyouUI.Buttons :\n(BackToGame_function)[Back to Game]")

    if TopMenu_DeveloperConsoleButton.ButtonState == "UP" and not warnDialog.Enabled:
        if ConsoleWindowEnabled:
            ConsoleWindowEnabled = False
        else:
            ConsoleWindowEnabled = True

    if TopMenu_RestartGame.ButtonState == "UP" and not warnDialog.Enabled:
        # -- Alert to Restart -- #
        ShowWarnDialog(gtk.GetLangText("restartconfirm_title_generic", "overlay"),
                       gtk.GetLangText("restartconfirm_text_restart", "overlay"), 0)

    if TopMenu_MainMenu.ButtonState == "UP" and not warnDialog.Enabled:
        # -- Alert to Exit -- #
        ShowWarnDialog(gtk.GetLangText("restartconfirm_title_generic", "overlay"),
                       gtk.GetLangText("restartconfirm_text_exit", "overlay"), 1)

    # -- Run the Menu Animation -- #
    UpdateOpacityAnim()

    # -- Run the Back to Main Menu Animation -- #
    ExitToMainMenu_UpdateAnim()

    # -- Update Developer Console Windows -- #
    if ConsoleWindowEnabled:
        developWindow.Update()


def ShowWarnDialog(Title, Text, ActionType):
    global ConsoleWindowEnabled
    warnDialog.MessageTitle = Title
    warnDialog.MessageText = Text
    warnDialog.ActionType = ActionType
    warnDialog.Enabled = True
    warnDialog.AnimEnabled = True
    ConsoleWindowEnabled = False
    if volumeSlider.SliderObject_AnimMode == 1:
        volumeSlider.SliderObject_AnimEnabled = True

    sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Notify"))


def UpdateOpacityAnim():
    global UIOpacityAnimState
    global UIOpacity
    global UIOpacityAnimEnabled
    global UIOpacityAnimSpeed
    global CopyOfTheScreen
    global DarkerBackgroundSurface
    global UIObjectsSurface
    global UIOpacityPauseGame
    global ConsoleWindowEnabled
    global UIObjectsSurfaceUpdated
    global ExitToInitializeGame
    global UIOpacityAnim_InSoundPlayed
    global UIOpacityAnim_OutSoundPlayed
    global OpenedInGameError
    global UIOpacityAnim_InGameErrorSoundPlayed
    global CopyOfScreen_Last

    if UIOpacityAnimEnabled:
        if UIOpacityAnimState == 0:  # <- Enter Animation
            UIOpacity += UIOpacityAnimSpeed

            # -- Copy the Screen Surface -- #
            if not UIOpacityPauseGame:
                UIOpacityPauseGame = True
                print("Taiyou.SystemUI.AnimationTrigger : Screen Copied.")

            if OpenedInGameError and not UIOpacityAnim_InGameErrorSoundPlayed:
                ConsoleWindowEnabled = True
                UIOpacityAnim_InGameErrorSoundPlayed = True
                sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Error"))

            # -- Play the In Sound -- #
            if not UIOpacityAnim_InSoundPlayed:
                sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/In"))
                UIOpacityAnim_InSoundPlayed = True

            if UIOpacity >= 255:  # <- Triggers Animation End
                UIOpacity = 255
                UIOpacityAnimEnabled = False
                UIOpacityAnimState = 1
                UIOpacityAnim_InSoundPlayed = True
                UIOpacityAnim_OutSoundPlayed = True
                print("Taiyou.SystemUI.AnimationTrigger : Animation Start.")

        if UIOpacityAnimState == 1:  # <- Exit Animation
            UIOpacity -= UIOpacityAnimSpeed

            # -- Close Windows -- #
            if not OpenedInGameError:
                ConsoleWindowEnabled = False

            # -- Play the Out Sound -- #
            if not UIOpacityAnim_OutSoundPlayed:
                sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Out"))
                UIOpacityAnim_OutSoundPlayed = True

            if UIOpacity <= 0:  # <- Triggers Animation End
                UIOpacity = 0
                UIOpacityAnimEnabled = False
                UIOpacityAnimState = 0
                UiHandler.Messages.append("GAME_UPDATE:True")
                # -- Unload the Surfaces -- #
                CopyOfTheScreen = pygame.Surface((0, 0), pygame.SRCALPHA)
                DarkerBackgroundSurface = pygame.Surface((0, 0), pygame.SRCALPHA)
                UIObjectsSurface = pygame.Surface((0, 0), pygame.SRCALPHA)
                UIOpacityPauseGame = False
                UIObjectsSurfaceUpdated = False
                warnDialog.SurfacesUpdated = False
                ConsoleWindowEnabled = False
                CopyOfScreen_Last = False

                # -- Initialize the Game when exiting -- #
                if ExitToInitializeGame:
                    ExitToInitializeGame = False
                    UiHandler.Messages.append("TOGGLE_GAME_START")
                    UiHandler.Messages.append("SET_GAME_MODE")

                UIOpacityAnim_InSoundPlayed = False
                UIOpacityAnim_OutSoundPlayed = False
                OpenedInGameError = False
                UiHandler.Messages.append("SET_GAME_MODE")
                UIOpacityAnim_InGameErrorSoundPlayed = False
                UiHandler.SystemMenuEnabled = False


# -- Update the ExitToMainMenu Animation -- #
def ExitToMainMenu_UpdateAnim():
    global ExitToMainMenuAnim
    global ExitToMainMenuAnimOpacity
    global UIObjectsSurfaceUpdated
    global CopyOfTheScreen
    global UIOpacity
    global UIOpacityAnimEnabled
    global UIOpacityAnim_InSoundPlayed
    global UIOpacityAnim_OutSoundPlayed
    global UIOpacityAnimState

    if ExitToMainMenuAnim:
        ExitToMainMenuAnimOpacity += 5

        if ExitToMainMenuAnimOpacity >= 255:
            # -- Restart the RestarGameConfirm -- #
            warnDialog.AnimOpacity = 0
            warnDialog.AnimMode = 0
            warnDialog.AnimEnabled = False
            warnDialog.Enabled = False
            ExitToMainMenuAnim = False
            ExitToMainMenuAnimOpacity = 0
            UIObjectsSurfaceUpdated = False
            warnDialog.SurfacesUpdated = False
            CopyOfTheScreen.fill((0, 0, 0))

            # -- Restart Animation -- #
            UIOpacity = 0
            UIOpacityAnimEnabled = True
            UIOpacityAnim_InSoundPlayed = False
            UIOpacityAnim_OutSoundPlayed = False
            UIOpacityAnimState = 0

            # -- Update the Main Menu Scenarios -- #
            UiHandler.Messages.append("SET_MENU_MODE")
            UiHandler.Messages.append("REMOVE_GAME")

            UiHandler.SetMenuMode_Changes()

            UiHandler.CurrentMenuScreen = 2


def EventUpdate(event):
    global TopMenu_BackToGame_Button
    global TopMenu_DeveloperConsoleButton
    global TopMenu_RestartGame
    global ConsoleWindowEnabled
    global UIObjectsSurfaceUpdated
    global TopMenu_MainMenu

    # -- Update Buttons Events -- #
    if not warnDialog.Enabled:
        TopMenu_BackToGame_Button.Update(event)
        TopMenu_DeveloperConsoleButton.Update(event)
        TopMenu_RestartGame.Update(event)
        TopMenu_MainMenu.Update(event)
        volumeSlider.EventUpdate(event)

        # -- Update the Console only when it is Enabled -- #
        if ConsoleWindowEnabled:
            developWindow.EventUpdate(event)

    # -- Update the Surface when Window Size Changes -- #
    if event.type == pygame.VIDEORESIZE:
        UIObjectsSurfaceUpdated = False
        warnDialog.SurfacesUpdated = False

    # -- Update Dialog Buttons -- #
    if warnDialog.Enabled:
        warnDialog.EventUpdate(event)
