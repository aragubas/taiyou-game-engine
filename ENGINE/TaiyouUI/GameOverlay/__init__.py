#!/usr/bin/python3
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
from ENGINE import SOUND as sound
from ENGINE.TaiyouUI import DeveloperConsole as developWindow
import ENGINE as tge
from ENGINE import UTILS as utils
from ENGINE import TaiyouUI as UiHandler

TopBarRectangle = pygame.Rect(0,0,0,0)
DownBarRectangle = pygame.Rect(0,0,0,0)
UIObjectsSurface = pygame.Surface((5,5))
DarkerBackgroundSurface = pygame.Surface((5,5))
CopyOfTheScreen = pygame.Surface((5,5))
DISPLAYObject = pygame.Surface((5,5))
TopMenu_BackToGame_Button = gtk.Button
TopMenu_DeveloperConsoleButton = gtk.Button
TopMenu_RestartGame = gtk.Button
TopMenu_MainMenu = gtk.Button

# -- General -- #
UIOpacity = 0
UIOpacityAnimSpeed = 15
UIOpacityAnimEnabled = True
UIOpacityAnimState = 0
UIOpacityScreenCopyied = False
UIOpacityAnim_InSoundPlayed = False
UIOpacityAnim_OutSoundPlayed = False
ConsoleWindowEnabled = False
IsFirstOpening = True
UIObjectsSurfaceUpdated = False
ExitToInitializeGame = False
OpenedInGameError = False
AnimationNumb = 0

# -- Exit to Main Menu Anim -- #
ExitToMainMenuAnim = False
ExitToMainMenuAnimOpacity = 0
ExitTOMainMenuSurfaceCreated = False
ExitToMainMenuOpacityAnimBG = pygame.Surface((0,0))

# -- Restart Game Confirm -- #
RestartGameConfirm_Enabled = False
RestartGame_Surface = pygame.Surface
RestartGameConfirm_AnimMode = 0
RestartGameConfirm_AnimEnabled = False
RestartGameConfirm_UpdateBackground = False
RestartGameConfirm_AnimOpacity = 0
RestartGameConfirm_AnimNumb = 0
RestartGameConfirm_Rectangle = pygame.Rect(0,0,0,0)
RestartGameConfirm_YesButton = gtk.Button
RestartGameConfirm_NoButton = gtk.Button
RestartGameConfirm_Surface = pygame.Surface
RestartGameConfirm_SurfaceBackground = pygame.Surface
RestartGameConfirm_SurfacesUpdated = False
RestartGameConfirm_ActionType = 0
RestartGameConfirm_MessageTitle = "A"
RestartGameConfirm_MessageText = "B"

