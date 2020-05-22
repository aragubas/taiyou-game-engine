#!/usr/bin/python3.6
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
    return "1.7"
def Get_SpriteVersion():
    return "1.6"
def Get_SoundVersion():
    return "1.5"
def Get_RegistryVersion():
    return "1.4"
def Get_UtilsVersion():
    return "1.5"
def Get_GameObjVersion():
    return "2.0"
def Get_DeveloperConsoleVersion():
    return "1.5"
def Get_TaiyouUIVersion():
    return "1.8"

TaiyouGeneralVersion = float(Get_Version()) + float(Get_UtilsVersion()) + float(Get_RegistryVersion()) + float(Get_SpriteVersion()) + float(Get_SoundVersion()) + float(Get_GameObjVersion()) + float(Get_DeveloperConsoleVersion()) + float(Get_TaiyouUIVersion()) - 8.0


# -- Print Runtime Version -- #
print("TaiyouGameEngineRuntime version " + Get_Version())

# -- Imports --
from ENGINE import SPRITE as sprite
from ENGINE import SOUND as sound
from ENGINE import UTILS as utils
from ENGINE import REGISTRY as reg
from ENGINE.TaiyouUI import DeveloperConsole as devel
import os

# -- Variables --
CurrentGame_Title = ""
CurrentGame_ID = ""
CurrentGame_Version = ""
CurrentGame_SourceFolder = ""
CurrentGame_Folder = ""
IsGameRunning = False
VideoDriver = "x11"
AudioDriver = "alsa"
DiskAudioFile = "output.raw"
DiskAudioDelay = "150"
AudioFrequency = 96000
AudioSize = -16
AudioChannels = 2
AudioBufferSize = 500




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
    os.makedirs("Taiyou/HOME/Records",exist_ok=True)  # -- Records Folder
    os.makedirs("Taiyou/HOME/Version",exist_ok=True)  # -- Version Folder
    os.makedirs("Taiyou/HOME/Applets",exist_ok=True)  # -- Applets Folder

    # -- Make some files -- #
    if not os.path.isfile("Taiyou/HOME/Version/Taiyou.data"):
        LastTaiyouVersionFile = open("Taiyou/HOME/Version/Taiyou.data", "w")
        LastTaiyouVersionFile.write(str(TaiyouGeneralVersion))
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
    if not os.path.exists(Get_GlobalAppDataFolder()):
        os.makedirs(Get_GlobalAppDataFolder())


    print("Taiyou.Runtime.LoadFolderMetaData : Metadata Loading complete.")

