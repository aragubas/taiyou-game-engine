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
import pygame, sys, importlib, marshal
import traceback, threading
from datetime import datetime
from multiprocessing import Process
import gc

# The main Entry Point
print("TaiyouGameEngineMainScript version " + tge.Get_TaiyouMainVersion())

# -- Variables -- #
GameUpdateEnabled = False
clock = pygame.time.Clock()
FPS = 70
DISPLAY = pygame.display
IsFullscreen = False
IsMenuMode = True
CurrentRes_W = 800
CurrentRes_H = 600
WindowTitle = "Taiyou Game Engine v{0}".format(utils.FormatNumber(tge.TaiyouGeneralVersion))
UpdateTime_Calculated = 0
UpdateTime_MaxMS = 0
UpdateTime_MaxDelta = 0
GameObject = None
LastFPSValue = 60


def Initialize():
    global DISPLAY

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

        pygame.mixer.init(Frequency, Size, Channels, BufferSize)

        pygame.init()
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
        DISPLAY = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
    else:
        DISPLAY = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.FULLSCREEN)

    # -- Hide Mouse Cursor -- #
    pygame.mouse.set_visible(False)

    # -- Set Window Title -- #
    pygame.display.set_caption(WindowTitle)

    # -- Initialize the Taiyou UI -- #
    SystemUI.Initialize()

    print("Taiyou.GameExecution.Initialize : Initialization complete.")


