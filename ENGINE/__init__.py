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
    return "2.5"
def Get_SpriteVersion():
    return "1.9"
def Get_SoundVersion():
    return "1.9"
def Get_RegistryVersion():
    return "1.7"
def Get_UtilsVersion():
    return "1.5"
def Get_GameObjVersion():
    return "2.4"
def Get_DeveloperConsoleVersion():
    return "1.8"
def Get_TaiyouUIVersion():
    return "2.5"


TaiyouGeneralVersion = float(Get_Version()) + float(Get_UtilsVersion()) + float(Get_RegistryVersion()) + float(Get_SpriteVersion()) + float(Get_SoundVersion()) + float(Get_GameObjVersion()) + float(Get_DeveloperConsoleVersion()) + float(Get_TaiyouUIVersion()) - 8.0


# -- Print Runtime Version -- #
print("TaiyouGameEngineRuntime version " + Get_Version())

# -- Imports --
from ENGINE import SPRITE as sprite
from ENGINE import SOUND as sound
from ENGINE import UTILS as utils
from ENGINE import REGISTRY as reg
from ENGINE import TaiyouUI
from ENGINE.TaiyouUI import DeveloperConsole as devel
from ENGINE import TaiyouUI as TaiyouUI
import os, pygame

# -- Current Game Variables --
CurrentGame_Title = "null"
CurrentGame_ID = "null"
CurrentGame_Version = "null"
CurrentGame_SourceFolder = "null"
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

# -- User -- #
UserName = ""
UserLanguage = ""

# -- Taiyou Paths -- #
TaiyouPath_AppDataFolder = "Taiyou/HOME/AppsData"
TaiyouPath_SystemPath = "Taiyou/SYSTEM/"
TaiyouPath_TaiyouConfigFile = TaiyouPath_SystemPath + "Taiyou.config"

def InitUserData():
    global UserName
    global UserLanguage

    print("Taiyou.InitUserData : Started")
    conf_file = open("Taiyou/HOME/meta.data")

    for x in conf_file:
        x = x.rstrip()
        if not x.startswith("#"):
            SplitedParms = x.split(":")

            if SplitedParms[0] == "Username":
                UserName = str(SplitedParms[1])
                print("Taiyou.InitUserData : Username was set to:[{0}]".format(UserName))

            if SplitedParms[0] == "Language":
                UserLanguage = str(SplitedParms[1])
                print("Taiyou.InitUserData : Language was set to:[{0}]".format(UserLanguage))

    # -- Create Folders -- #
    print("Taiyou.InitUserData : Creating default folders...")
    # -- Home Directory -- #
    os.makedirs("Taiyou/HOME/Screenshots",exist_ok=True) # -- Screenshots Folder
    os.makedirs("Taiyou/HOME/Webcache",exist_ok=True) # -- Webcache Folder
    os.makedirs("Taiyou/HOME/Webcache/UPDATER/", exist_ok=True)  # -- Webcache Folder
    os.makedirs("Taiyou/HOME/Records",exist_ok=True)  # -- Records Folder
    os.makedirs("Taiyou/HOME/Version",exist_ok=True)  # -- Version Folder
    os.makedirs("Taiyou/HOME/Cache",exist_ok=True)  # -- Cache Folder

    print("Taiyou.InitUserData : Done!")

    # -- Make current Version File -- #
    print("Taiyou.InitUserData : Writting modules version data...")
    LastModulesVersion = open("Taiyou/HOME/Version/TaiyouModules.data", "w")
    LastModulesVersion.write("TGE=" + Get_Version() + "\n")
    LastModulesVersion.write("SPRITE=" + Get_SpriteVersion() + "\n")
    LastModulesVersion.write("SOUND=" + Get_SoundVersion() + "\n")
    LastModulesVersion.write("REGISTRY=" + Get_RegistryVersion() + "\n")
    LastModulesVersion.write("UTILS=" + Get_UtilsVersion() + "\n")
    LastModulesVersion.write("GAME_OBJ=" + Get_GameObjVersion() + "\n")
    LastModulesVersion.write("DEVELOPER_CONSOLE=" + Get_DeveloperConsoleVersion() + "\n")
    LastModulesVersion.write("TAIYOU_UI=" + Get_TaiyouUIVersion())
    LastModulesVersion.close()
    print("Taiyou.InitUserData : Done!")


