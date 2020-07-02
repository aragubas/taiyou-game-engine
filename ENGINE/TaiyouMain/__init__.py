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
from ENGINE.TaiyouUI import OverlayManager as ovelMng
import pygame, sys, importlib
import traceback, threading
from datetime import datetime

# The main Entry Point
print("TaiyouGameEngineMainScript version " + tge.Get_GameObjVersion())

# -- Variables -- #
GameUpdateEnabled = False
ResiziableWindow = False
clock = pygame.time.Clock()
FPS = 60
DISPLAY = pygame.display
IsFullscreen = False
IsMenuMode = True
CurrentRes_W = 800
CurrentRes_H = 600
WindowTitle = "Taiyou Game Engine v" + utils.FormatNumber(tge.TaiyouGeneralVersion)
UpdateTime_Calculated = 0
UpdateTime_MaxMS = 0
UpdateTime_MaxDelta = 0
GameObject = None
LastFPSValue = 60


def __init__():
    global DISPLAY

    print("TaiyouGameObject version " + tge.Get_GameObjVersion())

    # -- Load Engine Options -- #
    tge.InitEngine()

    # -- Initialize Pygame and Sound System -- #
    if tge.Get_IsSoundEnabled():
        print("Taiyou.GameExecution.Initialize : Initializing Pygame and Sound...")

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
        print("Taiyou.GameExecution.Initialize : Initializing Pygame")
        pygame.init()

    if not pygame.mixer.get_init() and tge.Get_IsSoundEnabled():
        print("Taiyou.GameExecution.Initialize : Sound System was unable to start.\nNo Sound will be played.")
        sound.DisableSoundSystem = True

    # -- Initialize FastEvent -- #
    print("Taiyou.GameExecution.Initialize : Initializing FastEvent")
    pygame.fastevent.init()

    # -- Set Variables -- #
    print("Taiyou.GameExecution.Initialize : Set Variables")
    if not tge.RunInFullScreen:
        DISPLAY = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE, tge.BitDepth)
    else:
        DISPLAY = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.FULLSCREEN, tge.BitDepth)

    # -- Set Invisible Cursor -- #
    pygame.mouse.set_visible(False)
    # -- Set Window Title -- #
    pygame.display.set_caption(WindowTitle)

    print("Taiyou.GameExecution.Initialize : Loading TaiyouUI Assets")
    sprite.LoadSpritesInFolder("Taiyou/SYSTEM/SOURCE")
    sound.LoadAllSounds("Taiyou/SYSTEM/SOURCE")
    reg.Initialize("Taiyou/SYSTEM/SOURCE/REG")
    SystemUI.Initialize()

    print("Taiyou.GameExecution.Initialize : Initialization complete.")

