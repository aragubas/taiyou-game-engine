#!/usr/bin/python3
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