def Initialize():
    global TopMenu_BackToGame_Button
    global TopMenu_DeveloperConsoleButton
    global TopMenu_RestartGame
    global RestartGameConfirm_YesButton
    global RestartGameConfirm_NoButton
    global TopMenu_MainMenu

    developWindow.Initialize()
    TopMenu_BackToGame_Button = gtk.Button(pygame.Rect(3, 1, 5, 5), "Start Game", 14)
    TopMenu_DeveloperConsoleButton = gtk.Button(pygame.Rect(3, 1, 5, 5), "Console", 14)
    TopMenu_RestartGame = gtk.Button(pygame.Rect(3,1,3,3), "Restart", 14)
    RestartGameConfirm_YesButton = gtk.Button(pygame.Rect(3,1,3,3), "Yes", 28)
    RestartGameConfirm_NoButton = gtk.Button(pygame.Rect(3,1,3,3), "No", 28)
    TopMenu_MainMenu = gtk.Button(pygame.Rect(3,1,1,3), "Exit", 14)
    RestartGameConfirm_YesButton.CustomColisionRectangle = True
    RestartGameConfirm_NoButton.CustomColisionRectangle = True

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
    global RestartGameConfirm_Enabled
    global RestartGameConfirm_YesButton
    global RestartGameConfirm_NoButton
    global RestartGameConfirm_Rectangle
    global RestartGame_Surface
    global RestartGameConfirm_AnimOpacity
    global RestartGameConfirm_UpdateBackground
    global OpenedInGameError
    global TopMenu_MainMenu
    global ExitToMainMenuAnim
    global ExitTOMainMenuSurfaceCreated
    global ExitToMainMenuOpacityAnimBG

    DISPLAYObject = Display
    # -- Draw the Dark Background -- #
    if not RestartGameConfirm_Enabled and not OpenedInGameError:
        Display.blit(CopyOfTheScreen, (0, 0))
    if not UIObjectsSurfaceUpdated:
        UIObjectsSurface = pygame.Surface((Display.get_width(), Display.get_height()), pygame.SRCALPHA)
        UIObjectsSurfaceUpdated = True

    sprite.RenderRectangle(UIObjectsSurface, (0, 0, 0, UIOpacity), (0, 0, UIObjectsSurface.get_width(), UIObjectsSurface.get_height()))

    # -- Render the Top Bar -- #
    gtk.Draw_Panel(UIObjectsSurface, TopBarRectangle, "DOWN")

    # -- Render the Down Bar -- #
    gtk.Draw_Panel(UIObjectsSurface, DownBarRectangle, "UP")

    # -- Render Buttons -- #
    TopMenu_BackToGame_Button.Render(UIObjectsSurface)
    TopMenu_DeveloperConsoleButton.Render(UIObjectsSurface)
    TopMenu_RestartGame.Render(UIObjectsSurface)
    TopMenu_MainMenu.Render(UIObjectsSurface)

    # -- Render Taiyou Version -- #
    sprite.RenderFont(UIObjectsSurface, "/PressStart2P.ttf", 16, "v" + str(utils.FormatNumber(tge.TaiyouGeneralVersion)), (240, 240, 240), 5, DownBarRectangle[1] + 7)

    # -- Draw the Developer Console -- #
    if ConsoleWindowEnabled:
        developWindow.Draw(UIObjectsSurface)

    # -- Restart Game Confirm -- #
    RenderRestartGameConfirm(UIObjectsSurface)

    Display.blit(UIObjectsSurface, (0, 0))

    if ExitToMainMenuAnim and ExitTOMainMenuSurfaceCreated:
        ExitToMainMenuOpacityAnimBG.fill((0,0,0))
        ExitToMainMenuOpacityAnimBG.set_alpha(ExitToMainMenuAnimOpacity * 2)

        Display.blit(ExitToMainMenuOpacityAnimBG, (0,0))
