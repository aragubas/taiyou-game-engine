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
from ENGINE.TaiyouUI import UIGTK as gtk
from ENGINE import SOUND as sound
from ENGINE import REGISTRY as reg

# -- Variables -- #
DefaultVolumeWasSet = False
SliderObject = gtk.Slider
SliderObject_IconIndex = 0
SliderObject_AnimOpacity = 0
SliderObject_AnimY = 0
SliderObject_AnimYEnabled = True
SliderObject_ToggleButton = gtk.SpriteButton
SliderObject_AnimEnabled = False
SliderObject_AnimMode = 0
SliderObject_AnimMultiplier = 0

LastVolume = 0
CommonDisplayInited = False
ObjX = 0
ObjY = 0


def Initialize():
    global SliderObject
    global SliderObject_ToggleButton

    SliderObject = gtk.Slider(800 - 48, 32, 0)
    SliderObject_ToggleButton = gtk.SpriteButton(pygame.Rect(0, 0, 32, 32), "/TAIYOU_UI/ICONS/SPEAKER/0.png")

def Draw(DISPLAY):
    global SliderObject_AnimY
    global SliderObject_ToggleButton
    global SliderObject
    global CommonDisplayInited

    # -- Render Volume Icon -- #
    SliderObject_ToggleButton.Render(DISPLAY)

    # -- Render Volume Slider -- #
    SliderObject.Render(DISPLAY)

    if not CommonDisplayInited:
        CommonDisplayInited = True


def Update():
    global DefaultVolumeWasSet
    global SliderObject_IconIndex
    global SliderObject_AnimOpacity
    global SliderObject_AnimEnabled
    global SliderObject_AnimMode
    global SliderObject_AnimY
    global SliderObject_AnimYEnabled
    global SliderObject_ToggleButton
    global SliderObject
    global LastVolume
    global CommonDisplayInited
    global ObjX
    global ObjY
    global SliderObject_AnimMultiplier

    if CommonDisplayInited:
        if not DefaultVolumeWasSet:
            DefaultVolumeWasSet = True
            SliderObject.SetValue(reg.ReadKey_int("/TaiyouSystem/CONF/global_volume", True))
            LastVolume = SliderObject.Value

        SliderObject.Set_Y(ObjY + SliderObject_AnimY)
        SliderObject.Set_Opacity(SliderObject_AnimOpacity)
        SliderObject.Set_X(ObjX - 2)

        if not SliderObject.Value == LastVolume:
            reg.WriteKey("/TaiyouSystem/CONF/global_volume", str(SliderObject.Value), True)
            print("GlobalVolume was set to:\n" + str(SliderObject.Value))
            LastVolume = SliderObject.Value

        if SliderObject.Value >= 100:
            sound.GlobalVolume = 1.0
        else:
            sound.GlobalVolume = float("0." + str(SliderObject.Value))

        # -- Update the Icon -- #
        if SliderObject.Value <= 45:
            SliderObject_IconIndex = 0
        if SliderObject.Value >= 45 and SliderObject.Value <= 75:
            SliderObject_IconIndex = 1
        if SliderObject.Value >= 75:
            SliderObject_IconIndex = 2

        # -- Update the Animation -- #
        if SliderObject_AnimEnabled:
            if SliderObject_AnimMode == 0:
                SliderObject_AnimMultiplier += 5
                SliderObject_AnimOpacity += SliderObject_AnimMultiplier

                if SliderObject_AnimYEnabled:
                    SliderObject_AnimY += 2

                    if SliderObject_AnimY >= 32:
                        SliderObject_AnimY = 32
                        SliderObject_AnimYEnabled = False

                if SliderObject_AnimOpacity >= 255:
                    SliderObject_AnimOpacity = 255
                    SliderObject_AnimY = 32
                    SliderObject_AnimMode = 1
                    SliderObject_AnimEnabled = False
                    SliderObject_AnimYEnabled = True
                    SliderObject_AnimMultiplier = 0

            if SliderObject_AnimMode == 1 and SliderObject_AnimEnabled:
                SliderObject_AnimMultiplier += 5
                SliderObject_AnimOpacity -= SliderObject_AnimMultiplier

                if SliderObject_AnimYEnabled:
                    SliderObject_AnimY -= 2

                    if SliderObject_AnimY <= 0:
                        SliderObject_AnimY = 0
                        SliderObject_AnimYEnabled = False

                if SliderObject_AnimOpacity <= -256:
                    SliderObject_AnimOpacity = -256
                    SliderObject_AnimY = 0
                    SliderObject_AnimMode = 0
                    SliderObject_AnimEnabled = False
                    SliderObject_AnimYEnabled = True
                    SliderObject_AnimMultiplier = 0

        # -- Update System Slider Toggle Button -- #
        SliderObject_ToggleButton.Set_X(ObjX)
        SliderObject_ToggleButton.Set_Y(ObjY)
        SliderObject_ToggleButton.Set_W(28)
        SliderObject_ToggleButton.Set_H(28)
        SliderObject_ToggleButton.Set_Sprite("/TAIYOU_UI/ICONS/SPEAKER/{0}.png".format(str(SliderObject_IconIndex)))

        # -- Toggle Volume Slider -- #
        if SliderObject_ToggleButton.ButtonState == "UP":
            if not SliderObject_AnimEnabled:
                SliderObject_AnimEnabled = True

def EventUpdate(event):
    global SliderObject
    global SliderObject_ToggleButton

    SliderObject.EventUpdate(event)
    SliderObject_ToggleButton.EventUpdate(event)
