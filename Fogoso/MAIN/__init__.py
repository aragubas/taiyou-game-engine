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
from Fogoso.MAIN.Screens import Game as ScreenGame
from Fogoso.MAIN.Screens import MainMenu as ScreenMenu
from Fogoso.MAIN.Screens import Settings as ScreenSettings
from Fogoso.MAIN.Screens import Intro as ScreenIntro
from Fogoso.MAIN.Screens.Game import MapRender as ScreenMap
from ENGINE import SPRITE as sprite
from random import randint
from Fogoso.MAIN import GameVariables as save
import pygame, sys



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
FadeEffectStyle = 0 # 0 = Blur, 1 = Pixalizate, 2 = Blur + Pixalizate, 3 = Pixalizate + Blur

# -- Engine Options -- #
Engine_MaxFPS = 0
Engine_ResW = 1024
Engine_ResH = 720

# -- Last Error Overlay -- #
LastErrorText = ""
LastErrorTextEnabled = False
LastErrorTextDeltaTime = 0

# -- Objects -- #
DefaultDisplay = pygame.Surface((0, 0))

# -- Screens -- #
CurrentScreen = 3

ClearColor = (0,0,0)

ErrorMessageEnabled = False
ErrorMessage = 'null'
ErrorMessageDelay = 0

CursorX = 0
CursorY = 0


def GameDraw(DISPLAY):
    global DefaultDisplay
    global LastErrorText
    global LastErrorTextDeltaTime
    global LastErrorTextEnabled
    global DefaultDisplay
    global CursorW
    global CursorH
    global ClearColor
    global ErrorMessageEnabled
    global ErrorMessage
    global ErrorMessageDelay

    # -- Clear the Surface -- #
    DefaultDisplay = DISPLAY
    DISPLAY.fill(ClearColor)

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
        GeneratedWindowTitle()
        if FadeEffectStyle == 0:
            FadeEffect.blit(sprite.Surface_Blur(DISPLAY, FadeEffectValue), (0,0))
        if FadeEffectStyle == 1:
            FadeEffect.blit(sprite.Surface_Pixalizate(DISPLAY, FadeEffectValue), (0,0))
        if FadeEffectStyle == 2:
            FadeEffect.blit(sprite.Surface_Blur(sprite.Surface_Pixalizate(DISPLAY, FadeEffectValue), FadeEffectValue), (0,0))
        if FadeEffectStyle == 3:
            FadeEffect.blit(sprite.Surface_Pixalizate(sprite.Surface_Blur(DISPLAY, FadeEffectValue), FadeEffectValue), (0, 0))

        DefaultDisplay.blit(FadeEffect, (0, 0))

    # -- Render the Error Message -- #
    if ErrorMessageEnabled:
        ErrorMessageDelay += 1

        gameObjs.Draw_Panel(DISPLAY, (0,5,DISPLAY.get_width(), sprite.GetText_height("/PressStart2P.ttf", reg.ReadKey_int("/props/error_message_text_size"), ErrorMessage)))
        sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", reg.ReadKey_int("/props/error_message_text_size"), ErrorMessage,(150,50,50),0,5,False)

        if ErrorMessageDelay >= reg.ReadKey_int("/props/error_message_delay_max"):
            ErrorMessageDelay = 0
            ErrorMessageEnabled = False

    # -- Render Cursor -- #
    sprite.Render(DefaultDisplay, "/cursors/{0}.png".format(str(Cursor_CurrentLevel)), Cursor_Position[0], Cursor_Position[1], CursorW, CursorH)

    # -- Render the Error Overlay -- #
    if LastErrorTextEnabled:
        LastErrorTextDeltaTime += 1

        sprite.RenderRectangle(DISPLAY, (0, 0, 0), (0, 2, DISPLAY.get_width() ,sprite.GetText_height("/PressStart2P.ttf",9,LastErrorText) * 2 + 4))
        sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 9, LastErrorText, (200, 0, 0), 5, 5, False)

        if LastErrorTextDeltaTime >= 1500:
            LastErrorTextDeltaTime = 0
            LastErrorTextEnabled = False
            LastErrorText = ""

def GeneratedWindowTitle():
    if reg.ReadKey_bool("/OPTIONS/random_title"):
        NumberMax = reg.ReadKey_int("/strings/gme_wt/all")
        Current = randint(0, NumberMax)
        print("GeneratedWindowTitle : ID=" + str(Current))

        pygame.display.set_caption("Fogoso : " + reg.ReadKey("/strings/gme_wt/" + str(Current)))


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
    global CursorW
    global CursorH
    
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

def SendErrorMessage(Message):
    global ErrorMessageEnabled
    global ErrorMessage
    global ErrorMessageDelay
    ErrorMessage = Message
    ErrorMessageEnabled = True
    ErrorMessageDelay = 0

