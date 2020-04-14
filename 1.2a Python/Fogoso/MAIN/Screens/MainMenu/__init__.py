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

# -- Imports -- #
import ENGINE.Registry as reg
import ENGINE.Utils as utils
import ENGINE.TGE as tge
import ENGINE.SOUND as sound
import Fogoso.MAIN.ClassesUtils as gameObjs
import Fogoso.MAIN.Screens.Game as ScreenGame
import Fogoso.MAIN.Screens.Settings as ScreenSettings
import Fogoso.MAIN as gameMainObj
import pygame, sys
import ENGINE.SPRITE as sprite
import importlib
import time
from random import randint

# -- Vars
IsControlsEnabled = False
MenuStartFlash = False
Menu_Delay = 0
Animation_Value = 0
Animation_CurrentAnim = 0
Animation_Enabled = False
CommonScreenObj = pygame.Surface

# -- Window Test
EverdayMessageWindow = gameObjs.Window
EverdayMessage_TextTitle = "Wait"
EverdayMessage_Text = "Loading message..."
EverdayMessage_UpdateMessage = True
EverdayMessage_GenerateNewMessageButton = gameObjs.Button
EverdayMessage_LastMessageID = 0

# -- Objects Declaration -- #
PlayButton = gameObjs.Button
SettingsButton = gameObjs.Button

def Initialize(DISPLAY):
    global PlayButton
    global SettingsButton
    global EverdayMessageWindow
    global EverdayMessage_GenerateNewMessageButton
    print("Menu Initialize")
    PlayButton = gameObjs.Button(pygame.Rect(50, 50, 0, 0), "Start", 18)
    SettingsButton = gameObjs.Button(pygame.Rect(50 ,50 ,0 ,0), "Settings", 18)
    EverdayMessageWindow = gameObjs.Window(pygame.Rect(5, DISPLAY.get_height() - 25, 550, 200), "Message", True)
    EverdayMessageWindow.ToggleMinimize()
    EverdayMessage_GenerateNewMessageButton = gameObjs.Button(pygame.Rect(0,0,0,0),"Next",18)
    EverdayMessage_GenerateNewMessageButton.CustomColisionRectangle = True

def EventUpdate(event):
    global PlayButton
    global SettingsButton
    global IsControlsEnabled
    global EverdayMessageWindow
    global EverdayMessage_GenerateNewMessageButton
    if IsControlsEnabled:
        PlayButton.Update(event)
        SettingsButton.Update(event)
        EverdayMessageWindow.EventUpdate(event)
        if not EverdayMessageWindow.WindowMinimized:
            EverdayMessage_GenerateNewMessageButton.Update(event)


def GameDraw(DISPLAY):
    global PlayButton
    global SettingsButton
    global IsControlsEnabled
    global CommonScreenObj
    global EverdayMessageWindow
    global EverdayMessage_TextTitle
    global EverdayMessage_Text
    global EverdayMessage_GenerateNewMessageButton
    CommonScreenObj = DISPLAY
    sprite.RenderFont(DISPLAY,"/PressStart2P.ttf",28,reg.ReadKeyWithTry("/gameTitle","Fogoso"),(255,255,255),DISPLAY.get_width() / 2 - sprite.GetText_width("/PressStart2P.ttf", 28, reg.ReadKeyWithTry("/gameTitle", "Fogoso")) / 2,20, reg.ReadKey_bool("/OPTIONS/font_aa"))

    if IsControlsEnabled:
        sprite.RenderRectangle(DISPLAY, (1, 22, 39), (Animation_Value + SettingsButton.Rectangle[0] - 2, PlayButton.Rectangle[1] - 2, SettingsButton.Rectangle[2] + 4, SettingsButton.Rectangle[3] + 4 + PlayButton.Rectangle[3] + 5))
        sprite.RenderRectangle(DISPLAY, (46, 192, 182), (Animation_Value + SettingsButton.Rectangle[0] - 2, PlayButton.Rectangle[1] - 2, SettingsButton.Rectangle[2] + 4, 2))

        PlayButton.Render(DISPLAY)
        SettingsButton.Render(DISPLAY)
        EverdayMessage(DISPLAY)

