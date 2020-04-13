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
import Fogoso.MAIN.ClassesUtils as gameObjs
import Fogoso.MAIN.Screens.Game as ScreenGame
import Fogoso.MAIN.Screens.MainMenu as ScreenMenu
import Fogoso.MAIN.Screens.Settings as ScreenSettings
import pygame, sys
import ENGINE.SPRITE as sprite
from datetime import datetime

# -- Messages -- #
Messages = list()

# -- Cursor Variables -- #
Cursor_Position = list((20, 20))
Cursor_CurrentLevel = 0 #-- 0 = Arrow, 1 = Resize, 2 = Move, 3 = Hand, 4 = Ibeam, 5 = Pirate *x cursor*
CursorW = 0
CursorH = 0

# -- Game Start Fade Effect -- #
FadeEffectState = False
FadeEffectCurrentState = 0
FadeEffectValue = 0
FadeEffectSpeed = 5
FadeEffectColor_R = 255
FadeEffectColor_G = 255
FadeEffectColor_B = 255

# -- Engine Options -- #
Engine_MaxFPS = 0
Engine_ResW = 0
Engine_ResH = 0
Engine_MouseHeld = False

# -- Date Variables -- #
Date_Hour = 0
Date_Minute = 0
Date_Secounds = 0
Date_Month = 0
Date_Day = 0
Date_Year = 0

# -- Last Error Overlay -- #
LastErrorText = ""
LastErrorTextEnabled = False
LastErrorTextDeltaTime = 0

# -- Objects -- #
DefaultDisplay = pygame.Surface((0, 0))

# -- Screens -- #
CurrentScreen = 0

def GameDraw(DISPLAY):
    global DefaultDisplay
    global FadeEffectColor_R
    global FadeEffectColor_G
    global FadeEffectColor_B
    global LastErrorText
    global LastErrorTextDeltaTime
    global LastErrorTextEnabled
    global DefaultDisplay
    global CursorW
    global CursorH
    global Date_Secounds

    # -- Clear the Surface -- #
    DefaultDisplay.fill((20, 25, 35))

    if not reg.ReadKey_bool("/OPTIONS/debug_enabled"):
        try:
            ScreenDraw(DefaultDisplay)
        except Exception as ex:
            WriteErrorLog(ex, "GameDraw", False)
    else:
        ScreenDraw(DefaultDisplay)

    # -- Render Fade Effect -- #
    if FadeEffectValue > 0:
        FadeEffect = pygame.Surface((DefaultDisplay.get_width(), DefaultDisplay.get_height()))
        FadeEffect.fill((FadeEffectColor_R, FadeEffectColor_G, FadeEffectColor_B))

        sprite.RenderRectangle(FadeEffect,(FadeEffectValue,FadeEffectValue,FadeEffectValue),(FadeEffect.get_width() / 2 - FadeEffectValue * 2 / 2 ,FadeEffect.get_height() / 2 - FadeEffectValue * 2 / 2 ,FadeEffectValue * 2,FadeEffectValue * 2))
        sprite.RenderRectangle(FadeEffect,(255 - FadeEffectValue,255 - FadeEffectValue,255 - FadeEffectValue),(FadeEffect.get_width() / 2 - FadeEffectValue / 2,FadeEffect.get_height() / 2 - FadeEffectValue / 2,FadeEffectValue,FadeEffectValue))

        FadeEffect.set_alpha(FadeEffectValue)
        DefaultDisplay.blit(FadeEffect, (0, 0))

    # -- Render Cursor -- #
    sprite.Render(DefaultDisplay, "/cursors/{0}.png".format(str(Cursor_CurrentLevel)), Cursor_Position[0], Cursor_Position[1], CursorW, CursorH)

    # -- Blit the HUD Surface to Window -- #
    if reg.ReadKey_bool("/OPTIONS/smooth_scaling"):
        pygame.transform.smoothscale(DefaultDisplay, (DISPLAY.get_width(), DISPLAY.get_height()), DISPLAY)
    else:
        pygame.transform.scale(DefaultDisplay, (DISPLAY.get_width(), DISPLAY.get_height()), DISPLAY)

    # -- Render the Error Overlay -- #
    if LastErrorTextEnabled:
        LastErrorTextDeltaTime += 1

        sprite.RenderRectangle(DISPLAY, (0, 0, 0), (0, 2, DISPLAY.get_width() ,sprite.GetText_height("/PressStart2P.ttf",9,LastErrorText) * 2 + 4))
        sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 9, LastErrorText, (200, 0, 0), 5, 5, False)

        if LastErrorTextDeltaTime >= 1500:
            LastErrorTextDeltaTime = 0
            LastErrorTextEnabled = False
            LastErrorText = ""


