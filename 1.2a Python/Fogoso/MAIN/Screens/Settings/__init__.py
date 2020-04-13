#!/usr/bin/env python3.7
#
#   Copyright 2020 Aragubas
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

# -- Imports -- #
import ENGINE.Registry as reg
import ENGINE.Utils as utils
import ENGINE.TGE as tge
import ENGINE.SOUND as sound
import Fogoso.MAIN.ClassesUtils as gameObjs
import Fogoso.MAIN as gameMain
import pygame, sys
import ENGINE.SPRITE as sprite
import importlib
import time
from random import randint

# -- Objects Definition -- #
OptionsScreen_CloseButton = gameObjs.Button
OptionsScreen_ChangeFps = gameObjs.UpDownButton
OptionsScreen_ChangeWindowSize = gameObjs.UpDownButton
OptionsScreen_FlashAnimationSpeed = gameObjs.UpDownButton
OptionsScreen_FontAntiAlias = gameObjs.Button
OptionsScreen_screenSmoothScaling = gameObjs.Button

ScreenToReturn = 0

def Update():
    global OptionsScreen_CloseButton
    global OptionsScreen_ChangeFps
    global OptionsScreen_ChangeWindowSize
    global OptionsScreen_FlashAnimationSpeed
    global OptionsScreen_FontAntiAlias
    global OptionsScreen_screenSmoothScaling

    if OptionsScreen_CloseButton.ButtonState == "UP":
        gameMain.FadeEffectValue = 255
        gameMain.FadeEffectCurrentState = 0
        gameMain.FadeEffectState = True
        gameMain.CurrentScreen = ScreenToReturn

    if OptionsScreen_ChangeFps.ButtonState == "UP":
        print("MaxFPS is [" + str(gameMain.Engine_MaxFPS) + "]")
        if gameMain.Engine_MaxFPS == 120:
            gameMain.Engine_MaxFPS = 0
        elif gameMain.Engine_MaxFPS == 75:
            gameMain.Engine_MaxFPS = 120
        elif gameMain.Engine_MaxFPS == 60:
            gameMain.Engine_MaxFPS = 75
        elif gameMain.Engine_MaxFPS == 0:
            gameMain.Engine_MaxFPS = 60
        gameMain.Messages.append("SET_FPS:" + str(gameMain.Engine_MaxFPS))
        reg.WriteKey("/OPTIONS/maxFPS", str(gameMain.Engine_MaxFPS))
        print("MaxFPS is now set to[" + str(gameMain.Engine_MaxFPS) + "]")

    if OptionsScreen_ChangeFps.ButtonState == "DOWN":
        print("MaxFPS is [" + str(gameMain.Engine_MaxFPS) + "]")
        if gameMain.Engine_MaxFPS == 120:
            gameMain.Engine_MaxFPS = 75
        elif gameMain.Engine_MaxFPS == 75:
            gameMain.Engine_MaxFPS = 60
        elif gameMain.Engine_MaxFPS == 60:
            gameMain.Engine_MaxFPS = 0
        elif gameMain.Engine_MaxFPS == 0:
            gameMain.Engine_MaxFPS = 120
        gameMain.Messages.append("SET_FPS:" + str(gameMain.Engine_MaxFPS))
        reg.WriteKey("/OPTIONS/maxFPS", str(gameMain.Engine_MaxFPS))
        print("MaxFPS is now set to[" + str(gameMain.Engine_MaxFPS) + "]")

    if OptionsScreen_ChangeWindowSize.ButtonState == "UP":
        CurrentW, CurrentH = gameMain.DefaultDisplay.get_size()
        print("OldResolution : " + str(CurrentW) + "x" + str(CurrentH))

        if CurrentW == 1280 and CurrentH == 1024:
            CurrentW = 800
            CurrentH = 600
        elif CurrentW == 720 and CurrentH == 480:
            CurrentW = 1280
            CurrentH = 1024
        elif CurrentW == 800 and CurrentH == 600:
            CurrentW = 720
            CurrentH = 480

        print("New Resolution : " + str(CurrentW) + "x" + str(CurrentH))
        reg.WriteKey("/OPTIONS/resW", str(CurrentW))
        reg.WriteKey("/OPTIONS/resH", str(CurrentH))
        gameMain.DefaultDisplay = pygame.Surface((CurrentW,CurrentH))

    if OptionsScreen_ChangeWindowSize.ButtonState == "DOWN":
        CurrentW, CurrentH = gameMain.DefaultDisplay.get_size()
        print("Old Resolution : " + str(CurrentW) + "x" + str(CurrentH))

        if CurrentW == 1280 and CurrentH == 1024:
            CurrentW = 720
            CurrentH = 480
        elif CurrentW == 720 and CurrentH == 480:
            CurrentW = 800
            CurrentH = 600
        elif CurrentW == 800 and CurrentH == 600:
            CurrentW = 1280
            CurrentH = 1024

        print("New Resolution : " + str(CurrentW) + "x" + str(CurrentH))
        reg.WriteKey("/OPTIONS/resW", str(CurrentW))
        reg.WriteKey("/OPTIONS/resH", str(CurrentH))
        gameMain.DefaultDisplay = pygame.Surface((CurrentW,CurrentH))

    if OptionsScreen_FlashAnimationSpeed.ButtonState == "UP":
        print("Old FlashAnimationSpeed : " + str(reg.ReadKey_int("/OPTIONS/fade_flash_speed")))
        if gameMain.FadeEffectSpeed <= 9:
            gameMain.FadeEffectSpeed += 1
        reg.WriteKey("/OPTIONS/fade_flash_speed", str(gameMain.FadeEffectSpeed))
        print("New FlashAnimationSpeed : " + str(reg.ReadKey_int("/OPTIONS/fade_flash_speed")))
    if OptionsScreen_FlashAnimationSpeed.ButtonState == "DOWN":
        print("Old FlashAnimationSpeed : " + str(reg.ReadKey_int("/OPTIONS/fade_flash_speed")))
        if gameMain.FadeEffectSpeed >= 2:
            gameMain.FadeEffectSpeed -= 1
        reg.WriteKey("/OPTIONS/fade_flash_speed", str(gameMain.FadeEffectSpeed))
        print("New FlashAnimationSpeed : " + str(reg.ReadKey_int("/OPTIONS/fade_flash_speed")))

    if OptionsScreen_FontAntiAlias.ButtonState == "UP":
        if reg.ReadKey_bool("/OPTIONS/font_aa"):
            reg.WriteKey("/OPTIONS/font_aa", "False")
        else:
            reg.WriteKey("/OPTIONS/font_aa", "True")

    if OptionsScreen_screenSmoothScaling.ButtonState == "UP":
        if reg.ReadKey_bool("/OPTIONS/smooth_scaling"):
            reg.WriteKey("/OPTIONS/smooth_scaling", "False")
        else:
            reg.WriteKey("/OPTIONS/smooth_scaling", "True")

    OptionsScreen_CloseButton.Set_X(gameMain.DefaultDisplay.get_width() - 120)