def ReceiveCommand(Command):
    global IsMenuMode
    global DISPLAY
    global ResiziableWindow
    global FPS
    global LastFPSValue

    CommandWasValid = False
    IsSpecialEvent = False

    try:
        if Command.startswith("SET_FPS") if Command else False:
            CommandWasValid = True
            IsSpecialEvent = True

            splitedArg = Command.split(':')
            FPS = int(splitedArg[1])

            if not IsMenuMode:
                LastFPSValue = FPS

            print("Taiyou.GameExecution.ReceiveCommand : MaxFPS Set to:" + str(FPS))

        elif Command.startswith("SET_RESOLUTION") if Command else False:
            CommandWasValid = True
            IsSpecialEvent = True

            splitedArg = Command.split(':')
            print("Taiyou.GameExecution.ReceiveCommand : Set Resolution to: {0}x{1}".format(str(splitedArg[1]), str(splitedArg[2])))

            CurrentRes_W = int(splitedArg[1])
            CurrentRes_H = int(splitedArg[2])
            if ResiziableWindow and not tge.RunInFullScreen:
                DISPLAY = pygame.display.set_mode((CurrentRes_W, CurrentRes_H), pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.HWACCEL | pygame.HWSURFACE, tge.BitDepth)

            if ResiziableWindow and tge.RunInFullScreen:
                ResiziableWindow = False
                DISPLAY = pygame.display.set_mode((CurrentRes_W, CurrentRes_H), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.FULLSCREEN, tge.BitDepth)

            if not ResiziableWindow:
                if not tge.RunInFullScreen:
                    DISPLAY = pygame.display.set_mode((CurrentRes_W, CurrentRes_H), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE, tge.BitDepth)
                else:
                    DISPLAY = pygame.display.set_mode((CurrentRes_W, CurrentRes_H), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.FULLSCREEN, tge.BitDepth)

        elif Command.startswith("KILL") if Command else False:
            CommandWasValid = True
            IsSpecialEvent = True

            print("Taiyou.GameExecution.ReceiveCommand : Killing Game Process")

            Destroy()

        elif Command.startswith("OVERLAY_LEVEL") if Command else False:
            CommandWasValid = True
            IsSpecialEvent = True

            splitedArg = Command.split(':')

            ovelMng.Set_OverlayLevel(int(splitedArg[1]))

            print("Taiyou.GameExecution.ReceiveCommand : Set OVERLAY_LEVEL to " + splitedArg[1])

        elif Command.startswith("SET_GAME_MODE") if Command else False:
            CommandWasValid = True
            IsSpecialEvent = True

            print("Taiyou.GameExecution.ReceiveCommand : Set Game Mode")

            IsMenuMode = False

            # -- Set the Last FPS Value set by the Game -- #
            FPS = LastFPSValue

            sound.UnpauseGameChannel()
            print("Taiyou.GameExecution.ReceiveCommand.SetGameMode : All Sounds on Game Channel has been unpaused.")

        elif Command.startswith("OPEN_GAME") if Command else False:
            CommandWasValid = True
            IsSpecialEvent = True

            print("Taiyou.GameExecution.ReceiveCommand : Open Game")
            splitedArg = Command.split(':')

            SetGameObject(splitedArg[1].rstrip())

        elif Command.startswith("REMOVE_GAME") if Command else False:
            CommandWasValid = True
            IsSpecialEvent = True

            print("Taiyou.GameExecution.ReceiveCommand : Remove Game Object, and unload all data related to it")

            RemoveGame()

        elif Command.startswith("SET_TITLE") if Command else False:
            CommandWasValid = True
            splitedArg = Command.split(';')

            pygame.display.set_caption(splitedArg[1])

        if not CommandWasValid:
            tge.devel.PrintToTerminalBuffer("TaiyouMessage: Invalid Command:\n'" + Command + "'")
        elif IsSpecialEvent:
            tge.devel.PrintToTerminalBuffer("TaiyouMessage: Command Processed:\n'" + Command + "'")

    except IndexError as ex:
        tge.devel.PrintToTerminalBuffer("TaiyouMessage EXCEPTION\nThe last command does not have the necessary number of arguments.")

def RemoveGame(UnloadGameAssts=True, CloseGameFolder=True):
    global GameObject
    global IsMenuMode

    print("Taiyou.GameExecution.RemoveGame : Suspend Game Code")

    # -- Call the Game Unload Function on Game -- #
    try:
        GameObject.Unload()
    except AttributeError:
        print("Taiyou.GameExecution.RemoveGame : Game has no Unload Function.")

    # -- Try to delete the Game Object -- #
    importlib.reload(GameObject)
    GameObject = None

    if UnloadGameAssts:
        print("Taiyou.GameExecution.RemoveGame : Unload Game Assets")

        sprite.Unload()
        sound.Unload()
        reg.Unload()

    if CloseGameFolder:
        print("Taiyou.GameExecution.RemoveGame : Close Game Folder")

        tge.CloseGameFolder()

    IsMenuMode = True

    print("Taiyou.GameExecution.RemoveGame : Operation Complete.")

def SetGameObject(GameFolder):
    global GameObject
    global DISPLAY

    try:
        print("Taiyou.GameExecution.SetGameObject : Open Game [" + GameFolder + "]")
        print("Taiyou.GameExecution.SetGameObject : MainModuleName is: [" + tge.Get_MainGameModuleName(GameFolder) + "]")

        GameObject = importlib.import_module(tge.Get_MainGameModuleName(GameFolder))

        if tge.Get_MainGameModuleName(tge.Get_GameFolder()) in sys.modules:  # -- If the module is not loaded
            print("Taiyou.GameExecution.GameStart : Game Code was not loaded yet.\nCalling Initialize")

            GameObject.Initialize(DISPLAY)  # -- Call the Game Initialize Function --

        else:
            print("Taiyou.GameExecution.GameStart : Game Code was already loaded.")

    except Exception as ex:
        SystemException(ex, "SetGameObject")

def SystemException(ex, ErrorPart="Unknown"):
    raise ex

