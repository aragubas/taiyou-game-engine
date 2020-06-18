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

Placeholder = "Place a Holder"

def Draw(Display):
    Text = gtk.GetLangText("title_info", "seletor/atribute_list/txt").format(Handler.SelectedGameInfosList[0], Handler.SelectedGameInfosList[1], Handler.SelectedGameInfosList[2], Handler.SelectedGameInfosList[3])

    sprite.FontRender(Display, "/Ubuntu_Bold.ttf", 14, Text, (230, 230, 230), Handler.GameInfosRectBox[0] + 5, Handler.GameInfosRectBox[1] + 25, True)

def Update():
    global Placeholder

def EventUpdate(event):
    global Placeholder

def Initialize():
    global Placeholder

