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
from Fogoso.MAIN.Screens import Game as ScreenGame
from Fogoso.MAIN.Screens import Settings as ScreenSettings
from Fogoso.MAIN.Screens import Intro as ScreenIntro
from Fogoso import MAIN as gameMainObj
from ENGINE import SPRITE as sprite
import pygame, sys
import importlib
import time
from random import randint

# -- Vars
Animation_Value = -300
Animation_ValueAdder = 1
Animation_CurrentAnim = 0
Animation_Enabled = True
Animation_NextScreen = 0

CommonScreenObj = pygame.Surface
ControlsInitialized = False

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
IntroSpriteButton = gameObjs.SpriteButton

def Initialize(DISPLAY):
    global PlayButton
    global SettingsButton
    global EverdayMessageWindow
    global EverdayMessage_GenerateNewMessageButton
    global IntroSpriteButton
    print("Menu Initialize")
    PlayButton = gameObjs.Button(pygame.Rect(50, 50, 0, 0), reg.ReadKey("/strings/main_menu/play_button"), 18)
    SettingsButton = gameObjs.Button(pygame.Rect(50 ,50 ,0 ,0), reg.ReadKey("/strings/main_menu/settings_button"), 18)
    EverdayMessageWindow = gameObjs.Window(pygame.Rect(350, 50, 550, 200), reg.ReadKey("/strings/main_menu/message_window/window_title"), True)
    EverdayMessage_GenerateNewMessageButton = gameObjs.Button(pygame.Rect(0,0,0,0), reg.ReadKey("/strings/main_menu/message_window/next_button"),18)
    EverdayMessage_GenerateNewMessageButton.CustomColisionRectangle = True
    gameMainObj.ClearColor = (1, 20, 30)
    IntroSpriteButton = gameObjs.SpriteButton(pygame.Rect(0,0,47, 45), ("/icon.png","/icon.png","/icon.png"))
    print("GameMenu : Initialize")

def EventUpdate(event):
    global PlayButton
    global SettingsButton
    global EverdayMessageWindow
    global EverdayMessage_GenerateNewMessageButton
    global ControlsInitialized
    global IntroSpriteButton

    if ControlsInitialized:
        PlayButton.Update(event)
        SettingsButton.Update(event)
        EverdayMessageWindow.EventUpdate(event)
        IntroSpriteButton.EventUpdate(event)
        if not EverdayMessageWindow.WindowMinimized:
            EverdayMessage_GenerateNewMessageButton.Update(event)


def GameDraw(DISPLAY):
    global PlayButton
    global SettingsButton
    global CommonScreenObj
    global EverdayMessageWindow
    global EverdayMessage_TextTitle
    global EverdayMessage_Text
    global EverdayMessage_GenerateNewMessageButton
    global ControlsInitialized
    global IntroSpriteButton
    CommonScreenObj = DISPLAY

    if ControlsInitialized:
        gameObjs.Draw_Panel(DISPLAY, (Animation_Value, 0, 300, DISPLAY.get_height()))

        sprite.RenderFont(DISPLAY,"/PressStart2P.ttf",18,reg.ReadKeyWithTry("/strings/main_menu/game_title","title"),(240,250,250), Animation_Value + 15,20, reg.ReadKey_bool("/OPTIONS/font_aa"))

        PlayButton.Render(DISPLAY)
        SettingsButton.Render(DISPLAY)

        IntroSpriteButton.Render(DISPLAY)
        sprite.RenderFont(DISPLAY,"/PressStart2P.ttf",10,reg.ReadKey("/strings/main_menu/about"),(240,250,250), IntroSpriteButton.Rectangle[0] + IntroSpriteButton.Rectangle[2] + 5,IntroSpriteButton.Rectangle[1] + 3, reg.ReadKey_bool("/OPTIONS/font_aa"))

        EverdayMessage(DISPLAY)

