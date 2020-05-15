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
import pygame, sys
from ENGINE import SPRITE as sprite
from ENGINE import REGISTRY as reg
from ENGINE.TaiyouUI import UIGTK as gtk
from ENGINE.TaiyouUI import GameOverlay as gameOverlay
from ENGINE.TaiyouUI import LicenseScreen as licenseScreen
import ENGINE as tge

CurrentMenuScreen = 0 # 0 = Game Overlay, 1 = Main Menu, 2 = Options, 3 = License
SystemMenuEnabled = True
Cursor_Position = (0,0)

def Initialize():
    print("TaiyouUI.Initialize : Started")

    gameOverlay.Initialize()

    print("TaiyouUI.Initialize : Initialization Complete.")

def Draw(Display):
    global SystemMenuEnabled
    global CurrentMenuScreen

    if SystemMenuEnabled:
        if CurrentMenuScreen == 3:
            licenseScreen.Draw(Display)
        if CurrentMenuScreen == 0:
            gameOverlay.Draw(Display)

    sprite.Render(Display, "/TAIYOU_UI/Cursor/0.png", Cursor_Position[0], Cursor_Position[1], 15, 22)

def Update():
    global SystemMenuEnabled
    global Cursor_Position
    global CurrentMenuScreen

    if SystemMenuEnabled:
        if CurrentMenuScreen == 3:
            licenseScreen.Update()
        if CurrentMenuScreen == 0:
            gameOverlay.Update()

        # -- Set Cursor Position -- #
        Cursor_Position = pygame.mouse.get_pos()

def EventUpdate(event):
    global SystemMenuEnabled
    global CurrentMenuScreen

    if SystemMenuEnabled:
        if CurrentMenuScreen == 3:
            licenseScreen.EventUpdate(event)
        if CurrentMenuScreen == 0:
            gameOverlay.EventUpdate(event)

Messages = list()

def SetMenuMode_Changes():
    print("TaiyouUI.SetMenuModeChanges")
    pygame.display.set_caption("Taiyou System Menu v" + tge.Get_TaiyouUIVersion())
    Messages.append("RESIZIABLE_WINDOW:False")
    Messages.append("SET_RESOLUTION:800:600")


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