def FadeAnimation():
    global FadeEffectCurrentState
    global FadeEffectValue
    global FadeEffectState
    FadeEffectCurrentState = 0
    FadeEffectValue = 255
    FadeEffectState = True

def Update():
    global FadeEffectSpeed
    global FadeEffectValue
    global FadeEffectState
    global FadeEffectCurrentState
    global Date_Hour
    global Date_Minute
    global Date_Day
    global Date_Month
    global Date_Year
    global Date_Secounds
    global CursorW
    global CursorH

    # -- Update the Date -- #
    Date_Hour = datetime.now().strftime('%H')
    Date_Minute = datetime.now().strftime('%M')
    Date_Secounds = datetime.now().strftime('%S')
    Date_Month = datetime.now().strftime('%m')
    Date_Year = datetime.now().strftime('%Y')

    # -- Set the Cursor Size -- #
    CursorW = reg.ReadKey_int("/CursorSize/" + str(Cursor_CurrentLevel) + "/w")
    CursorH = reg.ReadKey_int("/CursorSize/" + str(Cursor_CurrentLevel) + "/h")

    if not reg.ReadKey_bool("/OPTIONS/debug_enabled"):
        try:
            ScreensUpdate()
        except Exception as ex:
            WriteErrorLog(ex, "Update", True)
    else:
        ScreensUpdate()


    # -- Update the Fade Effect -- #
    if FadeEffectState:
        if FadeEffectCurrentState == 0:
            FadeEffectValue -= FadeEffectSpeed

            if FadeEffectValue <= 0:
                FadeEffectState = False
                FadeEffectValue = 0
                FadeEffectCurrentState = 0

CursorX = 0
CursorY = 0

def ScreensUpdate():
    if CurrentScreen == 0:
        ScreenMenu.Update()
    if CurrentScreen == 1:
        ScreenGame.Update()
    if CurrentScreen == 2:
        ScreenSettings.Update()

def ScreenDraw(DefaultDisplay):
    if CurrentScreen == 0:
        ScreenMenu.GameDraw(DefaultDisplay)
    if CurrentScreen == 1:
        ScreenGame.GameDraw(DefaultDisplay)
    if CurrentScreen == 2:
        ScreenSettings.GameDraw(DefaultDisplay)

def ScreenEventUpdate(event):
    if CurrentScreen == 0:
        ScreenMenu.EventUpdate(event)
    if CurrentScreen == 1:
        ScreenGame.EventUpdate(event)
    if CurrentScreen == 2:
        ScreenSettings.EventUpdate(event)

def EventUpdate(event):
    global Cursor_Position
    global Engine_MouseHeld
    global CursorX
    global CursorY
    global DefaultDisplay
    global CursorW
    global CursorH
    # -- Update Cursor Location -- #
    if event.type == pygame.MOUSEMOTION:
        # -- Set the Limits of Cursor -- #
        if Cursor_Position[0] >= DefaultDisplay.get_width() + CursorW:
            Cursor_Position[0] = DefaultDisplay.get_width() + CursorW
        if Cursor_Position[1] >= DefaultDisplay.get_height() + CursorH:
            Cursor_Position[1] = DefaultDisplay.get_height() + CursorH

        if Cursor_Position[1] <= 0:
            Cursor_Position[1] = 0
        if Cursor_Position[0] <= 0:
            Cursor_Position[0] = 0
        CursorX, CursorY = pygame.mouse.get_rel()
        Cursor_Position[0] = Cursor_Position[0] + CursorX
        Cursor_Position[1] = Cursor_Position[1] + CursorY

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_ESCAPE:
            if Engine_MouseHeld:
                Engine_MouseHeld = False
            else:
                Engine_MouseHeld = True

            pygame.event.set_grab(Engine_MouseHeld)

    if not reg.ReadKey_bool("/OPTIONS/debug_enabled"):
        try:
            ScreenEventUpdate(event)
        except Exception as ex:
            WriteErrorLog(ex, "EventUpdate", False)
    else:
        ScreenEventUpdate(event)

