#!/usr/bin/python3
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

# Import some stuff
from ENGINE import REGISTRY as reg
from ENGINE import SPRITE as sprite
import ENGINE as tge
import pygame, sys, importlib
import threading

# The main Entry Point
print("TaiyouGameEngineMainScript version 1.2")

# -- Global Variables -- #
IsGameRunning = False
GameDrawAllowed = False
ResiziableWindow = False
clock = pygame.time.Clock()
FPS = 75
ToggleGameStart = True
GameStarted = False
DISPLAY = pygame.display
IsFullscreen = False
CurrentRes_W = 0
CurrentRes_H = 0

# -- Receives command from the Game -- #
def ReceiveCommand(Command):
    global IsGameRunning
    global ToggleGameStart
    global FPS
    global DISPLAY
    global IsFullscreen
    global CurrentRes_W
    global CurrentRes_H
    global ResiziableWindow

    if Command.startswith("SET_FPS:") if Command else False:
        try:
            splitedArg = Command.split(':')
            FPS = int(splitedArg[1])
            print("Taiyou.ReceiveComamnd : MaxFPS Setted to:" + str(FPS))

        except:
            print("Taiyou.ReceiveComamnd_Error : Invalid Argument, [" + Command + "]")

    if Command.startswith("SET_RESOLUTION:") if Command else False:
        try:
            splitedArg = Command.split(':')
            print("Taiyou.ReceiveComamnd : Set Resoltion to: W;" + str(splitedArg[1]) + " H;" + str(splitedArg[2]))
            CurrentRes_W = int(splitedArg[1])
            CurrentRes_H = int(splitedArg[2])
            if ResiziableWindow:
                DISPLAY = pygame.display.set_mode((CurrentRes_W, CurrentRes_H), pygame.RESIZABLE)
            if not ResiziableWindow:
                DISPLAY = pygame.display.set_mode((CurrentRes_W, CurrentRes_H))

        except:
            print("Taiyou.ReceiveComamnd_Error : Invalid Argument, [" + Command + "]")

    if Command.startswith("RESIZIABLE_WINDOW:") if Command else False:
        try:
            splitedArg = Command.split(':')

            if splitedArg[1] == "True":
                DISPLAY = pygame.display.set_mode((CurrentRes_W,CurrentRes_H), pygame.RESIZABLE)
                ResiziableWindow = True
                print("Taiyou.ReceiveComamnd : Set RESIZIABLE_WINDOW to: True")

            if splitedArg[1] == "False":
                DISPLAY = pygame.display.set_mode((CurrentRes_W,CurrentRes_H))
                ResiziableWindow = False
                print("Taiyou.ReceiveComamnd : Set RESIZIABLE_WINDOW to: False")



        except Exception as ex:
            print("Taiyou.ReceiveComamnd_Error : Error, [" + str(ex) + "]")


def main():
    # Global Variables
    global ToggleGameStart
    global GameStarted
    global GameDrawAllowed
    global IsGameRunning
    global FPS
    global DISPLAY
    global ResiziableWindow

    print("Taiyou.Initialize : Initialize Pygame.Sound")
    pygame.init()
    pygame.mixer.quit()
    pygame.mixer.init(44100, -16, 2, 128)

    print("Taiyou.Initialize : Initialize Pygame")
    pygame.init()

    print("Taiyou.Initialize : Initialize Pygame.Font")
    pygame.font.init()

    CurrentGameFolder = open("currentGame", "r")
    CurrentGameFolder = CurrentGameFolder.read().rstrip()
    print("Taiyou.Initialize : GameFolder name is " + CurrentGameFolder)

    # -- Set Variables -- #
    DISPLAY = pygame.display.set_mode((800, 600))
    MainGameModuleName = CurrentGameFolder.replace("/", ".") + ".MAIN"

    print("Taiyou.Initialize : Set Game Object...")
    UserGameObject = importlib.import_module(MainGameModuleName)

    print("Taiyou.Initialize : Open Game Folder...")
    tge.OpenGameFolder(CurrentGameFolder)  # -- Load Game Assets -- #

    print("Taiyou.Initialize : Load registry keys...")
    reg.Initialize(tge.Get_GameSourceFolder() + "/REG")

    print("Taiyou.Initialize : Call Game Initialize")
    UserGameObject.Initialize(DISPLAY)  # -- Call the Game Initialize Function --

    print("Taiyou.Initialize : Initialization complete, Starting game loop...")
    while True:
        if FPS > 0:
            clock.tick(FPS)

        UpdateProcess = threading.Thread(target=UserGameObject.Update)
        UpdateProcess.daemon = True
        UpdateProcess.run()

        DrawProcess = threading.Thread(target=UserGameObject.GameDraw(DISPLAY))
        DrawProcess.daemon = True
        DrawProcess.run()


        # -- Receive command from the Current Game --
        ReceiveCommand(UserGameObject.ReadCurrentMessages())

        for event in pygame.event.get():
            pygame.event.pump()
            # -- Closes the Game when clicking on the X button
            if event.type == pygame.QUIT:
                reg.Unload()
                sprite.Unload()
                pygame.quit()
                sys.exit()

            # -- Window Resize Event -- #
            if ResiziableWindow:
                if event.type == pygame.VIDEORESIZE:
                    # Resize the Window
                    if ResiziableWindow:
                        DISPLAY = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    else:
                        DISPLAY = pygame.display.set_mode((event.w, event.h))

            # -- Update Game Pygame Events -- #
            EventUpdateProcess = threading.Thread(target=UserGameObject.EventUpdate(event))
            EventUpdateProcess.daemon = True
            EventUpdateProcess.run()


main()
