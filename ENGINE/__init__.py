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
    return "2.3"
def Get_SpriteVersion():
    return "1.7"
def Get_SoundVersion():
    return "1.7"
def Get_RegistryVersion():
    return "1.4"
def Get_UtilsVersion():
    return "1.5"
def Get_GameObjVersion():
    return "2.2"
def Get_DeveloperConsoleVersion():
    return "1.5"
def Get_TaiyouUIVersion():
    return "2.2"

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
import os

# -- Variables --
CurrentGame_Title = "null"
CurrentGame_ID = "null"
CurrentGame_Version = "null"
CurrentGame_SourceFolder = "null"
CurrentGame_Folder = "null"
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
 
# -- User -- #
UserName = ""
UserLanguage = ""
UserFormatCountry = ""


TaiyouAppDataFolder = "Taiyou/HOME/AppsData"

def InitUserData():
    global UserName
    global UserLanguage
    global UserFormatCountry

    conf_file = open("Taiyou/HOME/meta.data","r")
    print("Taiyou.InitUserData : Started")

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

            if SplitedParms[0] == "Format":
                UserFormatCountry = str(SplitedParms[1])
                print("Taiyou.InitUserData : Format Type was set to:[{0}]".format(UserFormatCountry))

    os.makedirs("Taiyou/HOME/Screenshots",exist_ok=True) # -- Screenshots Folder
    os.makedirs("Taiyou/HOME/Webcache",exist_ok=True) # -- Webcache Folder
    os.makedirs("Taiyou/HOME/Webcache/UPDATER/", exist_ok=True)  # -- Webcache Folder
    os.makedirs("Taiyou/HOME/Records",exist_ok=True)  # -- Records Folder
    os.makedirs("Taiyou/HOME/Version",exist_ok=True)  # -- Version Folder
    os.makedirs("Taiyou/HOME/Cache",exist_ok=True)  # -- Cache Folder

    # -- Make current Version File -- #
    LastTaiyouVersionFile = open("Taiyou/HOME/Version/TaiyouModules.data", "w")
    LastTaiyouVersionFile.write("TGE=" + Get_Version() + "\n")
    LastTaiyouVersionFile.write("SPRITE=" + Get_SpriteVersion() + "\n")
    LastTaiyouVersionFile.write("SOUND=" + Get_SoundVersion() + "\n")
    LastTaiyouVersionFile.write("REGISTRY=" + Get_RegistryVersion() + "\n")
    LastTaiyouVersionFile.write("UTILS=" + Get_UtilsVersion() + "\n")
    LastTaiyouVersionFile.write("GAME_OBJ=" + Get_GameObjVersion() + "\n")
    LastTaiyouVersionFile.write("DEVELOPER_CONSOLE=" + Get_DeveloperConsoleVersion() + "\n")
    LastTaiyouVersionFile.write("TAIYOU_UI=" + Get_TaiyouUIVersion())
    LastTaiyouVersionFile.close()


def LoadFolderMetaData(GameFolderDir):
    global CurrentGame_Title
    global CurrentGame_ID
    global CurrentGame_Version
    global CurrentGame_SourceFolder
    global CurrentGame_Folder
    global TaiyouAppDataFolder
    global TaiyouGeneralVersion

    print("Taiyou.Runtime.LoadFolderMetaData : Loading Taiyou Options file...")
    InfFileLocation = GameFolderDir + "/meta.data"

    inf_file = open(InfFileLocation,"r")

    CurrentGame_Folder = GameFolderDir

    LineIndex = 0
    for x in inf_file:
        LineIndex += 1
        if LineIndex == 1:
            CurrentGame_Title = x.rstrip()
            print("Taiyou.Runtime.LoadFolderMetaData : GameTitle[" + CurrentGame_Title + "]")
        
        if LineIndex == 2:
            CurrentGame_ID = x.rstrip()
            print("Taiyou.Runtime.LoadFolderMetaData : GameID[" + CurrentGame_ID + "]")
        
        if LineIndex == 3:
            CurrentGame_Version = x.rstrip()
            print("Taiyou.Runtime.LoadFolderMetaData : GameVersion[" + CurrentGame_Version + "]")

        if LineIndex == 4:
            CurrentGame_SourceFolder = GameFolderDir + "/" +  x.rstrip()
            print("Taiyou.Runtime.LoadFolderMetaData : GameSourceFolder[" + CurrentGame_SourceFolder + "]")


    print("Taiyou.Runtime.LoadFolderMetaData : Creating Temporary Files...")

    # -- Create Temporary File -- #
    f = open(".OpenedGameInfos", "w")
    f.write(str(CurrentGame_ID))
    f.write(str(CurrentGame_Folder))
    f.write(str(CurrentGame_Title))
    f.write(str(CurrentGame_Version))
    f.write(str(CurrentGame_SourceFolder))
    f.close()


    # -- Make Directories -- #
    utils.Directory_MakeDir(Get_GlobalAppDataFolder())


    print("Taiyou.Runtime.LoadFolderMetaData : Metadata Loading complete.")

