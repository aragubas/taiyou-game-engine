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
from ENGINE.TaiyouUI.GameOverlay import SystemVolumeSlider as volumeSlider
from ENGINE import TaiyouMain as taiyouMain
from ENGINE import DEBUGGING as debug

TopBarRectangle = pygame.Rect(0, 0, 0, 0)
DownBarRectangle = pygame.Rect(0, 0, 0, 0)
UIObjectsSurface = pygame.Surface((5, 5))
DarkerBackgroundSurface = pygame.Surface((5, 5))
CopyOfTheScreen = pygame.Surface((5, 5))
DISPLAYObject = pygame.Surface((5, 5))
TopMenu_BackToGame_Button = gtk.Button
TopMenu_DeveloperConsoleButton = gtk.Button
TopMenu_MainMenu = gtk.Button

# -- Animation -- #
UIOpacity = 0
UIOpacityPauseGame = True
UIOpacityAnim_InSoundPlayed = False
UIOpacityAnim_OutSoundPlayed = False
UIOpacityAnim_InGameErrorSoundPlayed = False
AnimationNumb = 0

# -- Global Animation Controller -- #
GlobalAnimationController = utils.AnimationController

# -- Console Window -- #
ConsoleWindowEnabled = False

# -- Boolean -- #
UIObjectsSurfaceUpdated = False
ExitToInitializeGame = False
OpenedInGameError = False
ObjectsInitialized = False

# -- Copy of Screen -- #
CopyOfScreen_Last = False
CopyOfScreen_Result = pygame.Surface((0, 0))
CopyOfScreen_BlurAmount = 0


# -- Exit to Main Menu Anim -- #
ExitToMainMenuAnim = False
ExitToMainMenuAnimOpacity = 0
ExitTOMainMenuSurfaceCreated = False
ExitToMainMenuOpacityAnimBG = pygame.Surface((0, 0))
PendingToExitToMainMenu = False

# -- Controls -- #
ControlsEnabled = False

def Initialize():
    global TopMenu_BackToGame_Button
    global TopMenu_DeveloperConsoleButton
    global TopMenu_MainMenu
    global GlobalAnimationController

    # -- Top Menu Buttons -- #
    TopMenu_BackToGame_Button = gtk.Button(pygame.Rect(3, 1, 5, 5), gtk.GetLangText("back", "overlay"), 18)
    TopMenu_DeveloperConsoleButton = gtk.Button(pygame.Rect(3, 1, 5, 5), gtk.GetLangText("console", "overlay"), 18)
    TopMenu_MainMenu = gtk.Button(pygame.Rect(3, 1, 1, 3), gtk.GetLangText("exit", "overlay"), 18)

    volumeSlider.Initialize()
    developWindow.Initialize()

    GlobalAnimationController = utils.AnimationController(multiplierRestart=True)
    GlobalAnimationController.ValueMultiplierSpeed = gtk.AnimationSpeed + 0.9

def Draw(Display):
    global UIObjectsSurface
    global TopBarRectangle
    global TopMenu_BackToGame_Button
    global TopMenu_DeveloperConsoleButton
    global UIOpacity
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

    # -- Draw the Screenshot of Screen -- #
    Draw_ScreenshotOfGameScreen(Display)

    # -- Initialize the UIObjectSurface -- #
    UIObjectsSurfaceUpdated = True
    ObjectsInitialized = True
    UIObjectsSurface = pygame.Surface((Display.get_width(), Display.get_height()), pygame.SRCALPHA)

    # -- Set Surface Alpha -- #
    UIObjectsSurface.set_alpha(UIOpacity)

    # -- Draw the Top Bar -- #
    gtk.Draw_Panel(UIObjectsSurface, TopBarRectangle, "DOWN")

    # -- Draw the Down Bar -- #
    gtk.Draw_Panel(UIObjectsSurface, DownBarRectangle, "UP")

    # -- Draw Buttons -- #
    TopMenu_BackToGame_Button.Render(UIObjectsSurface)
    TopMenu_DeveloperConsoleButton.Render(UIObjectsSurface)
    TopMenu_MainMenu.Render(UIObjectsSurface)

    # -- Draw Taiyou Version -- #
    sprite.FontRender(UIObjectsSurface, "/Ubuntu_Bold.ttf", 18, "v" + str(utils.FormatNumber(tge.TaiyouGeneralVersion)), (240, 240, 240), 5, DownBarRectangle[1] + 3)

    # -- Draw the Developer Console -- #
    if ConsoleWindowEnabled:
        developWindow.Draw(UIObjectsSurface)

    # -- Draw Volume Slider -- #
    volumeSlider.Draw(UIObjectsSurface)

    Display.blit(UIObjectsSurface, (0, 0))


