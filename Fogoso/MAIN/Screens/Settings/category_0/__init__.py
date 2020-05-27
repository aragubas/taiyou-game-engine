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
from Fogoso.MAIN import ClassesUtils as gameObjs
from Fogoso import MAIN as gameMain
from ENGINE import REGISTRY as reg
from ENGINE import sprite as sprite

# -- Objects Definition -- #
OptionsScreen_ChangeFps = gameObjs.UpDownButton
OptionsScreen_FlashAnimationSpeed = gameObjs.UpDownButton
OptionsScreen_FontAntiAlias = gameObjs.Button
OptionsScreen_FlashAnimStyle = gameObjs.UpDownButton

ElementsX = 0
ElementsY = 0

def Initialize():
    global OptionsScreen_ChangeFps
    global OptionsScreen_FlashAnimationSpeed
    global OptionsScreen_FontAntiAlias
    global OptionsScreen_FlashAnimStyle
    OptionsScreen_ChangeFps = gameObjs.UpDownButton(20, 100, 14)
    OptionsScreen_FlashAnimationSpeed = gameObjs.UpDownButton(20, 160, 14)
    OptionsScreen_FontAntiAlias = gameObjs.Button(pygame.Rect(0, 0, 0, 0),reg.ReadKey("/strings/settings/toggle_button"), 14)
    OptionsScreen_FlashAnimStyle = gameObjs.UpDownButton(0, 0, 14)

def EventUpdate(event):
    global OptionsScreen_ChangeFps
    global OptionsScreen_FlashAnimationSpeed
    global OptionsScreen_FontAntiAlias
    global OptionsScreen_FlashAnimStyle

    OptionsScreen_ChangeFps.Update(event)
    OptionsScreen_FlashAnimationSpeed.Update(event)
    OptionsScreen_FontAntiAlias.Update(event)
    OptionsScreen_FlashAnimStyle.Update(event)


