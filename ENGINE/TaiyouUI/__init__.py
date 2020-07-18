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
from ENGINE.TaiyouUI import SaveFolderSelect as saveFolderSelectScreen
from ENGINE.TaiyouUI.GameOverlay import SystemVolumeSlider as volumeSlider
from ENGINE.TaiyouUI import OverlayDialog as ovelDiag
from ENGINE import TaiyouMain as taiyouMain
from ENGINE.TaiyouUI import DeveloperConsole as devel
from ENGINE import utils
from ENGINE import SOUND as sound
import ENGINE as tge

CurrentMenuScreen = 2  # 0 = Game Overlay, 1 = License Screen, 2 = Main Menu, 3 = Save Folder Select, 4 = Loading Screen
SystemMenuEnabled = True

# -- Cursor Variables -- #
Cursor_Position = (0, 0)
Cursor_CurrentLevel = 0
OverlayDialogEnabled = False
ScreenLastFrame = pygame.Surface

DataPath = "Taiyou/SYSTEM/"

def Initialize():
    global DataPath

    print("TaiyouUI.Initialize : Started")

    # -- Load TaiyouUi Assets -- #
    sprite.LoadSpritesInFolder(DataPath)
    sound.LoadAllSounds(DataPath)
    reg.Initialize(DataPath, True)


    # -- Load the Language -- #
    gtk.SetLang(tge.Get_UserLanguage())

    # -- Initialize All Screens -- #
    gameOverlay.Initialize()
    seletorScreen.Initialize()
    loadingScreen.Initialize()
    licenseScreen.Initialize()
    saveFolderSelectScreen.Initialize()
    SetMenuMode_Changes()

    print("TaiyouUI.Initialize : Initialization Complete.")


def Draw(Display):
    global SystemMenuEnabled
    global CurrentMenuScreen
    global OverlayDialogEnabled
    global ScreenLastFrame

    if SystemMenuEnabled:
        if not OverlayDialogEnabled:
            if CurrentMenuScreen == 4:
                loadingScreen.Draw(Display)

            elif CurrentMenuScreen == 3:
                saveFolderSelectScreen.Draw(Display)

            elif CurrentMenuScreen == 2:
                seletorScreen.Draw(Display)

            elif CurrentMenuScreen == 1:
                licenseScreen.Draw(Display)

            elif CurrentMenuScreen == 0:
                gameOverlay.Draw(Display)

            # -- Aways copy the Last Frame of Display -- #
            ScreenLastFrame = Display.copy()

        # -- Draw the OverlayDialog -- #
        else:
            ovelDiag.Draw(Display)

    # -- Render the Cursor -- #
    sprite.ImageRender(Display, "/TAIYOU_UI/Cursor/{0}.png".format(str(Cursor_CurrentLevel)), Cursor_Position[0], Cursor_Position[1])


def Update():
    global SystemMenuEnabled
    global Cursor_Position
    global CurrentMenuScreen
    global OverlayDialogEnabled

    if SystemMenuEnabled:
        if not OverlayDialogEnabled:
            if CurrentMenuScreen == 4:
                loadingScreen.Update()

            elif CurrentMenuScreen == 3:
                saveFolderSelectScreen.Update()

            elif CurrentMenuScreen == 2:
                seletorScreen.Update()

            elif CurrentMenuScreen == 1:
                licenseScreen.Update()

            elif CurrentMenuScreen == 0:
                gameOverlay.Update()
        else:
            ovelDiag.Update()

        # -- Set Cursor Position -- #
        Cursor_Position = pygame.mouse.get_pos()


def EventUpdate(event):
    global SystemMenuEnabled
    global CurrentMenuScreen
    global OverlayDialogEnabled

    if SystemMenuEnabled:
        if not OverlayDialogEnabled:
            if CurrentMenuScreen == 4:
                loadingScreen.EventUpdate(event)

            elif CurrentMenuScreen == 3:
                saveFolderSelectScreen.EventUpdate(event)

            elif CurrentMenuScreen == 2:
                seletorScreen.EventUpdate(event)

            elif CurrentMenuScreen == 1:
                licenseScreen.EventUpdate(event)

            elif CurrentMenuScreen == 0:
                gameOverlay.EventUpdate(event)
        else:
            ovelDiag.EventUpdate(event)

def SetMenuMode_Changes():
    print("TaiyouUI.SetMenuModeChanges")

    # -- Set the Window Title -- #
    taiyouMain.ReceiveCommand(9, "Taiyou Game Engine v" + utils.FormatNumber(tge.TaiyouGeneralVersion))

    # -- Set the Default Icon -- #
    taiyouMain.ReceiveCommand(4, "/TAIYOU_UI/icon.png")

    # -- Set to 60FPS -- #
    taiyouMain.ReceiveCommand(0, 70)

    CurrentRes = pygame.display.get_window_size()
    if not CurrentRes[0] == 800 and not CurrentRes[1] == 600:
        taiyouMain.ReceiveCommand(1, "800x600")
        print("Taiyou.SetMenuChanges : CurrentResolution is different than 800x600 [{0}x{1}]".format(str(CurrentRes[0]), str(CurrentRes[1])))

    else:
        print("Taiyou.SetMenuChanges : CurrentResolution is equals to 800x600 [{0}x{1}]".format(str(CurrentRes[0]), str(CurrentRes[1])))

# -- This function is called when the Game Engine is Exiting -- #
def SaveSettings():
    volumeSlider.SaveSettings()
