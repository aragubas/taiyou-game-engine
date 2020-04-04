# -- Imports -- #
import ENGINE.Registry as reg
import ENGINE.Utils as utils
import ENGINE.TGE as tge
import ENGINE.SOUND as sound
import Fogoso.MAIN.ClassesUtils as gameObjs
import Fogoso.MAIN.Screens.Game as ScreenGame
import Fogoso.MAIN.Screens.MainMenu as ScreenMenu
import pygame, sys
import ENGINE.SPRITE as sprite
import importlib
import time
from random import randint

# -- Messages -- #
Messages = list()

# -- Cursor Variables -- #
Cursor_Position = (20, 20)
Cursor_CurrentFrame = 1
Cursor_AnimUpdateTick = 0
Cursor_CurrentLevel = 0

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

# -- Objects -- #
DefaultDisplay = pygame.Surface((0, 0))

# -- Screens -- #
CurrentScreen = 0

def GameDraw(DISPLAY):
    global DefaultDisplay
    global FadeEffectColor_R
    global FadeEffectColor_G
    global FadeEffectColor_B
    DefaultDisplay = DISPLAY

    if CurrentScreen == 0:
        ScreenMenu.GameDraw(DISPLAY)
    if CurrentScreen == 1:
        ScreenGame.GameDraw(DISPLAY)

    # -- Render Fade Effect -- #
    FadeEffect = pygame.Surface((DISPLAY.get_width(), DISPLAY.get_height()))
    FadeEffect.fill((FadeEffectColor_R, FadeEffectColor_G, FadeEffectColor_B))
    FadeEffect.set_alpha(FadeEffectValue)
    DISPLAY.blit(FadeEffect, (0, 0))

    # -- Render Cursor -- #
    sprite.Render(DISPLAY, "/cur_{0}/{1}.png".format(str(Cursor_CurrentLevel), str(Cursor_CurrentFrame)),
                  Cursor_Position[0], Cursor_Position[1], 18, 37)


def Update():
    global Cursor_CurrentLevel
    global Cursor_Position
    global Cursor_CurrentFrame
    global Cursor_AnimUpdateTick
    global FadeEffectSpeed
    global FadeEffectValue
    global FadeEffectState
    global FadeEffectCurrentState

    if CurrentScreen == 0:
        ScreenMenu.Update()
    if CurrentScreen == 1:
        ScreenGame.Update()

    # -- Update the cursor Animation -- #
    Cursor_AnimUpdateTick += 1
    if Cursor_AnimUpdateTick >= 10:
        Cursor_CurrentFrame += 1
        if Cursor_CurrentFrame >= 10:
            Cursor_CurrentFrame = 1
        Cursor_AnimUpdateTick = 0

    # -- Update the Fade Effect -- #
    if FadeEffectState:
        if FadeEffectCurrentState == 0:
            FadeEffectValue -= FadeEffectSpeed

            if FadeEffectValue <= 0:
                FadeEffectState = False
                FadeEffectValue = 0
                FadeEffectCurrentState = 1
        if FadeEffectCurrentState == 1:
            FadeEffectValue += FadeEffectSpeed

            if FadeEffectValue >= 255:
                FadeEffectState = False
                FadeEffectValue = 0
                FadeEffectCurrentState = 0


def EventUpdate(event):
    global Cursor_Position
    # -- Update Cursor Location -- #
    if event.type == pygame.MOUSEMOTION:
        Cursor_Position = pygame.mouse.get_pos()

    if CurrentScreen == 0:
        ScreenMenu.EventUpdate(event)
    if CurrentScreen == 1:
        ScreenGame.EventUpdate(event)

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

    Engine_MaxFPS = reg.ReadKeyWithTry_int("/OPTIONS/maxFPS",60)
    Engine_ResW = reg.ReadKeyWithTry_int("/OPTIONS/resW", 800)
    Engine_ResH = reg.ReadKeyWithTry_int("/OPTIONS/resH", 600)
    FadeEffectSpeed = reg.ReadKeyWithTry_int("/OPTIONS/fade_flash_speed", 5)
    FadeEffectColor_R = reg.ReadKeyWithTry_int("/OPTIONS/fade_flash_r", 255)
    FadeEffectColor_G = reg.ReadKeyWithTry_int("/OPTIONS/fade_flash_g", 255)
    FadeEffectColor_B = reg.ReadKeyWithTry_int("/OPTIONS/fade_flash_b", 255)

    print("Data loading complete")

    # -- Load Screen Resolution -- #
    Messages.append("SET_RESOLUTION:{0}:{1}".format(Engine_ResW,Engine_ResH))

    Cursor_CurrentLevel = 1


def Initialize(DISPLAY):
    print("Game Initialization")

    # -- Hide the Cursor -- #
    pygame.mouse.set_visible(False)
    SetWindowParameters()

    # -- Load Engine Options -- #
    LoadOptions()

    # -- Only the Main Menu need to be initialized -- #
    if CurrentScreen == 0:
        ScreenMenu.Initialize(DISPLAY)

def SetWindowParameters():
    Messages.append("SET_FPS:" + str(Engine_MaxFPS))
    Messages.append("SET_RESOLUTION:800:600")
    pygame.display.set_caption("Fogoso : 1.0")


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
