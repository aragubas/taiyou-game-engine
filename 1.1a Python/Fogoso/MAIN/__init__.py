# -- Imports -- #
import ENGINE.Registry as reg
import Fogoso.MAIN.ClassesUtils as gameObjs
import Fogoso.MAIN.Screens.Game as ScreenGame
import Fogoso.MAIN.Screens.MainMenu as ScreenMenu
import Fogoso.MAIN.Screens.Settings as ScreenSettings
import pygame
import ENGINE.SPRITE as sprite

# -- Messages -- #
Messages = list()

# -- Cursor Variables -- #
Cursor_Position = (20, 20)
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
    if CurrentScreen == 2:
        ScreenSettings.GameDraw(DISPLAY)

    # -- Render Fade Effect -- #
    FadeEffect = pygame.Surface((DISPLAY.get_width(), DISPLAY.get_height()))
    FadeEffect.fill((FadeEffectColor_R, FadeEffectColor_G, FadeEffectColor_B))

    sprite.RenderRectangle(FadeEffect,(FadeEffectValue,FadeEffectValue,FadeEffectValue),(FadeEffect.get_width() / 2 - FadeEffectValue * 2 / 2 ,FadeEffect.get_height() / 2 - FadeEffectValue * 2 / 2 ,FadeEffectValue * 2,FadeEffectValue * 2))
    sprite.RenderRectangle(FadeEffect,(255 - FadeEffectValue,255 - FadeEffectValue,255 - FadeEffectValue),(FadeEffect.get_width() / 2 - FadeEffectValue / 2,FadeEffect.get_height() / 2 - FadeEffectValue / 2,FadeEffectValue,FadeEffectValue))

    FadeEffect.set_alpha(FadeEffectValue)
    DISPLAY.blit(FadeEffect, (0, 0))

    CursorW = 0
    CursorH = 0

    if Cursor_CurrentLevel == 0:
        CursorW = 15
        CursorH = 22
    if Cursor_CurrentLevel == 1:
        CursorW = 21
        CursorH = 20
    if Cursor_CurrentLevel == 2:
        CursorW = 19
        CursorH = 15
    if Cursor_CurrentLevel == 3:
        CursorW = 19
        CursorH = 19
    if Cursor_CurrentLevel == 4:
        CursorW = 10
        CursorH = 18
    if Cursor_CurrentLevel == 5:
        CursorW = 16
        CursorH = 16

    # -- Render Cursor -- #
    sprite.Render(DISPLAY, "/cursors/{0}.png".format(str(Cursor_CurrentLevel)),
                  Cursor_Position[0], Cursor_Position[1], CursorW, CursorH)

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

    if CurrentScreen == 0:
        ScreenMenu.Update()
    if CurrentScreen == 1:
        ScreenGame.Update()
    if CurrentScreen == 2:
        ScreenSettings.Update()

    # -- Update the Fade Effect -- #
    if FadeEffectState:
        if FadeEffectCurrentState == 0:
            FadeEffectValue -= FadeEffectSpeed

            if FadeEffectValue <= 0:
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
    if CurrentScreen == 2:
        ScreenSettings.EventUpdate(event)

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
    FadeEffectColor_R = reg.ReadKeyWithTry_int("/OPTIONS/fade_flash_r", 150)
    FadeEffectColor_G = reg.ReadKeyWithTry_int("/OPTIONS/fade_flash_g", 150)
    FadeEffectColor_B = reg.ReadKeyWithTry_int("/OPTIONS/fade_flash_b", 150)

    print("Data loading complete")

    # -- Load Screen Resolution -- #
    Messages.append("SET_RESOLUTION:{0}:{1}".format(Engine_ResW,Engine_ResH))


def Initialize(DISPLAY):
    print("Game Initialization")

    # -- Set Window Parameters -- #
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
    pygame.mouse.set_visible(False)

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
