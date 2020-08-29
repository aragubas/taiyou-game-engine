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
import pyglet, pygame
import Engine as tge
import os
from Engine import Utils

DefaultSprite = pyglet.image.load("Taiyou/default.png".replace("/", tge.CorrectSlash))

class ContentManager:
    def __init__(self):
        # -- Registry Keys -- #
        self.LoadedRegistryKeys_Data = list()
        self.LoadedRegistryKeys_Names = list()
        self.RegistrySystem_LastInit = ""

        # -- Texture -- #
        self.LoadedTextures_Name = list()
        self.LoadedTextures_Data = list()
        self.Texture_LastInit = ""

        # -- Sound Variables -- #
        self.SoundChannels = list()
        self.Sound_LastInit = ""
        self.AllLoadedSounds = {}
        self.SoundTuneCache_Names = list()
        self.SoundTuneCache_Cache = list()

    #region Registry I/O Functions
    def LoadRegKeysInFolder(self, reg_dir):
        """
        Load all keys on Specified Folder
        :param reg_dir:Specified Folder
        :return:
        """
        reg_dir = ''.join((tge.Current_ApplicationFolder, tge.CorrectSlash, reg_dir)).replace("/", tge.CorrectSlash)
        self.RegistrySystem_LastInit = reg_dir

        # -- Unload the Registry -- #
        self.UnloadRegistry()

        print("Taiyou.ContentManager.LoadRegistry : Loading Registry...")

        temp_reg_keys = Utils.Directory_FilesList(reg_dir)

        for x in temp_reg_keys:
            CorrectKeyName = x.replace(reg_dir, "").replace(".data", "")
            file = open(x, "r")

            CurrentLine = file.read().splitlines()
            AllData = ""
            for x in CurrentLine:
                if not x.startswith("#"):
                    AllData += x + "\n"

            # -- Format the Text -- #
            AllData = AllData.rstrip().replace("%n", "\n").replace("%t", "\t").replace("%s", " ")

            self.LoadedRegistryKeys_Names.append(CorrectKeyName)
            self.LoadedRegistryKeys_Data.append(AllData)

            print("Taiyou.ContentManager.LoadRegistry : KeyLoaded[" + CorrectKeyName + "]")

        print("Taiyou.ContentManager.LoadRegistry : Total of {0} registry keys loaded.".format(len(self.LoadedRegistryKeys_Names)))

        Utils.GarbageCollector_Collect()

    def ReloadRegistry(self):
        """
        Reload all Registry Keys
        :return:
        """
        print("Taiyou.ContentManager.ReloadRegistry : Reloading Registry...")
        self.UnloadRegistry()
        self.LoadRegKeysInFolder(self.Reg_LastInit)

        Utils.GarbageCollector_Collect()

    def UnloadRegistry(self):
        """
        Unload all registry keys
        :return:
        """

        # -- Clear the Registry -- #
        print("Taiyou.ContentManager.UnloadRegistry : Unloading Registry")
        self.LoadedRegistryKeys_Names.clear()
        self.LoadedRegistryKeys_Data.clear()

        Utils.GarbageCollector_Collect()

    def CorrectKeyName(self, keyEntred):
        """
        Returns the correct name of a key
        :param keyEntred:KeyTag
        :return:
        """
        if not keyEntred.startswith("/"):
            return "{0}{1}".format(tge.CorrectSlash, keyEntred)
        else:
            return keyEntred.replace("/", tge.CorrectSlash)

    def Get_RegKey(self, keyName, valueType=str):
        """
        Returns a String Key
        :param keyName:Name of Key [starting with /]
        :return:KeyData
        """
        if valueType is str:
            return self.LoadedRegistryKeys_Data[self.LoadedRegistryKeys_Names.index(self.CorrectKeyName(keyName))]

        elif valueType is int:
            return int(self.LoadedRegistryKeys_Data[self.LoadedRegistryKeys_Names.index(self.CorrectKeyName(keyName))])

        elif valueType is float:
            return float(self.LoadedRegistryKeys_Data[self.LoadedRegistryKeys_Names.index(self.CorrectKeyName(keyName))])

        elif valueType is bool:
            return self.LoadedRegistryKeys_Data[self.LoadedRegistryKeys_Names.index(self.CorrectKeyName(keyName))].lower() in ("true")

        else:
            return self.LoadedRegistryKeys_Data[self.LoadedRegistryKeys_Names.index(self.CorrectKeyName(keyName))]


    #endregion

    #region Texture I/O Functions
    def LoadSpritesInFolder(self, FolderName):
        """
        Load all sprites on the specified folder\n
        :param FolderName:Folder Path
        :return:
        """
        FolderName = ''.join((tge.Current_ApplicationFolder, tge.CorrectSlash, FolderName)).replace("/", tge.CorrectSlash)
        self.Texture_LastInit = FolderName

        temp_sprite_files = Utils.Directory_FilesList(FolderName)

        print("ContentManager.LoadSpritesInFolder : Started")

        for texture in temp_sprite_files:
            TextureName = texture.replace(FolderName, "")
            SourceName = texture.replace("/", tge.CorrectSlash).rstrip()
            print(''.join((SourceName, " Found")))

            self.LoadedTextures_Name.append(TextureName)
            self.LoadedTextures_Data.append(pyglet.image.load(SourceName))

        print("ContentManager.LoadSpritesInFolder : Operation Completed.")

    def GetSprite(self, SpriteResourceName):
        """
        Get the specified sprite resource on the Sprite Cache
        :param SpriteResourceName:
        :return:
        """
        try:
            return self.LoadedTextures_Data[self.LoadedTextures_Name.index(SpriteResourceName)]
        except:
            print("GetSprite : Sprite[" + SpriteResourceName + "] does not exist.")
            return DefaultSprite

    def UnloadSprite(self):
        """
        Unload all loaded sprites
        :return:
        """
        print("Sprite.Unload : Unloading Sprites...")

        self.LoadedTextures_Data.clear()
        self.LoadedTextures_Name.clear()

    #endregion

    #region Font Loader
    def AddFontsInFolder(self, FolderName):
        """
        Load all fonts on the specified folder\n
        WARNING: Directory must contain meta.data file
        :param FolderName:Folder Path
        :return:
        """
        FolderName = ''.join((tge.Current_ApplicationFolder, tge.CorrectSlash, FolderName)).replace("/", tge.CorrectSlash)

        temp_font_files = Utils.Directory_FilesList(FolderName)

        print("ContentManager.AddFontsInFolder : Started")

        LastfontTryed = ""
        for texture in temp_font_files:
            try:
                SourceName = texture.replace("/", tge.CorrectSlash).rstrip()
                LastfontTryed = SourceName
                pyglet.font.add_file(SourceName)
                print(''.join((SourceName, " added")))
            except Exception as ex:
                print("Error while adding the font {0}\n{1}".format(LastfontTryed, str(ex)))

        print("ContentManager.LoadFontsInFolder : Operation Completed")

    #endregion

    # region Sound I/O Functions
    def LoadSoundsInFolder(self, FolderName):
        """
        Load all sounds on the specified folder\n
        :param FolderName:Folder Path Name
        :return:
        """
        FolderName = ''.join((tge.Current_ApplicationFolder, tge.CorrectSlash, FolderName))
        self.Sound_LastInit = FolderName
        self.CreateSoundChannels()

        temp_sound_files = Utils.Directory_FilesList(FolderName)
        index = -1

        print("ContentManager.LoadSoundsInFolder : Loading Sounds")
        for x in temp_sound_files:
            try:
                index += 1
                print("\nContentManager.LoadSoundsInFolder : File[" + x + "] detected; Index[" + str(index) + "]")

                CorrectKeyName = x.replace(FolderName, "")
                self.AllLoadedSounds[CorrectKeyName] = (pygame.mixer.Sound(x))
            except pygame.error:
                break

            print("ContentManager.LoadSoundsInFolder : ItemAdded[" + CorrectKeyName + "]; Index[" + str(index) + "]\n")
        print("ContentManager.LoadSoundsInFolder : Operation Completed")

    def CreateSoundChannels(self):
        """
        Initialize the Sound System
        :return:
        """
        self.SoundChannels.clear()

        pygame.mixer.set_num_channels(255)

        for i in range(0, 255):
            self.SoundChannels.append(pygame.mixer.Channel(i))

    def InitSoundSystem(self, AudioFrequency=44000, AudioSize=-16, AudioChannels=2, AudioBufferSize=1500):
        print("Taiyou.ContentManager.InitSoundSystem : Initializing Sound System...")
        # -- Set some Variables -- #
        Frequency = int(AudioFrequency)
        Size = int(AudioSize)
        Channels = int(AudioChannels)
        BufferSize = int(AudioBufferSize)

        pygame.mixer.init(Frequency, Size, Channels, BufferSize)

        print("Taiyou.ContentManager.InitSoundSystem : Check for audio-avaliability...")

        if not pygame.mixer.get_init():
            print("Taiyou.ContentManager.InitSoundSystem : Sound System has failed to start.")

        else:
            print("Taiyou.ContentManager.InitSoundSystem : Sound System is ready!")

    def UnloadSounds(self):
        """
        Unload all loaded sounds
        :return:
        """
        if SoundDisabled: return

        self.AllLoadedSounds = ()
        self.SoundChannels = ()

    def ReloadSounds(self):
        """
        Reload all loaded sounds
        :return:
        """
        if SoundDisabled: return

        self.UnloadSounds()

    # endregion

    # region Sound Functions
    def GetTune_FromTuneCache(self, Frequency, Duration, SampleRate):
        """
        Get SoundTune from JIT Cache
        :param Frequency:Sound Frequency
        :param Duration:Sound Duration
        :param SampleRate:Sample Rate
        :return:
        """
        ObjName = Frequency + Duration + SampleRate
        try:  # -- Return the Tune from Cache, if existent -- #
            return self.SoundTuneCache_Cache[self.SoundTuneCache_Names.index(ObjName)]

        except ValueError:  # -- If not, generate the tune, then return it from cache -- #
            self.SoundTuneCache_Names.append(ObjName)
            self.SoundTuneCache_Cache.append(self.GenerateSoundTune(Frequency, Duration, SampleRate))

            return self.SoundTuneCache_Cache[self.SoundTuneCache_Names.index(ObjName)]

    def GenerateSoundTune(self, Frequency, Duration, SampleRate):
        """
        Generate Sound Tune
        :param Frequency:Frequency
        :param Duration:Duration
        :param SampleRate:Sample Rate
        :return:Buffer
        """
        # -- Generate the Tune -- #
        n_samples = int(round(Duration * SampleRate))

        # -- Setup our numpy array to handle 16 bit ints, which is what we set our mixer to expect with "bits" up above -- #
        buf = numpy.zeros((n_samples, 2), dtype=numpy.int16)
        max_sample = 2 ** (16 - 1) - 1

        for s in range(n_samples):
            t = float(s) / SampleRate  # time in seconds

            # grab the x-coordinate of the sine wave at a given time, while constraining the sample to what our mixer is set to with "bits"
            buf[s][0] = int(round(max_sample * math.sin(2 * math.pi * Frequency * t)))
            buf[s][1] = int(round(max_sample * math.sin(2 * math.pi * Frequency * t)))

        return buf

    def PlayTune(self, Frequency, Duration, Volume=1.0, LeftPan=1.0, RightPan=1.0, ForcePlay=False, PlayOnSpecificID=None, Fadeout=0, SampleRate=44000):
        """
        Play a tune on the Specified Frequency
        :param Frequency:Frequency
        :param Duration:Duration of Tune
        :param Volume:Volume
        :param LeftPan:LeftSpeaker Volume
        :param RightPan:RightSpeaker Volume
        :param ForcePlay:If channel is busy, stop and play the current sound
        :param PlayOnSpecificID:Play sound on a specified ChannelID
        :param Fadeout:Fadeout audio when stop playing
        :param SampleRate:Sample Rate of the Tone
        :return:
        """
        if Frequency == 0 or Duration == 0:
            return

        # -- Get the tune from the JIT Cache -- #
        sound = pygame.sndarray.make_sound(self.GetTune_FromTuneCache(Frequency, Duration, SampleRate))
        sound.set_volume(Volume)

        return self.PlaySoundObj(sound, PlayOnSpecificID, LeftPan, RightPan, Fadeout, ForcePlay)

    def PlaySoundObj(self, sound, PlayOnSpecificID, LeftPan, RightPan, Fadeout, ForcePlay):
        for i, channel in enumerate(self.SoundChannels):
            if not PlayOnSpecificID is None:
                if i == PlayOnSpecificID:
                    channel.stop()
                    channel.set_volume(LeftPan, RightPan)
                    channel.play(sound, fade_ms=Fadeout)
                    return i
            else:
                if not channel.get_busy():
                    channel.set_volume(LeftPan, RightPan)
                    channel.play(sound, fade_ms=Fadeout)
                    return i

                else:
                    if ForcePlay:
                        channel.stop()
                        channel.set_volume(LeftPan, RightPan)
                        channel.play(sound, fade_ms=Fadeout)
                        return i

    def StopAllChannels(self):
        """
        Stop all sound channels
        :return:
        """
        if SoundDisabled: return

        for channel in self.SoundChannels:
            channel.stop()

    def PauseAllChannels(self):
        """
        Pause all sounds on all channels
        :return:
        """
        if SoundDisabled: return

        for channel in self.SoundChannels:
            channel.pause()

    def UnpauseAllChannels(self):
        """
        Unpause all sounds on all channels
        :return:
        """
        if SoundDisabled: return

        for channel in self.SoundChannels:
            channel.unpause()

    def UnloadSoundTuneCache(self):
        utils.GarbageCollector_Collect()
        self.SoundTuneCache_Cache.clear()
        self.SoundTuneCache_Names.clear()
        utils.GarbageCollector_Collect()

    def PlaySound(self, SourceName, Volume=1.0, LeftPan=1.0, RightPan=1.0, ForcePlay=False, PlayOnSpecificID=None, Fadeout=0):
        """
        Play a Sound loaded into Sound System
        :param SourceName:Audio Source Name [starting with /]
        :param Volume:Audio Volume [range 0.0 to 1.0]
        :param LeftPan:Left Speaker Balance
        :param RightPan:Right Speaker Balance
        :param ForcePlay:Force the audio to be played, Can be useful if you really need to the sound to be played
        :param PlayOnSpecificID:Play the sound on a Specific ID
        :return:ChannelID
        """
        # -- Convert to the Correct Slash -- #
        SourceName = SourceName.replace("/", tge.CorrectSlash)

        # -- Get Sound -- #
        sound = self.AllLoadedSounds.get(SourceName)
        sound.set_volume(Volume)

        return self.PlaySoundObj(sound, PlayOnSpecificID, LeftPan, RightPan, Fadeout, ForcePlay)

    def StopSound(self, ChannelID):
        """
        Stop a sound playing on a specified ChannelID
        :param ChannelID:ChannelID
        :return:
        """
        if SoundDisabled: return

        for i, channel in enumerate(self.SoundChannels):
            if i == ChannelID:
                channel.stop()
                break

    def FadeoutSound(self, ChannelID, FadeoutTime):
        """
        Fade out a sound on a Specified Channel
        :param ChannelID:Specified ChannelID
        :param FadeoutTime:Fadeout time in Milisecounds
        :return:
        """
        if SoundDisabled: return

        for i, channel in enumerate(self.SoundChannels):
            if i == ChannelID:
                channel.fadeout(FadeoutTime)
                break

    def SetSoundVoume(self, ChannelID, NewVolume):
        """
        Set Volume of a Sound on Specific ID
        :param ChannelID:Specified ChannelID
        :param NewVolume:Volume (Range 0.0 to 1.0)
        :return:
        """
        if SoundDisabled: return

        for i, channel in enumerate(self.SoundChannels):
            if i == ChannelID:
                channel.set_volume(NewVolume)

    def Get_ChannelIsBusy(self, ChannelID):
        if SoundDisabled: return

        for i, channel in enumerate(self.SoundChannels):
            if i == ChannelID:
                return channel.get_busy()

        return False

    # endregion