def Draw_ScreenshotOfGameScreen(Display):
    global CopyOfScreen_Result
    global CopyOfScreen_Last
    global CopyOfScreen_BlurAmount
    global ExitToMainMenuAnim
    global ExitTOMainMenuSurfaceCreated
    global ExitToMainMenuAnimOpacity
    global GlobalAnimationController

    # -- Blur Amount Value -- #
    if not CopyOfScreen_Last:
        CopyOfScreen_BlurAmount = max(1.0, UIOpacity / reg.ReadKey_int("/TaiyouSystem/CONF/blur_amount", True)) * 14

    if GlobalAnimationController.Enabled:  # -- Draw the Animation -- #
        CopyOfScreen_Last = False
        if reg.ReadKey_bool("/TaiyouSystem/CONF/blur_enabled", True):
            # -- Pixalizate if Overlay Pixalizate is True -- #
            if not reg.ReadKey_bool("/TaiyouSystem/CONF/overlay_pixelizate", True):
                # -- Blur the Copy of Screen -- #
                Display.blit(sprite.Surface_Blur(CopyOfTheScreen, CopyOfScreen_BlurAmount), (0, 0))
            else:
                # -- Pixalizate Copy of Screen -- #
                Display.blit(sprite.Surface_Blur(CopyOfTheScreen, CopyOfScreen_BlurAmount, True), (0, 0))

        else:
            Display.blit(CopyOfTheScreen, (0, 0))

    # -- Draw the Last Frame -- #
    if not CopyOfScreen_Last and not GlobalAnimationController.Enabled:
        CopyOfScreen_Result = sprite.Surface_Blur(CopyOfTheScreen, CopyOfScreen_BlurAmount)
        CopyOfScreen_Last = True

    # -- Render the Last Frame -- #
    if CopyOfScreen_Last and not GlobalAnimationController.Enabled:  # -- Render the last frame of animation -- #
        Display.blit(CopyOfScreen_Result, (0, 0))

        if ExitToMainMenuAnim and ExitTOMainMenuSurfaceCreated:
            ExitToMainMenuOpacityAnimBG.set_alpha(ExitToMainMenuAnimOpacity)
            ExitToMainMenuOpacityAnimBG.fill((0, 0, 0, min(0, ExitToMainMenuAnimOpacity)))
            Display.blit(ExitToMainMenuOpacityAnimBG, (0, 0))


def Update():
    global TopBarRectangle
    global UIObjectsSurface
    global TopMenu_DeveloperConsoleButton
    global TopMenu_BackToGame_Button
    global AnimationNumb
    global DownBarRectangle
    global ConsoleWindowEnabled
    global ExitToInitializeGame
    global UIOpacityAnim_OutSoundPlayed
    global TopMenu_MainMenu
    global ExitTOMainMenuSurfaceCreated
    global ExitToMainMenuAnim
    global ExitToMainMenuOpacityAnimBG
    global ObjectsInitialized
    global PendingToExitToMainMenu
    global ExitToMainMenuAnimOpacity
    global ControlsEnabled

    if ObjectsInitialized:
        volumeSlider.Update()
        volumeSlider.ObjX = UIObjectsSurface.get_width() - 40
        volumeSlider.ObjY = TopBarRectangle[1] + 2

    # -- Exit to Main Menu Anim -- #
    if ExitToMainMenuAnim:
        if not ExitTOMainMenuSurfaceCreated:
            ExitToMainMenuOpacityAnimBG = pygame.Surface((DISPLAYObject.get_width(), DISPLAYObject.get_height()))
            ExitTOMainMenuSurfaceCreated = True

    AnimationNumb = UIOpacity - 255

    TopBarRectangle = pygame.Rect(0, AnimationNumb, UIObjectsSurface.get_width(), 34)
    DownBarRectangle = pygame.Rect(0, UIObjectsSurface.get_height() - AnimationNumb - 25, UIObjectsSurface.get_width(), 34)

    # -- Set Objects X -- #
    TopMenu_BackToGame_Button.Set_X(AnimationNumb + 2)
    TopMenu_MainMenu.Set_X(TopMenu_BackToGame_Button.Rectangle[0] + TopMenu_BackToGame_Button.Rectangle[2] + 2)
    TopMenu_DeveloperConsoleButton.Set_X(TopMenu_MainMenu.Rectangle[0] + TopMenu_MainMenu.Rectangle[2] + 2)

    # -- Set Objects Y -- #
    TopMenu_BackToGame_Button.Set_Y(AnimationNumb + 2)
    TopMenu_DeveloperConsoleButton.Set_Y(TopMenu_BackToGame_Button.Rectangle[1])
    TopMenu_MainMenu.Set_Y(TopMenu_BackToGame_Button.Rectangle[1])

    if ControlsEnabled:
        UpdateControls()

    # -- Run the Menu Animation -- #
    if not ExitToMainMenuAnim:
        UpdateOpacityAnim()

    # -- Run the Back to Main Menu Animation -- #
    ExitToMainMenu_UpdateAnim()

    # -- Update Developer Console Windows -- #
    if ConsoleWindowEnabled:
        developWindow.Update()