def LoadFolderMetaData(GameFolderDir):
    global CurrentGame_Title
    global CurrentGame_ID
    global CurrentGame_Version
    global CurrentGame_SourceFolder
    global CurrentGame_Folder
    global TaiyouPath_AppDataFolder
    global TaiyouGeneralVersion

    print("Taiyou.Runtime.LoadFolderMetaData : Loading Taiyou Options file...")
    InfFileLocation = GameFolderDir + "/meta.data"

    inf_file = open(InfFileLocation, "r")

    CurrentGame_Folder = GameFolderDir

    LineIndex = 0
    for x in inf_file:
        LineIndex += 1
        if LineIndex == 1:
            CurrentGame_Title = x.rstrip()
            print("Taiyou.Runtime.LoadFolderMetaData : Game Title[{0}]".format(CurrentGame_Title))
        
        if LineIndex == 2:
            CurrentGame_ID = x.rstrip()
            print("Taiyou.Runtime.LoadFolderMetaData : Game ID[{0}]".format(CurrentGame_ID))
        
        if LineIndex == 3:
            CurrentGame_Version = x.rstrip()
            print("Taiyou.Runtime.LoadFolderMetaData : Game Version[{0}]".format(CurrentGame_Version))

        if LineIndex == 4:
            CurrentGame_SourceFolder = GameFolderDir + "/" + x.rstrip()
            print("Taiyou.Runtime.LoadFolderMetaData : Game Source Folder[{0}]".format(CurrentGame_SourceFolder))

    # -- Create Temporary File -- #
    print("Taiyou.Runtime.LoadFolderMetaData : Creating Temporary Files...")

    f = open(TaiyouPath_SystemPath + ".LastOpenedGame", "w")
    f.write(str(CurrentGame_ID))
    f.write(str(CurrentGame_Folder))
    f.write(str(CurrentGame_Title))
    f.write(str(CurrentGame_Version))
    f.write(str(CurrentGame_SourceFolder))
    f.close()

    print("Taiyou.Runtime.LoadFolderMetaData : Done!")

    # -- Make Directories -- #
    print("Taiyou.Runtime.LoadFolderMetaData : Creating AppData Folder...")

    utils.Directory_MakeDir(Get_GlobalAppDataFolder())

    print("Taiyou.Runtime.LoadFolderMetaData : Done!")

    print("Taiyou.Runtime.LoadFolderMetaData : Metadata Loading complete.")

