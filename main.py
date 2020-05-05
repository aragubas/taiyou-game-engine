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
import os

from ENGINE import REGISTRY as reg
from ENGINE import SPRITE as sprite
from ENGINE import SOUND as sound
import ENGINE as tge
import pygame, sys, importlib
import threading

# The main Entry Point
print("TaiyouGameEngineMainScript version 1.3")

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
            print("Taiyou.ReceiveCommand : MaxFPS Set to:" + str(FPS))

        except:
            print("Taiyou.ReceiveCommand_Error : Invalid Argument, [" + Command + "]")

    if Command.startswith("SET_RESOLUTION:") if Command else False:
        try:
            splitedArg = Command.split(':')
            print("Taiyou.ReceiveCommand : Set Resoltion to: W;" + str(splitedArg[1]) + " H;" + str(splitedArg[2]))
            CurrentRes_W = int(splitedArg[1])
            CurrentRes_H = int(splitedArg[2])
            if ResiziableWindow:
                DISPLAY = pygame.display.set_mode((CurrentRes_W, CurrentRes_H), pygame.RESIZABLE)
            if not ResiziableWindow:
                DISPLAY = pygame.display.set_mode((CurrentRes_W, CurrentRes_H))

        except:
            print("Taiyou.ReceiveCommand_Error : Invalid Argument, [" + Command + "]")

    if Command.startswith("RESIZIABLE_WINDOW:") if Command else False:
        try:
            splitedArg = Command.split(':')

            if splitedArg[1] == "True":
                DISPLAY = pygame.display.set_mode((CurrentRes_W,CurrentRes_H), pygame.RESIZABLE)
                ResiziableWindow = True
                print("Taiyou.ReceiveCommand : Set RESIZIABLE_WINDOW to: True")

            if splitedArg[1] == "False":
                DISPLAY = pygame.display.set_mode((CurrentRes_W,CurrentRes_H))
                ResiziableWindow = False
                print("Taiyou.ReceiveCommand_Error : Set RESIZIABLE_WINDOW to: False")



        except Exception as ex:
            print("Taiyou.ReceiveCommand_Error : Error, [" + str(ex) + "]")


class GameInstance:
    def __init__(self, CurrentGameFolder):
        global DISPLAY
        print("Taiyou.Initialize : Initializing Sound System")
        pygame.init()
        pygame.mixer.quit()
        pygame.mixer.init(44100, -16, 2, 128)

        print("Taiyou.Initialize : Initialize Font")
        pygame.font.init()

        print("Taiyou.Initialize : GameFolder name is " + CurrentGameFolder)

        # -- Set Variables -- #
        self.DISPLAY = pygame.display.set_mode((800, 600), pygame.HWSURFACE)
        MainGameModuleName = CurrentGameFolder.replace("/", ".") + ".MAIN"

        print("Taiyou.Initialize : Set Game Object")
        self.GameObject = importlib.import_module(MainGameModuleName)

        print("Taiyou.Initialize : Open Game Folder")
        tge.OpenGameFolder(CurrentGameFolder)  # -- Load Game Assets -- #

        print("Taiyou.Initialize : Load registry keys")
        reg.Initialize(tge.Get_GameSourceFolder() + "/REG")

        print("Taiyou.Initialize : Initialize Game")
        self.GameObject.Initialize(DISPLAY)  # -- Call the Game Initialize Function --

        print("Taiyou.Initialize : Initialization complete.")

    def run(self):
        if FPS > 0:
            clock.tick(FPS)

        UpdateProcess = threading.Thread(target=self.GameObject.Update)
        UpdateProcess.daemon = True
        UpdateProcess.run()

        self.GameObject.GameDraw(self.DISPLAY)

        # -- Receive command from the Current Game --
        ReceiveCommand(self.GameObject.ReadCurrentMessages())

        for event in pygame.event.get():
            # -- Closes the Game when clicking on the X button
            if event.type == pygame.QUIT:
                reg.Unload()
                sprite.Unload()
                sound.Unload()
                pygame.quit()
                sys.exit()

            # -- Resize Window Event -- #
            if ResiziableWindow:
                if event.type == pygame.VIDEORESIZE:
                    # Resize the Window
                    if ResiziableWindow:
                        self.DISPLAY = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            # -- Update Game Pygame Events -- #
            EventUpdateProcess = threading.Thread(target=self.GameObject.EventUpdate(event))
            EventUpdateProcess.daemon = True
            EventUpdateProcess.run()


# -- Create Game Instance -- #
GameFolderName = open("currentGame", "r")
GameFolderName = GameFolderName.read().rstrip()
if os.path.exists(GameFolderName):
    print("Taiyou.InitScript : Game Folder does exist, Continuing...")
else:
    print("Taiyou.InitScript : Game Folder does not exist, Exiting...")
    sys.exit()

Instance = GameInstance(GameFolderName)

while True:
    Instance.run()