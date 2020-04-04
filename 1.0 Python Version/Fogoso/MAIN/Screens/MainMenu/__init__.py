# -- Imports -- #
import ENGINE.Registry as reg
import ENGINE.Utils as utils
import ENGINE.TGE as tge
import ENGINE.SOUND as sound
import Fogoso.MAIN.ClassesUtils as gameObjs
import Fogoso.MAIN.Screens.Game as ScreenGame
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
CommonScreenObj = pygame.Surface((0,0))

# -- Objects Declaration -- #
PlayButton = gameObjs.Button



def Initialize(DISPLAY):
    global PlayButton
    print("Menu Initialize")
    PlayButton = gameObjs.Button((50,50,0,0),"Play",18)

def EventUpdate(event):
    global PlayButton
    PlayButton.Update(event)

def GameDraw(DISPLAY):
    global PlayButton
    global CommonScreenObj
    CommonScreenObj = DISPLAY
    DISPLAY.fill((20,20,20))

    sprite.RenderFont(DISPLAY,"/PressStart2P.ttf",12,"Fogoso",(255,255,255),5,5)

    PlayButton.Render(DISPLAY)

def Update():
    global Menu_Delay
    global IsControlsEnabled
    global PlayButton
    global CommonScreenObj
    global MenuStartFlash

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

    if Menu_Delay <= 50:
        Menu_Delay += 1
    else:
        IsControlsEnabled = True
