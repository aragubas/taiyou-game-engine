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

# -- Imports --
from ENGINE import UTILS as utils
import ENGINE as tge
import pygame
import time

print("Taiyou Sound System version " + tge.Get_SoundVersion())

AllLoadedSounds = {}

DisableSoundSystem = False

GameSoundChannels = ()
SystemSoundChannels = ()

GlobalVolume = 1.0


def LoadAllSounds(FolderName):
    """
    Load all sounds on the Specified Folder
    :param FolderName:the Specified Folder
    :return:
    """
    global AllLoadedSounds
    global GameSoundChannels
    global DisableSoundSystem
    global SystemSoundChannels

    if DisableSoundSystem:
        return

    GameSoundChannels = ()
    SystemSoundChannels = ()

    pygame.mixer.set_num_channels(255)

    for i in range(0, 249):
        GameSoundChannels += (pygame.mixer.Channel(i),)

    for i in range(250, 255):
        SystemSoundChannels += (pygame.mixer.Channel(i),)

    if DisableSoundSystem:
        return
    FolderName = FolderName + "/SOUND"
    temp_sound_files = utils.Directory_FilesList(FolderName)
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
    """
    Unload all sounds loaded
    :return:
    """
    global AllLoadedSounds
    global GameSoundChannels
    global DisableSoundSystem
    global SystemSoundChannels

    if DisableSoundSystem:
        return

    AllLoadedSounds = {}

    LoadAllSounds("Taiyou/SYSTEM/SOURCE")

def Reload():
    """
    Reload all sounds
    :return:
    """
    global AllLoadedSounds
    global GameSoundChannels
    global DisableSoundSystem
    global SystemSoundChannels

    if not DisableSoundSystem:
        # -- Stop all Sounds -- #
        for i, Channel in enumerate(GameSoundChannels):
            Channel.stop()

        Unload()
        LoadAllSounds(tge.Get_GameSourceFolder())

        LoadAllSounds("Taiyou/SYSTEM/SOURCE")

def PauseGameChannel():
    global AllLoadedSounds
    global GameSoundChannels
    global DisableSoundSystem
    global SystemSoundChannels

    for i, Channel in enumerate(GameSoundChannels):
        Channel.pause()

def UnpauseGameChannel():
    global AllLoadedSounds
    global GameSoundChannels
    global DisableSoundSystem
    global SystemSoundChannels

    for i, Channel in enumerate(GameSoundChannels):
        Channel.unpause()

def PlaySound(SourceName, Volume=1.0, LeftPan=1.0, RightPan=1.0, PlayOnSystemChannel=False):
    """
    Play a Sound loaded into Sound System
    :param SourceName:Audio Source Name [starting with /]
    :param Volume:Audio Volume [range 0.0 to 1.0]
    :param LeftPan:Left Speaker Balance
    :param RightPan:Right Speaker Balance
    :param PlayOnSystemChannel:Play sound on System Sound Channel
    :return:
    """
    global AllLoadedSounds
    global GameSoundChannels
    global DisableSoundSystem
    global SystemSoundChannels

    if not DisableSoundSystem:

        # -- Get Sound -- #
        sound = AllLoadedSounds.get(SourceName)
        sound.set_volume(Volume * GlobalVolume)

        if not PlayOnSystemChannel:
            for i, GameChannel in enumerate(GameSoundChannels):
                if not GameChannel.get_busy():
                    GameChannel.set_volume(LeftPan, RightPan)
                    GameChannel.play(sound)
                    break

        else:
            for i, SystemChannel in enumerate(SystemSoundChannels):
                if not SystemChannel.get_busy():
                    SystemChannel.set_volume(LeftPan, RightPan)
                    SystemChannel.play(sound)
                    break


def StopSound(SourceName):
    if not DisableSoundSystem:
        global AllLoadedSounds
        sound = AllLoadedSounds.get(SourceName)
        sound.stop()
