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
import pygame, os, sys
from ENGINE import SPRITE as sprite
from ENGINE import SOUND as sound
from ENGINE.TaiyouUI import UIGTK as gtk
from ENGINE import TaiyouUI as taiyouUI
import ENGINE as tge
from ENGINE import utils
from ENGINE import SPRITE as sprite
from ENGINE import REGISTRY as reg
from ENGINE import SOUND as sound
from ENGINE import REGISTRY as reg
from ENGINE.TaiyouUI import loadingScreen as loadingScreen


OpacityAnimation_Enabled = True
OpacityAnimation_Opacity = 0
OpacityAnimation_Mode = 0
LoadingNextStage = False
LoadingStage = -1
LoadingNextStageDelay = 0
LoadingSquare = gtk.LoadingSquare

GameFolderToOpen = "TESTMODE"

def Initialize():
    global LoadingSquare

    LoadingSquare = gtk.LoadingSquare(5, 5)

def Draw(Display):
    global OpacityAnimation_Opacity
    global LoadingStage
    global LoadingSquare
    Display.fill((0,0,0))

    LoadingSquare.Render(Display)

    LoadingSquare.Y = Display.get_height() - 38
    LoadingSquare.X = Display.get_width() - 38
    LoadingSquare.Opacity = OpacityAnimation_Opacity

def Update():
    global OpacityAnimation_Enabled
    global OpacityAnimation_Opacity
    global OpacityAnimation_Mode
    global LoadingNextStage
    global LoadingNextStageDelay
    global LoadingStage
    global GameFolderToOpen
    global LoadingSquare

    LoadingSquare.Update()

    if LoadingNextStage and not GameFolderToOpen == "TESTMODE":
        LoadingStage += 1
        if LoadingStage == 0:
            if utils.Directory_Exists(GameFolderToOpen):
                
        if LoadingStage == 1:
            sprite.LoadSpritesInFolder(GameFolderToOpen + "/SOURCE")
        if LoadingStage == 2:
            sound.LoadAllSounds(GameFolderToOpen + "/SOURCE")
        if LoadingStage == 3:
            reg.Initialize(GameFolderToOpen + "/SOURCE/REG")
        if LoadingStage == 4:
            tge.LoadFolderMetaData(GameFolderToOpen)
        if LoadingStage == 5:
            taiyouUI.Messages.append("OPEN_GAME:" + GameFolderToOpen)
            taiyouUI.Messages.append("TOGGLE_GAME_START")

            OpacityAnimation_Enabled = True


    if OpacityAnimation_Mode == 1 and not OpacityAnimation_Enabled:
        LoadingNextStageDelay += 1


        if LoadingNextStageDelay >= 5000:
            LoadingNextStageDelay = 0
            LoadingNextStage = True

    if OpacityAnimation_Enabled:
        if OpacityAnimation_Mode == 0:
            OpacityAnimation_Opacity += 15

            if OpacityAnimation_Opacity >= 255:
                OpacityAnimation_Opacity = 255
                OpacityAnimation_Mode = 1
                OpacityAnimation_Enabled = False
                LoadingNextStage = True

        if OpacityAnimation_Mode == 1:
            OpacityAnimation_Opacity -= 15

            if OpacityAnimation_Opacity <= 0:
                OpacityAnimation_Opacity = 0
                OpacityAnimation_Mode = 0
                OpacityAnimation_Enabled = True
                LoadingStage = -1
                LoadingNextStageDelay = 0
                LoadingNextStage = False

                taiyouUI.CurrentMenuScreen = 0
                taiyouUI.Messages.append("SET_GAME_MODE")
                taiyouUI.Messages.append("GAME_UPDATE:True")

                taiyouUI.gameOverlay.UIOpacityAnimEnabled = False
                taiyouUI.SystemMenuEnabled = False

def EventUpdate(event):
    global OpacityAnimation_Opacity