def InitEngine():
    global TaiyouAppDataFolder
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

    print("\n\n\n# -- General Taiyou Runtime Version -- #\n\nThis version is the sum of all modules version, so it is 'The Taiyou Version'.\nGeneral Version is [" + str(utils.FormatNumber(TaiyouGeneralVersion)) + "/{0}].\n\n\n".format(str(TaiyouGeneralVersion)))
    conf_file = open("Taiyou.config","r")

    for x in conf_file:
        x = x.rstrip()
        SplitedParms = x.split(":")

        if not x.startswith("#"):
            if SplitedParms[0] == "DisableFontRendering":
                if SplitedParms[1] == "True":
                    sprite.FontRenderingDisabled = True
                else:
                    sprite.FontRenderingDisabled = False

                print("Taiyou.Runtime.InitEngine : Disable font rendering set to:" + str(sprite.FontRenderingDisabled ))

            if SplitedParms[0] == "DisableSpriteRendering":
                if SplitedParms[1] == "True":
                    sprite.SpriteRenderingDisabled = True
                else:
                    sprite.SpriteRenderingDisabled = False

                print("Taiyou.Runtime.InitEngine : Disable sprite rendering set to:" + str(sprite.SpriteRenderingDisabled))

            if SplitedParms[0] == "DisableRectangleRendering":
                if SplitedParms[1] == "True":
                    sprite.RectangleRenderingDisabled = True
                else:
                    sprite.RectangleRenderingDisabled = False

                print("Taiyou.Runtime.InitEngine : Disable rectangle rendering set to:" + str(sprite.RectangleRenderingDisabled))

            if SplitedParms[0] == "DisableSpriteTransparency":
                if SplitedParms[1] == "True":
                    sprite.SpriteTransparency = True
                else:
                    sprite.SpriteTransparency = False

                print("Taiyou.Runtime.InitEngine : Disable sound system set to:" + str(sprite.SpriteTransparency))

            if SplitedParms[0] == "DisableSoundSystem":
                if SplitedParms[1] == "True":
                    sound.DisableSoundSystem = True
                else:
                    sound.DisableSoundSystem = False

                print("Taiyou.Runtime.InitEngine : Disable sound system set to:" + str(sound.DisableSoundSystem))

            if SplitedParms[0] == "AppDataFolder":
                TaiyouAppDataFolder = SplitedParms[1].rstrip()

                print("Taiyou.Runtime.InitEngine : TaiyouAppDataFolder set to:" + str(SplitedParms[1].rstrip()))

            if SplitedParms[0] == "VideoDriver":
                VideoDriver = SplitedParms[1].rstrip()

                print("Taiyou.Runtime.InitEngine : Video Driver was set to:" + str(SplitedParms[1].rstrip()))

            if SplitedParms[0] == "AudioDriver":
                AudioDriver = SplitedParms[1].rstrip()

                print("Taiyou.Runtime.InitEngine : Audio Driver was set to:" + str(SplitedParms[1].rstrip()))

            if SplitedParms[0] == "AudioFrequency":
                AudioFrequency = int(SplitedParms[1].rstrip())

                print("Taiyou.Runtime.InitEngine : Audio Frequency was set to:" + str(SplitedParms[1].rstrip()))

            if SplitedParms[0] == "AudioSize":
                AudioSize = int(SplitedParms[1].rstrip())

                print("Taiyou.Runtime.InitEngine : Audio Size was set to:" + str(SplitedParms[1].rstrip()))

            if SplitedParms[0] == "AudioChannels":
                AudioChannels = int(SplitedParms[1].rstrip())

                print("Taiyou.Runtime.InitEngine : Audio Channels was set to:" + str(SplitedParms[1].rstrip()))

            if SplitedParms[0] == "AudioBufferSize":
                AudioBufferSize = int(SplitedParms[1].rstrip())

                print("Taiyou.Runtime.InitEngine : Audio Buffer Size was set to:" + str(SplitedParms[1].rstrip()))

            if SplitedParms[0] == "RunInFullScreen":
                if SplitedParms[1].rstrip() == "True":
                    RunInFullScreen = True
                elif SplitedParms[1].rstrip() == "False":
                    RunInFullScreen = False
                else:
                    RunInFullScreen = False

                print("Taiyou.Runtime.InitEngine : Run in Fullscreen was set to:" + str(SplitedParms[1].rstrip()))

            if SplitedParms[0] == "VideoX11_CenterWindow":
                if SplitedParms[1].rstrip() == "True":
                    VideoX11CenterWindow = True
                elif SplitedParms[1].rstrip() == "False":
                    VideoX11CenterWindow = False
                else:
                    VideoX11CenterWindow = False

                print("Taiyou.Runtime.InitEngine : VideoX11CenterWindow was set to:" + str(SplitedParms[1].rstrip()))

            if SplitedParms[0] == "VideoX11_DGAMouse":
                if SplitedParms[1].rstrip() == "True":
                    VideoX11DGAMouse = True
                elif SplitedParms[1].rstrip() == "False":
                    VideoX11DGAMouse = False
                else:
                    VideoX11DGAMouse = False

                print("Taiyou.Runtime.InitEngine : VideoX11DGAMouse was set to:" + str(SplitedParms[1].rstrip()))

            if SplitedParms[0] == "VideoX11_YUV_HWACCEL":
                if SplitedParms[1].rstrip() == "True":
                    VideoX11YUV_HWACCEL = True
                elif SplitedParms[1].rstrip() == "False":
                    VideoX11YUV_HWACCEL = False
                else:
                    VideoX11YUV_HWACCEL = False

                print("Taiyou.Runtime.InitEngine : VideoX11YUV_HWACCEL was set to:" + str(SplitedParms[1].rstrip()))

            if SplitedParms[0] == "AutoBootGameFolder":
                TaiyouUI.CurrentMenuScreen = 4
                TaiyouUI.loadingScreen.GameFolderToOpen = SplitedParms[1].rstrip()

                print("Taiyou.Runtime.InitEngine : AutoBoot Game Folder was set to:" + str(SplitedParms[1].rstrip()))

            if SplitedParms[0] == "InputMouseDriver":
                InputMouseDriver = SplitedParms[1].rstrip()

                print("Taiyou.Runtime.InitEngine : InputMouseDriver was set to:" + str(SplitedParms[1].rstrip()))

            if SplitedParms[0] == "InputDisableMouse":
                if SplitedParms[1].rstrip() == "True":
                    InputDisableMouse = True
                elif SplitedParms[1].rstrip() == "False":
                    InputDisableMouse = False
                else:
                    InputDisableMouse = False

                print("Taiyou.Runtime.InitEngine : InputDisableMouse was set to:" + str(SplitedParms[1].rstrip()))

            if SplitedParms[0] == "IgnoreSDL2Parameters":
                if SplitedParms[1].rstrip() == "True":
                    IgnoreSDL2Parameters = True
                elif SplitedParms[1].rstrip() == "False":
                    IgnoreSDL2Parameters = False
                else:
                    IgnoreSDL2Parameters = False

                print("Taiyou.Runtime.InitEngine : IgnoreSDL2Parameters was set to:" + str(SplitedParms[1].rstrip()))


