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
import pygame
from ENGINE import SPRITE as sprite
from ENGINE import TaiyouMain as main
from ENGINE import UTILS as utils

TextToBeDisplayed = "FPS"

def Update():
    global TextToBeDisplayed
    TextToBeDisplayed = "FPS {0}/{1}; Tick: {2}".format(str(main.FPS), utils.FormatNumber(main.clock.get_fps(), 3), utils.FormatNumber(main.clock.get_time(), 3))

def Draw(DISPLAY):
    global TextToBeDisplayed

    sprite.FontRender(DISPLAY, "/PressStart2P.ttf", 9, TextToBeDisplayed, (255, 255, 255), 15, 15, False, (20, 30, 23), Opacity=200)


def EventUpdate(event):
    pass