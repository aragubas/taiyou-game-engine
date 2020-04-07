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

# -- Objects Declaration -- #
PlayButton = gameObjs.Button
SettingsButton = gameObjs.Button

def Initialize(DISPLAY):
    global PlayButton
    global SettingsButton
    global EverdayMessageWindow
    print("Menu Initialize")
    PlayButton = gameObjs.Button(pygame.Rect(50, 50, 0, 0), "Start", 18)
    SettingsButton = gameObjs.Button(pygame.Rect(50 ,50 ,0 ,0), "Settings", 18)
    EverdayMessageWindow = gameObjs.Window(pygame.Rect(50, 50, 200, 200), "Message", True)


def EventUpdate(event):
    global PlayButton
    global SettingsButton
    global IsControlsEnabled
    global EverdayMessageWindow
    if IsControlsEnabled:
        PlayButton.Update(event)
        SettingsButton.Update(event)
        EverdayMessageWindow.EventUpdate(event)

def GameDraw(DISPLAY):
    global PlayButton
    global SettingsButton
    global IsControlsEnabled
    global CommonScreenObj
    global EverdayMessageWindow
    CommonScreenObj = DISPLAY
    DISPLAY.fill((20,20,20))

    sprite.RenderFont(DISPLAY,"/PressStart2P.ttf",28,reg.ReadKeyWithTry("/gameTitle","Fogoso"),(255,255,255),DISPLAY.get_width() / 2 - sprite.GetText_width("/PressStart2P.ttf",28,reg.ReadKeyWithTry("gameTitle","Fogoso")) / 2,20)

    if IsControlsEnabled:
        sprite.RenderRectangle(DISPLAY, (255, 255, 200), (Animation_Value + SettingsButton.Rectangle[0] - 2, PlayButton.Rectangle[1] - 2, SettingsButton.Rectangle[2] + 4, SettingsButton.Rectangle[3] + 4 + PlayButton.Rectangle[3] + 5))
        PlayButton.Render(DISPLAY)
        SettingsButton.Render(DISPLAY)

        # -- Draw the message on the Message Winow -- #
        EverdayMessageWindow.Render(DISPLAY)
        EverdayMessageWindow.WindowSurface.fill((4, 21, 32))

        # -- Render Message Title -- #
        sprite.RenderRectangle(EverdayMessageWindow.WindowSurface, (56, 65, 74), (0, 0, EverdayMessageWindow.WindowSurface.get_width(), 30))

        if reg.ReadKeyWithTry_bool("/IsFirstInitialization", True):
            sprite.RenderFont(EverdayMessageWindow.WindowSurface, "/PressStart2P.ttf", 18, "Welcome!", (255, 255, 255), 5, 7)
            sprite.RenderFont(EverdayMessageWindow.WindowSurface, "/PressStart2P.ttf", 10, "1\n2\n3", (255, 255, 255), 5, 37)

        # -- Blit the message -- #
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

        # -- Update Play Button Position -- #
        PlayButton.Set_X(Animation_Value + CommonScreenObj.get_width() / 2 - sprite.GetText_width("/PressStart2P.ttf", 18, PlayButton.ButtonText) / 2 - 8)
        PlayButton.Set_Y(Animation_Value + CommonScreenObj.get_height() / 2 - sprite.GetText_height("/PressStart2P.ttf", 18, PlayButton.ButtonText) / 2 - 8)

        SettingsButton.Set_X(Animation_Value + CommonScreenObj.get_width() / 2 - sprite.GetText_width("/PressStart2P.ttf", 18, SettingsButton.ButtonText) / 2 - 8)
        SettingsButton.Set_Y(Animation_Value + CommonScreenObj.get_height() / 2 - sprite.GetText_height("/PressStart2P.ttf", 18, SettingsButton.ButtonText) / 2 - 8 + PlayButton.Rectangle[3] + 5)


    if Menu_Delay <= 50:
        Menu_Delay += 1
    else:
        IsControlsEnabled = True