def InitEngine():
    global TaiyouPath_AppDataFolder
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

    print("\n\n\n# -- General Taiyou Runtime Version -- #\n\nThis version is the sum of all modules version, so it is 'The Taiyou Version'.\nGeneral Version is [" + str(utils.FormatNumber(TaiyouGeneralVersion)) + "/{0}].\n\n\n".format(str(TaiyouGeneralVersion)))
    conf_file = open(TaiyouPath_TaiyouConfigFile)

    for x in conf_file:
        x = x.rstrip()
        SplitedParms = x.split(":")

        if not x.startswith("#"):
            # -- Disable Font Rendering -- #
            if SplitedParms[0] == "DisableFontRendering":
                if SplitedParms[1] == "True":
                    sprite.FontRenderingDisabled = True
                else:
                    sprite.FontRenderingDisabled = False

                print("Taiyou.Runtime.InitEngine : Disable font rendering set to:" + str(sprite.FontRenderingDisabled ))

            # -- Disable Sprite Rendering -- #
            if SplitedParms[0] == "DisableSpriteRendering":
                if SplitedParms[1] == "True":
                    sprite.SpriteRenderingDisabled = True
                else:
                    sprite.SpriteRenderingDisabled = False

                print("Taiyou.Runtime.InitEngine : Disable sprite rendering set to:" + str(sprite.SpriteRenderingDisabled))

            # -- Disable Rectangle Rendering -- #
            if SplitedParms[0] == "DisableRectangleRendering":
                if SplitedParms[1] == "True":
                    sprite.RectangleRenderingDisabled = True
                else:
                    sprite.RectangleRenderingDisabled = False

                print("Taiyou.Runtime.InitEngine : Disable rectangle rendering set to:" + str(sprite.RectangleRenderingDisabled))

            # -- Disable Sprite Transparency -- #
            if SplitedParms[0] == "DisableSpriteTransparency":
                if SplitedParms[1] == "True":
                    sprite.SpriteTransparency = True
                else:
                    sprite.SpriteTransparency = False

                print("Taiyou.Runtime.InitEngine : Disable sound system set to:" + str(sprite.SpriteTransparency))

            # -- Disable Sound System -- #
            if SplitedParms[0] == "DisableSoundSystem":
                if SplitedParms[1] == "True":
                    sound.DisableSoundSystem = True
                else:
                    sound.DisableSoundSystem = False

                print("Taiyou.Runtime.InitEngine : Disable sound system set to:" + str(sound.DisableSoundSystem))

            # -- AppData Folder Path -- #
            if SplitedParms[0] == "AppDataFolder":
                TaiyouPath_AppDataFolder = SplitedParms[1].rstrip()

                print("Taiyou.Runtime.InitEngine : TaiyouAppDataFolder set to:" + str(TaiyouPath_AppDataFolder))

            # -- SDL Option: Video Driver -- #
            if SplitedParms[0] == "VideoDriver":
                VideoDriver = SplitedParms[1].rstrip()

                print("Taiyou.Runtime.InitEngine : Video Driver was set to:" + str(VideoDriver))

            # -- SDL Option: Audio Driver -- #
            if SplitedParms[0] == "AudioDriver":
                AudioDriver = SplitedParms[1].rstrip()

                print("Taiyou.Runtime.InitEngine : Audio Driver was set to:" + str(AudioDriver))

            # -- SoundSystem: Audio Device Frequency -- #
            if SplitedParms[0] == "AudioFrequency":
                AudioFrequency = int(SplitedParms[1].rstrip())

                print("Taiyou.Runtime.InitEngine : Audio Frequency was set to:" + str(AudioFrequency))

            # -- SoundSystem: Audio Device Frame Size -- #
            if SplitedParms[0] == "AudioSize":
                AudioSize = int(SplitedParms[1].rstrip())

                print("Taiyou.Runtime.InitEngine : Audio Size was set to:" + str(AudioSize))

            # -- SoundSystem: Audio Device Audio Channels -- #
            if SplitedParms[0] == "AudioChannels":
                AudioChannels = int(SplitedParms[1].rstrip())

                print("Taiyou.Runtime.InitEngine : Audio Channels was set to:" + str(AudioChannels))

            # -- SoundSystem: Audio Device Buffer Size -- #
            if SplitedParms[0] == "AudioBufferSize":
                AudioBufferSize = int(SplitedParms[1].rstrip())

                print("Taiyou.Runtime.InitEngine : Audio Buffer Size was set to:" + str(AudioBufferSize))

            # -- Run in Fullscreen -- #
            if SplitedParms[0] == "RunInFullScreen":
                if SplitedParms[1].rstrip() == "True":
                    RunInFullScreen = True
                elif SplitedParms[1].rstrip() == "False":
                    RunInFullScreen = False
                else:
                    RunInFullScreen = False

                print("Taiyou.Runtime.InitEngine : Run in Fullscreen was set to:" + str(RunInFullScreen))

            # -- SDL Option: Center Window -- #
            if SplitedParms[0] == "VideoX11_CenterWindow":
                if SplitedParms[1].rstrip() == "True":
                    VideoX11CenterWindow = True
                elif SplitedParms[1].rstrip() == "False":
                    VideoX11CenterWindow = False
                else:
                    VideoX11CenterWindow = False

                print("Taiyou.Runtime.InitEngine : VideoX11CenterWindow was set to:" + str(VideoX11CenterWindow))

            # -- SDL Option: DGA Mouse -- #
            if SplitedParms[0] == "VideoX11_DGAMouse":
                if SplitedParms[1].rstrip() == "True":
                    VideoX11DGAMouse = True
                elif SplitedParms[1].rstrip() == "False":
                    VideoX11DGAMouse = False
                else:
                    VideoX11DGAMouse = False

                print("Taiyou.Runtime.InitEngine : VideoX11DGAMouse was set to:" + str(VideoX11DGAMouse))

            # -- SDL Option: YUV Hardware Acelleration -- #
            if SplitedParms[0] == "VideoX11_YUV_HWACCEL":
                if SplitedParms[1].rstrip() == "True":
                    VideoX11YUV_HWACCEL = True
                elif SplitedParms[1].rstrip() == "False":
                    VideoX11YUV_HWACCEL = False
                else:
                    VideoX11YUV_HWACCEL = False

                print("Taiyou.Runtime.InitEngine : VideoX11YUV_HWACCEL was set to:" + str(VideoX11YUV_HWACCEL))

            # -- TaiyouUi: Autoboot Game Folder -- #
            if SplitedParms[0] == "AutoBoot":
                TaiyouUI.CurrentMenuScreen = 4
                TaiyouUI.loadingScreen.GameFolderToOpen = SplitedParms[1].rstrip()

                print("Taiyou.Runtime.InitEngine : AutoBoot Game Folder was set to:" + str(TaiyouUI.loadingScreen.GameFolderToOpen))

            # -- SDL Option: Mouse Driver -- #
            if SplitedParms[0] == "InputMouseDriver":
                InputMouseDriver = SplitedParms[1].rstrip()

                print("Taiyou.Runtime.InitEngine : InputMouseDriver was set to:" + str(InputMouseDriver))

            # -- SDL Option: Disable Mouse -- #
            if SplitedParms[0] == "InputDisableMouse":
                if SplitedParms[1].rstrip() == "True":
                    InputDisableMouse = True
                elif SplitedParms[1].rstrip() == "False":
                    InputDisableMouse = False
                else:
                    InputDisableMouse = False

                print("Taiyou.Runtime.InitEngine : InputDisableMouse was set to:" + str(InputDisableMouse))

            # -- Ignore all SDL Parameters -- #
            if SplitedParms[0] == "IgnoreSDL2Parameters":
                if SplitedParms[1].rstrip() == "True":
                    IgnoreSDL2Parameters = True
                elif SplitedParms[1].rstrip() == "False":
                    IgnoreSDL2Parameters = False
                else:
                    IgnoreSDL2Parameters = False

                print("Taiyou.Runtime.InitEngine : IgnoreSDL2Parameters was set to:" + str(IgnoreSDL2Parameters))

            # -- Sprite: SmoothScaleBackend Backend -- #
            if SplitedParms[0] == "SmoothScaleBackend":
                SmoothScaleTransform = SplitedParms[1].rstrip()

                print("Taiyou.Runtime.InitEngine : SmoothScaleBackend was set to:" + str(SmoothScaleTransform))

            # -- Pygame: FastEvent -- #
            if SplitedParms[0] == "FastEvent":
                if SplitedParms[1].rstrip() == "True":
                    PygameFastEvent = True
                elif SplitedParms[1].rstrip() == "False":
                    PygameFastEvent = False
                else:
                    PygameFastEvent = False

                print("Taiyou.Runtime.InitEngine : FastEvent was set to:" + str(PygameFastEvent))

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

    InitUserData()