2
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
    global IsFirstOpening
    global ExitToInitializeGame
    global RestartGameConfirm_Enabled
    global RestartGameConfirm_YesButton
    global RestartGameConfirm_NoButton
    global RestartGameConfirm_Rectangle
    global RestartGameConfirm_AnimEnabled
    global RestartGameConfirm_AnimMode
    global RestartGameConfirm_AnimNumb
    global UIOpacityAnim_OutSoundPlayed
    global RestartGameConfirm_ActionType
    global TopMenu_MainMenu
    global ExitTOMainMenuSurfaceCreated
    global ExitToMainMenuAnim
    global ExitToMainMenuOpacityAnimBG

    # -- Exit to Main Menu Anim -- #
    if ExitToMainMenuAnim:
        if not ExitTOMainMenuSurfaceCreated:
            ExitToMainMenuOpacityAnimBG = pygame.Surface((DISPLAYObject.get_width(), DISPLAYObject.get_height()))
            ExitTOMainMenuSurfaceCreated = True
            print("ExitToMainMenuSurface has been created.")

    # -- Restart Game Dialog -- #
    if RestartGameConfirm_Enabled:
        RestartGameConfirm_Rectangle = pygame.Rect((UIObjectsSurface.get_width() / 2 - 440 / 2, UIObjectsSurface.get_height() / 2 - 150 / 2, 440, 150))

        RestartGameConfirm_YesButton.Set_X(110)
        RestartGameConfirm_NoButton.Set_X(RestartGameConfirm_YesButton.Rectangle[0] + RestartGameConfirm_YesButton.Rectangle[2] + 50)

        RestartGameConfirm_YesButton.Set_Y(RestartGameConfirm_Rectangle[3] - RestartGameConfirm_YesButton.Rectangle[3] + 2)
        RestartGameConfirm_NoButton.Set_Y(RestartGameConfirm_YesButton.Rectangle[1])

        RestartGameConfirm_YesButton.ColisionRectangle = pygame.Rect(RestartGameConfirm_Rectangle[0] + 110, RestartGameConfirm_Rectangle[1] + RestartGameConfirm_Rectangle[3] - RestartGameConfirm_YesButton.Rectangle[3] + 2, RestartGameConfirm_YesButton.Rectangle[2], RestartGameConfirm_YesButton.Rectangle[3])
        RestartGameConfirm_NoButton.ColisionRectangle = pygame.Rect(RestartGameConfirm_YesButton.ColisionRectangle[0] + RestartGameConfirm_YesButton.Rectangle[2] + 50, RestartGameConfirm_Rectangle[1] + RestartGameConfirm_Rectangle[3] - RestartGameConfirm_YesButton.Rectangle[3] + 2, RestartGameConfirm_NoButton.Rectangle[2], RestartGameConfirm_NoButton.Rectangle[3])

        if RestartGameConfirm_YesButton.ButtonState == "UP":
            if RestartGameConfirm_ActionType == 0:
                UiHandler.Messages.append("RESTART_GAME")
                IsFirstOpening = True
                ExitToInitializeGame = True
                tge.devel.PrintToTerminalBuffer("TaiyouUI.Buttons :\nRestart Game")
                RestartGameConfirm_AnimEnabled = True
            elif RestartGameConfirm_ActionType == 1:
                ExitToMainMenuAnim = True

            sound.PlaySound("/TAIYOU_UI/HUD_Confirm.ogg")

        if RestartGameConfirm_NoButton.ButtonState == "UP":
            RestartGameConfirm_AnimEnabled = True
            sound.PlaySound("/TAIYOU_UI/HUD_Out.ogg")

    AnimationNumb = UIOpacity - 255 + UIOpacityAnimSpeed

    if IsFirstOpening:
        TopMenu_BackToGame_Button.Set_Text("Start Game")
    else:
        TopMenu_BackToGame_Button.Set_Text("Back")

    TopBarRectangle = pygame.Rect(0, AnimationNumb, UIObjectsSurface.get_width(), 25)
    DownBarRectangle = pygame.Rect(0, UIObjectsSurface.get_height() - AnimationNumb - 25, UIObjectsSurface.get_width(), 25)

    # -- Set Objects X -- #
    TopMenu_MainMenu.Set_X(TopMenu_RestartGame.Rectangle[0] + TopMenu_RestartGame.Rectangle[2] + 2)
    TopMenu_DeveloperConsoleButton.Set_X(TopMenu_BackToGame_Button.Rectangle[0] + TopMenu_BackToGame_Button.Rectangle[2] + 2)
    TopMenu_RestartGame.Set_X(TopMenu_DeveloperConsoleButton.Rectangle[0] + TopMenu_DeveloperConsoleButton.Rectangle[2] + 2)
    TopMenu_BackToGame_Button.Set_X(3)

    # -- Set Objects Y -- #
    TopMenu_BackToGame_Button.Set_Y(AnimationNumb + 3)
    TopMenu_DeveloperConsoleButton.Set_Y(TopMenu_BackToGame_Button.Rectangle[1])
    TopMenu_RestartGame.Set_Y(TopMenu_BackToGame_Button.Rectangle[1])
    TopMenu_MainMenu.Set_Y(TopMenu_BackToGame_Button.Rectangle[1])

    if TopMenu_BackToGame_Button.ButtonState == "UP" and not RestartGameConfirm_Enabled:
        UIOpacityAnim_OutSoundPlayed = False
        if not UIOpacityAnimEnabled:
            UIOpacityAnimEnabled = True
            tge.devel.PrintToTerminalBuffer("TaiyouUI.Buttons :\n(BackToGame_function)[Back to Game]")
            if IsFirstOpening and not ExitToInitializeGame:
                ExitToInitializeGame = True
                tge.devel.PrintToTerminalBuffer("TaiyouUI.Buttons :\n(BackToGame_function)[Start Game]")

    if TopMenu_DeveloperConsoleButton.ButtonState == "UP" and not RestartGameConfirm_Enabled:
        if ConsoleWindowEnabled:
            ConsoleWindowEnabled = False
        else:
            ConsoleWindowEnabled = True

    if TopMenu_RestartGame.ButtonState == "UP" and not RestartGameConfirm_Enabled:
        # -- Alert to Restart -- #
        ShowRestartConfirm("Are you Sure?", "Did you really want to Restart?\nAny unsaved data will be lost.", 0)

    if TopMenu_MainMenu.ButtonState == "UP" and not RestartGameConfirm_Enabled:
        # -- Alert to Restart -- #
        ShowRestartConfirm("Are you Sure?", "Did you really want to Exit?\nAny unsaved data will be lost.", 1)

    # -- Run the Menu Animation -- #
    UpdateOpacityAnim()

    # -- Run the Back to Main Menu Animation -- #
    ExitToMainMenu_UpdateAnim()

    # -- Run the Restart Confirm Animation -- #
    RestartConfirmOpacity()

    # -- Update Developer Console Windows -- #
    if ConsoleWindowEnabled:
        developWindow.Update()


