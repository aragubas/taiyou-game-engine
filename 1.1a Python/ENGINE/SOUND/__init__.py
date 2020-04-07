import ENGINE.Utils as utils
import pygame

print("Taiyou Sound System version 1.0")











AllLoadedSoundsNames = list()
AllLoadedSounds = list()
CurrentBGMPlaying = list()

def LoadAllSounds(FolderName):
    FolderName = FolderName + "/SOUND"
    temp_SoundFiles = utils.GetFileInDir(FolderName)
    index = -1

    print("LoadAllSounds : Loading all Sounds...")
    for x in temp_SoundFiles:
        index += 1
        print("\nLoadAllSounds : File[" + x + "] detected; Index[" + str(index) + "]")

        CorrectKeyName = x.replace(FolderName, "")
        AllLoadedSoundsNames.append(CorrectKeyName)
        AllLoadedSounds.append(pygame.mixer.Sound(open(x,"r")))

        print("LoadAllSounds : ItemAdded[" + CorrectKeyName + "]; Index[" + str(index) + "]\n")

def PlaySound(SourceName):
    AllLoadedSounds[AllLoadedSoundsNames.index(SourceName)].play()

def StopSound(SourceName):
    index = AllLoadedSoundsNames.index(SourceName)
    CurrentMusic = AllLoadedSounds[index]
    print("StopSound : SoundIndex[" + str(index) + "]")

    CurrentMusic.stop()