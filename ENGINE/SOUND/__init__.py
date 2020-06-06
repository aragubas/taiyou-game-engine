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

CurrentBGMPlaying = list()

DisableSoundSystem = False

GameSoundChannels = list()
SystemSoundChannels = list()
def LoadAllSounds(FolderName):
    """
    Load all sounds on the Specified Folder
    :param FolderName:the Specified Folder
    :return:
    """
    global GameSoundChannels
    global SystemSoundChannels

    GameSoundChannels.clear()

    pygame.mixer.set_num_channels(255)

    for i in range(0, 200):
        GameSoundChannels.append(pygame.mixer.Channel(i))

    for i in range(200, 255):
        SystemSoundChannels.append(pygame.mixer.Channel(i))

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
    """
    Unload all sounds loaded
    :return:
    """
    if DisableSoundSystem:
        return
    print("Sound.Unload : Unloading All Sounds...")

    AllLoadedSounds.clear()

    print("Sound.Unload : Reloading TaiyouUI Sounds...")
    LoadAllSounds("Taiyou/SYSTEM/SOURCE")

    print("Sound.Unload : Operation Completed Sucefully.")

def Reload():
    """
    Reload all sounds
    :return:
    """
    if not DisableSoundSystem:
        print("Sound.Reload : Reloading All Sounds...")

        Unload()
        LoadAllSounds(tge.Get_GameSourceFolder())

        print("Sound.Reload : Re-Loading TaiyouUI sounds...")
        LoadAllSounds("Taiyou/SYSTEM/SOURCE")


        print("Sound.Reload : Operation Completed.")

def PauseGameChannel():
    global GameSoundChannels

    for i, Channel in enumerate(GameSoundChannels):
        Channel.pause()
        print("SoundChannel " + str(i) + " was been paused.")

def UnpauseGameChannel():
    global GameSoundChannels

    for i, Channel in enumerate(GameSoundChannels):
        Channel.unpause()
        print("SoundChannel " + str(i) + " was been resumed.")


def PlaySound(SourceName, Volume=0.5, LeftPan=1.0, RightPan=1.0, PlayOnSystemChannel=False):
    """
    Play a sound loaded on the Sound System
    :param SourceName:Sound File Name [starting with /]
    :param Volume:Volume in range 0.0 to 1.0
    :return:
    """
    if not DisableSoundSystem:
        global AllLoadedSounds
        global GameSoundChannels
        global SystemSoundChannels

        # -- Play on Mono -- #
        if tge.AudioChannels == 1:

            sound = AllLoadedSounds.get(SourceName)
            sound.set_volume(Volume)
            sound.play()

        elif tge.AudioChannels >= 2:
            # -- Play Stereo Audio -- #
            sound = AllLoadedSounds.get(SourceName)
            sound.set_volume(Volume)

            if not PlayOnSystemChannel:
                for i, GameChannel in enumerate(GameSoundChannels):
                    if not GameChannel.get_busy():
                        GameChannel.set_volume(LeftPan, RightPan)

                        GameChannel.play(sound)
                        print("Found Game Channel in {0}".format(str(i)))
                        break
                    else:
                        print("Sound Game Channel {0} is busy.".format(str(i)))
            else:
                for i, SystemChannel in enumerate(SystemSoundChannels):
                    if not SystemChannel.get_busy():
                        SystemChannel.set_volume(LeftPan, RightPan)

                        SystemChannel.play(sound)
                        print("Found System Channel in {0}".format(str(i)))
                        break
                    else:
                        print("Sound System Channel {0} is busy.".format(str(i)))


def StopSound(SourceName):
    if not DisableSoundSystem:
        global AllLoadedSounds
        sound = AllLoadedSounds.get(SourceName)
        sound.stop()