def ShowRestartConfirm(Title, Text, ActionType):
    global RestartGameConfirm_MessageTitle
    global RestartGameConfirm_MessageText
    global RestartGameConfirm_ActionType
    global RestartGameConfirm_Enabled
    global ConsoleWindowEnabled
    global RestartGameConfirm_AnimEnabled
    RestartGameConfirm_MessageTitle = Title
    RestartGameConfirm_MessageText = Text
    RestartGameConfirm_ActionType = ActionType
    RestartGameConfirm_Enabled = True
    RestartGameConfirm_AnimEnabled = True
    ConsoleWindowEnabled = False
    sound.PlaySound("/TAIYOU_UI/HUD_Notify.ogg")

def RenderRestartGameConfirm(UIObjectsSurface):
    global RestartGameConfirm_Surface
    global RestartGameConfirm_SurfaceBackground
    global RestartGameConfirm_SurfacesUpdated
    global RestartGameConfirm_MessageTitle
    global RestartGameConfirm_MessageText

    if RestartGameConfirm_Enabled:
        # -- Render the Background -- #
        if not RestartGameConfirm_SurfacesUpdated:
            RestartGameConfirm_SurfacesUpdated = True
            RestartGameConfirm_SurfaceBackground = pygame.Surface((UIObjectsSurface.get_width() - RestartGameConfirm_AnimNumb, UIObjectsSurface.get_height()))
            RestartGameConfirm_SurfaceBackground.fill((0, 0, 0))
        RestartGameConfirm_Surface = pygame.Surface((RestartGameConfirm_Rectangle[2] + 2, RestartGameConfirm_Rectangle[3] + 2), pygame.SRCALPHA)

        RestartGameConfirm_SurfaceBackground.set_alpha(RestartGameConfirm_AnimOpacity)
        UIObjectsSurface.blit(RestartGameConfirm_SurfaceBackground, (0, 0))

        # -- Set the Background Alfa -- #
        RestartGameConfirm_Surface.set_alpha(RestartGameConfirm_AnimOpacity)

        gtk.Draw_Panel(RestartGameConfirm_Surface, (0, 0, RestartGameConfirm_Rectangle[2], RestartGameConfirm_Rectangle[3]), "BORDER")

        sprite.RenderRectangle(RestartGameConfirm_Surface, gtk.PANELS_INDICATOR_COLOR, (0, 0, RestartGameConfirm_Rectangle[2], 30))
        sprite.RenderFont(RestartGameConfirm_Surface, "/PressStart2P.ttf", 18, RestartGameConfirm_MessageTitle, (230, 230, 230), sprite.GetText_width("/PressStart2P.ttf", 18, "Are you sure?") / 2 - 18, 5)

        sprite.RenderFont(RestartGameConfirm_Surface, "/PressStart2P.ttf", 14, RestartGameConfirm_MessageText, (230, 230, 230), 4, 35)

        # -- Render OK Button -- #
        RestartGameConfirm_YesButton.Render(RestartGameConfirm_Surface)
        RestartGameConfirm_NoButton.Render(RestartGameConfirm_Surface)

        UIObjectsSurface.blit(RestartGameConfirm_Surface, (RestartGameConfirm_Rectangle[0], RestartGameConfirm_Rectangle[1] - RestartGameConfirm_AnimNumb * 0.8))

