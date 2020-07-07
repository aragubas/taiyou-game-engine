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
from ENGINE.TaiyouUI import GameSeletor as Handler
from ENGINE.TaiyouUI import OverlayDialog as dialog
from ENGINE import TaiyouMain as taiyouMain

OpacityAnimation_Enabled = True
OpacityAnimation_Opacity = 0
OpacityAnimation_Mode = 0
LoadingNextStage = False
LoadingStage = -1
LoadingNextStageDelay = 0
LoadingSquare = gtk.LoadingSquare
CommonDisplay = pygame.Surface((5,5))
GameIcon = pygame.image
GameTitle = "null"


# -- Anim Slipe -- #
AnimSlipeEnabled = False
AnimSlipeColorRAddMode = 0
AnimSlipeColorGAddMode = 0
AnimSlipeColorBAddMode = 0
AnimSlipeColorMode = 0
BackgroundR = 0
BackgroundG = 0
BackgroundB = 0

GameFolderToOpen = "null"

SliderTest = gtk.Slider

# -- UI is Locked -- #
DialogEnabled = False
DialogExcp = Exception

def Initialize():
    global LoadingSquare
    global GameIcon
    GameIcon = sprite.GetSprite("/TAIYOU_UI/no_icon.png")

    LoadingSquare = gtk.LoadingSquare(5, 5)
    dialog.Initialize()

def Draw(Display):
    global OpacityAnimation_Opacity
    global LoadingStage
    global LoadingSquare
    global CommonDisplay
    global BackgroundR
    global BackgroundG
    global BackgroundB
    global GameIcon
    global GameTitle
    global DialogEnabled

    Display.fill((BackgroundR, BackgroundG, BackgroundB))
    CommonDisplay = Display

    # -- Render RAW Game Icon -- #
    LogoSur = pygame.Surface((240 * 2, 150 * 2), pygame.SRCALPHA)
    if not DialogEnabled:
        LogoSur.set_alpha(OpacityAnimation_Opacity)
    else:
        LogoSur.set_alpha(OpacityAnimation_Opacity - 50)

    LogoSur.blit(pygame.transform.scale(GameIcon, (LogoSur.get_width(), LogoSur.get_height())), (0,0))

    Display.blit(LogoSur, (800 / 2 - LogoSur.get_width() / 2, 50))

    # -- Render Game Title -- #
    sprite.FontRender(Display, "/Ubuntu_Bold.ttf", 32, GameTitle, (230, 230, 230), 800 / 2 - sprite.GetFont_width("/Ubuntu_Bold.ttf", 32, GameTitle) / 2, 50 + LogoSur.get_height(), Opacity=OpacityAnimation_Opacity)

    # -- Render Loading Animation -- #
    LoadingSquare.Render(Display)

    if DialogEnabled:
        dialog.Draw(Display)


def Update():
    global GameFolderToOpen
    global LoadingSquare
    global CommonDisplay
    global AnimSlipeEnabled
    global GameTitle
    global DialogEnabled

    if not DialogEnabled:
        AnimSlipeUpdate()
        LoadingSquare.Update()

        LoadingSquare.Y = CommonDisplay.get_height() - 38
        LoadingSquare.X = CommonDisplay.get_width() - 38
        LoadingSquare.Opacity = OpacityAnimation_Opacity

        OpacityAnimation()
        UpdateLoadingStages()

        # -- Workaround if Autoboot GameFolder was selected -- #
        if Handler.SelectedGameInfo[1] == "null":
            GameTitle = GameFolderToOpen
        else:
            GameTitle = Handler.SelectedGameInfo[1]

    else:
        dialog.Update()

