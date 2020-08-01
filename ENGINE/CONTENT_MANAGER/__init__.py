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
import os, time

print("Taiyou ContentManager version " + tge.Get_ContentManagerVersion())

DefaultSprite = pygame.image.load("Taiyou/default.png")

FontRenderingDisabled = False
SpriteRenderingDisabled = False
RectangleRenderingDisabled = False
SpriteTransparency = False
SoundEnabled = False

class ContentManager:
    def __init__(self):
        self.Sprites_Name = ()
        self.Sprites_Data = ()
        self.reg_keys = ()
        self.reg_contents = ()
        self.Fonts_Name = ()
        self.Fonts_Data = ()
        self.CurrentLoadedFonts_Name = ()
        self.CurrentLoadedFonts_Contents = ()
        self.Reg_LastInit = ""
        self.Sprite_LastInit = ""
        self.Sound_LastInit = ""
        self.Font_Path = ""
        self.SoundChannels = ()
        self.AllLoadedSounds = {}


    #region Sprite I/O Functions
    def LoadSpritesInFolder(self, FolderName):
        pygame.font.init()
        folder_name = FolderName + "Data/SPRITE"
        index = -1

        self.Sprite_LastInit = FolderName

        sprite_metadata = open(folder_name + "/meta.data", "r")
        sprite_meta_lines = sprite_metadata.readlines()

        print("ContentManager.LoadSpritesInFolder : Loading all Sprites...")

        for line in sprite_meta_lines:
            line = line.rstrip()
            if not line.startswith('#') and not line == "":
                currentLine = line.split(':')
                spriteLocation = folder_name + currentLine[0]
                print("[{0}]".format(spriteLocation))
                self.Sprites_Name += (currentLine[0],)

                if currentLine[1] == "True":
                    try:
                        if not SpriteTransparency:
                            self.Sprites_Data += (pygame.image.load(spriteLocation).convert_alpha(),)
                        else:
                            self.Sprites_Data += (pygame.image.load(spriteLocation).convert(),)
                        print("ContentManager.LoadSpritesInFolder : ItemAdded[" + currentLine[0] + "]; Index[" + str(index) + "] Transparent: True\n")

                    except FileNotFoundError:
                        print("ContentManager.LoadSpritesInFolder : ERROR!\nCannot find the image[" + spriteLocation + "]")
                        self.Sprites_Data += (DefaultSprite,)

                elif currentLine[1] == "False":
                    self.Sprites_Data += (pygame.image.load(spriteLocation).convert(),)
                    print("ContentManager.LoadSpritesInFolder : ItemAdded[" + currentLine[0] + "]; Index[" + str(index) + "] Transparent: True\n")

                else:
                    print("ContentManager.LoadSpritesInFolder : MetadataFileError!, Value[" + line + "] is invalid.")

        else:
            print("Sprite.LoadFonts : Directory does not have Font Packs to be installed.")

        print("ContentManager.LoadSpritesInFolder : Operation Completed.")

    def LoadSprite(self, SpritePath, Transparency=False):
        if utils.Directory_Exists(SpritePath):
            self.Sprites_Name.append("/" + os.path.basename(SpritePath))

            if Transparency:
                self.Sprites_Data += (pygame.image.load(SpritePath).convert_alpha(),)

            else:
                self.Sprites_Data += (pygame.image.load(SpritePath).convert(), )

    def GetSprite(self, SpriteResourceName):
        try:
            return self.Sprites_Data[self.Sprites_Name.index(SpriteResourceName)]
        except:
            print("GetSprite : Sprite[" + SpriteResourceName + "] does not exist.")
            return DefaultSprite

    def UnloadSprite(self):
        print("Sprite.Unload : Unloading Sprites...")
        utils.GarbageCollector_Collect()
        del self.Sprites_Data
        del self.Sprites_Name
        del CurrentLoadedFonts_Name
        utils.GarbageCollector_Collect()

        self.Sprites_Data = ()
        self.Sprites_Name = ()

    def ReloadSprite(self):
        print("Sprite.Reload : Reloading Sprites...")

        Unload()

        LoadSpritesInFolder(tge.Get_GameSourceFolder())

        print("Sprite.Reload : Operation Completed")

    def UnloadSprite(self, SpriteResourceName):
        try:
            sprite_index = self.Sprites_Name.index(SpriteResourceName)

            print("UnloadSprite : Sprite[" + SpriteResourceName + "] unloaded sucefully.")

            del self.Sprites_Data[sprite_index]
        except:
            print("UnloadSprite : Sprite[" + SpriteResourceName + "] does not exist.")
    #endregion

    #region Registry I/O functions
    def LoadRegKeysInFolder(self, reg_dir):
        """
        Load all keys on Specified Folder
        :param reg_dir:Specified Folder
        :return:
        """

        self.Reg_LastInit = reg_dir
        start_time = time.time()
        # -- Unload the Registry -- #
        self.UnloadRegistry()

        print("Taiyou.ContentManager.LoadRegistry : Loading Application Registry")

        reg_dir = reg_dir + "Data{0}REG".format(tge.TaiyouPath_CorrectSlash)
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

            self.reg_keys += (CorrectKeyName,)
            self.reg_contents += (AllData,)

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
        self.reg_keys = ()
        self.reg_contents = ()

        utils.GarbageCollector_Collect()

    def CorrectKeyName(self, keyEntred):
        if not keyEntred.startswith("/"):
            return "{0}{1}".format(tge.TaiyouPath_CorrectSlash, keyEntred)
        else:
            return keyEntred.replace("/", tge.TaiyouPath_CorrectSlash)

    def LoadFonts(self, FolderName):
        self.Font_Path = FolderName + "Data{0}FONT".format(tge.TaiyouPath_CorrectSlash)

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
        FileLocation = "{0}{1}Data{1}REG{1}{2}.data".format(tge.CurrentGame_Folder, tge.TaiyouPath_CorrectSlash, keyName.replace("/", tge.TaiyouPath_CorrectSlash))

        # -- Create the directory -- #
        os.makedirs(os.path.dirname(FileLocation), exist_ok=True)

        print("Taiyou.ContentManager.Write_RegKey : Registry File Location;" + FileLocation)

        # -- Write the Actual Registry Key -- #
        f = open(FileLocation, "w+")
        f.write(keyValue)
        f.close()

        self.ReloadRegistry()

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
    #endregion

    #region Sprite Rendering Functions
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
        :param ImageNotLoaded:Set True if sprite parameter is not a string
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
        return X <= DISPLAY.get_width() and X >= (0 - Width) and Y <= DISPLAY.get_height() and Y >= (0 - Height)
    #endregion

    #region Font Rendering
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

            if X <= DISPLAY.get_width() and Y <= DISPLAY.get_height() and X >= -FontFileObject.render(Text, antialias, ColorRGB).get_width() and Y >= -FontFileObject.render(Text, antialias, ColorRGB).get_height() and not Text == "":
                # -- Fix Opacity Range -- #
                if Opacity < 0:
                    Opacity = 0
                if Opacity > 255:
                    Opacity = 255

                # -- Render Multiple Lines -- #
                if len(Text.splitlines()) > 1:
                    for i, l in enumerate(Text.splitlines()):
                        if not backgroundColor == None:  # -- If background was provided, render with Background
                            FontSurface = FontFileObject.render(l, antialias, ColorRGB, backgroundColor)

                            if not Opacity == 255:  # -- Set the Font Opacity, if needed
                                FontSurface.set_alpha(Opacity)

                            DISPLAY.blit(FontSurface, (X, Y + Size * i))

                        else:  # -- Render Without Background -- #
                            FontSurface = FontFileObject.render(l, antialias, ColorRGB)

                            if not Opacity == 255:  # -- Set the Font Opacity, if needed
                                FontSurface.set_alpha(Opacity)

                            DISPLAY.blit(FontSurface, (X, Y + Size * i))

                else:  # -- Render Single Line Text -- #
                    if not backgroundColor == None:  # -- If background was provided, render with Background
                        FontSurface = FontFileObject.render(Text, antialias, ColorRGB, backgroundColor)

                        if not Opacity == 255:  # -- Set the Font Opacity, if needed
                            FontSurface.set_alpha(Opacity)

                        DISPLAY.blit(FontSurface, (X, Y))

                    else:
                        FontSurface = FontFileObject.render(Text, antialias, ColorRGB)

                        if not Opacity == 255:  # -- Set the Font Opacity, if needed
                            FontSurface.set_alpha(Opacity)

                        DISPLAY.blit(FontSurface, (X, Y))

    def GetFont_object(self, FontFileLocation, Size):
        """
        Returns a Font Object on the Taiyou Font Cache
        :param FontFileLocation:The name of font file [starting with /]
        :param Size:Font Object Size
        :return:Font Object
        """

        if not FontRenderingDisabled:
            FontCacheName = FontFileLocation + ":" + str(Size)
            try:
                return self.CurrentLoadedFonts_Contents[self.CurrentLoadedFonts_Name.index(FontCacheName)]

            except ValueError:  # -- Add font to the FontCache if was not found -- #
                print("Sprite.GetFontObject ; Creating Font Cache Object")

                self.CurrentLoadedFonts_Name += (FontCacheName,)
                FontPath = self.Font_Path + FontFileLocation.replace("/", tge.TaiyouPath_CorrectSlash)
                print(FontPath)

                self.CurrentLoadedFonts_Contents += (pygame.font.Font(FontPath, Size),)

                print("Sprite.GetFontObject ; FontCacheObjName: " + FontCacheName)

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

        return self.GetFont_object(FontFileLocation, FontSize).render(Text, True, (255, 255, 255)).get_height() * len(
            Text.splitlines())

    #endregion

    # Sound I/O Functions
    def LoadSoundsInFolder(self, FolderName):
        if SoundEnabled: return
        self.Sound_LastInit = FolderName
        self.SoundChannels = ()

        pygame.mixer.set_num_channels(255)

        for i in range(0, 255):
            self.SoundChannels += (pygame.mixer.Channel(i),)

        FolderName = FolderName + "Data/SOUND"
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

    def UnloadSounds(self):
        if SoundEnabled: return

        self.AllLoadedSounds = ()
        self.SoundChannels = ()

    def ReloadSounds(self):
        if SoundEnabled: return

        self.UnloadSounds()

        self.LoadSoundsInFolder(self.Sound_LastInit)
    #endregion

    #region Sound Functions
    def PauseAllChannels(self):
        if SoundEnabled: return

        for i, Channel in enumerate(self.SoundChannels):
            Channel.pause()

    def UnpauseAllChannels(self):
        if SoundEnabled: return

        for i, Channel in enumerate(self.SoundChannels):
            Channel.unpause()

    def PlaySound(self, SourceName, Volume=1.0, LeftPan=1.0, RightPan=1.0, ForcePlay=False, PlayOnSpecificID=None):
        """
        Play a Sound loaded into Sound System
        :param SourceName:Audio Source Name [starting with /]
        :param Volume:Audio Volume [range 0.0 to 1.0]
        :param LeftPan:Left Speaker Balance
        :param RightPan:Right Speaker Balance
        :param ForcePlay:Force the audio to be played, Can be useful if you really need to the sound to be played
        :param PlayOnSpecificID:Play the sound on a Specific ID
        :return:
        """
        if SoundEnabled: return

        # -- Get Sound -- #
        sound = self.AllLoadedSounds.get(SourceName)
        sound.set_volume(Volume)

        for i, GameChannel in enumerate(self.SoundChannels):
            if not PlayOnSpecificID is None:
                if i == PlayOnSpecificID:
                    GameChannel.stop()
                    GameChannel.set_volume(LeftPan, RightPan)
                    GameChannel.play(sound)
                    return i
            else:
                if not GameChannel.get_busy():
                    GameChannel.set_volume(LeftPan, RightPan)
                    GameChannel.play(sound)
                    return i

                else:
                    if ForcePlay:
                        GameChannel.stop()
                        GameChannel.set_volume(LeftPan, RightPan)
                        GameChannel.play(sound)
                        return i

    def StopSound(self, ChannelID):
        if SoundEnabled: return

        for i, GameChannel in enumerate(self.SoundChannels):
            if i == ChannelID:
                GameChannel.stop()

    def FadeoutSound(self, ChannelID, FadeoutTime):
        if SoundEnabled: return

        for i, GameChannel in enumerate(self.SoundChannels):
            if i == ChannelID:
                GameChannel.fadeout(FadeoutTime)

    #endregion