def RestartConfirmOpacity():
    global RestartGameConfirm_AnimEnabled
    global RestartGameConfirm_AnimMode
    global RestartGameConfirm_AnimOpacity
    global RestartGameConfirm_AnimNumb
    global RestartGameConfirm_Enabled

    if RestartGameConfirm_AnimEnabled:
        RestartGameConfirm_AnimNumb = RestartGameConfirm_AnimOpacity - 255 + 15

        if RestartGameConfirm_AnimMode == 0:
            RestartGameConfirm_AnimOpacity += 15

            if RestartGameConfirm_AnimOpacity >= 255:
                RestartGameConfirm_AnimOpacity = 255
                RestartGameConfirm_AnimMode = 1
                RestartGameConfirm_AnimEnabled = False

        if RestartGameConfirm_AnimMode == 1:
            RestartGameConfirm_AnimOpacity -= 15

            if RestartGameConfirm_AnimOpacity <= 0:
                RestartGameConfirm_AnimOpacity = 0
                RestartGameConfirm_AnimMode = 0
                RestartGameConfirm_AnimEnabled = False
                RestartGameConfirm_Enabled = False


def UpdateOpacityAnim():
    global UIOpacityAnimState
    global UIOpacity
    global UIOpacityAnimEnabled
    global UIOpacityAnimSpeed
    global CopyOfTheScreen
    global DarkerBackgroundSurface
    global UIObjectsSurface
    global UIOpacityScreenCopyied
    global ConsoleWindowEnabled
    global IsFirstOpening
    global UIObjectsSurfaceUpdated
    global ExitToInitializeGame
    global UIOpacityAnim_InSoundPlayed
    global UIOpacityAnim_OutSoundPlayed
    global RestartGameConfirm_SurfacesUpdated
    global OpenedInGameError

    if UIOpacityAnimEnabled:
        if UIOpacityAnimState == 0: # <- Enter Animation
            UIOpacity += UIOpacityAnimSpeed

            # -- Copy the Screen Surface -- #
            if not UIOpacityScreenCopyied and not OpenedInGameError:
                CopyOfTheScreen = DISPLAYObject.copy()

                UIOpacityScreenCopyied = True
                print("Taiyou.SystemUI.AnimationTrigger : Screen Copied.")
                UiHandler.Messages.append("GAME_UPDATE:False")

            if OpenedInGameError:
                ConsoleWindowEnabled = True
                sound.PlaySound("/TAIYOU_UI/HUD_Error.ogg")

            # -- Play the In Sound -- #
            if not UIOpacityAnim_InSoundPlayed:
                sound.PlaySound("/TAIYOU_UI/HUD_In.ogg")
                UIOpacityAnim_InSoundPlayed = True

            if UIOpacity >= 255: # <- Triggers Animation End
                UIOpacity = 255
                UIOpacityAnimEnabled = False
                UIOpacityAnimState = 1
                UIOpacityAnim_InSoundPlayed = True
                UIOpacityAnim_OutSoundPlayed = True
                print("Taiyou.SystemUI.AnimationTrigger : Animation Start.")

        if UIOpacityAnimState == 1: # <- Exit Animation
            UIOpacity -= UIOpacityAnimSpeed

            # -- Close Windows -- #
            if not OpenedInGameError:
                ConsoleWindowEnabled = False

            # -- Play the Out Sound -- #
            if not UIOpacityAnim_OutSoundPlayed:
                sound.PlaySound("/TAIYOU_UI/HUD_Out.ogg")
                UIOpacityAnim_OutSoundPlayed = True


            if UIOpacity <= 0: # <- Triggers Animation End
                UIOpacity = 0
                UIOpacityAnimEnabled = False
                UIOpacityAnimState = 0
                UiHandler.Messages.append("GAME_UPDATE:True")
                print("Taiyou.SystemUI.AnimationTrigger : Animation End.")
                # -- Unload the Surfaces -- #
                CopyOfTheScreen = pygame.Surface((0,0), pygame.SRCALPHA)
                DarkerBackgroundSurface = pygame.Surface((0,0), pygame.SRCALPHA)
                UIObjectsSurface = pygame.Surface((0,0), pygame.SRCALPHA)
                UIOpacityScreenCopyied = False
                UIObjectsSurfaceUpdated = False
                RestartGameConfirm_SurfacesUpdated = False

                # -- Initialize the Game when exiting -- #
                if ExitToInitializeGame and IsFirstOpening:
                    ExitToInitializeGame = False
                    print("Taiyou.SystemUI.AnimationTrigger : Toggle Game Initialize")
                    UiHandler.Messages.append("TOGGLE_GAME_START")
                    print("Taiyou.SystemUI.AnimationTrigger : Toggle Game Initialize, complete.")

                IsFirstOpening = False
                UIOpacityAnim_InSoundPlayed = False
                UIOpacityAnim_OutSoundPlayed = False
                OpenedInGameError = False
                UiHandler.SystemMenuEnabled = False

