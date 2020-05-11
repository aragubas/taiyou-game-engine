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
from ENGINE.TaiyouUI import DeveloperConsole as developWindow

TopBarRectangle = pygame.Rect(0,0,0,0)
UIObjectsSurface = pygame.Surface((5,5))
DarkerBackgroundSurface = pygame.Surface((5,5))
CopyOfTheScreen = pygame.Surface((5,5))
DISPLAYObject = pygame.Surface((5,5))
Cursor_Position = (0,0)
TopMenu_BackToGame_Button = gtk.Button
TopMenu_DeveloperConsoleButton = gtk.Button
TopMenu_RestartGame = gtk.Button

UIOpacity = 0
UIOpacityAnimSpeed = 15
UIOpacityAnimEnabled = True
UIOpacityAnimState = 0
UIOpacityScreenCopyied = False
SystemMenuEnabled = True


AnimationNumb = 0

def Initialize():
    global TopMenu_BackToGame_Button
    global TopMenu_DeveloperConsoleButton
    global TopMenu_RestartGame
    TopMenu_BackToGame_Button = gtk.Button((3,1,5,5), "Back", 18)
    TopMenu_DeveloperConsoleButton = gtk.Button((3,1,5,5), "Console", 18)
    TopMenu_RestartGame = gtk.Button((3,1,3,3), "Restart", 18)
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
    global SystemMenuEnabled
    global DarkerBackgroundSurface
    global DISPLAYObject
    global CopyOfTheScreen
    DISPLAYObject = Display
    if SystemMenuEnabled:
        # -- Draw the Dark Background -- #
        Display.blit(CopyOfTheScreen, (0,0))
        UIObjectsSurface = pygame.Surface((Display.get_width(), Display.get_height()), pygame.SRCALPHA)


        #UIObjectsSurface.fill((0,0,0, UIOpacity))
        sprite.RenderRectangle(UIObjectsSurface, (0,0,0, UIOpacity), (0,0, UIObjectsSurface.get_width(), UIObjectsSurface.get_height()))

        # -- Render the Top Bar -- #
        gtk.Draw_Panel(UIObjectsSurface, TopBarRectangle, "DOWN")

        # -- Render Buttons -- #
        TopMenu_BackToGame_Button.Render(UIObjectsSurface)
        TopMenu_DeveloperConsoleButton.Render(UIObjectsSurface)
        TopMenu_RestartGame.Render(UIObjectsSurface)

        # -- Draw the Developer Console -- #
        developWindow.Draw(UIObjectsSurface)

        sprite.Render(UIObjectsSurface, "/TAIYOU_UI/Cursor/0.png", Cursor_Position[0],Cursor_Position[1], 15,22)

        Display.blit(UIObjectsSurface, (0,0))


def Update():
    global Cursor_Position
    global TopBarRectangle
    global UIObjectsSurface
    global TopMenu_DeveloperConsoleButton
    global TopMenu_BackToGame_Button
    global UIOpacityAnimEnabled
    global SystemMenuEnabled
    global AnimationNumb
    global UIOpacityAnimSpeed
    global TopMenu_RestartGame

    if SystemMenuEnabled:
        AnimationNumb = UIOpacity - 255 + UIOpacityAnimSpeed

        TopBarRectangle = pygame.Rect(0, AnimationNumb, UIObjectsSurface.get_width(), 25)

        TopMenu_DeveloperConsoleButton.Set_X(TopMenu_BackToGame_Button.Rectangle[0] + TopMenu_BackToGame_Button.Rectangle[2] + 2)
        TopMenu_RestartGame.Set_X(TopMenu_DeveloperConsoleButton.Rectangle[0] + TopMenu_DeveloperConsoleButton.Rectangle[2] + 2)
        TopMenu_DeveloperConsoleButton.Set_Y(AnimationNumb + 2)
        TopMenu_BackToGame_Button.Set_Y(AnimationNumb + 2)
        TopMenu_RestartGame.Set_Y(AnimationNumb + 2)

        if TopMenu_BackToGame_Button.ButtonState == "UP":
            if not UIOpacityAnimEnabled:
                UIOpacityAnimEnabled = True

        UpdateOpacityAnim()

        # -- Update Developer Console Windows -- #
        developWindow.Update()

        # -- Set Cursor Position -- #
        Cursor_Position = pygame.mouse.get_pos()


def UpdateOpacityAnim():
    global UIOpacityAnimState
    global UIOpacity
    global UIOpacityAnimEnabled
    global UIOpacityAnimSpeed
    global SystemMenuEnabled
    global Messages
    global CopyOfTheScreen
    global DarkerBackgroundSurface
    global UIObjectsSurface
    global UIOpacityScreenCopyied

    if UIOpacityAnimEnabled:
        if UIOpacityAnimState == 0:
            UIOpacity += UIOpacityAnimSpeed

            # -- Copy the Screen Surface -- #
            if not UIOpacityScreenCopyied:
                CopyOfTheScreen = DISPLAYObject.copy()

                UIOpacityScreenCopyied = True
                print("Taiyou.SystemUI.AnimationTrigger : Screen Copied.")
                Messages.append("GAME_UPDATE:False")

            if UIOpacity >= 255:
                UIOpacity = 255
                UIOpacityAnimEnabled = False
                UIOpacityAnimState = 1
                print("Taiyou.SystemUI.AnimationTrigger : Animation Start.")



        if UIOpacityAnimState == 1:
            UIOpacity -= UIOpacityAnimSpeed

            if UIOpacity <= 0:
                UIOpacity = 0
                UIOpacityAnimEnabled = False
                UIOpacityAnimState = 0
                Messages.append("GAME_UPDATE:True")
                print("Taiyou.SystemUI.AnimationTrigger : Animation End.")
                # -- Unload the Surfaces -- #
                CopyOfTheScreen = pygame.Surface((5,5))
                DarkerBackgroundSurface = pygame.Surface((5,5))
                UIObjectsSurface = pygame.Surface((5,5))
                UIOpacityScreenCopyied = False
                SystemMenuEnabled = False

def EventUpdate(event):
    global TopMenu_BackToGame_Button
    global TopMenu_DeveloperConsoleButton
    global SystemMenuEnabled
    global TopMenu_RestartGame

    if SystemMenuEnabled:
        TopMenu_BackToGame_Button.Update(event)
        TopMenu_DeveloperConsoleButton.Update(event)
        TopMenu_RestartGame.Update(event)

        developWindow.EventUpdate(event)

Messages = list()
# -- Send the messages on the Message Quee to the Game Engine -- #
def ReadCurrentMessages():
    global Messages
    try:
        for x in Messages:
            Messages.remove(x)
            print("SystemUI : MessageSent[" + x + "]")
            return x
    except:
        return ""