def EverdayMessage(DISPLAY):
    global EverdayMessageWindow
    # -- Draw the message on the Message Winow -- #
    EverdayMessageWindow.Render(DISPLAY)
    if not EverdayMessageWindow.WindowMinimized:

        # -- Render Message -- #
        sprite.RenderRectangle(EverdayMessageWindow.WindowSurface, (56, 65, 74),
                               (0, 0, EverdayMessageWindow.WindowSurface.get_width(), 30))
        if not reg.ReadKey_bool("/Save/cheater"):
            sprite.RenderFont(EverdayMessageWindow.WindowSurface, "/PressStart2P.ttf", 18, EverdayMessage_TextTitle,
                              (255, 255, 255), 5, 7, reg.ReadKey_bool("/OPTIONS/font_aa"))
            sprite.RenderFont(EverdayMessageWindow.WindowSurface, "/PressStart2P.ttf", 10, EverdayMessage_Text, (255, 255, 255),
                              5, 37, reg.ReadKey_bool("/OPTIONS/font_aa"))
        else:
            sprite.RenderFont(EverdayMessageWindow.WindowSurface, "/PressStart2P.ttf", 18, reg.ReadKey("/strings/main_menu/EMW/cheater_title"),
                              (255, 255, 255), 5, 7, reg.ReadKey_bool("/OPTIONS/font_aa"))
            sprite.RenderFont(EverdayMessageWindow.WindowSurface, "/PressStart2P.ttf", 10, reg.ReadKey("/strings/main_menu/EMW/cheater_text"),
                              (255, 255, 255),
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

MenuDelay = 0
def Update():
    global PlayButton
    global SettingsButton
    global CommonScreenObj
    global Animation_Value
    global Animation_Enabled
    global Animation_CurrentAnim
    global EverdayMessage_Text
    global EverdayMessage_TextTitle
    global EverdayMessage_UpdateMessage
    global EverdayMessage_LastMessageID
    global ControlsInitialized
    global MenuDelay
    global Animation_ValueAdder
    global Animation_NextScreen
    global IntroSpriteButton

    if not ControlsInitialized:
        MenuDelay += 1
        if MenuDelay > 1:
            MenuDelay = 0
            ControlsInitialized = True

    if EverdayMessage_UpdateMessage:
        EverdayMessage_UpdateMessage = False
        if reg.ReadKeyWithTry_bool("/strings/main_menu/EMW/first_message", True):
            EverdayMessage_TextTitle = "Welcome!"
            EverdayMessage_Text = reg.ReadKey("/strings/main_menu/EMW/first")
            reg.WriteKey("/strings/main_menu/EMW/first_message", "False")
        MessageID = randint(0,reg.ReadKey_int("/strings/main_menu/EMW/total_messages"))
        if EverdayMessage_LastMessageID == MessageID:
            MessageID = randint(MessageID, reg.ReadKey_int("/strings/main_menu/EMW/total_messages"))

        EverdayMessage_TextTitle = reg.ReadKey("/strings/main_menu/EMW/" + str(MessageID) + "_title")
        EverdayMessage_Text = reg.ReadKey("/strings/main_menu/EMW/" + str(MessageID))
        print("EverdayMessage_UpdateMessage : MessageID[" + str(MessageID) + "]")

    if Animation_Enabled:
        if Animation_CurrentAnim == 0:
            Animation_ValueAdder += 0.5
            Animation_Value += Animation_ValueAdder

            if Animation_Value >= 0:
                Animation_Value = 0
                Animation_ValueAdder = 1
                Animation_Enabled = False
                Animation_CurrentAnim = 1
        if Animation_CurrentAnim == 1:
            Animation_ValueAdder += 0.5
            Animation_Value -= Animation_ValueAdder

            if Animation_Value <= -300:
                Animation_Value = -300
                Animation_Enabled = True
                Animation_CurrentAnim = 0
                Animation_ValueAdder = 1

                if Animation_NextScreen == -1:
                    ScreenIntro.Initialize(CommonScreenObj)

                if Animation_NextScreen == 1:
                    ScreenGame.Initialize(CommonScreenObj)

                if Animation_NextScreen == 2:
                    ScreenSettings.ScreenToReturn = 0
                    ScreenSettings.Initialize()

                gameMainObj.FadeEffectValue = 255
                gameMainObj.FadeEffectCurrentState = 0
                gameMainObj.FadeEffectState = True
                gameMainObj.CurrentScreen = Animation_NextScreen

    if ControlsInitialized:
        if PlayButton.ButtonState == "UP":
            Animation_NextScreen = 1
            Animation_Enabled = True
        if SettingsButton.ButtonState == "UP":
            Animation_NextScreen = 2
            Animation_Enabled = True
        if IntroSpriteButton.ButtonState == "UP":
            Animation_NextScreen = -1
            Animation_Enabled = True

        if EverdayMessage_GenerateNewMessageButton.ButtonState == "UP" and not EverdayMessageWindow.WindowMinimized:
            EverdayMessage_UpdateMessage = True

        # -- Update Play Button Position -- #
        PlayButton.Set_X(Animation_Value + 20)
        PlayButton.Set_Y(CommonScreenObj.get_height() / 2 - PlayButton.Rectangle[3])

        # -- Update Settings Button Position -- #
        SettingsButton.Set_X(PlayButton.Rectangle[0])
        SettingsButton.Set_Y(PlayButton.Rectangle[1] + SettingsButton.Rectangle[3] + 5)

        # -- Update Intro Button Position -- #
        IntroSpriteButton.Set_X(Animation_Value + 15)
        IntroSpriteButton.Set_Y(CommonScreenObj.get_height() - IntroSpriteButton.Rectangle[3] - 15)