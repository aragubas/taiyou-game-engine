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

# -- Imports -- #
from ENGINE import REGISTRY as reg
from ENGINE import UTILS as utils
import ENGINE as tge
from ENGINE import SOUND as sound
from Fogoso.MAIN import ClassesUtils as gameObjs
from Fogoso import MAIN as gameMain
from ENGINE import SPRITE as sprite
from Fogoso.MAIN.Screens.Settings import category_0 as Category0
from Fogoso.MAIN.Screens.Settings import category_1 as Category1
from Fogoso.MAIN.Screens.Settings import category_2 as Category2

import pygame, sys

import importlib
import time
from random import randint

ScreenToReturn = 0
OptionsScreen_CloseButton = gameObjs.Button
OptionsScreen_UpDownCategory = gameObjs.UpDownButton

# -- Category -- #
Current_Category = 2

# -- Elements -- #
ElementsX = 0
ElementsY = 0



def Update():
    global ScreenToReturn
    global Current_Category
    global ElementsY
    global ElementsX
    global OptionsScreen_UpDownCategory

    # -- Update Elements Location -- #
    ElementsX = gameMain.DefaultDisplay.get_width() / 2 - 275
    ElementsY = gameMain.DefaultDisplay.get_height() / 2 - 125

    # -- Update UpDown Button Location -- #
    OptionsScreen_UpDownCategory.Set_X(ElementsX + 558 - OptionsScreen_UpDownCategory.Get_Width() - 5)
    OptionsScreen_UpDownCategory.Set_Y(ElementsY + 3)

    # -- Change Category UP Button -- #
    if OptionsScreen_UpDownCategory.ButtonState == "UP":
        MaxCategory = reg.ReadKey_int("/props/settings_max_category")
        Current_Category += 1
        if Current_Category > MaxCategory:
            Current_Category = 0
        gameMain.FadeAnimation()

    if OptionsScreen_UpDownCategory.ButtonState == "DOWN":
        MaxCategory = reg.ReadKey_int("/props/settings_max_category")
        Current_Category -= 1
        if Current_Category < 0:
            Current_Category = MaxCategory
        gameMain.FadeAnimation()

    if Current_Category == 0:
        Category0.Update()
        # -- Set the Elements Position -- #
        Category0.ElementsY = ElementsY
        Category0.ElementsX = ElementsX
    if Current_Category == 1:
        Category1.Update()
        # -- Set the Elements Position -- #
        Category1.ElementsY = ElementsY
        Category1.ElementsX = ElementsX
    if Current_Category == 2:
        Category2.Update()
        # -- Set the Elements Position -- #
        Category2.ElementsX = ElementsX
        Category2.ElementsY = ElementsY

    if OptionsScreen_CloseButton.ButtonState == "UP":
        gameMain.FadeEffectValue = 255
        gameMain.FadeEffectCurrentState = 0
        gameMain.FadeEffectState = True
        gameMain.CurrentScreen = ScreenToReturn

    OptionsScreen_CloseButton.Set_X(gameMain.DefaultDisplay.get_width() - 120)


def GameDraw(DISPLAY):
    global Current_Category
    global ElementsY
    global ElementsX
    global OptionsScreen_UpDownCategory

    # -- Draw the Background -- #
    gameObjs.Draw_Panel(DISPLAY, (ElementsX, ElementsY, 558, 258))

    # -- Render the Title Text -- #
    sprite.RenderRectangle(DISPLAY, (1, 22, 39), (ElementsX, ElementsY, 558, 22))
    sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 15, reg.ReadKey("/strings/settings/category/{0}".format(str(Current_Category))), (246, 247, 248), ElementsX + 5,
                      ElementsY + 4, reg.ReadKey_bool("/OPTIONS/font_aa"))

    # -- Render Close Button -- #
    OptionsScreen_CloseButton.Render(DISPLAY)

    # -- Render UpDown Button -- #
    OptionsScreen_UpDownCategory.Render(DISPLAY)

    # -- Render Categorys -- #
    if Current_Category == 0:
        Category0.Render(DISPLAY)
    if Current_Category == 1:
        Category1.Render(DISPLAY)
    if Current_Category == 2:
        Category2.Render(DISPLAY)

def Initialize():
    global OptionsScreen_CloseButton
    global OptionsScreen_UpDownCategory

    OptionsScreen_CloseButton = gameObjs.Button(pygame.rect.Rect(0, 5, 0, 0), reg.ReadKey("/strings/settings/back_button"), 14)
    OptionsScreen_UpDownCategory = gameObjs.UpDownButton(5,5,14)

    gameMain.ClearColor = (1,24,32)

    Category0.Initialize()
    Category1.Initialize()
    Category2.Initialize()

def EventUpdate(event):
    global Current_Category
    global OptionsScreen_CloseButton
    global OptionsScreen_UpDownCategory
    OptionsScreen_CloseButton.Update(event)
    OptionsScreen_UpDownCategory.Update(event)

    if Current_Category == 0:
        Category0.EventUpdate(event)
    if Current_Category == 1:
        Category1.EventUpdate(event)
    if Current_Category == 2:
        Category2.EventUpdate(event)