def GameDraw(DISPLAY):
    global OptionsScreen_CloseButton
    global OptionsScreen_ChangeFps
    global OptionsScreen_ChangeWindowSize
    global OptionsScreen_FlashAnimationSpeed
    global OptionsScreen_FontAntiAlias
    global OptionsScreen_screenSmoothScaling

    # -- Render the Options Menu Background -- #
    ElementsX = DISPLAY.get_width() / 2 - 275
    ElementsY = DISPLAY.get_height() / 2 - 125
    sprite.RenderRectangle(DISPLAY, (0, 12, 29), (ElementsX - 4, ElementsY - 4, 558, 258))
    sprite.RenderRectangle(DISPLAY, (1, 22, 39), (ElementsX, ElementsY, 550, 250))

    # -- Render The Title Text -- #
    sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 28, "-- Options --", (246, 247, 248), ElementsX + 95,
                      ElementsY + 5, reg.ReadKey_bool("/OPTIONS/font_aa"))
    # -- Render Close Button -- #
    OptionsScreen_CloseButton.Render(DISPLAY)
    # -- Render Max FPS Option -- #
    OptionsScreen_ChangeFps.Render(DISPLAY)
    OptionsScreen_ChangeFps.Set_X(ElementsX + 20)
    OptionsScreen_ChangeFps.Set_Y(ElementsY + 50)
    sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 14, "Max FPS:" + str(gameMain.Engine_MaxFPS),
                      (255, 255, 255), ElementsX + 95, ElementsY + 52, reg.ReadKey_bool("/OPTIONS/font_aa"))

    # -- Render Resolution Option -- #
    OptionsScreen_ChangeWindowSize.Render(DISPLAY)
    OptionsScreen_ChangeWindowSize.Set_X(ElementsX + 20)
    OptionsScreen_ChangeWindowSize.Set_Y(ElementsY + 75)
    ResName = "Invalid"
    if gameMain.DefaultDisplay.get_width() == 800 and DISPLAY.get_height() == 600:
        ResName = "SVGA,4:3"
    if gameMain.DefaultDisplay.get_width() == 720 and DISPLAY.get_height() == 480:
        ResName = "VGA,4:3"
    if gameMain.DefaultDisplay.get_width() == 1280 and DISPLAY.get_height() == 1024:
        ResName = "SXGA,5:3"
    sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 14,
                      "Resolution:" + str(DISPLAY.get_width()) + "x" + str(
                          DISPLAY.get_height()) + "[{0}]".format(ResName),
                      (255, 255, 255), ElementsX + 95, ElementsY + 78, reg.ReadKey_bool("/OPTIONS/font_aa"))

    # -- Render Flash Animation Speed -- #
    OptionsScreen_FlashAnimationSpeed.Render(DISPLAY)
    OptionsScreen_FlashAnimationSpeed.Set_X(ElementsX + 20)
    OptionsScreen_FlashAnimationSpeed.Set_Y(ElementsY + 100)
    sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 14, "Flash Animation Speed:" + str(gameMain.FadeEffectSpeed),
                      (255, 255, 255), ElementsX + 95, ElementsY + 102, reg.ReadKey_bool("/OPTIONS/font_aa"))

    # -- Render FontAntiAlias -- #
    OptionsScreen_FontAntiAlias.Render(DISPLAY)
    OptionsScreen_FontAntiAlias.Set_X(ElementsX + 20)
    OptionsScreen_FontAntiAlias.Set_Y(ElementsY + 120)
    sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 14, "Font AntiAlias: " + str(reg.ReadKey_bool("/OPTIONS/font_aa")), (255, 255, 255),ElementsX + 120,ElementsY + 122, reg.ReadKey_bool("/OPTIONS/font_aa"))

    # -- Render SmoothScaling -- #
    OptionsScreen_screenSmoothScaling.Render(DISPLAY)
    OptionsScreen_screenSmoothScaling.Set_X(ElementsX + 20)
    OptionsScreen_screenSmoothScaling.Set_Y(ElementsY + 140)
    sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 14, "Screen Smooth Scaling: " + str(reg.ReadKey_bool("/OPTIONS/smooth_scaling")), (255, 255, 255),ElementsX + 120,ElementsY + 142, reg.ReadKey_bool("/OPTIONS/font_aa"))