# -- Reset Game Folder Variables -- #
def CloseGameFolder():
    global CurrentGame_Title
    global CurrentGame_ID
    global CurrentGame_Version
    global CurrentGame_SourceFolder
    global CurrentGame_Folder

    print("TGE.RestartGameFolder : Removing all LoadedGame Variables and Temporary files...")
    CurrentGame_Title = "null"
    CurrentGame_ID = "null"
    CurrentGame_Version = "null"
    CurrentGame_SourceFolder = "null"
    CurrentGame_Folder = "null"
    os.remove(TaiyouPath_SystemPath + ".LastOpenedGame")


#region return Game Infos Functions
def Get_GameTitle():
    global CurrentGame_Title
    return CurrentGame_Title

def Get_GameID():
    global CurrentGame_ID
    return CurrentGame_ID

def Get_GameVersion():
    global CurrentGame_Version
    return CurrentGame_Version

def Get_GameSourceFolder():
    global CurrentGame_SourceFolder
    if CurrentGame_SourceFolder == "null":
        return "Taiyou/SYSTEM/SOURCE"
    return CurrentGame_SourceFolder

def Get_GameFolder():
    global CurrentGame_Folder
    return CurrentGame_Folder

def Get_GlobalAppDataFolder():
    global CurrentGame_ID
    global CurrentGame_Version
    global TaiyouPath_AppDataFolder
    return TaiyouPath_AppDataFolder + "{0}/{1}/".format(str(CurrentGame_ID), str(CurrentGame_Version))

def Get_MainGameModuleName(GameFolder):
    return "{0}{1}".format(GameFolder.replace("/", "."), ".MAIN")

def GetData_InGameMetaDataFile(metaDataFilePath, MetaPartToReturn):
    # -- Read Meta Data File -- #
    LineNumber = 0

    with open(metaDataFilePath) as file_in:
        for line in file_in:
            LineNumber += 1

            if LineNumber == 0:  # -- Game Name
                if MetaPartToReturn == "GAME_NAME":
                    return line

            if LineNumber == 1:  # -- Game ID
                if MetaPartToReturn == "GAME_ID":
                    return line

            if LineNumber == 2:  # -- Game Version
                if MetaPartToReturn == "GAME_VERSION":
                    return line

            if LineNumber == 3:  # -- Game Source Folder
                if MetaPartToReturn == "GAME_SOURCE_FOLDER":
                    return line

            if LineNumber == 4:  # -- Game Folder Name
                if MetaPartToReturn == "GAME_FOLDER":
                    return line.rstrip()

            if LineNumber == 5:  # -- Animation Banner Frames
                if MetaPartToReturn == "GAME_ANIMATION_BANNER_FRAMES":
                    return int(line)

            if LineNumber == 6:  # -- Animation Banner Frames Delay
                if MetaPartToReturn == "GAME_ANIMATION_BANNER_DELAY":
                    return int(line)


#endregion


#region return IsEnabled Functions
def Get_IsSoundEnabled():
    return not sound.DisableSoundSystem

def Get_IsFontRenderingEnabled():
    return sprite.FontRenderingDisabled

#endregions


#region return User Information
def Get_UserLanguage():
    return UserLanguage

def Get_Username():
    return UserName

#endregion