def EventUpdate():
    global IsMenuMode
    global GameUpdateEnabled
    global DISPLAY
    global FPS

    # -- Internaly Process Pygame Events -- #
    pygame.fastevent.pump()

    for event in pygame.fastevent.get():
        # -- Closes the Game when clicking on the X button
        if event.type == pygame.QUIT:
            Destroy()

        # -- Menu Key -- #
        elif event.type == pygame.KEYUP and event.key == pygame.K_F12:
            if not IsMenuMode:
                IsMenuMode = True
                GameUpdateEnabled = False
                SystemUI.gameOverlay.CopyOfTheScreen = DISPLAY.copy()
                sound.PauseGameChannel()
                print("Taiyou.GameExecution.ReceiveCommand.SetGameMode : All Sounds on Game Channel has been paused.")
                FPS = 60  # -- Default TaiyouUI FPS

                if not SystemUI.SystemMenuEnabled and SystemUI.CurrentMenuScreen == 0:
                    SystemUI.SystemMenuEnabled = True
                    SystemUI.gameOverlay.UIOpacityAnimEnabled = True
                    SystemUI.gameOverlay.UIOpacityScreenCopyied = False

        # -- Resize Window Event -- #
        elif ResiziableWindow and not tge.RunInFullScreen:
            if event.type == pygame.VIDEORESIZE:
                # Resize the Window
                DISPLAY = pygame.display.set_mode((event.w, event.h), pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.HWACCEL)

        # -- Do Game Events -- #
        try:
            if not IsMenuMode:
                GameObject.EventUpdate(event)

        except Exception as ex:  # -- Exception Handler
            GameException(ex, "Game Events")

        # -- Do SystemMenu Events -- #
        if IsMenuMode:
            SystemUI.EventUpdate(event)

        # -- Do OverlayManager Events -- #
        ovelMng.EventUpdate(event)

def GameException(Exception, ErrorPart="Unknown"):
    global GameUpdateEnabled
    global IsMenuMode
    global DISPLAY

    if not reg.ReadKey_bool("/TaiyouSystem/CONF/exception_handler"):
        raise Exception
    else:
        ExceptionText = "\n\nGame Exception! in [" + ErrorPart + "]:\n\n" + str(Exception) + "\n\n"

        tge.devel.PrintToTerminalBuffer(ExceptionText)
        GameUpdateEnabled = False
        IsMenuMode = True
        SystemUI.SystemMenuEnabled = True
        if not SystemUI.gameOverlay.OpenedInGameError:
            SystemUI.gameOverlay.UIOpacityAnimEnabled = True
            SystemUI.gameOverlay.OpenedInGameError = True
            SystemUI.gameOverlay.CopyOfTheScreen = DISPLAY.copy()

        print(ExceptionText)

def Run():
    global GameObject
    global FPS
    global DISPLAY
    global IsMenuMode

    # -- Run the Clock -- #
    clock.tick(FPS)

    # -- If MenuMode, update the Menu -- #
    if IsMenuMode:
        SystemUI.Update()
        SystemUI.Draw(DISPLAY)

        # -- Draw the Overlay, when its enabled -- #
        ovelMng.Render(DISPLAY)

        # -- Flip the Screen -- #
        pygame.display.flip()

        # -- Receive Commands from System Menu -- #
        if len(SystemUI.Messages) >= 1:
            ReceiveCommand(SystemUI.ReadCurrentMessages())

    else:  # -- Else, Update the Game -- #
        try:
            # -- Do Game Update -- #
            GameObject.Update()

            # -- Do Game Draw -- #
            GameObject.GameDraw(DISPLAY)

            # -- Draw the Overlay, when its enabled -- #
            ovelMng.Render(DISPLAY)

            # -- Flip the Screen -- #
            pygame.display.flip()

            # -- Receive command from the Current Game -- #
            if len(GameObject.Messages) >= 1:
                ReceiveCommand(GameObject.ReadCurrentMessages())

        except Exception as ex:
            GameException(ex, "Game Update/Draw")

    # -- Update Events -- #
    EventUpdate()

    # -- Update OverlayManager -- #
    ovelMng.Update()

def Destroy():
    print("Taiyou.GameExecution.Destroy : Closing [" + tge.Get_GameTitle() + "]...")
    # -- Unload Things -- #
    reg.Unload()
    sprite.Unload()
    sound.Unload()
    pygame.mixer.quit()
    pygame.quit()
    print("Taiyou.GameExecution.Destroy : Game [" + tge.Get_GameTitle() + "] has been closed.")
    sys.exit()