def ScreensUpdate():
    if CurrentScreen == -1:
        ScreenIntro.Update()
    if CurrentScreen == 0:
        ScreenMenu.Update()
    if CurrentScreen == 1:
        ScreenGame.Update()
    if CurrentScreen == 2:
        ScreenSettings.Update()
    if CurrentScreen == 3:
        ScreenMap.Update()

def ScreenDraw(DefaultDisplay):
    if CurrentScreen == -1:
        ScreenIntro.GameDraw(DefaultDisplay)
    if CurrentScreen == 0:
        ScreenMenu.GameDraw(DefaultDisplay)
    if CurrentScreen == 1:
        ScreenGame.GameDraw(DefaultDisplay)
    if CurrentScreen == 2:
        ScreenSettings.GameDraw(DefaultDisplay)
    if CurrentScreen == 3:
        ScreenMap.GameDraw(DefaultDisplay)

def ScreenEventUpdate(event):
    if CurrentScreen == -1:
        ScreenIntro.EventUpdate(event)
    if CurrentScreen == 0:
        ScreenMenu.EventUpdate(event)
    if CurrentScreen == 1:
        ScreenGame.EventUpdate(event)
    if CurrentScreen == 2:
        ScreenSettings.EventUpdate(event)
    if CurrentScreen == 3:
        ScreenMap.EventUpdate(event)

def ScreensInitialize(DISPLAY):
    if CurrentScreen == -1:
        ScreenIntro.Initialize(DISPLAY)
    if CurrentScreen == 0:
        ScreenMenu.Initialize(DISPLAY)
    if CurrentScreen == 1:
        ScreenGame.Initialize(DISPLAY)
    if CurrentScreen == 2:
        ScreenSettings.Initialize()
    if CurrentScreen == 3:
        ScreenMap.Initialize()

def EventUpdate(event):
    global Cursor_Position
    global CursorX
    global CursorY
    global DefaultDisplay
    global CursorW
    global CursorH
    # -- Update Cursor Location -- #
    if event.type == pygame.MOUSEMOTION:
        Cursor_Position[0], Cursor_Position[1] = pygame.mouse.get_pos()

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
    global FadeEffectStyle
    print("LoadOptions : Init")
    FadeEffectState = True
    FadeEffectCurrentState = 0
    FadeEffectValue = 255

    # -- Engine Flags -- #
    Engine_MaxFPS = reg.ReadKey_int("/OPTIONS/maxFPS")

    # -- Fade Effect -- #
    FadeEffectSpeed = reg.ReadKey_int("/OPTIONS/fade_flash_speed")

    # -- Fade Style -- #
    FadeEffectStyle = reg.ReadKey_int("/OPTIONS/fade_flash_style")


    print("LoadOptions : Data loading complete")

    
def Initialize(DISPLAY):
    global CurrentScreen
    print("Game Initialization")

    # -- Load Engine Options -- #
    LoadOptions()

    # -- Apply Engine Options -- #
    SetWindowParameters()
    GeneratedWindowTitle()

    # -- Set the Default Screen -- #
    CurrentScreen = reg.ReadKey_int("/props/CurrentScreen")

    if not reg.ReadKey_bool("/OPTIONS/debug_enabled"):
        try:
            ScreensInitialize(DISPLAY)
        except Exception as ex:
            WriteErrorLog(ex,"Initialize", True)
    else:
        ScreensInitialize(DISPLAY)
    

def SetWindowParameters():
    global DefaultDisplay
    DefaultDisplay = pygame.Surface((reg.ReadKey_int("/props/default_resW"), reg.ReadKey_int("/props/default_resH")))

    Messages.append("SET_FPS:" + str(Engine_MaxFPS))
    Messages.append("RESIZIABLE_WINDOW:True")
    Messages.append("SET_RESOLUTION:{0}:{1}".format(str(reg.ReadKey_int("/props/default_resW")), str(reg.ReadKey_int("/props/default_resH"))))

    pygame.display.set_caption("Fogoso : Ready!")
    pygame.mouse.set_visible(False)

    print("SetWindowParameters : FPS:{0}".format(str(Engine_MaxFPS)))

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
    global LastErrorText
    global LastErrorTextEnabled

    print("A fatal error has been occoured:\n" + str(ex))

    LastErrorText = str(ex) + "\nfunc(" + func + ")"
    LastErrorTextEnabled = True

    if ExitWhenFinished:
        ErrorLogName = "/LOG/crash_func(" + str(func) + ")"
        print("WriteErrorLog ; Error log file write at:\n" + ErrorLogName)
        reg.WriteKey(ErrorLogName, str(ex))
        print("WriteErrorLog ; Closing Game...\n")
        pygame.quit()
        sys.exit()

