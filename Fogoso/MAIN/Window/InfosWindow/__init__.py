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

from ENGINE import SPRITE as sprite
from ENGINE import REGISTRY as reg
from Fogoso.MAIN.Screens import Game as GameScreen 
from Fogoso.MAIN import ClassesUtils as gameObjs
from Fogoso import MAIN as GameMain
import pygame

print("Fogoso Infos Window, Version 1.0")

# -- Field -- #
WindowObject = gameObjs.Window
DrawnSurface = pygame.Surface((0,0))

# -- Buttons Declaration -- #
NextButton = gameObjs.Button
PreviousButton = gameObjs.Button


def Initialize():
    global WindowObject
    global BuyButton
    global DrawnSurface
    global ListItems
    global BuyAmout
    global PreviousButton
    global NextButton
    WindowObject = gameObjs.Window(pygame.Rect(100,100,reg.ReadKey_int("/props/window/infos/last_w"),reg.ReadKey_int("/props/window/infos/last_h")), reg.ReadKey("/strings/window/infos/window_title"),True)
    NextButton = gameObjs.Button(pygame.Rect(0,0,0,0), ">", 12)
    PreviousButton = gameObjs.Button(pygame.Rect(0,0,0,0), "<", 12)
    NextButton.CustomColisionRectangle = True
    PreviousButton.CustomColisionRectangle = True
    WindowObject.Minimizable = False
    DrawnSurface = WindowObject.WindowSurface


CurrentCategory = 0 # 0 - Maintenance Info
DrawnSurfaceGlob = pygame.Surface
TransitionSurface = pygame.Surface((0,0))
TransitionEnabled = False
TransitionY = 1
TransitionAdder = 1
TransitionBGSurf = pygame.Surface((0,0))
def Render(DISPLAY):
    global WindowObject
    global DrawnSurface
    global NextButton
    global PreviousButton
    global DrawnSurfaceGlob
    global TransitionSurface
    global TransitionEnabled
    global TransitionY
    global TransitionBGSurf
    global TransitionAdder
    # -- Update the Surface -- #
    DrawnSurface = WindowObject.WindowSurface
    if TransitionEnabled and reg.ReadKey_bool("/OPTIONS/Windows_transitions"):
        # -- Render the Transition Surface -- #
        TransitionBGSurf = pygame.Surface((DrawnSurface.get_width(),DrawnSurface.get_height()), pygame.SRCALPHA)        
        TransitionBGSurf.blit(TransitionSurface, (0, TransitionY))
        DrawnSurface.blit(sprite.Surface_Blur(TransitionBGSurf,1.0 + TransitionY / 4), (0,0))

        TransitionAdder += 1
        TransitionY += TransitionAdder

        # -- Detect Animation End -- #
        if TransitionY >= DrawnSurface.get_height() - TransitionAdder:
            TransitionY = 1
            TransitionEnabled = False
            TransitionSurface = DrawnSurface.copy()
        

    # -- Draw the Top Bar -- #
    sprite.RenderRectangle(DrawnSurface, (1, 22, 39, 100), (0,0, DrawnSurface.get_width(), 20))
    sprite.RenderFont(DrawnSurface, "/PressStart2P.ttf", 15, reg.ReadKey("/strings/window/infos/category_" + str(CurrentCategory)), (240, 240, 240), 5,3, reg.ReadKey_bool("/OPTIONS/font_aa"))

    # -- Draw the Arrows -- #
    NextButton.Render(DrawnSurface)
    PreviousButton.Render(DrawnSurface)

    # -- Draw the Category -- #
    if CurrentCategory == 0:
        DrawCategory_0(DrawnSurface)
    if CurrentCategory == 1:
        DrawCategory_1(DrawnSurface)

    # -- Update Controls -- #
    UpdateControls(DrawnSurface)

    #sprite.RenderFont(DrawnSurface, "/PressStart2P.ttf", 10, reg.ReadKey("/strings/window/infos/txt_previuos_best") + str("{:5.2f}".format(reg.ReadKey_float("/Save/money_per_click_last_best"))), (140, 240, 140), 5, 95)

    WindowObject.Render(DISPLAY)
    DISPLAY.blit(DrawnSurface, WindowObject.WindowSurface_Dest)
    DrawnSurfaceGlob = DrawnSurface