def EverdayMessage(DISPLAY):
    # -- Draw the message on the Message Winow -- #
    EverdayMessageWindow.Render(DISPLAY)
    if not EverdayMessageWindow.WindowMinimized:
        EverdayMessageWindow.WindowSurface.fill((4, 21, 32))

        # -- Render Message -- #
        sprite.RenderRectangle(EverdayMessageWindow.WindowSurface, (56, 65, 74),
                               (0, 0, EverdayMessageWindow.WindowSurface.get_width(), 30))
        sprite.RenderFont(EverdayMessageWindow.WindowSurface, "/PressStart2P.ttf", 18, EverdayMessage_TextTitle,
                          (255, 255, 255), 5, 7, reg.ReadKey_bool("/OPTIONS/font_aa"))
        sprite.RenderFont(EverdayMessageWindow.WindowSurface, "/PressStart2P.ttf", 10, EverdayMessage_Text, (255, 255, 255),
                          5, 37, reg.ReadKey_bool("/OPTIONS/font_aa"))

        # -- Render Next Button -- ##
        EverdayMessage_GenerateNewMessageButton.Set_X(
            EverdayMessageWindow.WindowRectangle[2] - EverdayMessage_GenerateNewMessageButton.Rectangle[2] - 5)
        EverdayMessage_GenerateNewMessageButton.Set_Y(
            EverdayMessageWindow.WindowRectangle[3] - EverdayMessage_GenerateNewMessageButton.Rectangle[3] - 25)

        # -- Set the right Colision Rectangle -- #
        ColisionX = EverdayMessageWindow.WindowRectangle[0] + EverdayMessage_GenerateNewMessageButton.Rectangle[0]
        ColisionY = EverdayMessageWindow.WindowRectangle[1] + EverdayMessage_GenerateNewMessageButton.Rectangle[1] + EverdayMessage_GenerateNewMessageButton.Rectangle[3] - 2
        EverdayMessage_GenerateNewMessageButton.Set_ColisionX(ColisionX)
        EverdayMessage_GenerateNewMessageButton.Set_ColisionY(ColisionY)

        EverdayMessage_GenerateNewMessageButton.Render(EverdayMessageWindow.WindowSurface)

        # -- Blit Window to Screen -- #
        DISPLAY.blit(EverdayMessageWindow.WindowSurface, EverdayMessageWindow.WindowSurface_Dest)


def Update():
    global Menu_Delay
    global IsControlsEnabled
    global PlayButton
    global SettingsButton
    global CommonScreenObj
    global MenuStartFlash
    global Animation_Value
    global Animation_Enabled
    global Animation_CurrentAnim
    global EverdayMessage_Text
    global EverdayMessage_TextTitle
    global EverdayMessage_UpdateMessage
    global EverdayMessage_LastMessageID

    if EverdayMessage_UpdateMessage:
        EverdayMessage_UpdateMessage = False
        if reg.ReadKeyWithTry_bool("/EMW/first_message", True):
            EverdayMessage_TextTitle = "Welcome!"
            EverdayMessage_Text = reg.ReadKey("/EMW/first")
            reg.WriteKey("/EMW/first_message", "False")
        MessageID = randint(0,reg.ReadKey_int("/EMW/total_messages"))
        if EverdayMessage_LastMessageID == MessageID:
            MessageID = randint(MessageID, reg.ReadKey_int("/EMW/total_messages"))

        EverdayMessage_TextTitle = reg.ReadKey("/EMW/" + str(MessageID) + "_title")
        EverdayMessage_Text = reg.ReadKey("/EMW/" + str(MessageID))
        print("EverdayMessage_UpdateMessage : MessageID[" + str(MessageID) + "]")

    if Animation_Enabled:
        if Animation_CurrentAnim == 0:
            Animation_Value += 1

            if Animation_Value >= 50:
                Animation_Value = 0
                Animation_Enabled = False
                Animation_CurrentAnim = 1
        if Animation_CurrentAnim == 1:
            Animation_Value -= 1

            if Animation_Value >= 50:
                Animation_Value = 0
                Animation_Enabled = False
                Animation_CurrentAnim = 1

    if not MenuStartFlash:
        gameMainObj.FadeEffectState = 0
        gameMainObj.FadeEffectValue = 255
        gameMainObj.FadeEffectState = True
        MenuStartFlash = True

    if IsControlsEnabled:
        if PlayButton.ButtonState == "UP":
            ScreenGame.Initialize(CommonScreenObj)
            gameMainObj.CurrentScreen += 1
            Menu_Delay = 0
            IsControlsEnabled = False
            MenuStartFlash = False
            gameMainObj.Cursor_CurrentLevel = 0
        if SettingsButton.ButtonState == "UP":
            ScreenSettings.Initialize()
            ScreenSettings.ScreenToReturn = gameMainObj.CurrentScreen
            gameMainObj.CurrentScreen = 2
            Menu_Delay = 0
            IsControlsEnabled = False
            MenuStartFlash = False
            gameMainObj.FadeEffectValue = 255
            gameMainObj.FadeEffectCurrentState = 0
            gameMainObj.FadeEffectState = True

        if EverdayMessage_GenerateNewMessageButton.ButtonState == "UP" and not EverdayMessageWindow.WindowMinimized:
            EverdayMessage_UpdateMessage = True

        # -- Update Play Button Position -- #
        PlayButton.Set_X(Animation_Value + CommonScreenObj.get_width() / 2 - sprite.GetText_width("/PressStart2P.ttf", 18, PlayButton.ButtonText) / 2 - 8)
        PlayButton.Set_Y(Animation_Value + CommonScreenObj.get_height() / 2 - sprite.GetText_height("/PressStart2P.ttf", 18, PlayButton.ButtonText) / 2 - 8)

        SettingsButton.Set_X(Animation_Value + CommonScreenObj.get_width() / 2 - sprite.GetText_width("/PressStart2P.ttf", 18, SettingsButton.ButtonText) / 2 - 8)
        SettingsButton.Set_Y(Animation_Value + CommonScreenObj.get_height() / 2 - sprite.GetText_height("/PressStart2P.ttf", 18, SettingsButton.ButtonText) / 2 - 8 + PlayButton.Rectangle[3] + 5)

    if Menu_Delay <= 50:
        Menu_Delay += 1
    else:
        IsControlsEnabled = True