def ReceiveCommand(Command, Arguments=None):
    """
    Sends a command to the Game Engine
    \n
    Command:                   Argument\n
    0 - Set FPS:                Integer\n
    1 - Set Resolution:         [Width]x[Height]\n
    2 - KILL:                   None\n
    3 - OverlayLevel:           Integer\n
    4 - Set Icon:               String [Sprite Name loaded on Sprite System]\n
    5 - Set Game Mode:          None\n
    6 - Set Menu Mode:          None\n
    7 - Open Game:              String [GameFolder Name]\n
    8 - Remove Game:            None\n
    9 - Set Title:              String\n
    10 - Switch Game Folder:    None\n
    :param Command:CommandCode
    :param Arguments:Argument of Specified Command
    :return:
    """
    global IsMenuMode
    global DISPLAY
    global FPS
    global LastFPSValue
    global GameUpdateEnabled
    global CurrentRes_W
    global CurrentRes_H

    CommandWasValid = False
    IsSpecialEvent = False

    try:
        if Command == 0:
            CommandWasValid = True
            IsSpecialEvent = True

            FPS = int(Arguments)

            LastFPSValue = FPS

            print("Taiyou.GameExecution.ReceiveCommand : MaxFPS Set to:" + str(FPS))

        elif Command == 1:
            CommandWasValid = True
            IsSpecialEvent = True

            splitedArg = Arguments.split('x')
            print("Taiyou.GameExecution.ReceiveCommand : Set Resolution to: {0}x{1}".format(str(splitedArg[0]), str(splitedArg[1])))

            CurrentRes_W = int(splitedArg[0])
            CurrentRes_H = int(splitedArg[1])

            SetDisplay()

        elif Command == 2:
            CommandWasValid = True
            IsSpecialEvent = True

            print("Taiyou.GameExecution.ReceiveCommand : Killing Game Process")

            Destroy()

        elif Command == 3:
            CommandWasValid = True
            IsSpecialEvent = True

            splitedArg = int(Arguments)

            ovelMng.Set_OverlayLevel(int(splitedArg[1]))

            print("Taiyou.GameExecution.ReceiveCommand : Set OVERLAY_LEVEL to " + splitedArg[1])

        elif Command == 4:
            CommandWasValid = True
            IsSpecialEvent = True

            pygame.display.set_icon(sprite.GetSprite(Arguments))

            print("Taiyou.GameExecution.ReceiveCommand : Set Icon to " + str(Arguments))

        elif Command == 5:
            CommandWasValid = True
            IsSpecialEvent = True

            print("Taiyou.GameExecution.ReceiveCommand.SetGameMode : Enabling Game Mode...")

            # -- Disable System Menu -- #
            IsMenuMode = False

            # -- Set the Last FPS Value set by the Game -- #
            FPS = LastFPSValue

            # -- Force Collect on GC -- #
            utils.GarbageCollector_Collect()

            # -- Unpause Paused Channels -- #
            sound.UnpauseGameChannel()

            # -- Unload System Registy -- #
            print("Taiyou.GameExecution.ReceiveCommand.SetGameMode : Unloading System Registry...")
            reg.Unload(True)

            # -- Force Collect on GC -- #
            utils.GarbageCollector_Collect()
            print("Taiyou.GameExecution.ReceiveCommand.SetGameMode : Done")

        elif Command == 6:
            CommandWasValid = True
            IsSpecialEvent = True

            if not IsMenuMode:
                # -- Reload System Reg -- #
                reg.Reload(True)

                print("Taiyou.GameExecution.ReceiveCommand : Set Menu Mode")

                SystemUI.CurrentMenuScreen = 0
                IsMenuMode = True
                GameUpdateEnabled = False
                SystemUI.gameOverlay.CopyOfTheScreen = DISPLAY.copy()
                sound.PauseGameChannel()
                print("Taiyou.GameExecution.ReceiveCommand.SetGameMode : All Sounds on Game Channel has been paused.")
                FPS = 70  # -- Default TaiyouUI FPS

                # -- Force GC to collect -- #
                utils.GarbageCollector_Collect()

                # -- Print GC infos -- #
                print(utils.GarbageCollector_GetInfos())

                if not SystemUI.SystemMenuEnabled and SystemUI.CurrentMenuScreen == 0:
                    SystemUI.SystemMenuEnabled = True
                    SystemUI.gameOverlay.UIOpacityAnimEnabled = True
                    SystemUI.gameOverlay.UIOpacityScreenCopyied = False

        elif Command == 7:
            CommandWasValid = True
            IsSpecialEvent = True

            # -- Set Game Object -- #
            SetGameObject(Arguments.rstrip())

            print("Taiyou.GameExecution.ReceiveCommand : Open Game [{0}]".format(str(Arguments).rstrip()))

        elif Command == 8:
            CommandWasValid = True
            IsSpecialEvent = True

            print("Taiyou.GameExecution.ReceiveCommand : Remove Game Object, and unload all data related to it")

            RemoveGame()

        elif Command == 9:
            CommandWasValid = True

            pygame.display.set_caption(Arguments)

        elif Command == 10:
            CommandWasValid = True

            # -- Check if is Necessary to Select a Save Folder -- #
            if tge.CurrentGame_SaveFolderDecided:
                return

            # -- Reload System Reg -- #
            print("Taiyou.GameExecution.ReceiveCommand.SwitchSaveFolder : Reloading System Registry...")
            reg.Reload(True)

            if not IsMenuMode:
                print("Taiyou.GameExecution.ReceiveCommand.SwitchSaveFolder : Enabling System Menu")
                # -- Force Collect on GC -- #
                utils.GarbageCollector_Collect()

                IsMenuMode = True
                GameUpdateEnabled = False
                SystemUI.saveFolderSelectScreen.CopyOfTheScreen = DISPLAY.copy()
                sound.PauseGameChannel()
                print("Taiyou.GameExecution.ReceiveCommand.SetMenuMode : All Sounds on Game Channel has been paused.")
                FPS = 70  # -- Default TaiyouUI FPS
                SystemUI.CurrentMenuScreen = 3

                if not SystemUI.SystemMenuEnabled and SystemUI.CurrentMenuScreen == 3:
                    SystemUI.SystemMenuEnabled = True
                    SystemUI.saveFolderSelectScreen.UIOpacityAnimEnabled = True
                    SystemUI.saveFolderSelectScreen.UIOpacityScreenCopyied = False

        if not CommandWasValid:
            Txt = "TaiyouMessage: Invalid Command:\n'{0}'".format(Command)
            tge.devel.PrintToTerminalBuffer(Txt)
            print(Txt)
        elif IsSpecialEvent:
            Txt = "TaiyouMessage: Command Processed:\n'{0}'".format(Command)
            tge.devel.PrintToTerminalBuffer(Txt)
            print(Txt)

    except IndexError:
        Txt = "TaiyouMessage EXCEPTION\nThe Command {0}\ndoes not have the necessary number of arguments.".format(str(Command))
        tge.devel.PrintToTerminalBuffer(Txt)
        print(Txt)

def SetDisplay():
    global DISPLAY
    global CurrentRes_W
    global CurrentRes_H

    if not tge.RunInFullScreen:
        DISPLAY = pygame.display.set_mode((CurrentRes_W, CurrentRes_H), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)

    else:
        DISPLAY = pygame.display.set_mode((CurrentRes_W, CurrentRes_H), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.FULLSCREEN)


