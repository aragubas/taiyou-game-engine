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

# -- Modules Versions -- #
def Get_Version():
    return "2.9"
def Get_SpriteVersion():
    return "2.4"
def Get_SoundVersion():
    return "2.0"
def Get_RegistryVersion():
    return "2.4"
def Get_UtilsVersion():
    return "1.8"
def Get_TaiyouMainVersion():
    return "3.3"
def Get_DeveloperConsoleVersion():
    return "2.0"
def Get_DebuggingVersion():
    return "1.4"
def Get_BootloaderVersion():
    return "1.5"

# -- Calculate the Version of Taiyou Game Engine -- #
TaiyouGeneralVersion = float(Get_Version()) + float(Get_UtilsVersion()) + float(Get_RegistryVersion()) + float(Get_SpriteVersion()) + float(Get_SoundVersion()) + float(Get_TaiyouMainVersion()) + float(Get_DeveloperConsoleVersion()) + float(Get_DebuggingVersion()) + float(Get_BootloaderVersion()) - 9.0


# -- Print Runtime Version -- #
print("TaiyouGameEngineRuntime version " + Get_Version())

# -- Imports --
from ENGINE import CONTENT_MANAGER as cntMng
from ENGINE import SOUND as sound
from ENGINE import APPDATA as appData
from ENGINE import FX as fx
from ENGINE import SHAPES as shape
from ENGINE import UTILS as utils
from ENGINE import APPDATA as reg
from ENGINE import taiyouMain
import os, pygame
import platform
from os.path import expanduser


# -- Current Game Variables -- #
CurrentGame_Folder = "null"

# -- Arguments -- #
IsGameRunning = False
VideoDriver = "null"
VideoX11CenterWindow = False
VideoX11DGAMouse = False
VideoX11YUV_HWACCEL = False
AudioDriver = "null"
AudioFrequency = 0
AudioSize = -0
AudioChannels = 0
AudioBufferSize = 0
RunInFullScreen = False
InputMouseDriver = "fbcon"
InputDisableMouse = False
IgnoreSDL2Parameters = True
PygameFastEvent = True
SmoothScaleTransform = "MMX"

# -- Taiyou Paths -- #
TaiyouPath_SystemPath = "Taiyou"
TaiyouPath_TaiyouConfigFile = TaiyouPath_SystemPath + "Taiyou.config"
TaiyouPath_CorrectSlash = "/"
TaiyouPath_AppDataFolder = ""
TaiyouPath_CorrectAssetsFolder = ""

# -- Splash -- #
ApplicationSplash = None