def Update():
    global OptionsScreen_ChangeFps
    global OptionsScreen_FlashAnimationSpeed
    global OptionsScreen_FontAntiAlias
    global OptionsScreen_FlashAnimStyle

    if OptionsScreen_ChangeFps.ButtonState == "UP":
        print("MaxFPS is [" + str(gameMain.Engine_MaxFPS) + "]")
        if gameMain.Engine_MaxFPS == 60:
            gameMain.Engine_MaxFPS = 25
        elif gameMain.Engine_MaxFPS == 25:
            gameMain.Engine_MaxFPS = 30
        elif gameMain.Engine_MaxFPS == 30:
            gameMain.Engine_MaxFPS = 45
        elif gameMain.Engine_MaxFPS == 45:
            gameMain.Engine_MaxFPS = 60

        gameMain.Messages.append("SET_FPS:" + str(gameMain.Engine_MaxFPS))
        reg.WriteKey("/OPTIONS/maxFPS", str(gameMain.Engine_MaxFPS))
        print("MaxFPS is now set to[" + str(gameMain.Engine_MaxFPS) + "]")

    if OptionsScreen_ChangeFps.ButtonState == "DOWN":
        print("MaxFPS is [" + str(gameMain.Engine_MaxFPS) + "]")
        if gameMain.Engine_MaxFPS == 60:
            gameMain.Engine_MaxFPS = 45
        elif gameMain.Engine_MaxFPS == 45:
            gameMain.Engine_MaxFPS = 30
        elif gameMain.Engine_MaxFPS == 30:
            gameMain.Engine_MaxFPS = 25
        elif gameMain.Engine_MaxFPS == 25:
            gameMain.Engine_MaxFPS = 60

        gameMain.Messages.append("SET_FPS:" + str(gameMain.Engine_MaxFPS))
        reg.WriteKey("/OPTIONS/maxFPS", str(gameMain.Engine_MaxFPS))
        print("MaxFPS is now set to[" + str(gameMain.Engine_MaxFPS) + "]")

    if OptionsScreen_FlashAnimationSpeed.ButtonState == "UP":
        print("Old FlashAnimationSpeed : " + str(reg.ReadKey_int("/OPTIONS/fade_flash_speed")))
        if gameMain.FadeEffectSpeed <= reg.ReadKey_int("/OPTIONS/props/fade_flash_speed_max"):
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

    if OptionsScreen_FlashAnimStyle.ButtonState == "UP":
        CurrentValue = reg.ReadKey_int("/OPTIONS/fade_flash_style")
        MaxValue = reg.ReadKey_int("/OPTIONS/props/fade_flash_style_max")

        if CurrentValue < MaxValue:
            CurrentValue += 1
        else:
            CurrentValue = 0

        reg.WriteKey("/OPTIONS/fade_flash_style", str(CurrentValue))
        gameMain.FadeEffectStyle = CurrentValue

    if OptionsScreen_FlashAnimStyle.ButtonState == "DOWN":
        CurrentValue = reg.ReadKey_int("/OPTIONS/fade_flash_style")
        MaxValue = reg.ReadKey_int("/OPTIONS/props/fade_flash_style_max")

        if CurrentValue > -1:
            CurrentValue -= 1
        if CurrentValue == -1:
            CurrentValue = MaxValue

        reg.WriteKey("/OPTIONS/fade_flash_style", str(CurrentValue))
        gameMain.FadeEffectStyle = CurrentValue

    # -- Set Positions -- #
    OptionsScreen_ChangeFps.Set_X(ElementsX + 20)
    OptionsScreen_ChangeFps.Set_Y(ElementsY + 50)

    OptionsScreen_FlashAnimationSpeed.Set_X(ElementsX + 20)
    OptionsScreen_FlashAnimationSpeed.Set_Y(ElementsY + 75)

    OptionsScreen_FontAntiAlias.Set_X(ElementsX + 20)
    OptionsScreen_FontAntiAlias.Set_Y(ElementsY + 100)

    OptionsScreen_FlashAnimStyle.Set_X(ElementsX + 20)
    OptionsScreen_FlashAnimStyle.Set_Y(ElementsY + 125)


def Render(DISPLAY):
    # -- Render Max FPS Option -- #
    OptionsScreen_ChangeFps.Render(DISPLAY)
    sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 14,
                      reg.ReadKey("/strings/settings/max_fps") + str(gameMain.Engine_MaxFPS),
                      (255, 255, 255), ElementsX + 95, ElementsY + 52, reg.ReadKey_bool("/OPTIONS/font_aa"))

    # -- Render Flash Animation Speed -- #
    OptionsScreen_FlashAnimationSpeed.Render(DISPLAY)
    sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 14,
                      reg.ReadKey("/strings/settings/flash_anim_speed") + str(gameMain.FadeEffectSpeed),
                      (255, 255, 255), ElementsX + 95, ElementsY + 77, reg.ReadKey_bool("/OPTIONS/font_aa"))

    # -- Render FontAntiAlias -- #
    OptionsScreen_FontAntiAlias.Render(DISPLAY)

    sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 14,
                      reg.ReadKey("/strings/settings/font_aa") + str(reg.ReadKey_bool("/OPTIONS/font_aa")),
                      (255, 255, 255), ElementsX + 120, ElementsY + 102, reg.ReadKey_bool("/OPTIONS/font_aa"))

    # -- Render FlashAnimStyle -- #
    OptionsScreen_FlashAnimStyle.Render(DISPLAY)
    sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 14, reg.ReadKey("/strings/settings/flash_anim_style") + reg.ReadKey("/OPTIONS/desc/fade_flash/" + reg.ReadKey("/OPTIONS/fade_flash_style")), (255, 255, 255), ElementsX + 95, ElementsY + 127,
                      reg.ReadKey_bool("/OPTIONS/font_aa"))