def UpdateControls():
    global TopMenu_BackToGame_Button
    global UIOpacityAnim_OutSoundPlayed
    global ControlsEnabled
    global ConsoleWindowEnabled
    global PendingToExitToMainMenu
    global TopMenu_MainMenu
    global ExitToMainMenuAnim

    if TopMenu_BackToGame_Button.ButtonState == 2:
        UIOpacityAnim_OutSoundPlayed = False
        if not GlobalAnimationController.Enabled:
            GlobalAnimationController.Enabled = True
            ControlsEnabled = False
            tge.devel.PrintToTerminalBuffer("TaiyouUI.Buttons :\n(BackToGame_func)[Variables Set]")

    if TopMenu_DeveloperConsoleButton.ButtonState == 2:
        if ConsoleWindowEnabled:
            ConsoleWindowEnabled = False
        else:
            ConsoleWindowEnabled = True

    if TopMenu_MainMenu.ButtonState == 2:
        TopMenu_MainMenu.ButtonState = 0
        taiyouMain.SystemUI.OverlayDialogEnabled = True
        taiyouMain.SystemUI.ovelDiag.Subscreen = 2

        PendingToExitToMainMenu = True
        taiyouMain.SystemUI.ovelDiag.subscreen2.Response = ""
        taiyouMain.SystemUI.ovelDiag.subscreen2.ResponseType = "YESNO"
        taiyouMain.SystemUI.ovelDiag.subscreen2.SetMessage(gtk.GetLangText("restartconfirm_title_generic", "overlay"), gtk.GetLangText("restartconfirm_text_exit", "overlay"))
        tge.devel.PrintToTerminalBuffer("TaiyouUI.Buttons :\n(BackToMainMenu_func)[Variables Set]")

    if PendingToExitToMainMenu:
        if taiyouMain.SystemUI.ovelDiag.subscreen2.ResponseTrigger:
            if taiyouMain.SystemUI.ovelDiag.subscreen2.Response == "YES":
                tge.devel.PrintToTerminalBuffer("TaiyouUI.PendingOperations :\n(ExitToMainMenu)[Function Called]")
                ExitToMainMenuAnim = True
                PendingToExitToMainMenu = False
                ControlsEnabled = False


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

    sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Notify", True))


def UpdateOpacityAnim():
    global UIOpacity
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
    global ControlsEnabled
    global ExitTOMainMenuSurfaceCreated
    global GlobalAnimationController

    GlobalAnimationController.Update()
    UIOpacity = GlobalAnimationController.Value

    if GlobalAnimationController.Enabled:
        if GlobalAnimationController.CurrentMode:  # <- When Opening the Menu;
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
                sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/In", True))
                UIOpacityAnim_InSoundPlayed = True

            if GlobalAnimationController.Value >= 255:
                UIOpacity = 255
                UIOpacityAnim_InSoundPlayed = True
                UIOpacityAnim_OutSoundPlayed = True
                print("Taiyou.SystemUI.AnimationTrigger : Animation Start.")
                ControlsEnabled = True
                ExitTOMainMenuSurfaceCreated = False

        elif not GlobalAnimationController.CurrentMode:  # <- When Backing to the Game
            # -- Close Windows -- #
            if not OpenedInGameError:
                ConsoleWindowEnabled = False

            # -- Play the Out Sound -- #
            if not UIOpacityAnim_OutSoundPlayed:
                sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Out", True))
                UIOpacityAnim_OutSoundPlayed = True

            if GlobalAnimationController.Value <= 0:
                UIOpacity = 0
                UnloadVars()

                # -- Enable GameLoop -- #
                taiyouMain.ReceiveCommand(5)
                print("Taiyou.SystemUI.AnimationTrigger : Animation End.")


