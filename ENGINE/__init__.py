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

# -- Imports --
from ENGINE import SPRITE as sprite
from ENGINE import SOUND as sound

print("TaiyouGameEngineRuntime version 1.1")

# -- Variables --
CurrentGame_Title = ""
CurrentGame_ID = ""
CurrentGame_Version = ""
CurrentGame_SourceFolder = ""
CurrentGame_Folder = ""


def OpenGameFolder(GameFolderDir):
    global CurrentGame_Title
    global CurrentGame_ID
    global CurrentGame_Version
    global CurrentGame_SourceFolder
    global CurrentGame_Folder

    print("Taiyou.Runtime.OpenGameFolder : Loading inf file...")
    InfFileLocation = GameFolderDir + "/meta.data"

    inf_file = open(InfFileLocation,"r")

    CurrentGame_Folder = GameFolderDir

    LineIndex = 0
    for x in inf_file:
        LineIndex += 1
        if LineIndex == 1:
            CurrentGame_Title = x.rstrip()
            print("Taiyou.Runtime.OpenGameFolder : GameTitle[" + CurrentGame_Title + "]")
        
        if LineIndex == 2:
            CurrentGame_ID = x.rstrip()
            print("Taiyou.Runtime.OpenGameFolder : GameID[" + CurrentGame_ID + "]")
        
        if LineIndex == 3:
            CurrentGame_Version = x.rstrip()
            print("Taiyou.Runtime.OpenGameFolder : GameVersion[" + CurrentGame_Version + "]")
        
        if LineIndex == 4:
            CurrentGame_SourceFolder = GameFolderDir + "/" +  x.rstrip()
            print("Taiyou.Runtime.OpenGameFolder : GameSourceFolder[" + CurrentGame_SourceFolder + "]")
        

    print("Taiyou.Runtime.OpenGameFolder : inf file loading complete, Loading Assets...")

    sprite.LoadSpritesInFolder(CurrentGame_SourceFolder)
    sound.LoadAllSounds(CurrentGame_SourceFolder)
    print("Taiyou.Runtime.OpenGameFolder : Game Loading complete, Loading Engine Configuration...")

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