# -- Maintenance Category -- #
def DrawCategory_0(DISPLAY):
    sprite.RenderFont(DrawnSurface, "/PressStart2P.ttf", 10, reg.ReadKey("/strings/window/infos/txt_maintenance") + str("{:5.2f}".format(GameScreen.Current_Maintenance)), (240, 240, 240), 5, 30, reg.ReadKey_bool("/OPTIONS/font_aa"))
    sprite.RenderFont(DrawnSurface, "/PressStart2P.ttf", 10, reg.ReadKey("/strings/window/infos/txt_maintenance_delay") + str(GameScreen.MaintenanceCost_DeltaMax) + "/" + str(GameScreen.MaintenanceCost_Delta), (220, 220, 220), 5, 45, reg.ReadKey_bool("/OPTIONS/font_aa"))
    sprite.RenderFont(DrawnSurface, "/PressStart2P.ttf", 10, reg.ReadKey("/strings/window/infos/txt_maintenance_base") + str("{:5.2f}".format(reg.ReadKey_float("/Save/general_maintenance"))), (200, 200, 200), 5, 60, reg.ReadKey_bool("/OPTIONS/font_aa"))

# -- Money Category -- #
def DrawCategory_1(DISPLAY):
    sprite.RenderFont(DrawnSurface, "/PressStart2P.ttf", 10, reg.ReadKey("/strings/window/infos/txt_money_per_click") + str("{:5.2f}".format(GameScreen.Current_MoneyValuePerClick)), (240, 240, 240), 5, 30, reg.ReadKey_bool("/OPTIONS/font_aa"))
    sprite.RenderFont(DrawnSurface, "/PressStart2P.ttf", 10, reg.ReadKey("/strings/window/infos/txt_previuos_best") + str(reg.ReadKey_float("/Save/money_per_click_last_best")), (220, 220, 220), 5, 45, reg.ReadKey_bool("/OPTIONS/font_aa"))
    #sprite.RenderFont(DrawnSurface, "/PressStart2P.ttf", 10, reg.ReadKey("/strings/window/infos/txt_maintenance_base") + str("{:5.2f}".format(reg.ReadKey_float("/Save/general_maintenance"))), (200, 200, 200), 5, 60)

def UpdateControls(DISPLAY):
    global NextButton
    global PreviousButton
    global WindowObject
    global CurrentCategory
    # -- Update Next Button -- #
    NextButton.Set_X(DISPLAY.get_width() - NextButton.Rectangle[2])
    NextButton.Set_Y(2)
    NextButton.Set_ColisionX(WindowObject.WindowRectangle[0] + NextButton.Rectangle[0])
    NextButton.Set_ColisionY(WindowObject.WindowRectangle[1] + NextButton.Rectangle[1] + NextButton.Rectangle[3])

    # -- Update Previous Button -- #    
    PreviousButton.Set_X(NextButton.Rectangle[0] - PreviousButton.Rectangle[2] - 5)
    PreviousButton.Set_Y(NextButton.Rectangle[1])
    PreviousButton.Set_ColisionX(WindowObject.WindowRectangle[0] + PreviousButton.Rectangle[0])
    PreviousButton.Set_ColisionY(WindowObject.WindowRectangle[1] + PreviousButton.Rectangle[1] + PreviousButton.Rectangle[3])
    

def EventUpdate(event):
    global NextButton
    global PreviousButton
    global CurrentCategory
    global TransitionSurface
    global DrawnSurfaceGlob
    global TransitionEnabled
    global TransitionY
    global TransitionAdder
    WindowObject.EventUpdate(event)
    NextButton.Update(event)
    PreviousButton.Update(event)

    if PreviousButton.ButtonState == "UP":
        if CurrentCategory > 0:
            TransitionSurface = DrawnSurfaceGlob.copy()
            CurrentCategory -= 1
        else:
            CurrentCategory = reg.ReadKey_int("/strings/window/infos/category_max")
        # -- Trigger Transition Animation (if enabled) -- #
        if reg.ReadKey_bool("/OPTIONS/Windows_transitions"):
            TransitionEnabled = True
            TransitionY = 0
            TransitionAdder = 1

    if NextButton.ButtonState == "UP":
        if CurrentCategory < reg.ReadKey_int("/strings/window/infos/category_max"):
            TransitionSurface = DrawnSurfaceGlob.copy()
            CurrentCategory += 1
        else:
            CurrentCategory = 0
        # -- Trigger Transition Animation (if enabled) -- #
        if reg.ReadKey_bool("/OPTIONS/Windows_transitions"):
            TransitionEnabled = True
            TransitionY = 0
            TransitionAdder = 1
