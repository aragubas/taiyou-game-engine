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
from ENGINE.TaiyouUI import UIGTK as gtk
from ENGINE.TaiyouUI import GameOverlay as handler
from ENGINE import SPRITE as sprite
from ENGINE import SOUND as sound
from ENGINE import REGISTRY as reg
import ENGINE as tge

# -- Restart Game Confirm -- #
Enabled = False
Surface = pygame.Surface
AnimMode = 0
AnimEnabled = False
UpdateBackground = False
AnimOpacity = 0
AnimNumb = 0
Rectangle = pygame.Rect(0,0,0,0)
YesButton = gtk.Button
NoButton = gtk.Button
Surface = pygame.Surface
SurfaceBackground = pygame.Surface
SurfacesUpdated = False
ActionType = 0
MessageTitle = "A"
MessageText = "B"
CommonDisplay = pygame.Surface

def Initialize():
    global YesButton
    global NoButton
    YesButton = gtk.Button(pygame.Rect(3,1,3,3), gtk.GetLangText("exit_yes", "overlay"), 28)
    NoButton = gtk.Button(pygame.Rect(3,1,3,3), gtk.GetLangText("exit_no", "overlay"), 28)

    YesButton.CustomColisionRectangle = True
    NoButton.CustomColisionRectangle = True

def Update():
    global Enabled
    global SurfacesUpdated
    global SurfaceBackground
    global CommonDisplay
    global YesButton
    global NoButton
    global AnimEnabled
    global Rectangle
    global CommonDisplay

    if Enabled:
        # -- Update the Opacity Anim -- #
        UpdateOpacityAnim()
        Rectangle = pygame.Rect((CommonDisplay.get_width() / 2 - 440 / 2, CommonDisplay.get_height() / 2 - 150 / 2, 440, 150))

        YesButton.Set_X(5)
        NoButton.Set_X(YesButton.Rectangle[0] + YesButton.Rectangle[2] + 15)

        YesButton.Set_Y(Rectangle[3] - YesButton.Rectangle[3] - 3)
        NoButton.Set_Y(YesButton.Rectangle[1])

        YesButton.ColisionRectangle = pygame.Rect(Rectangle[0] + 5, Rectangle[1] + Rectangle[3] - YesButton.Rectangle[3] + 2, YesButton.Rectangle[2], YesButton.Rectangle[3])
        NoButton.ColisionRectangle = pygame.Rect(YesButton.ColisionRectangle[0] + YesButton.Rectangle[2] + 15, Rectangle[1] + Rectangle[3] - YesButton.Rectangle[3] + 2, NoButton.Rectangle[2], NoButton.Rectangle[3])

        if YesButton.ButtonState == "UP":
            if ActionType == 0:
                tge.TaiyouUI.Messages.append("RELOAD_GAME")
                handler.ExitToInitializeGame = True
                tge.devel.PrintToTerminalBuffer("TaiyouUI.Buttons :\nRestart Game")
                AnimEnabled = True
            elif ActionType == 1:
                handler.ExitToMainMenuAnim = True

            sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Confirm"))

        if NoButton.ButtonState == "UP":
            AnimEnabled = True
            sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Decline"))

def UpdateOpacityAnim():
    global AnimEnabled
    global AnimMode
    global AnimOpacity
    global AnimNumb
    global Enabled

    if AnimEnabled:
        AnimNumb = AnimOpacity - 255 + 15

        if AnimMode == 0:
            AnimOpacity += 15

            if AnimOpacity >= 255:
                AnimOpacity = 255
                AnimMode = 1
                AnimEnabled = False

        if AnimMode == 1:
            AnimOpacity -= 15

            if AnimOpacity <= 0:
                AnimOpacity = 0
                AnimMode = 0
                AnimEnabled = False
                Enabled = False


def Render(DISPLAY):
    global Enabled
    global SurfacesUpdated
    global SurfaceBackground
    global Surface
    global YesButton
    global NoButton
    global CommonDisplay

    if Enabled:
        CommonDisplay = DISPLAY

        # -- Render the Background -- #
        if not SurfacesUpdated:
            SurfacesUpdated = True
            SurfaceBackground = pygame.Surface((DISPLAY.get_width() - AnimNumb, DISPLAY.get_height()))
            SurfaceBackground.fill((0, 0, 0))
        Surface = pygame.Surface((Rectangle[2] + 2, Rectangle[3] + 2), pygame.SRCALPHA)

        SurfaceBackground.set_alpha(AnimOpacity)
        DISPLAY.blit(SurfaceBackground, (0, 0))

        # -- Set the Background Alfa -- #
        Surface.set_alpha(AnimOpacity)

        gtk.Draw_Panel(Surface, (0, 0, Rectangle[2], Rectangle[3]), "BORDER", AnimOpacity)

        sprite.Shape_Rectangle(Surface, gtk.PANELS_INDICATOR_COLOR, (0, 0, Rectangle[2], 30))

        sprite.FontRender(Surface, "/Ubuntu_Bold.ttf", 24, MessageTitle, (250, 250, 255), Surface.get_width() / 2 - sprite.GetFont_width("/Ubuntu_Bold.ttf", 24, MessageTitle) / 2, 1)

        sprite.FontRender(Surface, "/Ubuntu_Bold.ttf", 14, MessageText, (230, 230, 230, AnimOpacity), 4, 35)

        # -- Render Button -- #
        YesButton.Render(Surface)
        NoButton.Render(Surface)

        DISPLAY.blit(Surface, (Rectangle[0], Rectangle[1] - AnimNumb * 0.8))

def EventUpdate(event):
    YesButton.Update(event)
    NoButton.Update(event)
