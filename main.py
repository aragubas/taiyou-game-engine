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

import ENGINE as tge
from ENGINE import REGISTRY as reg
from ENGINE import SPRITE as sprite
from ENGINE import SOUND as sound
import pygame, sys, importlib
import threading

# The main Entry Point
print("TaiyouGameEngineMainScript version 1.4")

class GameInstance:
    def __init__(self, CurrentGameFolder):
        print("TaiyouGameObject version 1.1")
        self.GameUpdateEnabled = True
        self.GameDrawEnabled = True
        self.GameEventEnabled = True
        self.ResiziableWindow = False
        self.clock = pygame.time.Clock()
        self.FPS = 75
        self.ToggleGameStart = True
        self.GameStarted = False
        self.DISPLAY = pygame.display
        self.IsFullscreen = False
        self.CurrentRes_W = 800
        self.CurrentRes_H = 600
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
        self.DISPLAY = pygame.display.set_mode((800, 600), pygame.HWSURFACE | pygame.DOUBLEBUF)
        MainGameModuleName = CurrentGameFolder.replace("/", ".") + ".MAIN"

        print("Taiyou.GameObject.Initialize : Set Game Object")
        self.GameObject = importlib.import_module(MainGameModuleName)

        print("Taiyou.GameObject.Initialize : Open Game Folder")
        tge.OpenGameFolder(CurrentGameFolder)  # -- Load Game Assets -- #

        print("Taiyou.GameObject.Initialize : Load registry keys")
        reg.Initialize(tge.Get_GameSourceFolder() + "/REG")

        print("Taiyou.GameObject.Initialize : Call Initialize Game")
        self.GameObject.Initialize(self.DISPLAY)  # -- Call the Game Initialize Function --

        print("Taiyou.GameObject.Initialize : Initialization complete.")

    def ReceiveCommand(self, Command):
        if Command.startswith("SET_FPS:") if Command else False:
            try:
                splitedArg = Command.split(':')
                self.FPS = int(splitedArg[1])
                print("Taiyou.ReceiveCommand : MaxFPS Set to:" + str(self.FPS))

            except:
                print("Taiyou.ReceiveCommand_Error : Invalid Argument, [" + Command + "]")

        if Command.startswith("SET_RESOLUTION:") if Command else False:
            try:
                splitedArg = Command.split(':')
                print("Taiyou.ReceiveCommand : Set Resoltion to: W;" + str(splitedArg[1]) + " H;" + str(splitedArg[2]))
                self.CurrentRes_W = int(splitedArg[1])
                self.CurrentRes_H = int(splitedArg[2])
                if self.ResiziableWindow:
                    self.DISPLAY = pygame.display.set_mode((self.CurrentRes_W, self.CurrentRes_H),
                                                      pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
                if not self.ResiziableWindow:
                    self.DISPLAY = pygame.display.set_mode((self.CurrentRes_W, self.CurrentRes_H), pygame.HWSURFACE | pygame.DOUBLEBUF)

            except:
                print("Taiyou.ReceiveCommand_Error : Invalid Argument, [" + Command + "]")

        if Command.startswith("RESIZIABLE_WINDOW:") if Command else False:
            try:
                splitedArg = Command.split(':')

                if splitedArg[1] == "True":
                    self.DISPLAY = pygame.display.set_mode((self.CurrentRes_W, self.CurrentRes_H),
                                                      pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
                    self.ResiziableWindow = True
                    print("Taiyou.ReceiveCommand : Set RESIZIABLE_WINDOW to: True")

                if splitedArg[1] == "False":
                    self.DISPLAY = pygame.display.set_mode((self.CurrentRes_W, self.CurrentRes_H), pygame.HWSURFACE | pygame.DOUBLEBUF)
                    self.ResiziableWindow = False
                    print("Taiyou.ReceiveCommand_Error : Set RESIZIABLE_WINDOW to: False")



            except Exception as ex:
                print("Taiyou.ReceiveCommand_Error : Error, [" + str(ex) + "]")

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def taiyou_dc(self):
        self.clear_console()
        InputLoopEnabled = True

        while InputLoopEnabled:
            CurrentInput = input("$: ")
            print("\033[95m")
            SplitedComma = CurrentInput.split(' ')

            if SplitedComma[0] == "help" or SplitedComma[0] == "hlp":
                self.clear_console()
                print("Taiyou DC [Developer Console] version 1.0")
                print("RuntimeVersion: " + tge.Get_Version())
                print("Template: [Command][ShortName] [ARGUMENTS] - [Description]")
                print("\n\n")
                print("help{hlp} - This list of commands")
                print("setFlag{sfl} [FLAG_NAME] [VALUE] - Set flag value")
                print("destroy{des} - Kill the current game")
                print("reload{rel} [REGISTRY,SPRITE/FONT,SOUND] - Reload")
                print("clear{cls} - Clear the Screen")
                print("getFlags{gfl} - Get all changeable flags.")
                print("continue{cnt} - Continue game execution")
                print("versions{ver} - Print all Taiyou Game Engine components versions")
                print("gameData{gmd} - Print loaded game data")

            try:
                # -- Destroy Command -- #
                if SplitedComma[0] == "destroy" or SplitedComma[0] == "des":
                    self.destroy()

                # -- Reload Command -- #
                if SplitedComma[0] == "reload" or SplitedComma[0] == "rel":
                    print("Reload")

                    if SplitedComma[1] == "REGISTRY":
                        print("Reloading Registry...")
                        reg.Reload()
                        print("Done!")
                    elif SplitedComma[1] == "SPRITE":
                        print("Reloading Sprites...")
                        sprite.Reload()
                        print("Done!")

                    elif SplitedComma[1] == "SOUND":
                        print("Reloading Sound...")
                        sound.Reload()
                        print("Done!")

                    else:
                        raise TypeError("[" + SplitedComma[1] + "] is not a valid argument.")

                # -- Get Flag Command -- #
                if SplitedComma[0] == "getFlags" or SplitedComma[0] == "gfl":
                    VarsList = "GAME_DRAW[BOOL], GAME_UPDATE[BOOL], GAME_EVENTS[BOOL], FPS[INT]"
                    print("GetVars\n" + VarsList)

                # -- Set Flag Command -- #
                if SplitedComma[0] == "setFlag" or SplitedComma[0] == "sfl":
                    print("SetFlag\n")

                    FlagName = SplitedComma[1]
                    FlagValue = SplitedComma[2]

                    # -- Set FPS Flag -- #
                    if FlagName == "FPS":
                        self.FPS = int(FlagValue)

                    # -- Set Game Draw Flag -- #
                    if FlagName == "GAME_DRAW":
                        Value = False
                        if FlagValue == "True":
                            Value = True
                            FlagValue = "TRUE"
                        elif FlagValue == "False":
                            Value = False
                            FlagValue = "FALSE"
                        else:
                            raise TypeError("[" + FlagValue + "] is not a valid BOOLEAN")
                        self.GameDrawEnabled = Value


                    # -- Set Game Events Flag -- #
                    if FlagName == "GAME_EVENTS":
                        Value = False
                        if FlagValue == "True":
                            Value = True
                            FlagValue = "TRUE"
                        elif FlagValue == "False":
                            Value = False
                            FlagValue = "FALSE"
                        else:
                            raise TypeError("[" + FlagValue + "] is not a valid BOOLEAN")
                        self.GameEventEnabled = Value

                    # -- Set Game Update Flag -- #
                    if FlagName == "GAME_UPDATE":
                        Value = False
                        if FlagValue == "True":
                            Value = True
                            FlagValue = "TRUE"
                        elif FlagValue == "False":
                            Value = False
                            FlagValue = "FALSE"
                        else:
                            raise TypeError("[" + FlagValue + "] is not a valid BOOLEAN")
                        self.GameUpdateEnabled = Value

                    # -- Print Flag Assingment -- #
                    print("Flag [{0}] was set to [{1}]".format(str(FlagName), str(FlagValue)))

                # -- Continue Command -- #
                if SplitedComma[0] == "continue" or SplitedComma[0] == "cnt":
                    print("Continue game execution...")
                    InputLoopEnabled = False

                # -- Clear Command -- #
                if SplitedComma[0] == "clear" or SplitedComma[0] == "cls":
                    self.clear_console()

                # -- Clear Command -- #
                if SplitedComma[0] == "versions" or SplitedComma[0] == "ver":
                    print("Taiyou Developer Console [DC] Version 1.0")
                    print("Taiyou Runtime Version " + tge.Get_Version())
                    print("Taiyou Sprite/Font Version " + tge.Get_SpriteVersion())
                    print("Taiyou Sound System Version " + tge.Get_SoundVersion())
                    print("Taiyou Sound System Version " + tge.Get_SoundVersion())

            except IndexError:
                print("\033[91mARGUMENTS ERROR!\nThe command: [{0}] does not have the correct amount of arguments.".format(str(SplitedComma[0])))
            except TypeError as ex:
                print("\033[91mTYPO ERROR!\n" + str(ex) + "\n in [" + SplitedComma[0] + "]")

    def run(self):
        if self.FPS > 0:
            self.clock.tick(self.FPS)

        # -- Do Game Update -- #
        if self.GameUpdateEnabled:
            UpdateProcess = threading.Thread(target=self.GameObject.Update)
            UpdateProcess.daemon = True
            UpdateProcess.run()

        # -- Do Game Draw -- #
        if self.GameDrawEnabled:
            self.GameObject.GameDraw(self.DISPLAY)

        # -- Receive command from the Current Game --
        self.ReceiveCommand(self.GameObject.ReadCurrentMessages())

        for event in pygame.event.get():
            # -- Closes the Game when clicking on the X button
            if event.type == pygame.QUIT:
                self.destroy()

            if event.type == pygame.KEYUP and event.key == pygame.K_F12:
                self.taiyou_dc()

            # -- Resize Window Event -- #
            if self.ResiziableWindow:
                if event.type == pygame.VIDEORESIZE:
                    # Resize the Window
                    self.DISPLAY = pygame.display.set_mode((event.w, event.h), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

            # -- Do Game Events -- #
            if self.GameEventEnabled:
                self.GameObject.EventUpdate(event)

    def destroy(self):
        print("Taiyou.GameObject.Destroy : Closing [" + tge.Get_GameTitle() + "]...")
        # -- Unload Things -- #
        reg.Unload()
        sprite.Unload()
        sound.Unload()
        pygame.quit()
        # -- Remove Temporary Files -- #
        os.remove(".AppDataPath")
        os.remove(".OpenedGameInfos")
        print("Taiyou.GameObject.Destroy : Game [" + tge.Get_GameTitle() + "] has been closed.")
        sys.exit()


# -- Create Game Instance -- #
GameFolderName = open("currentGame", "r")
GameFolderName = GameFolderName.read().rstrip()
if os.path.exists(GameFolderName):
    print("\n\nTaiyou.InitScript : Game Folder does exist, Continuing...")
else:
    print("Taiyou.InitScript : Game Folder does not exist, Exiting...")
    sys.exit()

Instance = GameInstance(GameFolderName)

while True:
    Instance.run()