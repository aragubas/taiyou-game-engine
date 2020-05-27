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
from Fogoso.MAIN import ClassesUtils as gameObjs
from Fogoso import MAIN as gameMain
from ENGINE import SPRITE as sprite
from Fogoso.MAIN.Screens import Game as gameScr
from Fogoso.MAIN import GameVariables as save
import pygame, os

# -- Receive Log -- #
ReceiveLog_Y_Offset = 0
ReceiveLog_Y_OffsetAdder = 0
ReceiveLog_Y_AnimEnabled = False
ReceiveLog_Y_AnimType = 0
TextGrind_Text = list()
TextGrind_X = list()
TextGrind_Y = list()
TextGrind_AliveTime = list()
TextGrind_IsGrindText = list()
TextGrind_TextColor = list()
TextGrind_Value = list()

ReceiveLog_CloseButton = gameObjs.Button

def Initialize():
    global ReceiveLog_CloseButton
    ReceiveLog_CloseButton = gameObjs.Button(pygame.rect.Rect(320, 0, 0, 0), reg.ReadKey("/strings/button/game/down_arrow"),16)


def EventUpdate(event):
    global ReceiveLog_CloseButton
    ReceiveLog_CloseButton.Update(event)

def Unload():
    TextGrind_Y.clear()
    TextGrind_X.clear()
    TextGrind_AliveTime.clear()
    TextGrind_IsGrindText.clear()
    TextGrind_Value.clear()
    TextGrind_Text.clear()
    TextGrind_TextColor.clear()

def Update():
    global ReceiveLog_CloseButton
    global ReceiveLog_Y_AnimType
    global ReceiveLog_Y_OffsetAdder
    global ReceiveLog_Y_Offset
    global ReceiveLog_Y_AnimEnabled

    if ReceiveLog_CloseButton.ButtonState == "UP":
        ReceiveLog_Y_AnimEnabled = True

    # -- Update Buttons Location -- #
    ReceiveLog_CloseButton.Rectangle = pygame.rect.Rect(gameMain.DefaultDisplay.get_width() - 30, ReceiveLog_Y_Offset + gameMain.DefaultDisplay.get_height() - 353, ReceiveLog_CloseButton.Rectangle[2], ReceiveLog_CloseButton.Rectangle[3])

    # -- Update the Receive Log Hide Animation -- #
    if ReceiveLog_Y_AnimEnabled:
        if ReceiveLog_Y_AnimType == 0:
            ReceiveLog_Y_OffsetAdder += 1
            ReceiveLog_Y_Offset += ReceiveLog_Y_OffsetAdder

            if ReceiveLog_Y_Offset >= 310:
                ReceiveLog_Y_Offset = 310
                ReceiveLog_Y_OffsetAdder = 0
                ReceiveLog_Y_AnimType = 1
                ReceiveLog_Y_AnimEnabled = False
                ReceiveLog_CloseButton.ButtonText = reg.ReadKey("/strings/button/game/up_arrow")

        if ReceiveLog_Y_AnimType == 1:
            ReceiveLog_Y_OffsetAdder += 1
            ReceiveLog_Y_Offset -= ReceiveLog_Y_OffsetAdder

            if ReceiveLog_Y_Offset <= 0:
                ReceiveLog_Y_Offset = 0
                ReceiveLog_Y_OffsetAdder = 0
                ReceiveLog_Y_AnimType = 0
                ReceiveLog_Y_AnimEnabled = False
                ReceiveLog_CloseButton.ButtonText = reg.ReadKey("/strings/button/game/down_arrow")


def AddMessageText(Text, IsGrindText, TextColor, Value=0):
    global TextGrind_Text
    global TextGrind_X
    global TextGrind_Y
    global TextGrind_AliveTimezmmz
    global TextGrind_IsGrindText
    global TextGrind_TextColor
    global TextGrind_Value

    TextGrind_Text.append(Text)
    TextGrind_X.append(gameMain.DefaultDisplay.get_width() - 355 + 5)
    TextGrind_Y.append(ReceiveLog_Y_Offset + gameMain.DefaultDisplay.get_height() - 27)
    TextGrind_AliveTime.append(0)
    TextGrind_IsGrindText.append(IsGrindText)
    TextGrind_TextColor.append(TextColor)
    TextGrind_Value.append(Value)

def DrawGrindText(DISPLAY):
    # -- Render the Window Background -- #
    GlobalX = DISPLAY.get_width() - 355
    GlobalY = ReceiveLog_Y_Offset + DISPLAY.get_height() - 355
    sprite.RenderRectangle(DISPLAY, (4, 21, 32), (GlobalX, GlobalY, 350, 350)) # -- Container Background -- #
    sprite.RenderRectangle(DISPLAY, (66, 75, 84), (GlobalX + 2, GlobalY + 2, 350 - 4, 350 - 4)) # -- Container Border -- #

    for x, TextGrind_TxT in enumerate(TextGrind_Text):
        sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 20, TextGrind_TxT, TextGrind_TextColor[x], TextGrind_X[x], TextGrind_Y[x])

        TextGrind_Y[x] -= x + 1
        if TextGrind_IsGrindText[x]:
            TextGrind_X[x] += TextGrind_AliveTime[x] / 128 * x

        TextGrind_AliveTime[x] += 1
        if x > 128 or gameScr.IsControlsEnabled == False or TextGrind_AliveTime[x] >= 500 + x or TextGrind_Y[x] <= ReceiveLog_Y_Offset + DISPLAY.get_height() - 350:
            if TextGrind_IsGrindText[x]:
                save.Current_Money += float(TextGrind_Value[x])
            TextGrind_Text.pop(x)
            TextGrind_X.pop(x)
            TextGrind_Y.pop(x)
            TextGrind_AliveTime.pop(x)
            TextGrind_IsGrindText.pop(x)
            TextGrind_TextColor.pop(x)
            TextGrind_Value.pop(x)


    # -- Render the Container Title -- #
    sprite.RenderRectangle(DISPLAY, (13, 10, 13), (GlobalX + 2, GlobalY + 2, 350 - 4, 24 - 4))
    sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 18, reg.ReadKey("/strings/game/receiving_log"), (250, 250, 255), GlobalX + 3,
                      GlobalY + 3)

    ReceiveLog_CloseButton.Render(DISPLAY)
