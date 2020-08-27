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
import pygame, datetime, traceback
from ENGINE import cntMng
from ENGINE import MAIN
from ENGINE import utils
import ENGINE as tge


DefaultContent = cntMng.ContentManager
AnimationController = utils.AnimationController
LogoAnimationReady = False
Opacity = 0
AnimationNextEnableDelay = 0
AnimationMode = 0
AnimationEndDelay = 0
TextToDisplay = "/aragubas"
BootFromGameError = False
ErrorLogWritten = False
IntroSoundPlayed = False
ErrorSoundPlayed = False
ShutdownSwitch = False
ImageToDisplay = "/logo.png"

def Initialize(DISPLAY):
    global DefaultContent
    global AnimationController
    global LogoAnimationReady

    DefaultContent = cntMng.ContentManager()

    DefaultContent.LoadSpritesInFolder("RES/img")
    DefaultContent.LoadRegKeysInFolder("RES/reg")
    DefaultContent.LoadSoundsInFolder("RES/sound")
    DefaultContent.SetFontPath("RES/font")

    print("Sounds Loaded")
    print(DefaultContent.AllLoadedSounds)
    print("Initialize Called")
    
    pygame.mouse.set_visible(False)
    MAIN.ReceiveCommand(5, "Taiyou Game Engine v{0}".format(utils.FormatNumber(tge.TaiyouGeneralVersion)))
    MAIN.ReceiveCommand(0, 60)

    AnimationController = utils.AnimationController(DefaultContent.Get_RegKey("/animation_speed", float), multiplierRestart=True)

    if DefaultContent.Get_RegKey("/skip_intro", bool):
        InitializationStep()

def GameDraw(DISPLAY):
    global DefaultContent
    global Opacity
    global TextToDisplay
    global ImageToDisplay

    DISPLAY.fill((0, 0, 0))
    # -- Render the Background -- #
    DefaultContent.ImageRender(DISPLAY, "/background.png", 0, 0, Opacity=Opacity)

    # -- Render the Taiyou Logo -- #
    DefaultContent.ImageRender(DISPLAY, ImageToDisplay, 800 / 2 - DefaultContent.GetImage_width(ImageToDisplay) / 2, 50, Opacity=Opacity)

    # -- Render the Aragubas Name -- #
    DefaultContent.FontRender(DISPLAY, "/Ubuntu_Bold.ttf", 18, DefaultContent.Get_RegKey(TextToDisplay), (255, 255, 255), 800 / 2 - DefaultContent.GetFont_width("/Ubuntu_Bold.ttf", 18, DefaultContent.Get_RegKey(TextToDisplay)) / 2, 60 + DefaultContent.GetImage_height(ImageToDisplay), Opacity=Opacity)


    # -- Render the Cursor -- #
    DefaultContent.ImageRender(DISPLAY, "/cursor.png", pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

def Update():
    global LogoAnimationReady
    global AnimationController
    global Opacity
    global AnimationNextEnableDelay
    global AnimationMode
    global AnimationEndDelay
    global DefaultContent
    global TextToDisplay
    global BootFromGameError
    global ErrorLogWritten
    global IntroSoundPlayed
    global ErrorSoundPlayed
    global ImageToDisplay

    # -- If Animation is Ready, Switch to Game -- #
    if LogoAnimationReady and not BootFromGameError:
        tge.InitializeGame()
        LogoAnimationReady = False
        BootFromGameError = True
        TextToDisplay = "/game_boot_error"
        AnimationController.Enabled = True

        return

    AnimationController.Update()

    if BootFromGameError and not ErrorSoundPlayed:
        ErrorSoundPlayed = True
        ImageToDisplay = "/warning.png"
        DefaultContent.PlaySound("/notify.wav")

    # -- Play the Intro Sound -- #
    if not IntroSoundPlayed and not BootFromGameError:
        IntroSoundPlayed = True
        DefaultContent.PlaySound("/intro.wav")

    if not AnimationController.Enabled and AnimationEndDelay == 0 and not BootFromGameError:
        AnimationNextEnableDelay += 1

        if AnimationNextEnableDelay >= DefaultContent.Get_RegKey("/animation_next_delay", int):
            AnimationController.Enabled = True
            AnimationMode += 1

    Opacity = AnimationController.Value

    if AnimationMode == 2 and not BootFromGameError:
        AnimationController.Enabled = False
        AnimationEndDelay += 1

        if AnimationEndDelay >= DefaultContent.Get_RegKey("/animation_end_delay", int):
            InitializationStep()

    if AnimationMode == 3 and not BootFromGameError:
        AnimationMode += 1
        AnimationController.Enabled = True

    if BootFromGameError and not ErrorLogWritten:
        ErrorLogWritten = True
        WriteGameBootErrorLog()

    if ShutdownSwitch and not AnimationController.Enabled and BootFromGameError:
        MAIN.Destroy()

def WriteGameBootErrorLog():
    LogFile = open("GameBootError.txt", "w")
    # -- Write the File Header -- #
    LogFile.write("-- TaiyouGameEngine has failed while booting an Application. --\nThis log file has been written on:\n{0}\n\n".format(datetime.datetime.now()))
    LogFile.write("Traceback:\n{0}\n".format(traceback.format_exc()))
    LogFile.write("\nTaiyou Game Engine Modules Version:\n")

    ModulesTxt = "Runtime: {0}\n\nAppData: {1}\n\nContentManager: {2}\n\nFx: {3}\n\nMain: {4}\n\nShape: {5}\n\nUtils: {6}\n\nMain: {7}"
    try:
        ModulesTxt = ModulesTxt.format(str(tge.Get_Version()), str(tge.Get_AppDataVersion()), str(tge.Get_ContentManagerVersion()), str(tge.Get_FXVersion()), str(tge.Get_TaiyouMainVersion()), str(tge.Get_ShapeVersion()), str(tge.Get_UtilsVersion()), str(tge.Get_MAINVersion()))
        LogFile.write(ModulesTxt)

    except Exception as ex:
        print("Taiyou.Bootloader : Error while parsing the string:\n" + str(ex))
        LogFile.write("ERROR WHILE PARSING THE STRING.")

    LogFile.close()


def InitializationStep():
    global LogoAnimationReady
    global AnimationMode
    global TextToDisplay
    global AnimationEndDelay

    # -- Check if there is any game to Initialize -- #
    CurrentGame_Folder = open(".current_game", "r").read().rstrip()

    if CurrentGame_Folder == "":
        AnimationMode += 1
        TextToDisplay = "/no_game_selected"
        AnimationEndDelay = 50
        print("No Game to Initialize.")

    else:
        LogoAnimationReady = True


def EventUpdate(event):
    global BootFromGameError
    global AnimationController
    global ShutdownSwitch

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_ESCAPE and BootFromGameError:
            ShutdownSwitch = True
            AnimationController.Enabled = True
