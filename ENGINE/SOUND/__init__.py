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

print("Taiyou Sound System version " + tge.Get_SoundVersion())

AllLoadedSounds = {}

CurrentBGMPlaying = list()

DisableSoundSystem = False

def LoadAllSounds(FolderName):
    if DisableSoundSystem:
        return
    FolderName = FolderName + "/SOUND"
    temp_sound_files = utils.GetFileInDir(FolderName)
    index = -1

    print("Sound.LoadAllSounds : Loading Sounds")
    for x in temp_sound_files:
        index += 1
        print("\nSound.LoadAllSounds : File[" + x + "] detected; Index[" + str(index) + "]")

        CorrectKeyName = x.replace(FolderName, "")
        AllLoadedSounds[CorrectKeyName] = (pygame.mixer.Sound(x))

        print("Sound.LoadAllSounds : ItemAdded[" + CorrectKeyName + "]; Index[" + str(index) + "]\n")
    print("Sound.LoadAllSounds : Operation Completed")

def Unload():
    if DisableSoundSystem:
        return
    print("Sound.Unload : Unloading All Sounds...")

    AllLoadedSounds.clear()

    print("Sound.Unload : Reloading TaiyouUI Sounds...")
    LoadAllSounds("Taiyou/SYSTEM/SOURCE")

    print("Sound.Unload : Operation Completed Sucefully.")

def Reload():
    if not DisableSoundSystem:
        print("Sound.Reload : Reloading All Sounds...")

        Unload()
        LoadAllSounds(tge.Get_GameSourceFolder())

        print("Sound.Reload : Re-Loading TaiyouUI sounds...")
        LoadAllSounds("Taiyou/SYSTEM/SOURCE")


        print("Sound.Reload : Operation Completed.")


def PlaySound(SourceName):
    if not DisableSoundSystem:
        global AllLoadedSounds

        sound = AllLoadedSounds.get(SourceName)
        sound.play()


def StopSound(SourceName):
    if not DisableSoundSystem:
        global AllLoadedSounds
        sound = AllLoadedSounds.get(SourceName)
        sound.stop()

