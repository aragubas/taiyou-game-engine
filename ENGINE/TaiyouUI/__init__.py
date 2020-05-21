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
from ENGINE.TaiyouUI import GameSeletor as seletorScreen
from ENGINE.TaiyouUI import loadingScreen as loadingScreen
import ENGINE as tge

CurrentMenuScreen = 2 # 0 = Game Overlay, 1 = Option, 2 = Main Menu, 4 = Loading Screen
SystemMenuEnabled = True
Cursor_Position = (0,0)

def Initialize():
    print("TaiyouUI.Initialize : Started")

    # -- Load the Language -- #
    gtk.SetLang(reg.ReadKey("/TaiyouSystem/CONF/lang"))


    gameOverlay.Initialize()
    seletorScreen.Initialize()
    loadingScreen.Initialize()

    print("TaiyouUI.Initialize : Initialization Complete.")

def Draw(Display):
    global SystemMenuEnabled
    global CurrentMenuScreen

    if SystemMenuEnabled:
        if CurrentMenuScreen == 4:
            loadingScreen.Draw(Display)
        if CurrentMenuScreen == 2:
            seletorScreen.Draw(Display)
        if CurrentMenuScreen == 0:
            gameOverlay.Draw(Display)

    sprite.Render(Display, "/TAIYOU_UI/Cursor/0.png", Cursor_Position[0], Cursor_Position[1], 15, 22)

def Update():
    global SystemMenuEnabled
    global Cursor_Position
    global CurrentMenuScreen

    if SystemMenuEnabled:
        if CurrentMenuScreen == 4:
            loadingScreen.Update()
        if CurrentMenuScreen == 2:
            seletorScreen.Update()
        if CurrentMenuScreen == 0:
            gameOverlay.Update()

        # -- Set Cursor Position -- #
        Cursor_Position = pygame.mouse.get_pos()

def EventUpdate(event):
    global SystemMenuEnabled
    global CurrentMenuScreen

    if SystemMenuEnabled:
        if CurrentMenuScreen == 4:
            loadingScreen.EventUpdate(event)
        if CurrentMenuScreen == 2:
            seletorScreen.EventUpdate(event)
        if CurrentMenuScreen == 0:
            gameOverlay.EventUpdate(event)


def SetMenuMode_Changes():
    print("TaiyouUI.SetMenuModeChanges")
    pygame.display.set_caption("Taiyou System Menu v" + tge.Get_TaiyouUIVersion())
    Messages.append("RESIZIABLE_WINDOW:False")
    if not pygame.display.get_window_size() == (800,600):
        Messages.append("SET_RESOLUTION:800:600")


# -- Send the messages on the Message Quee to the Game Engine -- #
Messages = list()
def ReadCurrentMessages():
    global Messages
    try:
        for x in Messages:
            Messages.remove(x)
            print("SystemUI : MessageSent[" + x + "]")
            return x
    except:
        return ""
