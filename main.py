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

# -- Set Console Color -- #
print("\033[95m")

# Import some stuff
import os
import ENGINE as tge
from ENGINE import REGISTRY as reg
from ENGINE import SPRITE as sprite
from ENGINE import SOUND as sound
from ENGINE import UTILS as utils
from ENGINE import TaiyouUI as SystemUI
import pygame, sys, importlib
import threading

# The main Entry Point
print("TaiyouGameEngineMainScript version " + tge.Get_GameObjVersion())

class GameInstance:
    def __init__(self, CurrentGameFolder):
        print("TaiyouGameObject version " + tge.Get_GameObjVersion())
        self.GameUpdateEnabled = True
        self.ResiziableWindow = False
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.ToggleGameStart = False
        self.GameStarted = False
        self.DISPLAY = pygame.display
        self.IsFullscreen = False
        self.GameReloadCalled = False
        self.CurrentRes_W = 800
        self.CurrentRes_H = 600
        self.WindowTitle = "Taiyou Game Engine"
        self.OverlayLevel = -1
        # -- Initialize Pygame -- #
        pygame.init()

        # -- Initialize Sound System -- #
        if tge.Get_IsSoundEnabled():
            print("Taiyou.GameObject.InitializePygame : Initialize Sound System")

            pygame.mixer.quit()
            pygame.mixer.init(44100, -16, 2, 128)
        else:
            print("Taiyou.GameObject.InitializePygame : Sound System is disabled.")

        if tge.Get_IsFontRenderingEnabled():
            print("Taiyou.GameObject.InitializePygame : Initialize Font")
            pygame.font.init()
        else:
            print("Taiyou.GameObject.InitializePygame : Font Rendering is disabled.")

        # -- Set Variables -- #
        print("Taiyou.GameObject.Initialize : Set Variables")
        self.DISPLAY = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF)
        MainGameModuleName = CurrentGameFolder.replace("/", ".") + ".MAIN"
        pygame.mouse.set_visible(False)
        pygame.display.set_caption("Taiyou Game Engine v" + utils.FormatNumber(tge.TaiyouGeneralVersion))

        print("Taiyou.GameObject.Initialize : Set Game Object")
        self.GameObject = importlib.import_module(MainGameModuleName)

        print("Taiyou.GameObject.Initialize : Open Game Folder")
        tge.OpenGameFolder(CurrentGameFolder)  # -- Load Game Assets -- #

        print("Taiyou.GameObject.Initialize : Load registry keys")
        reg.Initialize(tge.Get_GameSourceFolder() + "/REG")

        print("Taiyou.GameObject.Initialize : Loading Default Assets")
        sprite.LoadSpritesInFolder("Taiyou/HOME/SOURCE")

        print("Taiyou.GameObject.Initialize : Initialize SystemUI")
        SystemUI.Initialize()

        print("Taiyou.GameObject.Initialize : Initialization complete.")

    def ReceiveCommand(self, Command):
        if Command.startswith("SET_FPS:") if Command else False:
            try:
                splitedArg = Command.split(':')
                self.FPS = int(splitedArg[1])
                print("Taiyou.GameObject.ReceiveCommand : MaxFPS Set to:" + str(self.FPS))

            except:
                print("Taiyou.GameObject.ReceiveCommand : Invalid Argument, [" + Command + "]")

        if Command.startswith("SET_RESOLUTION:") if Command else False:
            try:
                splitedArg = Command.split(':')
                print("Taiyou.GameObject.ReceiveCommand : Set Resoltion to: W;" + str(splitedArg[1]) + " H;" + str(splitedArg[2]))
                self.CurrentRes_W = int(splitedArg[1])
                self.CurrentRes_H = int(splitedArg[2])
                if self.ResiziableWindow:
                    self.DISPLAY = pygame.display.set_mode((self.CurrentRes_W, self.CurrentRes_H), pygame.DOUBLEBUF | pygame.RESIZABLE)
                if not self.ResiziableWindow:
                    self.DISPLAY = pygame.display.set_mode((self.CurrentRes_W, self.CurrentRes_H), pygame.DOUBLEBUF)

            except:
                print("Taiyou.GameObject.ReceiveCommand : Invalid Argument, [" + Command + "]")

        if Command.startswith("RESIZIABLE_WINDOW:") if Command else False:
            try:
                splitedArg = Command.split(':')

                if splitedArg[1] == "True":
                    self.DISPLAY = pygame.display.set_mode((self.CurrentRes_W, self.CurrentRes_H), pygame.DOUBLEBUF | pygame.RESIZABLE)
                    self.ResiziableWindow = True
                    print("Taiyou.GameObject.ReceiveCommand : Set RESIZIABLE_WINDOW to: True")

                if splitedArg[1] == "False":
                    self.DISPLAY = pygame.display.set_mode((self.CurrentRes_W, self.CurrentRes_H), pygame.DOUBLEBUF)
                    self.ResiziableWindow = False
                    print("Taiyou.GameObject.ReceiveCommand : Set RESIZIABLE_WINDOW to: False")

            except Exception as ex:
                print("Taiyou.GameObject.ReceiveCommand_Error : Error, [" + str(ex) + "]")

        if Command.startswith("GAME_UPDATE:") if Command else False:
            try:
                splitedArg = Command.split(':')

                if splitedArg[1] == "True":
                    self.GameUpdateEnabled = True
                    print("Taiyou.GameObject.ReceiveCommand : Set GAME_UPDATE to: True")

                if splitedArg[1] == "False":
                    self.GameUpdateEnabled = False
                    print("Taiyou.GameObject.ReceiveCommand : Set GAME_UPDATE to: False")

            except Exception as ex:
                print("Taiyou.GameObject.ReceiveCommand_Error : Error, [" + str(ex) + "]")

        if Command.startswith("KILL") if Command else False:
            try:
                print("Taiyou.GameObject.ReceiveCommand : Killing Game Process")

                self.destroy()
            except Exception as ex:
                print("Taiyou.GameObject.ReceiveCommand_Error : Error, [" + str(ex) + "]")

        if Command.startswith("OVERLAY_LEVEL:") if Command else False:
            try:
                splitedArg = Command.split(':')
                self.OverlayLevel = int(splitedArg[1])

                print("Taiyou.GameObject.ReceiveCommand : Set OVERLAY_LEVEL to " + splitedArg[1])

            except Exception as ex:
                print("Taiyou.GameObject.ReceiveCommand_Error : Error, [" + str(ex) + "]")

        if Command.startswith("TOGGLE_GAME_START") if Command else False:
            try:
                print("Taiyou.GameObject.ReceiveCommand : Toggle Game Start")

                self.ToggleGameStart = True
            except Exception as ex:
                print("Taiyou.GameObject.ReceiveCommand_Error : Error, [" + str(ex) + "]")

        if Command.startswith("RELOAD_GAME") if Command else False:
            try:
                print("Taiyou.GameObject.ReceiveCommand : Reload Game")

                self.GameReloadCalled = True
            except Exception as ex:
                print("Taiyou.GameObject.ReceiveCommand_Error : Error, [" + str(ex) + "]")

    def render_overlay(self):
        if self.OverlayLevel == 0:
            sprite.RenderFont(self.DISPLAY, "/PressStart2P.ttf", 12, "FPS {0}/{1}".format(str(self.FPS), utils.FormatNumber(self.clock.get_fps(), 3)), (10,10,10), 17,17, False)
            sprite.RenderFont(self.DISPLAY, "/PressStart2P.ttf", 12, "FPS {0}/{1}".format(str(self.FPS), utils.FormatNumber(self.clock.get_fps(), 3)), (240,240,240), 15,15, False)

    def run(self):
        if self.FPS > 0:
            self.clock.tick(self.FPS)

        # -- Toggle Game Start -- #
        if self.ToggleGameStart:
            self.ToggleGameStart = False
            self.GameObject.Initialize(self.DISPLAY)  # -- Call the Game Initialize Function --
            print("Taiyou.GameObject.Run : Initialized Called")
            self.GameStarted = True

        # -- Reload Game Object -- #
        if self.GameReloadCalled:
            importlib.reload(self.GameObject)
            print("Taiyou.GameObject.Run : Reload Game Object")

        # -- Do Game Update -- #
        if self.GameUpdateEnabled and self.GameStarted:
            self.GameObject.Update()
        SystemUI.Update()

        # -- Do Game Draw -- #
        if self.GameUpdateEnabled and self.GameStarted:
            self.GameObject.GameDraw(self.DISPLAY)
        SystemUI.Draw(self.DISPLAY)

        if not self.OverlayLevel == -1:
            self.render_overlay()

        pygame.display.flip()

        # -- Receive command from the Current Game --
        if self.GameUpdateEnabled and self.GameStarted:
            if len(self.GameObject.Messages) >= 1:
                self.ReceiveCommand(self.GameObject.ReadCurrentMessages())
        # -- Only Receive Command when it is Enabled -- #
        if len(SystemUI.Messages) >= 1:
            self.ReceiveCommand(SystemUI.ReadCurrentMessages())

        for event in pygame.event.get():
            # -- Closes the Game when clicking on the X button
            if event.type == pygame.QUIT:
                self.destroy()

            if event.type == pygame.KEYUP and event.key == pygame.K_F12:
                if not SystemUI.SystemMenuEnabled:
                    SystemUI.SystemMenuEnabled = True
                    SystemUI.UIOpacityAnimEnabled = True

            # -- Resize Window Event -- #
            if self.ResiziableWindow:
                if event.type == pygame.VIDEORESIZE:
                    # Resize the Window
                    self.DISPLAY = pygame.display.set_mode((event.w, event.h), pygame.DOUBLEBUF | pygame.RESIZABLE)

            # -- Do Game Events -- #
            if self.GameUpdateEnabled and self.GameStarted:
                self.GameObject.EventUpdate(event)
            SystemUI.EventUpdate(event)
            pygame.event.pump()

    def destroy(self):
        print("Taiyou.GameObject.Destroy : Closing [" + tge.Get_GameTitle() + "]...")
        # -- Unload Things -- #
        reg.Unload()
        sprite.Unload()
        sound.Unload()
        pygame.quit()
        print("Taiyou.GameObject.Destroy : Destroy Game Object")
        self.GameObject = 42
        # -- Remove Temporary Files -- #
        os.remove(".AppDataPath")
        os.remove(".OpenedGameInfos")
        print("Taiyou.GameObject.Destroy : Game [" + tge.Get_GameTitle() + "] has been closed.")
        sys.exit()


# -- Create Game Instance -- #
GameFolderName = open("currentGame", "r")
GameFolderName = GameFolderName.read().rstrip()
if os.path.exists(GameFolderName):
    print("\n\nTaiyou.Initialize : Game Folder does exist, Continuing...")
else:
    print("Taiyou.Initialize : Game Folder does not exist, Exiting...")
    sys.exit()

Instance = GameInstance(GameFolderName)

while True:
    Instance.run()