#IgnoreDriversParameters
    
    if not IgnoreSDL2Parameters:
        # -- Set the Enviroments Variables -- #
        os.environ['SDL_VIDEODRIVER'] = str(VideoDriver) # -- Set the Video Driver
        os.environ['SDL_AUDIODRIVER'] = str(AudioDriver) # -- Set the Audio Driver

        # -- Set Input Enviroments -- #
        os.environ['SDL_MOUSEDRV'] = str(InputMouseDriver) # -- Set the Mouse Driver
        os.environ['SDL_NOMOUSE'] = str(InputDisableMouse) # -- Set the Mouse Driver



        # -- Set X11 Enviroment Keys -- #
        if VideoDriver == "x11":
            if VideoX11CenterWindow:
                os.environ['SDL_VIDEO_CENTERED'] = "True"# -- Set the Centered Window

            if VideoX11DGAMouse:
                os.environ['SDL_VIDEO_X11_DGAMOUSE'] = "True"# -- Set the DGA Mouse Parameter

            if VideoX11YUV_HWACCEL:
                os.environ['SDL_VIDEO_YUV_HWACCEL'] = "True"# -- Set the YUV HWACCEL Parameter

    else:
        print("Taiyou.Runtime.InitEngine : SDL2 Parameters has been disabled")


    InitUserData()

def CloseGameFolder():
    global CurrentGame_Title
    global CurrentGame_ID
    global CurrentGame_Version
    global CurrentGame_SourceFolder
    global CurrentGame_Folder

    CurrentGame_Title = "null"
    CurrentGame_ID = "null"
    CurrentGame_Version = "null"
    CurrentGame_SourceFolder = "null"
    CurrentGame_Folder = "null"
    os.remove(".OpenedGameInfos")


# -- Return Infos -- #
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
    global TaiyouAppDataFolder
    return TaiyouAppDataFolder + "{0}/{1}/".format(str(CurrentGame_ID), str(CurrentGame_Version))

def Get_IsSoundEnabled():
    return not sound.DisableSoundSystem

def Get_IsFontRenderingEnabled():
    return sprite.FontRenderingDisabled

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