def RemoveGame(UnloadGameAssts=True, CloseGameFolder=True):
    global GameObject
    global IsMenuMode

    # -- Call the Game Unload Function on Game -- #
    try:
        GameObject.Unload()
    except:
        print("Taiyou.GameExecution.RemoveGame : Game has no Unload Function.")

    # -- Try to delete the Game Object -- #
    print("Taiyou.GameExecution.RemoveGame : Unloading Game Code")

    try:
        utils.GarbageCollector_Collect()
        try:
            importlib.reload(GameObject)
        except:
            pass

        utils.GarbageCollector_Collect()
        for count in range(0, sys.getrefcount(GameObject) - 1):
            del GameObject
            utils.GarbageCollector_Collect()

        utils.GarbageCollector_Collect()
        GameObject = None

    except:
        utils.GarbageCollector_Collect()

    print("Taiyou.GameExecution.RemoveGame : Done!")

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

        # -- Remove any residue of Last Opened Game -- #
        utils.GarbageCollector_Collect()
        RemoveGame(False, False)
        utils.GarbageCollector_Collect()

        # -- Initialize the Game Object -- #
        utils.GarbageCollector_Collect()
        GameObject = importlib.import_module(tge.Get_MainGameModuleName(GameFolder))

        GameObject.Initialize(DISPLAY)  # -- Call the Game Initialize Function --
        utils.GarbageCollector_Collect()

    except Exception as ex:
        SystemException(ex, "SetGameObject")

def SystemException(ex, ErrorPart="Unknown"):
    raise ex

def EventUpdate():
    global IsMenuMode
    global StepByStep_Step
    global StepByStep_EnabledToggle
    global DISPLAY

    # -- Internaly Process Pygame Events -- #
    pygame.fastevent.pump()

    for event in pygame.fastevent.get():
        # -- Closes the Game when clicking on the X button
        if event.type == pygame.QUIT:
            Destroy()

        # -- Menu Key -- #
        elif event.type == pygame.KEYUP and event.key == pygame.K_F12:
            ReceiveCommand(6)

        # -- Do Game Events -- #
        try:
            if not IsMenuMode:
                GameObject.EventUpdate(event)

        except Exception as ex:  # -- Exception Handler
            GameException(ex, "Game Events")

        # -- Do SystemMenu Events -- #
        SystemUI.EventUpdate(event)

        # -- Do OverlayManager Events -- #
        ovelMng.EventUpdate(event)

def GameException(Exception, ErrorPart="Unknown"):
    global GameUpdateEnabled
    global IsMenuMode
    global DISPLAY

    # -- Reload System Registry -- #
    print("Taiyou.GameException!")
    reg.Reload(True)

    if not reg.ReadKey_bool("/TaiyouSystem/CONF/exception_handler", True):
        raise Exception
    else:

        ExceptionText = "\n\nGame Exception! in [" + ErrorPart + "]:\n\n" + str(Exception) + "\n\n"

        tge.devel.PrintToTerminalBuffer(ExceptionText)
        GameUpdateEnabled = False
        IsMenuMode = True
        SystemUI.SystemMenuEnabled = True
        SystemUI.CurrentMenuScreen = 0
        if not SystemUI.gameOverlay.OpenedInGameError:
            SystemUI.gameOverlay.UIOpacityAnimEnabled = True
            SystemUI.gameOverlay.OpenedInGameError = True
            SystemUI.gameOverlay.CopyOfTheScreen = DISPLAY.copy()

        print(ExceptionText)

def Engine_Draw():
    global DISPLAY
    global IsMenuMode

    if not IsMenuMode:  # -- Draw System Menu
        try:
            # -- Do Game Draw -- #
            GameObject.GameDraw(DISPLAY)

        except Exception as ex:
            GameException(ex, "Game Draw")

    # -- Draw SystemUI -- #
    SystemUI.Draw(DISPLAY)

    # -- Draw the Overlay -- #
    ovelMng.Render(DISPLAY)


def Engine_Update():
    # -- If not MenuMode, update the Game -- #
    if not IsMenuMode:
        try:
            # -- Do Game Update -- #
            GameObject.Update()

        except Exception as ex:
            GameException(ex, "Game Update")

    # -- Update TaiyouUI -- #
    SystemUI.Update()

    # -- Update Overlay -- #
    ovelMng.Update()

StepByStep_Step = False
StepByStep_EnabledToggle = False

def Run():
    global GameObject
    global FPS
    global DISPLAY
    global IsMenuMode
    global StepByStep_Step

    # -- Disable Engine Update when Minimized -- #
    # -- Run Events -- #
    EventUpdate()

    # -- Run the Update Code -- #
    Engine_Update()

    # -- Limit the FPS -- #
    clock.tick(FPS)

    # -- Run the Draw Code -- #
    Engine_Draw()

    # -- Flip the Screen -- #
    pygame.display.flip()

def Destroy():
    print("Taiyou.GameExecution.Destroy : Save TaiyouUI Settings")
    # -- Save Settings -- #
    SystemUI.SaveSettings()

    print("Taiyou.GameExecution.Destroy : Unloading all loaded assets")
    # -- Unload Things -- #
    reg.Unload()
    sprite.Unload()
    sound.Unload()
    pygame.quit()

    utils.GarbageCollector_Collect()
    print("Taiyou.GameExecution.Destroy : Taiyou Game Engine has been closed.")
    sys.exit()