def ExitToMainMenu_UpdateAnim():
    global ExitToMainMenuAnim
    global ExitToMainMenuAnimOpacity
    global RestartGameConfirm_AnimNumb
    global RestartGameConfirm_Enabled
    global RestartGameConfirm_AnimOpacity
    global RestartGameConfirm_AnimMode
    global RestartGameConfirm_AnimNumb
    global RestartGameConfirm_AnimEnabled
    global IsFirstOpening

    if ExitToMainMenuAnim:
        ExitToMainMenuAnimOpacity += 5

        if ExitToMainMenuAnimOpacity >= 255:
            print("ExitToMainMenuAnim.AnimationTrigger : Animation has been ended.")

            # -- Restart the RestarGameConfirm -- #
            RestartGameConfirm_AnimOpacity = 0
            RestartGameConfirm_AnimMode = 0
            RestartGameConfirm_AnimEnabled = False
            RestartGameConfirm_Enabled = False
            ExitToMainMenuAnim = False
            ExitToMainMenuAnimOpacity = 0

            IsFirstOpening = True

            # -- Update the Main Menu Shenageins -- #
            UiHandler.Messages.append("SET_MENU_MODE")
            UiHandler.Messages.append("REMOVE_GAME")

            UiHandler.SetMenuMode_Changes()

            UiHandler.CurrentMenuScreen = 3

def EventUpdate(event):
    global TopMenu_BackToGame_Button
    global TopMenu_DeveloperConsoleButton
    global TopMenu_RestartGame
    global ConsoleWindowEnabled
    global UIObjectsSurfaceUpdated
    global RestartGameConfirm_Enabled
    global RestartGameConfirm_YesButton
    global RestartGameConfirm_NoButton
    global RestartGameConfirm_Enabled
    global RestartGameConfirm_SurfacesUpdated
    global TopMenu_MainMenu

    # -- Update Buttons Events -- #
    if not RestartGameConfirm_Enabled:
        TopMenu_BackToGame_Button.Update(event)
        TopMenu_DeveloperConsoleButton.Update(event)
        TopMenu_RestartGame.Update(event)
        TopMenu_MainMenu.Update(event)

    # -- Update the Surface when Window Size Changes -- #
    if event.type == pygame.VIDEORESIZE:
        UIObjectsSurfaceUpdated = False
        RestartGameConfirm_SurfacesUpdated = False

    # -- Update the OK Button on Notification -- #
    if RestartGameConfirm_Enabled:
        RestartGameConfirm_YesButton.Update(event)
        RestartGameConfirm_NoButton.Update(event)

    # -- Update the Console only when it is Enabled -- #
    if ConsoleWindowEnabled:
        developWindow.EventUpdate(event)