def UpdateLoadingStages():
    global LoadingNextStage
    global LoadingNextStageDelay
    global LoadingStage
    global OpacityAnimation_Enabled

    if LoadingNextStage and not GameFolderToOpen == "null":
        LoadingStage += 1

        if LoadingStage == 0:
            if utils.Directory_Exists(GameFolderToOpen):
                print("Taiyou.LoadingScreen : Game Exists")
            else:
                print("Taiyou.LoadingScreen : Game does not Exists")

        elif LoadingStage == 1:
            print("Taiyou.LoadingScreen : Load Folder Metadata")
            tge.LoadFolderMetaData(GameFolderToOpen)

        elif LoadingStage == 2:
            print("Taiyou.LoadingScreen : Load Game Sprites")
            sprite.LoadSpritesInFolder(GameFolderToOpen + "/SOURCE")

        elif LoadingStage == 3:
            print("Taiyou.LoadingScreen : Load Game Sounds")
            sound.LoadAllSounds(GameFolderToOpen + "/SOURCE")

        elif LoadingStage == 4:
            print("Taiyou.LoadingScreen : Load Game Registry Keys")
            reg.Initialize(GameFolderToOpen + "/SOURCE/REG")

        elif LoadingStage == 5:
            print("Taiyou.LoadingScreen : Load Game Code")
            taiyouMain.ReceiveCommand("OPEN_GAME:" + GameFolderToOpen)

            OpacityAnimation_Enabled = True

        print("Taiyou.LoadingStage : Loading Step " + str(LoadingStage) + "/5")
        LoadingNextStage = False

    if not OpacityAnimation_Enabled and not AnimSlipeEnabled:
        LoadingNextStageDelay += 1

        if LoadingNextStageDelay >= 5:
            LoadingNextStageDelay = 0
            LoadingNextStage = True


def OpacityAnimation():
    global OpacityAnimation_Enabled
    global OpacityAnimation_Opacity
    global OpacityAnimation_Mode
    global LoadingNextStage
    global LoadingStage
    global GameFolderToOpen
    global LoadingNextStageDelay
    global AnimSlipeEnabled

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
                GameFolderToOpen = "null"
                AnimSlipeEnabled = False

                taiyouUI.CurrentMenuScreen = 0
                taiyouMain.ReceiveCommand("SET_GAME_MODE")

                taiyouUI.gameOverlay.UIOpacityAnimEnabled = False
                taiyouUI.SystemMenuEnabled = False


def AnimSlipeUpdate():
    global AnimSlipeEnabled
    global AnimSlipeColorRAddMode
    global AnimSlipeColorGAddMode
    global AnimSlipeColorBAddMode
    global AnimSlipeColorMode
    global BackgroundR
    global BackgroundG
    global BackgroundB

    if AnimSlipeEnabled:
        AnimationSpeed = 2
        if AnimSlipeColorMode == 0:
            if AnimSlipeColorRAddMode == 0:
                BackgroundR += AnimationSpeed
            if AnimSlipeColorGAddMode == 0:
                BackgroundG += AnimationSpeed
            if AnimSlipeColorBAddMode == 0:
                BackgroundB += AnimationSpeed

            if BackgroundR >= 24:
                AnimSlipeColorRAddMode = 1
                BackgroundR = 24

            if BackgroundG >= 61:
                AnimSlipeColorGAddMode = 1
                BackgroundG = 61

            if BackgroundB >= 126:
                AnimSlipeColorBAddMode = 1
                BackgroundB = 126

            if AnimSlipeColorRAddMode == 1 and AnimSlipeColorGAddMode == 1 and AnimSlipeColorBAddMode == 1:
                AnimSlipeEnabled = True
                AnimSlipeColorMode = 1
                AnimSlipeColorRAddMode = 0
                AnimSlipeColorGAddMode = 0
                AnimSlipeColorBAddMode = 0

        if AnimSlipeColorMode == 1:
            if AnimSlipeColorRAddMode == 0:
                BackgroundR -= AnimationSpeed
            if AnimSlipeColorGAddMode == 0:
                BackgroundG -= AnimationSpeed
            if AnimSlipeColorBAddMode == 0:
                BackgroundB -= AnimationSpeed

            if BackgroundR <= 0:
                AnimSlipeColorRAddMode = 1
                BackgroundR = 0

            if BackgroundG <= 0:
                AnimSlipeColorGAddMode = 1
                BackgroundG = 0

            if BackgroundB <= 0:
                AnimSlipeColorBAddMode = 1
                BackgroundB = 0

            if AnimSlipeColorRAddMode == 1 and AnimSlipeColorGAddMode == 1 and AnimSlipeColorBAddMode == 1:
                AnimSlipeEnabled = False
                AnimSlipeColorMode = 0
                AnimSlipeColorRAddMode = 0
                AnimSlipeColorGAddMode = 0
                AnimSlipeColorBAddMode = 0


def EventUpdate(event):
    global OpacityAnimation_Opacity
