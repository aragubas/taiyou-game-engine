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
import pygame, sys, os
from pygame import gfxdraw
import binascii
import struct
from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
import glob
import os, time, numpy, math

print("Taiyou ContentManager version " + tge.Get_ContentManagerVersion())

DefaultSprite = pygame.image.load("Taiyou/default.png")

FontRenderingDisabled = False
SpriteRenderingDisabled = False
RectangleRenderingDisabled = False
SpriteTransparency = False
SoundDisabled = False


class ContentManager:
    def __init__(self):
        """
        Manages Loaded Sounds, Sprites and Registry Keys.
        """
        self.Sprites_Name = list()
        self.Sprites_Data = list()
        self.reg_keys = list()
        self.reg_contents = list()
        self.Fonts_Name = list()
        self.Fonts_Data = list()
        self.CurrentLoadedFonts_Name = list()
        self.CurrentLoadedFonts_Contents = list()
        self.Reg_LastInit = ""
        self.Sprite_LastInit = ""
        self.Sound_LastInit = ""
        self.Font_Path = ""
        self.SoundChannels = list()
        self.AllLoadedSounds = {}
        self.SoundTuneCache_Names = list()
        self.SoundTuneCache_Cache = list()

    # region Sprite I/O Functions
    def LoadSpritesInFolder(self, FolderName):
        """
        Load all sprites on the specified folder\n
        Alert: Folder must contain meta.data file.
        :param FolderName:Folder Path
        :return:
        """
        pygame.font.init()
        FolderName = tge.Get_GameSourceFolder() + FolderName
        index = -1

        self.Sprite_LastInit = FolderName

        sprite_metadata = open(FolderName + "/meta.data", "r")
        sprite_meta_lines = sprite_metadata.readlines()

        print("ContentManager.LoadSpritesInFolder : Loading all Sprites...")

        for line in sprite_meta_lines:
            line = line.rstrip()
            if not line.startswith('#') and not line == "":
                currentLine = line.split(':')
                spriteLocation = FolderName + currentLine[0]
                print("[{0}]".format(spriteLocation))
                self.Sprites_Name += (currentLine[0],)

                if currentLine[1] == "True":
                    try:
                        if not SpriteTransparency:
                            self.Sprites_Data.append(pygame.image.load(spriteLocation).convert_alpha())
                        else:
                            self.Sprites_Data.append(pygame.image.load(spriteLocation).convert())
                        print("ContentManager.LoadSpritesInFolder : ItemAdded[" + currentLine[0] + "]; Index[" + str(index) + "] Transparent: True\n")

                    except FileNotFoundError:
                        print("ContentManager.LoadSpritesInFolder : ERROR!\nCannot find the image[" + spriteLocation + "]")
                        self.Sprites_Data.append(DefaultSprite)

                elif currentLine[1] == "False":
                    self.Sprites_Data.append(pygame.image.load(spriteLocation).convert())
                    print("ContentManager.LoadSpritesInFolder : ItemAdded[" + currentLine[0] + "]; Index[" + str(index) + "] Transparent: True\n")

                else:
                    print("ContentManager.LoadSpritesInFolder : MetadataFileError!, Value[" + line + "] is invalid.")

        else:
            print("Sprite.LoadFonts : Directory does not have Font Packs to be installed.")

        print("ContentManager.LoadSpritesInFolder : Operation Completed.")

    def LoadSprite(self, SpritePath, Transparency=False):
        """
        Load the Specified Sprite
        :param SpritePath:Path to the Specified Sprite
        :param Transparency:Bool Value to import with transparency or not
        :return:
        """
        if utils.Directory_Exists(SpritePath):
            self.Sprites_Name.append("/" + os.path.basename(SpritePath))

            if Transparency:
                self.Sprites_Data.append(pygame.image.load(SpritePath).convert_alpha())

            else:
                self.Sprites_Data.append(pygame.image.load(SpritePath).convert())

    def GetSprite(self, SpriteResourceName):
        """
        Get the specified sprite resource on the Sprite Cache
        :param SpriteResourceName:
        :return:
        """
        try:
            return self.Sprites_Data[self.Sprites_Name.index(SpriteResourceName)]
        except:
            print("GetSprite : Sprite[" + SpriteResourceName + "] does not exist.")
            return DefaultSprite

    def UnloadSprite(self):
        """
        Unload all loaded sprites
        :return:
        """
        print("Sprite.Unload : Unloading Sprites...")
        utils.GarbageCollector_Collect()
        del self.Sprites_Data
        del self.Sprites_Name
        del CurrentLoadedFonts_Name
        utils.GarbageCollector_Collect()

        self.Sprites_Data = list()
        self.Sprites_Name = list()

    def ReloadSprite(self):
        """
        Reload all loaded sprites
        :return:
        """
        print("Sprite.Reload : Reloading Sprites...")

        Unload()

        LoadSpritesInFolder(tge.Get_GameSourceFolder())

        print("Sprite.Reload : Operation Completed")

    def UnloadSprite(self, SpriteResourceName):
        """
        Unload the Specified Sprite Resource
        :param SpriteResourceName: Sprite Resource Name
        :return:
        """
        try:
            sprite_index = self.Sprites_Name.index(SpriteResourceName)

            print("UnloadSprite : Sprite[" + SpriteResourceName + "] unloaded sucefully.")

            del self.Sprites_Data[sprite_index]
        except:
            print("UnloadSprite : Sprite[" + SpriteResourceName + "] does not exist.")

    # endregion

    # region Sprite Rendering Functions
    def ImageRender(self, DISPLAY, sprite, X, Y, Width=0, Height=0, SmoothScaling=False, Opacity=255, ColorKey=None, ImageNotLoaded=False):
        """
        Render a Image loaded to the Sprite System
        :param DISPLAY:Surface to be rendered
        :param sprite:Sprite Resource Name [starting with /]
        :param X:X Location
        :param Y:Y Location
        :param Width:Scale Width
        :param Height:Scale Height
        :param SmoothScaling:Smooth Pixels [This option can decrease peformace]
        :param Opacity: Alpha value of sprite's surface
        :param ColorKey: ColorKey of sprite
        :param ImageNotLoaded:Set True if sprite parameter is a path
        :return:
        """
        if not SpriteRenderingDisabled:
            # -- Workaround to make Opacity Value not raise exception -- #
            if Opacity <= 0:
                Opacity = 0
            if Opacity >= 255:
                Opacity = 255

            try:
                if self.IsOnScreen(DISPLAY, X, Y, Width, Height):
                    # -- Set the Image Variable -- #
                    if not ImageNotLoaded:
                        Image = self.GetSprite(sprite)
                    else:
                        Image = sprite

                    if Width == 0 and Height == 0:  # -- Render Image With no Transformation -- #
                        Image.set_alpha(Opacity)
                        Image.set_colorkey(ColorKey)

                        DISPLAY.blit(Image, (X, Y))

                    else:
                        if not SmoothScaling:  # -- Render Images with Fast Scaling -- #
                            Image.set_alpha(Opacity)
                            Image.set_colorkey(ColorKey)

                            DISPLAY.blit(pygame.transform.scale(Image, (Width, Height)), (X, Y))
                        else:  # -- Render Image with Smooth Scaling -- #
                            Image.set_alpha(Opacity)
                            Image.set_colorkey(ColorKey)

                            DISPLAY.blit(pygame.transform.smoothscale(Image, (Width, Height)), (X, Y))

            except Exception as ex:
                print("Sprite.Render : Error while rendering sprite;\n" + str(ex))

    def IsOnScreen(self, DISPLAY, X, Y, Width, Height):
        """
        Check if Object is on Screen
        :param DISPLAY:Source Surface
        :param X:X position
        :param Y:Y position
        :param Width:Width
        :param Height:Height
        :return:Boolean Value
        """
        return X <= DISPLAY.get_width() and X >= (0 - Width) and Y <= DISPLAY.get_height() and Y >= (0 - Height)

    # endregion

    # region Registry I/O functions
    def LoadRegKeysInFolder(self, reg_dir):
        """
        Load all keys on Specified Folder
        :param reg_dir:Specified Folder
        :return:
        """
        reg_dir = tge.Get_GameSourceFolder() + reg_dir
        self.Reg_LastInit = tge.Get_GameSourceFolder() + reg_dir

        start_time = time.time()
        # -- Unload the Registry -- #
        self.UnloadRegistry()

        print("Taiyou.ContentManager.LoadRegistry : Loading Application Registry")

        temp_reg_keys = utils.Directory_FilesList(reg_dir)
        index = -1

        for x in temp_reg_keys:
            index += 1

            CorrectKeyName = x.replace(reg_dir, "").replace(".data", "")
            file = open(x, "r")

            CurrentLine = file.read().splitlines()
            AllData = ""
            for x in CurrentLine:
                if not x.startswith("#"):
                    AllData += x + "\n"

            # -- Format the Text -- #
            AllData = AllData.rstrip().replace("%n", "\n").replace("%t", "\t").replace("%s", " ")

            self.reg_keys.append(CorrectKeyName)
            self.reg_contents.append(AllData)

            print("Taiyou.ContentManager.LoadRegistry : KeyLoaded[" + CorrectKeyName + "]")

        print("Taiyou.ContentManager.LoadRegistry : Total of {0} registry keys loaded. In {1} seconds.".format(str(len(self.reg_keys)), utils.FormatNumber(time.time() - start_time, 4)))

        utils.GarbageCollector_Collect()

    def ReloadRegistry(self):
        """
        Reload all Registry Keys
        :return:
        """
        CurrentGameFolder = "{0}{1}".format(tge.CurrentGame_Folder, tge.TaiyouPath_CorrectSlash)

        print("Taiyou.ContentManager.ReloadRegistry : Reloading Registry...")
        self.UnloadRegistry()
        self.LoadRegKeysInFolder(self.Reg_LastInit)

        utils.GarbageCollector_Collect()

    def UnloadRegistry(self):
        """
        Unload all registry keys
        :return:
        """

        # -- Clear the Registry -- #
        print("Taiyou.ContentManager.UnloadRegistry : Unloading Registry")
        self.reg_keys = list()
        self.reg_contents = list()

        utils.GarbageCollector_Collect()

    def CorrectKeyName(self, keyEntred):
        """
        Returns the correct name of a key
        :param keyEntred:KeyTag
        :return:
        """
        if not keyEntred.startswith("/"):
            return "{0}{1}".format(tge.TaiyouPath_CorrectSlash, keyEntred)
        else:
            return keyEntred.replace("/", tge.TaiyouPath_CorrectSlash)

    def SetFontPath(self, FolderName):
        """
        Set the path to the JIT Font Cache
        :param FolderName:
        :return:
        """
        self.Font_Path = tge.Get_GameSourceFolder() + FolderName

    def Get_RegKey(self, keyName, valueType=str):
        """
        Returns a String Key
        :param keyName:Name of Key [starting with /]
        :return:KeyData
        """
        try:
            if valueType is str:
                return self.reg_contents[self.reg_keys.index(self.CorrectKeyName(keyName))]

            elif valueType is int:
                return int(self.reg_contents[self.reg_keys.index(self.CorrectKeyName(keyName))])

            elif valueType is float:
                return float(self.reg_contents[self.reg_keys.index(self.CorrectKeyName(keyName))])

            elif valueType is bool:
                return self.reg_contents[self.reg_keys.index(self.CorrectKeyName(keyName))].lower() in ("true", "yes", "t", "1")

            else:
                return self.reg_contents[self.reg_keys.index(self.CorrectKeyName(keyName))]

        except ValueError:
            raise FileNotFoundError("Taiyou.ContentManager.Get_RegKey Error!\nCannot find the Registry Key [{0}].".format(str(keyName)))

    def Write_RegKey(self, keyName, keyValue):
        """
        Write an Registry Key
        :param keyName:KeyTag
        :param keyValue:New Value
        :return:
        """
        FileLocation = "{0}{1}Data{1}REG{1}{2}.data".format(tge.CurrentGame_Folder, tge.TaiyouPath_CorrectSlash, keyName.replace("/", tge.TaiyouPath_CorrectSlash))

        # -- Create the directory -- #
        os.makedirs(os.path.dirname(FileLocation), exist_ok=True)

        print("Taiyou.ContentManager.Write_RegKey : Registry File Location;" + FileLocation)

        # -- Modify the Loaded Value in Memory -- #
        Index = self.reg_keys.index(keyName)
        self.reg_contents[Index] = keyValue

        # -- Write the Actual Registry Key -- #
        f = open(FileLocation, "w+")
        f.write(keyValue)
        f.close()

        print("Taiyou.ContentManager.Write_RegKey : Registry File Written.")

    def KeyExists(self, keyName):
        """
        Returns True if the Specified Key Exists
        :param keyName: Specified Key [starting with /]
        :return: Value to Return
        """
        try:
            Test = self.reg_contents[self.reg_keys.index(self.CorrectKeyName(keyName))]
            return True
        except ValueError:
            return False

    # endregion

    # region Font Rendering
    def FontRender(self, DISPLAY, FontFileLocation, Size, Text, ColorRGB, X, Y, antialias=True, backgroundColor=None, Opacity=255):
        """
        Render a Text using a font loaded into Taiyou Font Cache
        :param DISPLAY:Surface Name
        :param FontFileLocation:Font Resource Name [starting with /]
        :param Size:Font Size
        :param Text:Text to be Rendered
        :param ColorRGB:Color in RGB Format [R, G, B]
        :param X:X Location
        :param Y:Y Location
        :param antialias:Smooth Pixels [This option can decrea se peformace]
        :return:
        """
        if not FontRenderingDisabled:
            # -- Get the FontFileObject, required for all functions here -- #
            FontFileObject = self.GetFont_object(FontFileLocation, Size)
            ColorRGB = utils.FixColorRange(ColorRGB)

            if X <= DISPLAY.get_width() and Y <= DISPLAY.get_height() and X >= -FontFileObject.render(Text, antialias, ColorRGB).get_width() and Y >= -FontFileObject.render(Text, antialias, ColorRGB).get_height() and not Text == "":
                # -- Fix Opacity Range -- #
                if Opacity < 0:
                    Opacity = 0
                if Opacity > 255:
                    Opacity = 255

                # -- Render Multiple Lines -- #
                for i, l in enumerate(Text.splitlines()):
                    if not backgroundColor == None:  # -- If background was provided, render with Background
                        FontSurface = FontFileObject.render(l, antialias, ColorRGB, backgroundColor)

                        if not Opacity == 255:  FontSurface.set_alpha(Opacity)

                        DISPLAY.blit(FontSurface, (X, Y + Size * i))

                    else:  # -- Render Without Background -- #
                        FontSurface = FontFileObject.render(l, antialias, ColorRGB)

                        if not Opacity == 255:  # -- Set the Font Opacity, if needed
                            FontSurface.set_alpha(Opacity)

                        DISPLAY.blit(FontSurface, (X, Y + Size * i))

    def GetFont_object(self, FontFileLocation, Size):
        """
        Returns a Font Object on the Taiyou Font Cache
        :param FontFileLocation:The name of font file [starting with /]
        :param Size:Font Object Size
        :return:Font Object
        """

        if not FontRenderingDisabled:
            FontCacheName = ''.join((FontFileLocation, str(Size)))
            try:
                return self.CurrentLoadedFonts_Contents[self.CurrentLoadedFonts_Name.index(FontCacheName)]

            except ValueError:  # -- Add font to the FontCache if was not found -- #
                self.CurrentLoadedFonts_Name.append(FontCacheName)
                FontPath = self.Font_Path + FontFileLocation.replace("/", tge.TaiyouPath_CorrectSlash)
                print(FontPath)

                self.CurrentLoadedFonts_Contents.append(pygame.font.Font(FontPath, Size))

                return self.CurrentLoadedFonts_Contents[self.CurrentLoadedFonts_Name.index(FontCacheName)]

    def GetFont_width(self, FontFileLocation, FontSize, Text):
        """
        Get the width of a font, from a specified text.
        :param FontFileLocation:FontFile Name
        :param FontSize:FontSize
        :param Text:Text
        :return:Size (int)
        """

        TotalSize = 0
        for i, l in enumerate(Text.splitlines()):
            CurrentSize = 0
            CurrentSize += self.GetFont_object(FontFileLocation, FontSize).render(l, True, (255, 255, 255)).get_width()

            if CurrentSize > TotalSize:
                TotalSize = CurrentSize

        return TotalSize

    def GetFont_height(self, FontFileLocation, FontSize, Text):
        """
        Get the height of a font, from a specified text.
        :param FontFileLocation:FontFile Name
        :param FontSize:FontSize
        :param Text:Text
        :return:Size (int)
        """

        return self.GetFont_object(FontFileLocation, FontSize).render(Text, True, (255, 255, 255)).get_height() * len(Text.splitlines())

    # endregion

    # region Sound I/O Functions
    def LoadSoundsInFolder(self, FolderName):
        """
        Load all sounds on the specified folder\n
        :param FolderName:Folder Path Name
        :return:
        """
        if SoundDisabled: return
        FolderName = tge.Get_GameSourceFolder() + FolderName
        self.Sound_LastInit = FolderName
        self.InitSoundSystem()

        temp_sound_files = utils.Directory_FilesList(FolderName)
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

    def InitSoundSystem(self):
        """
        Initialize the Sound System
        :return:
        """
        self.SoundChannels.clear()

        pygame.mixer.set_num_channels(255)

        for i in range(0, 255):
            self.SoundChannels.append(pygame.mixer.Channel(i))

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
        if SoundDisabled or Frequency == 0 or Duration == 0:
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
        if SoundDisabled: return

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
