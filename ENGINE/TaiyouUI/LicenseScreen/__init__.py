#!/usr/bin/python3.6
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
from ENGINE import REGISTRY as reg
from ENGINE import TaiyouUI as SystemUIHandler

LicenseText = "Lorem ipsum dolor sit amet"
AragubasLogoRect = pygame.Rect(0,0,0,0)

DISPLAY = pygame.Surface
SurfaceCreated = False
Animation_Enabled = True
Animation_Mode = 0
Animation_Opacity = 0
Animation_StartDelay = 0

def Draw(Display):
    global Animation_Opacity
    global LicenseText
    global AragubasLogoRect
    global DISPLAY
    global SurfaceCreated
    # -- Set the Display Global Variable -- #
    DISPLAY = Display
    Display.fill((0,0,0))

    if len(LicenseText) > 0:
        sprite.RenderFont(Display, "/PressStart2P.ttf", 18, LicenseText, (Animation_Opacity, Animation_Opacity, Animation_Opacity), 5,5)

    SurfaceCreated = True

def Update():
    global AragubasLogoRect
    global DISPLAY
    global Animation_Opacity
    global Animation_Enabled
    global Animation_Mode
    global Animation_StartDelay
    global LicenseText

    if SurfaceCreated:
        AragubasLogoRect = pygame.Rect(5, DISPLAY.get_height() - 69, 64, 64)

    LicenseText = reg.ReadKey("/TaiyouSystem/licenseText")

    if Animation_Enabled:
        if Animation_StartDelay < 50:
            Animation_StartDelay += 1

        if Animation_Mode == 0 and Animation_StartDelay >= 50:
            Animation_Opacity += 15

            if Animation_Opacity >= 255:
                Animation_Opacity = 255
                Animation_Mode = 1
                Animation_Enabled = False
                Animation_StartDelay = 0
                print("TaiyouUI.LicenseScreen.AnimationTrigger : Animation Start")

        if Animation_Mode == 1 and Animation_StartDelay >= 50:
            Animation_Opacity -= 15

            if Animation_Opacity <= -50:
                Animation_Opacity = 0
                Animation_Mode = 0
                Animation_Enabled = True
                Animation_StartDelay = 0

                SystemUIHandler.CurrentMenuScreen = 2


                print("TaiyouUI.LicenseScreen.AnimationTrigger : Animation End")

def EventUpdate(event):
    global DISPLAY
    global Animation_Enabled

    if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
        Animation_Enabled = True