def Initialize():
    global OptionsScreen_CloseButton
    global OptionsScreen_ChangeFps
    global OptionsScreen_ChangeWindowSize
    global OptionsScreen_FlashAnimationSpeed
    global OptionsScreen_FontAntiAlias
    global OptionsScreen_screenSmoothScaling

    OptionsScreen_CloseButton = gameObjs.Button(pygame.rect.Rect(0, 5, 0, 0),"< Back", 14)
    OptionsScreen_ChangeFps = gameObjs.UpDownButton(20, 100, 14)
    OptionsScreen_ChangeWindowSize = gameObjs.UpDownButton(20, 130, 14)
    OptionsScreen_FlashAnimationSpeed = gameObjs.UpDownButton(20, 160, 14)
    OptionsScreen_FontAntiAlias = gameObjs.Button(pygame.Rect(0,0,0,0),"Toggle", 14)
    OptionsScreen_screenSmoothScaling = gameObjs.Button(pygame.Rect(0,0,0,0),"Toggle", 14)
    gameMain.Cursor_CurrentLevel = 0


def EventUpdate(event):
    global OptionsScreen_CloseButton
    global OptionsScreen_ChangeFps
    global OptionsScreen_ChangeWindowSize
    global OptionsScreen_FlashAnimationSpeed
    global OptionsScreen_FontAntiAlias
    global OptionsScreen_screenSmoothScaling

    # -- Update all buttons -- #
    OptionsScreen_CloseButton.Update(event)
    OptionsScreen_ChangeFps.Update(event)
    OptionsScreen_ChangeWindowSize.Update(event)
    OptionsScreen_FlashAnimationSpeed.Update(event)
    OptionsScreen_FontAntiAlias.Update(event)
    OptionsScreen_screenSmoothScaling.Update(event)