def LoadOptions():
    global FadeEffectCurrentState
    global FadeEffectState
    global FadeEffectValue
    global FadeEffectSpeed
    global Engine_ResH
    global Engine_ResW
    global Engine_MaxFPS
    global Cursor_CurrentLevel
    global FadeEffectColor_R
    global FadeEffectColor_G
    global FadeEffectColor_B
    print("LoadOptions : Init")
    FadeEffectState = True
    FadeEffectCurrentState = 0
    FadeEffectValue = 255

    # -- Engine Flags -- #
    Engine_MaxFPS = reg.ReadKey_int("/OPTIONS/maxFPS")
    Engine_ResW = reg.ReadKey_int("/OPTIONS/resW")
    Engine_ResH = reg.ReadKey_int("/OPTIONS/resH")

    # -- Fade Effect -- #
    FadeEffectSpeed = reg.ReadKey_int("/OPTIONS/fade_flash_speed")
    FadeEffectColor_R = reg.ReadKey_int("/OPTIONS/fade_flash_r")
    FadeEffectColor_G = reg.ReadKey_int("/OPTIONS/fade_flash_g")
    FadeEffectColor_B = reg.ReadKey_int("/OPTIONS/fade_flash_b")

    print("LoadOptions : Data loading complete")


def Initialize(DISPLAY):
    print("Game Initialization")

    # -- Load Engine Options -- #
    LoadOptions()

    # -- Apply Engine Options -- #
    SetWindowParameters()

    try:
        if CurrentScreen == 0:
            ScreenMenu.Initialize(DefaultDisplay)
        if CurrentScreen == 1:
            ScreenGame.Initialize(DefaultDisplay)
        if CurrentScreen == 2:
            ScreenSettings.Initialize(DefaultDisplay)
    except Exception as ex:
        WriteErrorLog(ex,"Initialize", True)

def SetWindowParameters():
    global DefaultDisplay
    DefaultDisplay = pygame.Surface((Engine_ResW, Engine_ResH))

    Messages.append("SET_FPS:" + str(Engine_MaxFPS))
    Messages.append("RESIZIABLE_WINDOW:True")

    pygame.display.set_caption("Fogoso : Ready!")
    pygame.mouse.set_visible(False)

    print("SetWindowParameters : FPS:{0}".format(str(Engine_MaxFPS)))
    print("SetWindowParameters : ResW:{0}".format(str(Engine_ResW)))
    print("SetWindowParameters : ResH:{0}".format(str(Engine_ResH)))


def Event_InGameOverlayOpenned():
    print("Game : InGameOverlayOpenned")


def Event_InGameOverlayClosed():
    print("Game : InGameOverlayClosed")
    SetWindowParameters()


# -- Send the messages on the Message Quee to the Game Engine -- #
def ReadCurrentMessages():
    global FadeEffectCurrentState
    global FadeEffectState
    global FadeEffectValue
    try:
        for x in Messages:
            if "SET_RESOLUTION" in x:
                FadeEffectState = True
                FadeEffectCurrentState = 0
                FadeEffectValue = 255
            Messages.remove(x)
            print("Game : MessageSent[" + x + "]")
            return x
    except:
        return ""

def WriteErrorLog(ex, func, ExitWhenFinished=False):
    global Date_Hour
    global Date_Minute
    global Date_Day
    global Date_Month
    global Date_Year
    global Date_Secounds
    global LastErrorText
    global LastErrorTextEnabled

    print("A fatal error has been occoured:\n" + str(ex))

    LastErrorText = str(ex) + "\nfunc(" + func + ")"
    LastErrorTextEnabled = True

    if ExitWhenFinished:
        ErrorLogName = "/LOG/crash_func(" + str(func) + ")_" + str(Date_Year) + "." + str(Date_Day) + "." + str(
            Date_Month) + ". " + str(Date_Hour) + "," + str(Date_Minute) + "," + str(Date_Secounds)
        print("\n\n\n\n\nWriteErrorLog ; Error log file write at:\n" + ErrorLogName)
        reg.WriteKey(ErrorLogName, str(ex))
        print("WriteErrorLog ; Closing Game...\n\n\n\n\n")
        pygame.quit()
        sys.exit()

