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
from datetime import datetime
import ENGINE as tge
from ENGINE import SPRITE as sprite
from ENGINE.TaiyouUI import UIGTK as gtk
from ENGINE import SOUND as sound
from ENGINE import REGISTRY as reg
from ENGINE import UTILS as utils

ScreenshotBordersRect = pygame.Rect(0, 0, 2, 2)
ScreenshotTaken = False
ScreenshotBorderAnimValue = False
ScreenshotBorderAnimMode = False


def Run(DISPLAY):
    global ScreenshotBordersRect
    global ScreenshotBorderAnimValue
    global ScreenshotTaken
    global ScreenshotBorderAnimMode

    if not ScreenshotTaken:
        ScreenshotTaken = True

        FileName = "(" + str(datetime.now().day) + "-" + str(datetime.now().month) + "-" + str(datetime.now().year) + ")" + str(datetime.now().hour) + "-" + str(datetime.now().minute) + "-" + str(datetime.now().second) + ".png"

        ScreenshotFilePath = "Taiyou/HOME/Screenshots/"

        tge.devel.PrintToTerminalBuffer("Taiyou.ScreenshotUI:\nCreating screenshot directory...\n")

        if not tge.Get_GameID() == "null":
            # -- Create the Screenshot Directory -- #
            ScreenshotFilePath += tge.Get_GameID()
            utils.Directory_MakeDir(ScreenshotFilePath)

            ScreenshotFilePath += "/" + FileName

        else:
            ScreenshotFilePath += FileName


        tge.devel.PrintToTerminalBuffer("Taiyou.ScreenshotUI:\nWritting file to disk...\n")
        pygame.image.save(DISPLAY, ScreenshotFilePath) # -- Save the Screenshot -- #

        sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Decline"), 1.0, PlayOnSystemChannel=True)
        print("Taiyou.ScreenshotUI : Screenshot has been saved")

    if ScreenshotBorderAnimMode == 0:
        ScreenshotBorderAnimValue += 2

        if ScreenshotBorderAnimValue >= 16:
            ScreenshotBorderAnimValue = 16
            ScreenshotBorderAnimMode = 1

    if ScreenshotBorderAnimMode == 1:
        ScreenshotBorderAnimValue -= 2

        if ScreenshotBorderAnimValue <= 0:
            ScreenshotBorderAnimValue = 0
            ScreenshotBorderAnimMode = 0
            ScreenshotTaken = False
            Messages.append("OVERLAY_LEVEL:-1")

    ScreenshotBordersRect = pygame.Rect(0, 0, DISPLAY.get_width(), DISPLAY.get_height())

    if ScreenshotBorderAnimValue >= 1:
        BirchedColor = pygame.Surface((DISPLAY.get_width(), DISPLAY.get_height()))
        BirchedColor.set_alpha(ScreenshotBorderAnimValue * 5)

        sprite.Shape_Rectangle(BirchedColor, (255, 255, 255), (0, 0, DISPLAY.get_width(), DISPLAY.get_height()))

        DISPLAY.blit(BirchedColor, (0, 0))

        pygame.draw.rect(DISPLAY, gtk.Panels_IndicatorColor, ScreenshotBordersRect, int(ScreenshotBorderAnimValue * gtk.Panels_Indicator_Size))

        pygame.draw.rect(DISPLAY, gtk.Panels_BackgroundColor, ScreenshotBordersRect, ScreenshotBorderAnimValue)


# -- Send the messages on the Message Quee to the Game Engine -- #
Messages = list()


def ReadCurrentMessages():
    global Messages
    try:
        for x in Messages:
            Messages.remove(x)
            print("SystemUI : MessageSent[" + x + "]")
            return x
    except:
        return ""