def InitEngine():
    global VideoDriver
    global AudioDriver
    global VideoX11CenterWindow
    global AudioSize
    global AudioBufferSize
    global AudioChannels
    global AudioFrequency
    global RunInFullScreen
    global VideoX11DGAMouse
    global VideoX11YUV_HWACCEL
    global InputMouseDriver
    global InputDisableMouse
    global IgnoreSDL2Parameters
    global SmoothScaleTransform
    global PygameFastEvent
    global TaiyouPath_CorrectSlash
    global TaiyouPath_SystemPath
    global TaiyouPath_TaiyouConfigFile
    global TaiyouPath_CorrectSlash
    global CurrentGame_Folder
    global TaiyouPath_AppDataFolder
    global ApplicationSplash

    print("\n\n\n# -- General Taiyou Runtime Version -- #\n\nThis version is the sum of all modules version, so it is 'The Taiyou Version'.\nGeneral Version is [" + str(utils.FormatNumber(TaiyouGeneralVersion)) + "/{0}].\n\n\n".format(str(TaiyouGeneralVersion)))

    # -- Set the Home Directory -- #
    if platform.system() == "Linux":
        TaiyouPath_CorrectSlash = "/"
        TaiyouPath_SystemPath = "Taiyou/"
        TaiyouPath_TaiyouConfigFile = TaiyouPath_SystemPath + "Taiyou.config"

    elif platform.system() == "Windows":
        TaiyouPath_CorrectSlash = "\\"
        TaiyouPath_SystemPath = "Taiyou\\"
        TaiyouPath_TaiyouConfigFile = TaiyouPath_SystemPath + "Taiyou.config"

    conf_file = open(TaiyouPath_TaiyouConfigFile)

    for x in conf_file:
        x = x.rstrip()
        SplitedParms = x.split(":")

        if not x.startswith("#"):
            # -- Disable Font Rendering -- #
            if SplitedParms[0] == "DisableFontRendering":
                if SplitedParms[1] == "True":
                    CONTENT_MANAGER.FontRenderingDisabled = True
                else:
                    CONTENT_MANAGER.FontRenderingDisabled = False

                print("Taiyou.Runtime.InitEngine : Disable font rendering set to:" + str(CONTENT_MANAGER.FontRenderingDisabled))

            # -- Disable Sprite Rendering -- #
            elif SplitedParms[0] == "DisableSpriteRendering":
                if SplitedParms[1] == "True":
                    CONTENT_MANAGER.SpriteRenderingDisabled = True
                else:
                    CONTENT_MANAGER.SpriteRenderingDisabled = False

                print("Taiyou.Runtime.InitEngine : Disable sprite rendering set to:" + str(CONTENT_MANAGER.SpriteRenderingDisabled))

            # -- Disable Rectangle Rendering -- #
            elif SplitedParms[0] == "DisableRectangleRendering":
                if SplitedParms[1] == "True":
                    CONTENT_MANAGER.RectangleRenderingDisabled = True
                else:
                    CONTENT_MANAGER.RectangleRenderingDisabled = False

                print("Taiyou.Runtime.InitEngine : Disable rectangle rendering set to:" + str(CONTENT_MANAGER.RectangleRenderingDisabled))

            # -- Disable Sprite Transparency -- #
            elif SplitedParms[0] == "DisableSpriteTransparency":
                if SplitedParms[1] == "True":
                    CONTENT_MANAGER.SpriteTransparency = True
                else:
                    CONTENT_MANAGER.SpriteTransparency = False

                print("Taiyou.Runtime.InitEngine : Disable sound system set to:" + str(CONTENT_MANAGER.SpriteTransparency))

            # -- Disable Sound System -- #
            elif SplitedParms[0] == "DisableSoundSystem":
                if SplitedParms[1] == "True":
                    sound.DisableSoundSystem = True
                else:
                    sound.DisableSoundSystem = False

                print("Taiyou.Runtime.InitEngine : Disable sound system set to:" + str(sound.DisableSoundSystem))

            # -- AppData Folder Path -- #
            elif SplitedParms[0] == "AppDataFolder":
                TaiyouPath_AppDataFolder = SplitedParms[1].rstrip()

                print("Taiyou.Runtime.InitEngine : TaiyouAppDataFolder set to:" + str(TaiyouPath_AppDataFolder))

            # -- SDL Option: Video Driver -- #
            elif SplitedParms[0] == "VideoDriver":
                VideoDriver = SplitedParms[1].rstrip()

                print("Taiyou.Runtime.InitEngine : Video Driver was set to:" + str(VideoDriver))

            # -- SDL Option: Audio Driver -- #
            elif SplitedParms[0] == "AudioDriver":
                AudioDriver = SplitedParms[1].rstrip()

                print("Taiyou.Runtime.InitEngine : Audio Driver was set to:" + str(AudioDriver))

            # -- SoundSystem: Audio Device Frequency -- #
            elif SplitedParms[0] == "AudioFrequency":
                AudioFrequency = int(SplitedParms[1].rstrip())

                print("Taiyou.Runtime.InitEngine : Audio Frequency was set to:" + str(AudioFrequency))

            # -- SoundSystem: Audio Device Frame Size -- #
            elif SplitedParms[0] == "AudioSize":
                AudioSize = int(SplitedParms[1].rstrip())

                print("Taiyou.Runtime.InitEngine : Audio Size was set to:" + str(AudioSize))

            # -- SoundSystem: Audio Device Audio Channels -- #
            elif SplitedParms[0] == "AudioChannels":
                AudioChannels = int(SplitedParms[1].rstrip())

                print("Taiyou.Runtime.InitEngine : Audio Channels was set to:" + str(AudioChannels))

            # -- SoundSystem: Audio Device Buffer Size -- #
            elif SplitedParms[0] == "AudioBufferSize":
                AudioBufferSize = int(SplitedParms[1].rstrip())

                print("Taiyou.Runtime.InitEngine : Audio Buffer Size was set to:" + str(AudioBufferSize))

            # -- Run in Fullscreen -- #
            elif SplitedParms[0] == "RunInFullScreen":
                if SplitedParms[1].rstrip() == "True":
                    RunInFullScreen = True
                elif SplitedParms[1].rstrip() == "False":
                    RunInFullScreen = False
                else:
                    RunInFullScreen = False

                print("Taiyou.Runtime.InitEngine : Run in Fullscreen was set to:" + str(RunInFullScreen))

            # -- SDL Option: Center Window -- #
            elif SplitedParms[0] == "VideoX11_CenterWindow":
                if SplitedParms[1].rstrip() == "True":
                    VideoX11CenterWindow = True
                elif SplitedParms[1].rstrip() == "False":
                    VideoX11CenterWindow = False
                else:
                    VideoX11CenterWindow = False

                print("Taiyou.Runtime.InitEngine : VideoX11CenterWindow was set to:" + str(VideoX11CenterWindow))

            # -- SDL Option: DGA Mouse -- #
            elif SplitedParms[0] == "VideoX11_DGAMouse":
                if SplitedParms[1].rstrip() == "True":
                    VideoX11DGAMouse = True
                elif SplitedParms[1].rstrip() == "False":
                    VideoX11DGAMouse = False
                else:
                    VideoX11DGAMouse = False

                print("Taiyou.Runtime.InitEngine : VideoX11DGAMouse was set to:" + str(VideoX11DGAMouse))

            # -- SDL Option: YUV Hardware Acelleration -- #
            elif SplitedParms[0] == "VideoX11_YUV_HWACCEL":
                if SplitedParms[1].rstrip() == "True":
                    VideoX11YUV_HWACCEL = True
                elif SplitedParms[1].rstrip() == "False":
                    VideoX11YUV_HWACCEL = False
                else:
                    VideoX11YUV_HWACCEL = False

                print("Taiyou.Runtime.InitEngine : VideoX11YUV_HWACCEL was set to:" + str(VideoX11YUV_HWACCEL))

            # -- SDL Option: Mouse Driver -- #
            elif SplitedParms[0] == "InputMouseDriver":
                InputMouseDriver = SplitedParms[1].rstrip()

                print("Taiyou.Runtime.InitEngine : InputMouseDriver was set to:" + str(InputMouseDriver))

            # -- SDL Option: Disable Mouse -- #
            elif SplitedParms[0] == "InputDisableMouse":
                if SplitedParms[1].rstrip() == "True":
                    InputDisableMouse = True
                elif SplitedParms[1].rstrip() == "False":
                    InputDisableMouse = False
                else:
                    InputDisableMouse = False

                print("Taiyou.Runtime.InitEngine : InputDisableMouse was set to:" + str(InputDisableMouse))

            # -- Ignore all SDL Parameters -- #
            elif SplitedParms[0] == "IgnoreSDL2Parameters":
                if SplitedParms[1].rstrip() == "True":
                    IgnoreSDL2Parameters = True
                elif SplitedParms[1].rstrip() == "False":
                    IgnoreSDL2Parameters = False
                else:
                    IgnoreSDL2Parameters = False

                print("Taiyou.Runtime.InitEngine : IgnoreSDL2Parameters was set to:" + str(IgnoreSDL2Parameters))

            # -- Sprite: SmoothScaleBackend Backend -- #
            elif SplitedParms[0] == "SmoothScaleBackend":
                SmoothScaleTransform = SplitedParms[1].rstrip()

                print("Taiyou.Runtime.InitEngine : SmoothScaleBackend was set to:" + str(SmoothScaleTransform))

            # -- Pygame: FastEvent -- #
            elif SplitedParms[0] == "FastEvent":
                if SplitedParms[1].rstrip() == "True":
                    PygameFastEvent = True
                elif SplitedParms[1].rstrip() == "False":
                    PygameFastEvent = False
                else:
                    PygameFastEvent = False

                print("Taiyou.Runtime.InitEngine : FastEvent was set to:" + str(PygameFastEvent))

            # -- Default TaiyouUI Screen Value -- #
            elif SplitedParms[0] == "DefaultSystemUIScreen":
                TaiyouUI.CurrentMenuScreen = int(SplitedParms[1])

                print("Taiyou.Runtime.InitEngine : TaiyouUI Default Screen was set to:" + str(TaiyouUI.CurrentMenuScreen))

    if not IgnoreSDL2Parameters:   # -- Set SDL2 Parameters (if enabled) -- #
        # -- Set the Enviroments Variables -- #
        os.environ['SDL_VIDEODRIVER'] = str(VideoDriver)  # -- Set the Video Driver
        os.environ['SDL_AUDIODRIVER'] = str(AudioDriver)  # -- Set the Audio Driver

        # -- Set Input Enviroments -- #
        os.environ['SDL_MOUSEDRV'] = str(InputMouseDriver)  # -- Set the Mouse Driver
        os.environ['SDL_NOMOUSE'] = str(InputDisableMouse)  # -- Set the Mouse Driver

        # -- Set X11 Environment Keys -- #
        if VideoDriver == "x11":
            if VideoX11CenterWindow:
                os.environ['SDL_VIDEO_CENTERED'] = "True"  # -- Set the Centered Window

            if VideoX11DGAMouse:
                os.environ['SDL_VIDEO_X11_DGAMOUSE'] = "True"  # -- Set the DGA Mouse Parameter

            if VideoX11YUV_HWACCEL:
                os.environ['SDL_VIDEO_YUV_HWACCEL'] = "True"  # -- Set the YUV HWACCEL Parameter

    else:
        print("Taiyou.Runtime.InitEngine : SDL2 Parameters has been disabled")

    # -- Set SmoothScaleMethod -- #
    pygame.transform.set_smoothscale_backend(SmoothScaleTransform)

    # -- Initialize Pygame and Sound System -- #
    if Get_IsSoundEnabled():
        # -- Set some Variables -- #
        Frequency = int(AudioFrequency)
        Size = int(AudioSize)
        Channels = int(AudioChannels)
        BufferSize = int(AudioBufferSize)

        pygame.mixer.init(Frequency, Size, Channels, BufferSize)

        pygame.init()
    else:
        pygame.init()

    if not pygame.mixer.get_init() and Get_IsSoundEnabled():
        sound.DisableSoundSystem = True

    # -- Initialize FastEvent -- #
    pygame.fastevent.init()

    # -- Set the Game Folder -- #
    GameFolder = open(".current_game", "r").read().rstrip()
    CurrentGame_Folder = GameFolder

    # -- Set the AppData Folder -- #
    if platform.system() == "Linux":
        TaiyouPath_AppDataFolder = "AppData/" + GameFolder

    elif platform.system() == "Windows":
        TaiyouPath_AppDataFolder = "AppData\\" + GameFolder

    taiyouMain.CurrentRes_W = 800
    taiyouMain.CurrentRes_H = 600

    taiyouMain.SetDisplay()

    InitializeGame()

def InitializeGame():
    global TaiyouPath_CorrectSlash
    global CurrentGame_Folder
    global TaiyouPath_AppDataFolder
    global TaiyouPath_CorrectAssetsFolder

    # -- Load Game Assets -- #
    GameFolder = open(".current_game", "r").read().rstrip()

    TaiyouPath_CorrectAssetsFolder = "{0}{1}".format(GameFolder, TaiyouPath_CorrectSlash)

    taiyouMain.SetGameObject(GameFolder)


#region return Game Infos Functions
def Get_GameSourceFolder():
    global CurrentGame_Folder
    if CurrentGame_Folder == "null":
        return ""
    return CurrentGame_Folder + "/Data"

def Get_MainGameModuleName(GameFolder):
    return "{0}{1}".format(GameFolder.replace("/", "."), ".MAIN")

#endregion


#region return IsEnabled Functions
def Get_IsSoundEnabled():
    return not sound.DisableSoundSystem

def Get_IsFontRenderingEnabled():
    return CONTENT_MANAGER.FontRenderingDisabled

#endregion