def InitEngine():
    global TaiyouAppDataFolder
    global VideoDriver
    global AudioDriver
    global DiskAudioFile
    global DiskAudioDelay
    global AudioSize
    global AudioBufferSize
    global AudioChannels
    global AudioFrequency

    print("\n\n\n# -- General Taiyou Runtime Version -- #\n\nThis version is the sum of all modules version, so it is 'The Taiyou Version'.\nGeneral Version is [" + str(utils.FormatNumber(TaiyouGeneralVersion)) + "].\n\n\n")
    conf_file = open("Taiyou.config","r")

    for x in conf_file:
        x = x.rstrip()
        SplitedParms = x.split(":")

        if SplitedParms[0] == "DisableFontRendering":
            if SplitedParms[1] == "True":
                Value = True
            else:
                Value = False

            sprite.FontRenderingDisabled = Value
            print("Taiyou.Runtime.OpenGameFolder : Disable font rendering set to:" + str(Value))
        
        if SplitedParms[0] == "DisableSpriteRendering":
            if SplitedParms[1] == "True":
                Value = True
            else:
                Value = False

            sprite.SpriteRenderingDisabled = Value
            print("Taiyou.Runtime.OpenGameFolder : Disable sprite rendering set to:" + str(Value))


        if SplitedParms[0] == "DisableRectangleRendering":
            if SplitedParms[1] == "True":
                Value = True
            else:
                Value = False

            sprite.RectangleRenderingDisabled = Value
            print("Taiyou.Runtime.OpenGameFolder : Disable rectangle rendering set to:" + str(Value))

        if SplitedParms[0] == "DisableSpriteTransparency":
            if SplitedParms[1] == "True":
                Value = True
            else:
                Value = False

            sprite.SpriteTransparency = Value
            print("Taiyou.Runtime.OpenGameFolder : Disable sound system set to:" + str(Value))

        if SplitedParms[0] == "DisableSoundSystem":
            if SplitedParms[1] == "True":
                Value = True
            else:
                Value = False

            sound.DisableSoundSystem = Value
            print("Taiyou.Runtime.OpenGameFolder : Disable sound system set to:" + str(Value))

        if SplitedParms[0] == "AppDataFolder":
            TaiyouAppDataFolder = SplitedParms[1].rstrip()

            print("Taiyou.Runtime.OpenGameFolder : TaiyouAppDataFolder set to:" + str(SplitedParms[1].rstrip()))

        if SplitedParms[0] == "VideoDriver":
            VideoDriver = SplitedParms[1].rstrip()

            print("Taiyou.Runtime.OpenGameFolder : Video Driver was set to:" + str(SplitedParms[1].rstrip()))

        if SplitedParms[0] == "AudioDriver":
            AudioDriver = SplitedParms[1].rstrip()

            print("Taiyou.Runtime.OpenGameFolder : Audio Driver was set to:" + str(SplitedParms[1].rstrip()))

        if SplitedParms[0] == "DiskAudioFile":
            DiskAudioFile = SplitedParms[1].rstrip()

            print("Taiyou.Runtime.OpenGameFolder : Disk Audio File was set to:" + str(SplitedParms[1].rstrip()))

        if SplitedParms[0] == "DiskAudioDelay":
            DiskAudioDelay = SplitedParms[1].rstrip()

            print("Taiyou.Runtime.OpenGameFolder : Disk Audio Delay was set to:" + str(SplitedParms[1].rstrip()))

        if SplitedParms[0] == "AudioFrequency":
            AudioFrequency = int(SplitedParms[1].rstrip())

            print("Taiyou.Runtime.OpenGameFolder : Audio Frequency was set to:" + str(SplitedParms[1].rstrip()))

        if SplitedParms[0] == "AudioSize":
            AudioSize = int(SplitedParms[1].rstrip())

            print("Taiyou.Runtime.OpenGameFolder : Audio Size was set to:" + str(SplitedParms[1].rstrip()))

        if SplitedParms[0] == "AudioChannels":
            AudioChannels = int(SplitedParms[1].rstrip())

            print("Taiyou.Runtime.OpenGameFolder : Audio Channels was set to:" + str(SplitedParms[1].rstrip()))

        if SplitedParms[0] == "AudioBufferSize":
            AudioBufferSize = int(SplitedParms[1].rstrip())

            print("Taiyou.Runtime.OpenGameFolder : Audio Buffer Size was set to:" + str(SplitedParms[1].rstrip()))






    # -- Set the Video Driver -- #
    os.environ['SDL_VIDEODRIVER'] = VideoDriver
    os.environ['SDL_AUDIODRIVER'] = AudioDriver

    if AudioDriver == "disk":
        os.environ['SDL_DISKAUDIOFILE'] = DiskAudioFile
        os.environ['SDL_AUDIODRIVER'] = DiskAudioDelay

    InitUserData()

def CloseGameFolder():
    global CurrentGame_Title
    global CurrentGame_ID
    global CurrentGame_Version
    global CurrentGame_SourceFolder
    global CurrentGame_Folder

    CurrentGame_Title = ""
    CurrentGame_ID = ""
    CurrentGame_Version = ""
    CurrentGame_SourceFolder = ""
    CurrentGame_Folder = ""
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
    return sound.DisableSoundSystem

def Get_IsFontRenderingEnabled():
    return sprite.FontRenderingDisabled
