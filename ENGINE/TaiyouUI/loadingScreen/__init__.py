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
LoadingStageMax = 6
LoadingNextStageDelay = 0
LoadingStageWaitMax = 0
LoadingSquare = gtk.LoadingSquare
CommonDisplay = pygame.Surface((5,5))
GameIcon = pygame.image
GameTitle = "null"
LoadingStageText = "No Description found"

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
    global GameIcon
    global GameTitle
    global DialogEnabled
    global LoadingStageText

    Display.fill((0, 0, 0))
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

    # -- Render Loading Description -- #
    sprite.FontRender(Display, "/Ubuntu_Bold.ttf", 18, LoadingStageText, (230, 230, 230), 15, 600 - 28, Opacity=OpacityAnimation_Opacity)

    if DialogEnabled:
        dialog.Draw(Display)


def Update():
    global GameFolderToOpen
    global LoadingSquare
    global CommonDisplay
    global GameTitle
    global DialogEnabled
    global LoadingStageText
    global LoadingStage
    global LoadingStageMax

    if not DialogEnabled:
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

        # -- Update Loading Stage Text -- #
        try:
            LoadingStageText = "{0} {1}/{2}".format(gtk.GetLangText("step_{0}".format(str(LoadingStage)), "loading_stage_description"), str(LoadingStage), str(LoadingStageMax))
        except FileNotFoundError:
            LoadingStageText = ""

    else:
        dialog.Update()

def UpdateLoadingStages():
    global LoadingNextStage
    global LoadingNextStageDelay
    global LoadingStage
    global OpacityAnimation_Enabled
    global LoadingStageMax
    global LoadingStageWaitMax

    if LoadingNextStage and not GameFolderToOpen == "null":
        LoadingStage += 1

        if LoadingStage == 0:
            print("Taiyou.LoadingScreen : Saving TaiyouUI Settings...")
            taiyouUI.SaveSettings()
            print("Taiyou.LoadingScreen : Done!")
            LoadingStageWaitMax = reg.ReadKey_int("/TaiyouSystem/CONF/loading_delay", True)

        elif LoadingStage == 1:
            if utils.Directory_Exists(GameFolderToOpen):
                print("Taiyou.LoadingScreen : Game Exists")
            else:
                print("Taiyou.LoadingScreen : Game does not Exists")

        elif LoadingStage == 2:
            print("Taiyou.LoadingScreen : Load Folder Metadata")
            tge.LoadFolderMetaData(GameFolderToOpen + "/")

        elif LoadingStage == 3:
            print("Taiyou.LoadingScreen : Load Game Sprites")
            sprite.LoadSpritesInFolder(GameFolderToOpen + "/")

        elif LoadingStage == 4:
            print("Taiyou.LoadingScreen : Load Game Sounds")
            sound.LoadAllSounds(GameFolderToOpen + "/")

        elif LoadingStage == 5:
            print("Taiyou.LoadingScreen : Load Game Registry Keys")
            reg.Initialize(GameFolderToOpen + "/")

        elif LoadingStage == 6:
            print("Taiyou.LoadingScreen : Load Game Code")
            taiyouMain.ReceiveCommand(7, GameFolderToOpen)

            OpacityAnimation_Enabled = True

        print("Taiyou.LoadingStage : Loading Step {0}/{1}".format(str(LoadingStage), str(LoadingStageMax)))
        LoadingNextStage = False

    if not OpacityAnimation_Enabled:
        LoadingNextStageDelay += 1

        if LoadingNextStageDelay >= LoadingStageWaitMax:
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

                taiyouUI.CurrentMenuScreen = 0
                taiyouMain.ReceiveCommand(5)

                taiyouUI.gameOverlay.UIOpacityAnimEnabled = False
                taiyouUI.SystemMenuEnabled = False

def EventUpdate(event):
    pass
