#!/usr/bin/env python3.7
# -- Imports --
import ENGINE.SPRITE as sprite
import ENGINE.SOUND as sound

print("TaiyouGameEngine Runtime version 1.0")

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

    print("OpenGameFolder : Loading inf file...")
    InfFileLocation = GameFolderDir + "/meta.data"

    inf_file = open(InfFileLocation,"r")


    CurrentGame_Folder = GameFolderDir

    LineIndex = 0
    for x in inf_file:
        LineIndex += 1
        if LineIndex == 1:
            CurrentGame_Title = x.rstrip()
            print("LoadGameFolder : GameTitle[" + CurrentGame_Title + "]")
        
        if LineIndex == 2:
            CurrentGame_ID = x.rstrip()
            print("LoadGameFolder : GameID[" + CurrentGame_ID + "]")
        
        if LineIndex == 3:
            CurrentGame_Version = x.rstrip()
            print("LoadGameFolder : GameVersion[" + CurrentGame_Version + "]")
        
        if LineIndex == 4:
            CurrentGame_SourceFolder = GameFolderDir + "/" +  x.rstrip()
            print("LoadGameFolder : GameSourceFolder[" + CurrentGame_SourceFolder + "]")
        

    print("OpenGameFolder : inf file loading complete, Loading Assets...")

    sprite.LoadSpritesInFolder(CurrentGame_SourceFolder)
    sound.LoadAllSounds(CurrentGame_SourceFolder)
    print("OpenGameFolder : Game Loading complete, starting...")

def Get_GameSourceFolder():
    global CurrentGame_SourceFolder
    return CurrentGame_SourceFolder

def Get_GameFolder():
    global CurrentGame_Folder
    return CurrentGame_Folder

