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
import pygame, os, sys, shutil
from ENGINE import SPRITE as sprite
from ENGINE import SOUND as sound
from ENGINE.TaiyouUI import UIGTK as gtk
from ENGINE import TaiyouUI as taiyouUI
import ENGINE as tge
from ENGINE import utils
from ENGINE import SPRITE as sprite
from ENGINE import SOUND as sound
from ENGINE import REGISTRY as reg
from ENGINE.TaiyouUI import loadingScreen as loadingScreen
from ENGINE.TaiyouUI import OverlayDialog as UpdateDiag
from ENGINE.TaiyouUI.GameSeletor import GameInfos as Handler
from ENGINE.TaiyouUI import GameSeletor as HandlerOfHandler

Placeholder = "Place a Holder"

# -- Buttons -- #
RunUpdater_Button = gtk.Button
UpdateMetadata_Button = gtk.Button


def Draw(Display):
    global RunUpdater_Button
    global UpdateMetadata_Button

    RunUpdater_Button.Render(Display)
    UpdateMetadata_Button.Render(Display)

    if not reg.KeyExists("/TaiyouSystem/UPDATER/" + HandlerOfHandler.SelectedGameInfo[0] + "/ApplicationDataHasBeenDownloaded"):
        sprite.FontRender(Display, "/Ubuntu_Bold.ttf", 18, gtk.GetLangText("no_downloaded_data", "game_infos/online"), (230, 230, 230), Handler.GameInfosRectBox[0] + 5, Handler.GameInfosRectBox[1] + 25)
    else:
        BasicInfosText = gtk.GetLangText("basic_infos", "game_infos/online").format(
            reg.ReadKey("/TaiyouSystem/UPDATER/" + HandlerOfHandler.SelectedGameInfo[0] + "/CurrentVersion"),
            reg.ReadKey("/TaiyouSystem/UPDATER/" + HandlerOfHandler.SelectedGameInfo[0] + "/PatchNotes")
        )

        sprite.FontRender(Display, "/Ubuntu_Bold.ttf", 18, BasicInfosText, (230, 230, 230), Handler.GameInfosRectBox[0] + 5, Handler.GameInfosRectBox[1] + 25)


def Initialize():
    global RunUpdater_Button
    global UpdateMetadata_Button

    RunUpdater_Button = gtk.Button(pygame.Rect(5,5,5,5), gtk.GetLangText("updater_button", "game_infos/online"), 20)
    RunUpdater_Button.CustomColisionRectangle = True

    UpdateMetadata_Button = gtk.Button(pygame.Rect(5,5,5,5), gtk.GetLangText("metadata_update", "game_infos/online"), 20)
    UpdateMetadata_Button.CustomColisionRectangle = True

def Update():
    global RunUpdater_Button
    global UpdateMetadata_Button
    # -- Run Updater Button -- #
    RunUpdater_Button.Set_X(Handler.GameInfosRectBox[0] + 5)
    RunUpdater_Button.Set_Y(Handler.GameInfosRectBox[1] + Handler.GameInfosRectBox[3] - 32)

    RunUpdater_Button.Set_ColisionX(Handler.GameInfosSurface_Dest[0] + RunUpdater_Button.Rectangle[0])
    RunUpdater_Button.Set_ColisionY(Handler.GameInfosSurface_Dest[1] + RunUpdater_Button.Rectangle[1])

    # -- Update Metadata Button Button -- #
    UpdateMetadata_Button.Set_X(RunUpdater_Button.Rectangle[0] + RunUpdater_Button.Rectangle[2] + 3)
    UpdateMetadata_Button.Set_Y(RunUpdater_Button.Rectangle[1])

    UpdateMetadata_Button.Set_ColisionX(Handler.GameInfosSurface_Dest[0] + UpdateMetadata_Button.Rectangle[0])
    UpdateMetadata_Button.Set_ColisionY(Handler.GameInfosSurface_Dest[1] + UpdateMetadata_Button.Rectangle[1])

    # -- Update Button -- #
    if RunUpdater_Button.ButtonState == "UP":
        # -- Set Variables -- #
        HandlerOfHandler.ApplicationUpdateDialogEnabled = True
        UpdateDiag.ApplicationID = HandlerOfHandler.SelectedGameInfo[0]
        UpdateDiag.ApplicationName = HandlerOfHandler.SelectedGameInfo[1]
        UpdateDiag.ApplicationVersion = float(HandlerOfHandler.SelectedGameInfo[2])
        UpdateDiag.ApplicationFolder = HandlerOfHandler.SelectedGameInfo[3]
        RunUpdater_Button.ButtonState = "INACTIVE"

    # -- Metadata Update Button -- #
    if UpdateMetadata_Button.ButtonState == "UP":
        # -- Set Variables -- #
        HandlerOfHandler.ApplicationUpdateDialogEnabled = True
        UpdateDiag.ApplicationID = HandlerOfHandler.SelectedGameInfo[0]
        UpdateDiag.ApplicationName = HandlerOfHandler.SelectedGameInfo[1]
        UpdateDiag.ApplicationVersion = float(HandlerOfHandler.SelectedGameInfo[2])
        UpdateDiag.ApplicationFolder = HandlerOfHandler.SelectedGameInfo[3]
        UpdateDiag.subscreen1.IsMetadataUpdate = True
        UpdateDiag.subscreen1.VersionChecking = False

        UpdateMetadata_Button.ButtonState = "INACTIVE"




def EventUpdate(event):
    global RunUpdater_Button
    global UpdateMetadata_Button

    RunUpdater_Button.Update(event)
    UpdateMetadata_Button.Update(event)