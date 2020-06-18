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
from ENGINE.TaiyouUI.GameSeletor.GameInfos import TitleInfo as titleInfos
from ENGINE.TaiyouUI.GameSeletor.GameInfos import OnlineInfo as onlineInfos
from ENGINE.TaiyouUI.GameSeletor.GameInfos import LocalInfo as localInfos
from ENGINE.TaiyouUI import OverlayDialog as UpdateDiag
from ENGINE.TaiyouUI.GameSeletor import GameInfos as Handler
from ENGINE.TaiyouUI import GameSeletor as HandlerOfHandler

# -- Animation -- #
GameInfosAnim_Opacity = 0
GameInfosAnim_Enabled = False
GameInfosAnim_Mode = 0
GameInfosAnim_Last = "null"
GameInfosSurface = pygame.Surface
GameInfosSurface_Dest = (5,5)
GameInfosRectBox = pygame.Rect(0,0, 300,200)

# -- List Object -- #
GameAtibutesList = gtk.VerticalListWithDescription
SelectedGameInfosList = list()


# -- Update the Animation -- #
def GameInfosAnimUpdate():
    global GameInfosAnim_Enabled
    global GameInfosAnim_Mode
    global GameInfosAnim_Opacity
    if GameInfosAnim_Enabled:

        if GameInfosAnim_Mode == 0:
            GameInfosAnim_Opacity += 50

            if GameInfosAnim_Opacity >= 255:
                GameInfosAnim_Opacity = 255
                GameInfosAnim_Enabled = False
                GameInfosAnim_Mode = 1

        if GameInfosAnim_Mode == 1:
            GameInfosAnim_Opacity -= 50

            if GameInfosAnim_Opacity <= 0:
                GameInfosAnim_Opacity = 0
                GameInfosAnim_Enabled = True
                GameInfosAnim_Mode = 0

def Update():
    global GameAtibutesList
    global GameInfosRectBox
    global GameInfosSurface
    global GameInfosSurface_Dest

    GameInfosAnimUpdate()

    GameInfosSurface_Dest = (5, 600 - GameInfosRectBox[3] - 5)

    # -- Get Selected Game Infos List -- #
    Handler.SelectedGameInfosList.clear()

    # -- Title Informations -- #
    Handler.SelectedGameInfosList.append(HandlerOfHandler.InstalledGameList.SelectedItem.rstrip())
    Handler.SelectedGameInfosList.append(HandlerOfHandler.InstalledGameList.SelectedGameVersion.rstrip())
    Handler.SelectedGameInfosList.append(HandlerOfHandler.InstalledGameList.SelectedGameID.rstrip())
    Handler.SelectedGameInfosList.append(HandlerOfHandler.InstalledGameList.SelectedGameFolderName.rstrip())

    GameInfosRectBox = pygame.Rect(GameAtibutesList.Rectangle[2] + 5, GameAtibutesList.Rectangle[1], GameAtibutesList.Rectangle[2] + 20, GameAtibutesList.Rectangle[3])

    GameInfosSurface = pygame.Surface((GameAtibutesList.Rectangle[2] + GameInfosRectBox[2] - 10, GameAtibutesList.Rectangle[3]))

    GameAtibutesList.ColisionXOffset = 5
    GameAtibutesList.ColisionYOffset = 600 - GameInfosRectBox[3] - 5

    # -- Update the Subscreens -- #
    if GameAtibutesList.SelectedItemIndex == 0:
        titleInfos.Update()

    if GameAtibutesList.SelectedItemIndex == 1:
        localInfos.Update()

    if GameAtibutesList.SelectedItemIndex == 2:
        onlineInfos.Update()

def Initialize():
    global GameInfosSurface
    global GameInfosRectBox
    global GameAtibutesList
    GameAtibutesList = gtk.VerticalListWithDescription(pygame.Rect(0, 0, 370, 300))

    GameInfosSurface = pygame.Surface((GameAtibutesList.Rectangle[2] + GameInfosRectBox[2], GameAtibutesList.Rectangle[3]))
    # -- Add Items to the List --
    GameAtibutesList.AddItem(gtk.GetLangText("title_info", "seletor/atribute_list/title"), gtk.GetLangText("title_desc", "seletor/atribute_list"))
    GameAtibutesList.AddItem(gtk.GetLangText("local_info", "seletor/atribute_list/title"), gtk.GetLangText("local_desc", "seletor/atribute_list"))
    GameAtibutesList.AddItem(gtk.GetLangText("online_info", "seletor/atribute_list/title"), gtk.GetLangText("online_desc", "seletor/atribute_list"))

    onlineInfos.Initialize()
    localInfos.Initialize()
    titleInfos.Initialize()

def Draw(Display):
    global GameAtibutesList
    global GameInfosRectBox
    global GameInfosAnim_Last
    global GameInfosAnim_Enabled
    global GameInfosSurface
    global GameAtibutesList
    global GameInfosAnim_Opacity
    global GameInfosSurface_Dest

    if not GameInfosAnim_Last == HandlerOfHandler.InstalledGameList.SelectedItemIndex:
        GameInfosAnim_Last = HandlerOfHandler.InstalledGameList.SelectedItemIndex
        GameInfosAnim_Enabled = True

    # -- Clear the Surface -- #
    GameInfosSurface.fill((HandlerOfHandler.BackgroundR, HandlerOfHandler.BackgroundG, HandlerOfHandler.BackgroundB))
    GameInfosSurface.set_alpha(GameInfosAnim_Opacity)

    # -- Render Games Info List -- #
    GameAtibutesList.Render(GameInfosSurface)

    # -- Render Infos Box -- #
    gtk.Draw_Panel(GameInfosSurface, GameInfosRectBox, "BORDER")

    if GameAtibutesList.SelectedItemIndex == 0:
        titleInfos.Draw(GameInfosSurface)

    if GameAtibutesList.SelectedItemIndex == 1:
        localInfos.Draw(GameInfosSurface)

    if GameAtibutesList.SelectedItemIndex == 2:
        onlineInfos.Draw(GameInfosSurface)

    Display.blit(GameInfosSurface, GameInfosSurface_Dest)




def EventUpdate(event):
    global GameAtibutesList
    # -- Update Event of Games Info List -- #
    GameAtibutesList.Update(event)

    if GameAtibutesList.SelectedItemIndex == 0:
        titleInfos.EventUpdate(event)

    if GameAtibutesList.SelectedItemIndex == 1:
        localInfos.EventUpdate(event)

    if GameAtibutesList.SelectedItemIndex == 2:
        onlineInfos.EventUpdate(event)
