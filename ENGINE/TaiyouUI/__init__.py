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
import pygame, sys
from ENGINE import SPRITE as sprite
from ENGINE import REGISTRY as reg
from ENGINE.TaiyouUI import UIGTK as gtk
from ENGINE.TaiyouUI import GameOverlay as gameOverlay
from ENGINE.TaiyouUI import GameSeletor as seletorScreen
from ENGINE.TaiyouUI import LicenseScreen as licenseScreen
from ENGINE.TaiyouUI import loadingScreen as loadingScreen
from ENGINE.TaiyouUI import DeveloperConsole as devel
from ENGINE.TaiyouUI import ScreenshotUI as screenshotUI
from ENGINE import utils
import ENGINE as tge

CurrentMenuScreen = 1  # 0 = Game Overlay, 1 = License Screen, 2 = Main Menu, 3 = License Screen, 4 = Loading Screen
SystemMenuEnabled = True

# -- Cursor Variables -- #
Cursor_Position = (0, 0)
Cursor_CurrentLevel = 0

def Initialize():
    print("TaiyouUI.Initialize : Started")

    # -- Load the Language -- #
    gtk.SetLang(reg.ReadKey("/TaiyouSystem/CONF/lang"))

    # -- Initialize All Screens -- #
    gameOverlay.Initialize()
    seletorScreen.Initialize()
    loadingScreen.Initialize()
    licenseScreen.Initialize()
    SetMenuMode_Changes()

    print("TaiyouUI.Initialize : Initialization Complete.")


def Draw(Display):
    global SystemMenuEnabled
    global CurrentMenuScreen

    if SystemMenuEnabled:
        if CurrentMenuScreen == 4:
            loadingScreen.Draw(Display)

        if CurrentMenuScreen == 2:
            seletorScreen.Draw(Display)

        if CurrentMenuScreen == 1:
            licenseScreen.Draw(Display)

        if CurrentMenuScreen == 0:
            gameOverlay.Draw(Display)

    sprite.ImageRender(Display, "/TAIYOU_UI/Cursor/{0}.png".format(str(Cursor_CurrentLevel)), Cursor_Position[0], Cursor_Position[1])


def Update():
    global SystemMenuEnabled
    global Cursor_Position
    global CurrentMenuScreen

    if SystemMenuEnabled:
        if CurrentMenuScreen == 4:
            loadingScreen.Update()

        if CurrentMenuScreen == 2:
            seletorScreen.Update()

        if CurrentMenuScreen == 1:
            licenseScreen.Update()

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

        if CurrentMenuScreen == 1:
            licenseScreen.EventUpdate(event)

        if CurrentMenuScreen == 0:
            gameOverlay.EventUpdate(event)


def SetMenuMode_Changes():
    print("TaiyouUI.SetMenuModeChanges ; No Description")

    # -- Set the Window Title -- #
    Messages.append("SET_TITLE;" + "Taiyou Game Engine v" + utils.FormatNumber(tge.TaiyouGeneralVersion))
    # -- Set the Unresizeable window
    Messages.append("RESIZIABLE_WINDOW:FalseIfTrue")
    # -- Set the Default Icon -- #
    Messages.append("SET_ICON_BY_SPRITE:/TAIYOU_UI/icon.png")
    # -- Set to 60FPS -- #
    Messages.append("SET_FPS:60")

    CurrentRes = pygame.display.get_window_size()
    if not CurrentRes[0] == 800 and not CurrentRes[1] == 600:
        Messages.append("SET_RESOLUTION:800:600")
        print("Taiyou.SetMenuChanges : CurrentResolution is different than 800x600 [{0}x{1}]".format(str(CurrentRes[0]),
                                                                                                     str(CurrentRes[
                                                                                                             1])))
    else:
        print("Taiyou.SetMenuChanges : CurrentResolution is equals to 800x600 [{0}x{1}]".format(str(CurrentRes[0]),
                                                                                                str(CurrentRes[1])))


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
