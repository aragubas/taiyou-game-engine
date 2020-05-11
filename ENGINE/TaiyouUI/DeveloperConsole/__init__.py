#!/usr/bin/python3
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
from ENGINE.TaiyouUI import UIGTK as gtk

WindowObject = gtk.Window

def Initialize():
    global WindowObject

    WindowObject = gtk.Window(pygame.Rect(50,50,350, 250), "Developer Console", True)

def Update():
    global WindowObject

def EventUpdate(event):
    global WindowObject

    WindowObject.EventUpdate(event)

def Draw(DISPLAY):
    WindowObject.WindowSurface.fill((5,5,255))
    sprite.RenderFont(WindowObject.WindowSurface, "/PressStart2P.ttf", 18, "Lorem ipsum dolor\nsit amet contreus sued de las\nfleg dus sinus.", (255,0,0), 5,5)

    # -- Draw the Window Frame -- #
    WindowObject.Render(DISPLAY)

    # -- Draw the Window Content -- #
    DISPLAY.blit(WindowObject.WindowSurface, WindowObject.WindowSurface_Dest)