# -- Set all Variable to Default Value -- #
def UnloadVars():
    global ExitToMainMenuAnim
    global ExitToMainMenuAnimOpacity
    global UIObjectsSurfaceUpdated
    global CopyOfTheScreen
    global UIOpacity
    global UIOpacityAnim_InSoundPlayed
    global UIOpacityAnim_OutSoundPlayed
    global PendingToExitToMainMenu
    global UIOpacity
    global ExitTOMainMenuSurfaceCreated
    global CopyOfScreen_Result
    global ConsoleWindowEnabled
    global UIOpacityAnim_InGameErrorSoundPlayed
    global OpenedInGameError
    global CopyOfScreen_Last
    global UIOpacityPauseGame
    global ControlsEnabled
    global GlobalAnimationController
    global ExitToMainMenuAnim
    global ExitToMainMenuAnimOpacity

    # -- Restart Variables -- #
    UIOpacity = 0
    CopyOfTheScreen.fill((0, 0, 0))
    DarkerBackgroundSurface.fill((0, 0, 0))
    UIObjectsSurface.fill((0, 0, 0))
    CopyOfTheScreen.fill((0, 0, 0))
    CopyOfScreen_Result.fill((0, 0, 0))
    UIOpacityPauseGame = False
    UIObjectsSurfaceUpdated = False
    ConsoleWindowEnabled = False
    CopyOfScreen_Last = False
    UIOpacityAnim_InSoundPlayed = False
    UIOpacityAnim_OutSoundPlayed = False
    OpenedInGameError = False
    UIOpacityAnim_InGameErrorSoundPlayed = False
    UiHandler.SystemMenuEnabled = False
    ControlsEnabled = False
    ExitTOMainMenuSurfaceCreated = False
    GlobalAnimationController.Enabled = True
    GlobalAnimationController.CurrentMode = True
    GlobalAnimationController.DisableSignal = False
    GlobalAnimationController.ValueMultiplier = 1
    GlobalAnimationController.Value = 0
    ExitToMainMenuAnim = False
    ExitToMainMenuAnimOpacity = 0

# -- Update the ExitToMainMenu Animation -- #
def ExitToMainMenu_UpdateAnim():
    global ExitToMainMenuAnim
    global ControlsEnabled
    global UIOpacity
    global ExitToMainMenuAnimOpacity

    if ExitToMainMenuAnim:
        ControlsEnabled = False
        UIOpacity -= 5.0
        ExitToMainMenuAnimOpacity += 10.5

        if UIOpacity <= 0:
            # -- Restart Variables -- #
            UnloadVars()

            # -- Go To the Main Menu  -- #
            taiyouMain.ReceiveCommand(8)
            taiyouMain.ReceiveCommand(6)
            UiHandler.CurrentMenuScreen = 2
            UiHandler.Cursor_CurrentLevel = 0
            UiHandler.SystemMenuEnabled = True

            # -- Set Menu Mode DISPLAY Changes -- #
            UiHandler.SetMenuMode_Changes()



def EventUpdate(event):
    global TopMenu_BackToGame_Button
    global TopMenu_DeveloperConsoleButton
    global ConsoleWindowEnabled
    global UIObjectsSurfaceUpdated
    global TopMenu_MainMenu

    # -- Update Buttons Events -- #
    TopMenu_BackToGame_Button.Update(event)
    TopMenu_DeveloperConsoleButton.Update(event)
    TopMenu_MainMenu.Update(event)
    volumeSlider.EventUpdate(event)

    # -- Update the Console only when it is Enabled -- #
    if ConsoleWindowEnabled:
        developWindow.EventUpdate(event)
