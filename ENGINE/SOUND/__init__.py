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
from ENGINE import UTILS as utils
import ENGINE as tge
import pygame
import threading

print("Taiyou Sound System version 1.2")

AllLoadedSounds = {}

CurrentBGMPlaying = list()

DisableSoundSystem = False

def LoadAllSounds(FolderName):
    if DisableSoundSystem:
        return
    FolderName = FolderName + "/SOUND"
    temp_sound_files = utils.GetFileInDir(FolderName)
    index = -1

    print("LoadAllSounds : Loading all Sounds...")
    for x in temp_sound_files:
        index += 1
        print("\nLoadAllSounds : File[" + x + "] detected; Index[" + str(index) + "]")

        CorrectKeyName = x.replace(FolderName, "")
        AllLoadedSounds[CorrectKeyName] = (pygame.mixer.Sound(x))

        print("LoadAllSounds : ItemAdded[" + CorrectKeyName + "]; Index[" + str(index) + "]\n")

def Unload():
    if DisableSoundSystem:
        return
    print("Sound.Unload : Unloading All Sounds...")

    AllLoadedSounds.clear()

    print("Sound.Unload : Operation Completed Sucefully.")

def Reload():
    if DisableSoundSystem:
        return
    print("Sound.Reload : Reloading All Sounds...")

    Unload()
    LoadAllSounds(tge.Get_GameSourceFolder() + "/SOUND")

    print("Sound.Reload : Opearation Complted.")

def PlaySound(SourceName):
    if DisableSoundSystem:
        return
    global AllLoadedSounds
    sound = AllLoadedSounds.get(SourceName)
    sound.play()

def StopSound(SourceName):
    if DisableSoundSystem:
        return
    global AllLoadedSounds
    sound = AllLoadedSounds.get(SourceName)
    sound.stop()

