#! /usr/bin/python3.7
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
from ENGINE import UTILS as utils
from ENGINE import TaiyouUI as SystemUI
import pygame, sys, importlib
import traceback, threading
from datetime import datetime

# The main Entry Point
print("TaiyouGameEngineMainScript version " + tge.Get_GameObjVersion())

class GameInstance:
    def __init__(self):
        print("TaiyouGameObject version " + tge.Get_GameObjVersion())
        self.GameUpdateEnabled = False
        self.ResiziableWindow = False
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.DISPLAY = pygame.display
        self.IsFullscreen = False
        self.IsMenuMode = True
        self.CurrentRes_W = 800
        self.CurrentRes_H = 600
        self.WindowTitle = "Taiyou Game Engine v" + utils.FormatNumber(tge.TaiyouGeneralVersion)
        self.OverlayLevel = -1
        self.UpdateTime_Calculated = 0
        self.UpdateTime_MaxMS = 0
        self.UpdateTime_MaxDelta = 0
        self.GameObject = None
        self.LastFPSValue = 60

        # -- Load Engine Options -- #
        tge.InitEngine()

        # -- Initialize Pygame and Sound System -- #
        if tge.Get_IsSoundEnabled():
            print("Taiyou.GameObject.Initialize : Initializing Pygame and Sound...")

            # -- Set some Variables -- #
            Frequency = int(tge.AudioFrequency)
            Size = int(tge.AudioSize)
            Channels = int(tge.AudioChannels)
            BufferSize = int(tge.AudioBufferSize)

            # -- WORKAROUND: for removing audio delay -- #
            pygame.mixer.pre_init(Frequency, Size, Channels, BufferSize)
            pygame.init()
            pygame.mixer.quit()
            pygame.mixer.init(Frequency, Size, Channels, BufferSize)
        else:
            print("Taiyou.GameObject.Initialize : Initializing Pygame")
            pygame.init()

        if not pygame.mixer.get_init() and tge.Get_IsSoundEnabled():
            print("Taiyou.GameObject.Initialize : Sound System was unable to start.\nNo Sound will be played.")
            sound.DisableSoundSystem = True

        # -- Initialize FastEvent -- #
        print("Taiyou.GameObject.Initialize : Initializing FastEvent")
        pygame.fastevent.init()

        if not pygame.fastevent.get_init() and tge.Get_IsSoundEnabled():
            print("Taiyou.GameObject.Initialize : Cannot initialize FastEvent.\nUsing default events instead.")
            sound.DisableSoundSystem = True



        # -- Set Variables -- #
        print("Taiyou.GameObject.Initialize : Set Variables")
        if not tge.RunInFullScreen:
            self.DISPLAY = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.HWACCEL)
        else:
            self.DISPLAY = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.FULLSCREEN)

        # -- Set Invisible Cursor -- #
        pygame.mouse.set_visible(False)
        # -- Set Window Title -- #
        pygame.display.set_caption(self.WindowTitle)

        print("Taiyou.GameObject.Initialize : Loading TaiyouUI Assets")
        sprite.LoadSpritesInFolder("Taiyou/SYSTEM/SOURCE")
        sound.LoadAllSounds("Taiyou/SYSTEM/SOURCE")
        reg.Initialize("Taiyou/SYSTEM/SOURCE/REG")
        SystemUI.Initialize()

        print("Taiyou.GameObject.Initialize : Initialization complete.")

    def ReceiveCommand(self, Command):
        CommandWasValid = False
        IsSpecialEvent = False

        try:
            if Command.startswith("SET_FPS") if Command else False:
                CommandWasValid = True
                IsSpecialEvent = True

                splitedArg = Command.split(':')
                self.FPS = int(splitedArg[1])

                if not self.IsMenuMode:
                    self.LastFPSValue = self.FPS

                print("Taiyou.GameObject.ReceiveCommand : MaxFPS Set to:" + str(self.FPS))

            if Command.startswith("SET_RESOLUTION") if Command else False:
                CommandWasValid = True
                IsSpecialEvent = True

                splitedArg = Command.split(':')
                print("Taiyou.GameObject.ReceiveCommand : Set Resoltion to: {0}x{1}".format(str(splitedArg[1]), str(splitedArg[2])))

                self.CurrentRes_W = int(splitedArg[1])
                self.CurrentRes_H = int(splitedArg[2])
                if self.ResiziableWindow and not tge.RunInFullScreen:
                    self.DISPLAY = pygame.display.set_mode((self.CurrentRes_W, self.CurrentRes_H), pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.HWACCEL)

                if self.ResiziableWindow and tge.RunInFullScreen:
                    self.ResiziableWindow = False
                    self.DISPLAY = pygame.display.set_mode((self.CurrentRes_W, self.CurrentRes_H), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.FULLSCREEN)

                if not self.ResiziableWindow:
                    if not tge.RunInFullScreen:
                        self.DISPLAY = pygame.display.set_mode((self.CurrentRes_W, self.CurrentRes_H), pygame.DOUBLEBUF | pygame.HWACCEL)
                    else:
                        self.DISPLAY = pygame.display.set_mode((self.CurrentRes_W, self.CurrentRes_H), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.FULLSCREEN)

            if Command.startswith("RESIZIABLE_WINDOW") if Command else False:
                CommandWasValid = True
                IsSpecialEvent = True

                splitedArg = Command.split(':')

                if splitedArg[1] == "True":
                    if tge.RunInFullScreen:
                        return

                    self.DISPLAY = pygame.display.set_mode((self.CurrentRes_W, self.CurrentRes_H), pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.HWACCEL)

                    self.ResiziableWindow = True
                    print("Taiyou.GameObject.ReceiveCommand : Set RESIZIABLE_WINDOW to: True")

                if splitedArg[1] == "False":
                    if not tge.RunInFullScreen:
                        self.DISPLAY = pygame.display.set_mode((self.CurrentRes_W, self.CurrentRes_H), pygame.DOUBLEBUF | pygame.HWACCEL)
                    else:
                        self.DISPLAY = pygame.display.set_mode((self.CurrentRes_W, self.CurrentRes_H), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.FULLSCREEN)

                    self.ResiziableWindow = False
                    print("Taiyou.GameObject.ReceiveCommand : Set RESIZIABLE_WINDOW to: False")

                if splitedArg[1] == "FalseIfTrue":
                    if not tge.RunInFullScreen:
                        self.DISPLAY = pygame.display.set_mode((self.CurrentRes_W, self.CurrentRes_H), pygame.DOUBLEBUF | pygame.HWACCEL)
                    else:
                        self.DISPLAY = pygame.display.set_mode((self.CurrentRes_W, self.CurrentRes_H), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.FULLSCREEN)

                    self.ResiziableWindow = False
                    print("Taiyou.GameObject.ReceiveCommand : Set RESIZIABLE_WINDOW to: False")

            if Command.startswith("KILL") if Command else False:
                CommandWasValid = True
                IsSpecialEvent = True

                print("Taiyou.GameObject.ReceiveCommand : Killing Game Process")

                self.Destroy()

            if Command.startswith("OVERLAY_LEVEL") if Command else False:
                CommandWasValid = True
                IsSpecialEvent = True

                splitedArg = Command.split(':')

                self.OverlayLevel = int(splitedArg[1])

                print("Taiyou.GameObject.ReceiveCommand : Set OVERLAY_LEVEL to " + splitedArg[1])

            if Command.startswith("SET_GAME_MODE") if Command else False:
                CommandWasValid = True
                IsSpecialEvent = True

                print("Taiyou.GameObject.ReceiveCommand : Set Game Mode")

                self.IsMenuMode = False

                # -- Set the Last FPS Value set by the Game -- #
                self.FPS = self.LastFPSValue

                sound.UnpauseGameChannel()
                print("Taiyou.GameObject.ReceiveCommand.SetGameMode : All Sounds on Game Channel has been unpaused.")

            if Command.startswith("OPEN_GAME") if Command else False:
                CommandWasValid = True
                IsSpecialEvent = True

                print("Taiyou.GameObject.ReceiveCommand : Open Game")
                splitedArg = Command.split(':')

                self.SetGameObject(splitedArg[1].rstrip())

            if Command.startswith("REMOVE_GAME") if Command else False:
                CommandWasValid = True
                IsSpecialEvent = True

                print("Taiyou.GameObject.ReceiveCommand : Remove Game Object, and unload all data related to it")

                self.RemoveGame()

            if Command.startswith("SET_TITLE") if Command else False:
                CommandWasValid = True
                splitedArg = Command.split(';')

                pygame.display.set_caption(splitedArg[1])

            if not CommandWasValid:
                tge.devel.PrintToTerminalBuffer("TaiyouMessage: Invalid Command:\n'" + Command + "'")
            elif IsSpecialEvent:
                tge.devel.PrintToTerminalBuffer("TaiyouMessage: Command Processed:\n'" + Command + "'")

        except IndexError as ex:
            tge.devel.PrintToTerminalBuffer("TaiyouMessage EXCEPTION\nThe last command does not have the necessary number of arguments.")

    def RenderOverlay(self):
        # -- Render FPS/Frametime Delay -- #
        if self.OverlayLevel == 0:
            text = "FPS Set:{0} Current:{1}; Tick Max:{2} Current{3}".format(str(self.FPS), utils.FormatNumber(self.clock.get_fps(), 3), utils.FormatNumber(self.UpdateTime_MaxMS, 2, ["ms", "sec", "min", "h", "INSANE"]), utils.FormatNumber(self.clock.get_time(), 2, ["ms", "sec", "min", "h", "INSANE"]))

            sprite.FontRender(self.DISPLAY, "/PressStart2P.ttf", 9, text, (255, 255, 255), 15, 15, False, (20, 30, 23), Opacity=200)

        if self.OverlayLevel == 1:
            SystemUI.screenshotUI.Run(self.DISPLAY)
            if len(SystemUI.screenshotUI.Messages) >= 1:
                self.ReceiveCommand(SystemUI.screenshotUI.ReadCurrentMessages())

    def RemoveGame(self, UnloadGameAssts=True, CloseGameFolder=True):
        print("Taiyou.GameObject.RemoveGame : Suspend Game Code")

        # -- Call the Game Unload Function on Game -- #
        try:
            self.GameObject.Unload()
        except AttributeError:
            print("Taiyou.GameObject.RemoveGame : Game has no Unload Function.")

        # -- Try to delete the Game Object -- #
        importlib.reload(self.GameObject)
        self.GameObject = None

        if UnloadGameAssts:
            print("Taiyou.GameObject.RemoveGame : Unload Game Assets")

            sprite.Unload()
            sound.Unload()
            reg.Unload()

        if CloseGameFolder:
            print("Taiyou.GameObject.RemoveGame : Close Game Folder")

            tge.CloseGameFolder()

        self.IsMenuMode = True

        print("Taiyou.GameObject.RemoveGame : Operation Complete.")

    def SetGameObject(self, GameFolder):
        try:
            print("Taiyou.GameObject.SetGameObject : Open Game [" + GameFolder + "]")
            print("Taiyou.GameObject.SetGameObject : MainModuleName is: [" + tge.Get_MainGameModuleName(GameFolder) + "]")

            self.GameObject = importlib.import_module(tge.Get_MainGameModuleName(GameFolder))

            if tge.Get_MainGameModuleName(tge.Get_GameFolder()) in sys.modules:  # -- If the module is not loaded
                print("Taiyou.GameObject.GameStart : Game Code was not loaded yet.\nCalling Initialize")

                self.GameObject.Initialize(self.DISPLAY)  # -- Call the Game Initialize Function --

            else:
                print("Taiyou.GameObject.GameStart : Game Code was already loaded.")

        except Exception as ex:
            self.SystemException(ex, "SetGameObject")

    def SystemException(self, ex, ErrorPart="Unknown"):
        raise ex

    def EventUpdate(self):
        # -- Internaly Process Pygame Events -- #
        pygame.fastevent.pump()

        for event in pygame.fastevent.get():
            # -- Closes the Game when clicking on the X button
            if event.type == pygame.QUIT:
                self.Destroy()

            # -- Menu Key -- #
            if event.type == pygame.KEYUP and event.key == pygame.K_F12:
                if not self.IsMenuMode:
                    self.IsMenuMode = True
                    self.GameUpdateEnabled = False
                    SystemUI.gameOverlay.CopyOfTheScreen = self.DISPLAY.copy()
                    sound.PauseGameChannel()
                    print("Taiyou.GameObject.ReceiveCommand.SetGameMode : All Sounds on Game Channel has been paused.")
                    self.FPS = 60  # -- Default TaiyouUI FPS

                if not SystemUI.SystemMenuEnabled and SystemUI.CurrentMenuScreen == 0:
                    SystemUI.SystemMenuEnabled = True
                    SystemUI.gameOverlay.UIOpacityAnimEnabled = True
                    SystemUI.gameOverlay.UIOpacityScreenCopyied = False

            # -- Screenshot Key -- #
            if event.type == pygame.KEYUP and event.key == pygame.K_F11:
                self.OverlayLevel = 1

            # -- FPS Overlay Key -- #
            if event.type == pygame.KEYUP and event.key == pygame.K_F10:
                if self.OverlayLevel == 0:
                    self.OverlayLevel = -1
                else:
                    self.OverlayLevel = 0
                sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Click"), 0.5, PlayOnSystemChannel=True)


            # -- Resize Window Event -- #
            if self.ResiziableWindow and not tge.RunInFullScreen:
                if event.type == pygame.VIDEORESIZE:
                    # Resize the Window
                    self.DISPLAY = pygame.display.set_mode((event.w, event.h), pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.HWACCEL)

            # -- Do Game Events -- #
            try:
                if not self.IsMenuMode:
                    self.GameObject.EventUpdate(event)

            except Exception as ex:  # -- Exception Handler
                self.GameException(ex, "Game Events")

            # -- Do SystemMenu Events -- #
            if self.IsMenuMode:
                SystemUI.EventUpdate(event)

    def CalculateDelta(self):
        self.UpdateTime_MaxDelta += 1
        # -- Set Time -- #
        self.UpdateTime_Calculated = self.clock.get_time()

        if self.UpdateTime_MaxDelta > 50:
            if self.UpdateTime_Calculated > self.UpdateTime_MaxMS:
                self.UpdateTime_MaxMS = self.UpdateTime_Calculated

            self.UpdateTime_MaxDelta = 0

    def GameException(self, Exception, ErrorPart="Unknown"):
        if not reg.ReadKey_bool("/TaiyouSystem/CONF/exception_handler"):
            raise Exception
        else:
            ExceptionText = "\n\nGame Exception! in [" + ErrorPart + "]:\n\n" + str(Exception) + "\n\n"

            tge.devel.PrintToTerminalBuffer(ExceptionText)
            self.GameUpdateEnabled = False
            self.IsMenuMode = True
            SystemUI.SystemMenuEnabled = True
            if not SystemUI.gameOverlay.OpenedInGameError:
                SystemUI.gameOverlay.UIOpacityAnimEnabled = True
                SystemUI.gameOverlay.OpenedInGameError = True
                SystemUI.gameOverlay.CopyOfTheScreen = self.DISPLAY.copy()

            print(ExceptionText)

    def Run(self):
        # -- Run the Clock -- #
        self.clock.tick(self.FPS)

        # -- If MenuMode, update the Menu -- #
        if self.IsMenuMode:
            SystemUI.Update()
            SystemUI.Draw(self.DISPLAY)

            # -- Draw the Overlay, when it enabled -- #
            if not self.OverlayLevel == -1:
                self.RenderOverlay()

            # -- Flip the Screen -- #
            pygame.display.flip()

            # -- Receive Commands from System Menu -- #
            if len(SystemUI.Messages) >= 1:
                self.ReceiveCommand(SystemUI.ReadCurrentMessages())

        else:  # -- Else, Update the Game -- #
            try:
                # -- Do Game Update -- #
                self.GameObject.Update()

                # -- Do Game Draw -- #
                self.GameObject.GameDraw(self.DISPLAY)

                # -- Draw the Overlay, when its enabled -- #
                self.RenderOverlay()

                # -- Flip the Screen -- #
                pygame.display.flip()

                # -- Receive command from the Current Game -- #
                if len(self.GameObject.Messages) >= 1:
                    self.ReceiveCommand(self.GameObject.ReadCurrentMessages())

            except Exception as ex:
                self.GameException(ex, "Game Update/Draw")

        # -- Update Events -- #
        self.EventUpdate()

        # -- Calculate the MaxMS -- #
        if self.OverlayLevel >= 0:
            self.CalculateDelta()

    def Destroy(self):
        print("Taiyou.GameObject.Destroy : Closing [" + tge.Get_GameTitle() + "]...")
        # -- Unload Things -- #
        reg.Unload()
        sprite.Unload()
        sound.Unload()
        pygame.mixer.quit()
        pygame.quit()
        print("Taiyou.GameObject.Destroy : Game [" + tge.Get_GameTitle() + "] has been closed.")
        sys.exit()


# -- Create Game Instance -- #
Instance = GameInstance()

while True:
    Instance.Run()
