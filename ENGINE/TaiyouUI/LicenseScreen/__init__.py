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
from ENGINE import TaiyouUI as taiyouUI
from ENGINE import SPRITE as sprite
from ENGINE.TaiyouUI import UIGTK as gtk
from ENGINE import REGISTRY as reg
from ENGINE import SOUND as sound
import pygame

WaitTime = 0
WaitTimeEnabled = False
CenterLogoRectangle = (0, 0, 384, 300)
LicenseText = "Why this variable was not set?"
GlobalOpacity = 0
OpacityAnimMode = 0
OpacityAnimEnabled = True
IntroSoundPlayed = False

def Initialize():
    global LicenseText
    # -- Set the License Text -- #

    LicenseText = gtk.GetLangText("license_text")


def Update():
    global WaitTime
    global WaitTimeEnabled
    global GlobalOpacity
    global OpacityAnimMode
    global OpacityAnimEnabled
    global CenterLogoRectangle
    global IntroSoundPlayed

    # -- Update the Center Image -- #
    CenterLogoRectangle = (800 / 2 - CenterLogoRectangle[2] / 2, 600 / 2 - CenterLogoRectangle[3] / 1.2, CenterLogoRectangle[2], CenterLogoRectangle[3])

    if OpacityAnimEnabled:
        if OpacityAnimMode == 0:
            GlobalOpacity += 10

            if GlobalOpacity >= 255:
                GlobalOpacity = 255
                WaitTimeEnabled = True
                OpacityAnimEnabled = False

                # -- Play Intro Sound -- #
                if not IntroSoundPlayed:
                    sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Startup", True), PlayOnSystemChannel=True)
                    IntroSoundPlayed = True

        if OpacityAnimMode == 1 and OpacityAnimEnabled:
            GlobalOpacity -= 10

            if GlobalOpacity <= 0:
                GlobalOpacity = 0
                WaitTimeEnabled = True
                OpacityAnimEnabled = False

    # -- If Wait Time is enabled -- #
    if WaitTimeEnabled:
        WaitTime += 1

        if OpacityAnimMode == 0:
            if WaitTime >= 150:
                OpacityAnimMode = 1  # -- Last Animation Thing
                OpacityAnimEnabled = True
                WaitTimeEnabled = False
                WaitTime = 0

        if OpacityAnimMode == 1 and WaitTimeEnabled:
            WaitTime += 1

            if WaitTime >= 70:  # -- Restart Variables
                taiyouUI.CurrentMenuScreen = 2
                WaitTimeEnabled = False
                WaitTime = 0
                OpacityAnimMode = 0
                OpacityAnimEnabled = True
                IntroSoundPlayed = False




def Draw(DISPLAY):
    global CenterLogoRectangle
    global GlobalOpacity
    global LicenseText


    DISPLAY.fill((0, 0, 0))
    # -- Render Background -- #
    sprite.ImageRender(DISPLAY, "/TAIYOU_UI/BG/loading_bg.png", 0, 0, SmoothScaling=True, Opacity=GlobalOpacity)

    # -- Render the Logo -- #
    sprite.ImageRender(DISPLAY, "/taiyou.png", CenterLogoRectangle[0], CenterLogoRectangle[1], CenterLogoRectangle[2], CenterLogoRectangle[3], True, GlobalOpacity)

    # -- Render the License Text -- #
    sprite.FontRender(DISPLAY, "/Ubuntu_Lite.ttf", 15, LicenseText, (150, 150, 150), CenterLogoRectangle[0] / 2, CenterLogoRectangle[1] + 320, True, Opacity=GlobalOpacity)

def EventUpdate(event):
    pass