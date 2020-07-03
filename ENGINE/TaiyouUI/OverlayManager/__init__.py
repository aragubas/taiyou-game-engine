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

from ENGINE.TaiyouUI.OverlayManager import Screenshot as screenshotOverlay
from ENGINE.TaiyouUI.OverlayManager import Frametime as frametimeOverlay
from ENGINE.TaiyouUI.OverlayManager import Debug as debugOverlay
from ENGINE import *
import pygame
CurrentOverlayID = -1


def Update():
    if CurrentOverlayID == 0:  # -- Update Overlay FPS
        frametimeOverlay.Update()

    elif CurrentOverlayID == 1:  # -- Update Overlay Screenshot Overlay
        screenshotOverlay.Update()

    elif CurrentOverlayID == 2:  # -- Update Debug Profile
        debugOverlay.Update()

def Render(DISPLAY):
    if CurrentOverlayID == 0:  # -- Update Overlay FPS
        frametimeOverlay.Draw(DISPLAY)

    elif CurrentOverlayID == 1:  # -- Update Overlay Screenshot Overlay
        screenshotOverlay.Draw(DISPLAY)

    elif CurrentOverlayID == 2:
        debugOverlay.Draw(DISPLAY)

def Set_OverlayLevel(ID):
    global CurrentOverlayID
    CurrentOverlayID = int(ID)

def Get_OverlayLevel():
    global CurrentOverlayID
    return CurrentOverlayID

def EventUpdate(event):
    if CurrentOverlayID == 0:  # -- Update Overlay FPS
        frametimeOverlay.EventUpdate(event)

    elif CurrentOverlayID == 1:  # -- Update Overlay Screenshot Overlay
        screenshotOverlay.EventUpdate(event)

    elif CurrentOverlayID == 2:
        debugOverlay.EventUpdate(event)

    KeyWasValid = False

    # -- Toggle Keys -- #
    if event.type == pygame.KEYUP and event.key == pygame.K_F11:  # -- Screenshot Overlay -- #
        KeyWasValid = True

        Set_OverlayLevel(1)

    elif event.type == pygame.KEYUP and event.key == pygame.K_F10:  # -- FPS Overlay Key -- #
        KeyWasValid = True

        if Get_OverlayLevel() == 0:
            Set_OverlayLevel(-1)
        else:
            Set_OverlayLevel(0)

    elif event.type == pygame.KEYUP and event.key == pygame.K_F9:  # -- Debug Profile Overlay Key -- #
        KeyWasValid = True

        if Get_OverlayLevel() == 2:
            Set_OverlayLevel(-1)
        else:
            Set_OverlayLevel(2)

    if KeyWasValid:
        sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Click"), 0.5, PlayOnSystemChannel=True)