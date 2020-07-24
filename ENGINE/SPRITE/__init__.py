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

print("TaiyouGameEngine Sprite Utilitary version " + tge.Get_SpriteVersion())

# -- Variables --
Sprites_Name = ()
Sprites_Data = ()
Fonts_Name = ()
Fonts_Data = ()

DefaultSprite = pygame.image.load("Taiyou/SYSTEM/Data/SPRITE/default.png")

FontRenderingDisabled = False
SpriteRenderingDisabled = False
RectangleRenderingDisabled = False
SpriteTransparency = False

CurrentLoadedFonts_Name = ()
CurrentLoadedFonts_Contents = ()

def LoadSpritesInFolder(FolderName):
    global Sprites_Name
    global Sprites_Data

    pygame.font.init()
    folder_name = FolderName + "Data/SPRITE"
    index = -1

    sprite_metadata = open(folder_name + "/meta.data", "r")
    sprite_meta_lines = sprite_metadata.readlines()

    print("LoadSpritesInFolder : Loading all Sprites...")

    for line in sprite_meta_lines:
        line = line.rstrip()
        if not line.startswith('#') and not line == "":
            currentLine = line.split(':')
            spriteLocation = folder_name + currentLine[0]
            print("[{0}]".format(spriteLocation))
            Sprites_Name += (currentLine[0],)

            if currentLine[1] == "True":
                try:
                    if not SpriteTransparency:
                        Sprites_Data += (pygame.image.load(spriteLocation).convert_alpha(),)
                    else:
                        Sprites_Data += (pygame.image.load(spriteLocation).convert(),)
                    print("Sprite.LoadFolder : ItemAdded[" + currentLine[0] + "]; Index[" + str(index) + "] Transparent: True\n")

                except FileNotFoundError:
                    print("Sprite.LoadFolder : ERROR!\nCannot find the image[" + spriteLocation + "]")
                    Sprites_Data += (DefaultSprite,)

            elif currentLine[1] == "False":
                Sprites_Data += (pygame.image.load(spriteLocation).convert(),)
                print("Sprite.LoadFolder : ItemAdded[" + currentLine[0] + "]; Index[" + str(index) + "] Transparent: True\n")

            else:
                print("Sprite.LoadFolder : MetadataFileError!, Value[" + line + "] is invalid.")

    # -- Install Font Files to the Shared Resources Path -- #
    if utils.Directory_Exists(FolderName + "/FONT_PACKS"):
        print("Sprite.LoadFolder : Directory have Font Packs to be installed.")
        fontInstall_metadata = open(FolderName + "/FONT_PACKS/meta.data", "r")
        fontInstall_meta_lines = fontInstall_metadata.readlines()

        for font in fontInstall_meta_lines:
            font = font.rstrip()

            if not font.startswith("#"):
                CurrentFileName = FolderName + "/FONT_PACKS" + font
                DestinationDir = "Taiyou/SYSTEM/SOURCE/FONT" + font

                # -- Check if Destination Dir exist -- #
                if utils.File_Exists(DestinationDir):
                    print("Sprite.LoadFolder.CopyFontFile : FontFile \n[" + CurrentFileName + "] already exists.")
                else:
                    if not utils.File_Exists(CurrentFileName):
                        raise FileNotFoundError("The listed Font-Pack \n[" + CurrentFileName + "] does not exist.")

                    # -- Copy the Font File -- #
                    utils.FileCopy(CurrentFileName, DestinationDir)

                    # -- Check if Font File was copied -- #
                    if not utils.File_Exists(DestinationDir):
                        raise FileNotFoundError("An error occoured while copying the \n[" + CurrentFileName + "] font file.")

                    else:
                        print("Sprite.LoadFolder.CopyFontFile : \nFont[" + CurrentFileName + "] copied sucefully.")

    else:
        print("Sprite.LoadFolder : Directory does not have Font Packs to be installed.")

    print("Sprite.LoadFolder : Operation Completed.")


def LoadSprite(SpritePath, Transparency=False):
    if utils.Directory_Exists(SpritePath):
        Sprites_Name.append("/" + os.path.basename(SpritePath))

        if Transparency:
            Sprites_Data += (pygame.image.load(SpritePath).convert_alpha(),)

        else:
            Sprites_Data += (pygame.image.load(SpritePath).convert(), )


def GetSprite(SpriteResourceName):
    try:
        return Sprites_Data[Sprites_Name.index(SpriteResourceName)]
    except:
        print("GetSprite : Sprite[" + SpriteResourceName + "] does not exist.")
        return DefaultSprite


def Unload():
    print("Sprite.Unload : Unloading Sprites...")
    global Sprites_Data
    global Sprites_Name
    global CurrentLoadedFonts_Contents
    global CurrentLoadedFonts_Name

    utils.GarbageCollector_Collect()
    del Sprites_Data
    del Sprites_Name
    del CurrentLoadedFonts_Name
    utils.GarbageCollector_Collect()

    Sprites_Data = ()
    Sprites_Name = ()

    CurrentLoadedFonts_Contents = ()
    CurrentLoadedFonts_Name = ()

    print("Sprite.Unload : Reloading TaiyouUi Sprites...")

    # -- Reload Menu Sprites -- #
    LoadSpritesInFolder("Taiyou/SYSTEM/")

    print("Sprite.Unload : Operation Completed")


def Reload():
    print("Sprite.Reload : Reloading Sprites...")

    Unload()

    LoadSpritesInFolder(tge.Get_GameSourceFolder())

    # -- Reload Menu Sprites -- #
    LoadSpritesInFolder("Taiyou/SYSTEM/SOURCE")

    print("Sprite.Reload : Operation Completed")


def UnloadSprite(SpriteResourceName):
    try:
        sprite_index = Sprites_Name.index(SpriteResourceName)

        print("UnloadSprite : Sprite[" + SpriteResourceName + "] unloaded sucefully.")

        del Sprites_Data[sprite_index]
    except:
        print("UnloadSprite : Sprite[" + SpriteResourceName + "] does not exist.")


def ImageRender(DISPLAY, sprite, X, Y, Width=0, Height=0, SmoothScaling=False, Opacity=255, ColorKey=None, ImageNotLoaded=False):
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
            if IsOnScreen(DISPLAY, X, Y, Width, Height):
                # -- Set the Image Variable -- #
                if not ImageNotLoaded:
                    Image = GetSprite(sprite)
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

def IsOnScreen(DISPLAY, X, Y, Width, Height):
    return X <= DISPLAY.get_width() and X >= (0 - Width) and Y <= DISPLAY.get_height() and Y >= (0 - Height)

def FontRender(DISPLAY, FontFileLocation, Size, Text, ColorRGB, X, Y, antialias=True, backgroundColor=None, Opacity=255):
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
        FontFileObject = GetFont_object(FontFileLocation, Size)

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


def GetFont_object(FontFileLocation, Size):
    """
    Returns a Font Object on the Taiyou Font Cache
    :param FontFileLocation:The name of font file [starting with /]
    :param Size:Font Object Size
    :return:Font Object
    """
    global CurrentLoadedFonts_Contents
    global CurrentLoadedFonts_Name

    if not FontRenderingDisabled:
        FontCacheName = FontFileLocation + ":" + str(Size)
        try:
            return CurrentLoadedFonts_Contents[CurrentLoadedFonts_Name.index(FontCacheName)]

        except ValueError:  # -- Add font to the FontCache if was not found -- #
            print("Sprite.GetFontObject ; Creating Font Cache Object")

            CurrentLoadedFonts_Name += (FontCacheName,)
            CurrentLoadedFonts_Contents += (pygame.font.Font("Taiyou/SYSTEM/Data/FONT" + FontFileLocation, Size),)

            print("Sprite.GetFontObject ; FontCacheObjName: " + FontCacheName)

            return CurrentLoadedFonts_Contents[CurrentLoadedFonts_Name.index(FontCacheName)]


def Surface_Blur(surface, amt, fast_scale=False):
    """
    Applies blur to a Surface
    :param surface:Surface to be blurred
    :param amt:Amount of Blur [minimun 1.0]
    :param fast_scale:If true, pixalizate the surface insted of blurring
    :return:Returns the Blurred Surface
    """
    if amt < 1.0:
        print("Surface_Blue : Invalid Blur Amount.")
        return surface
    Scale = 1.0 / float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0] * Scale), int(surf_size[1] * Scale))
    if not fast_scale:
        surf = pygame.transform.smoothscale(surface, scale_size)
        surf = pygame.transform.smoothscale(surf, surf_size)
        return surf
    else:
        surf = pygame.transform.scale(surface, scale_size)
        surf = pygame.transform.scale(surf, surf_size)
        return surf


def Shape_Rectangle(DISPLAY, Color, Rectangle, BorderWidth=0, BorderRadius=0, Border_TopLeft_Radius=0, Border_TopRight_Radius=0, Border_BottomLeft_Radius=0, Border_BottomRight_Radius=0, DrawLines=False):
    if RectangleRenderingDisabled:
        return
    if Rectangle[0] <= DISPLAY.get_width() and Rectangle[0] >= 0 - Rectangle[2] and Rectangle[1] <= DISPLAY.get_height() and Rectangle[1] >= 0 - Rectangle[3]:
        # -- Fix the Color Range -- #
        Color = FixColorRange(Color)

        # -- Border Radius-- #
        if BorderRadius > 0 and Border_TopRight_Radius == 0 and Border_TopLeft_Radius == 0 and Border_BottomLeft_Radius == 0 and Border_BottomRight_Radius == 0:
            Border_TopRight_Radius = BorderRadius
            Border_TopLeft_Radius = BorderRadius
            Border_BottomRight_Radius = BorderRadius
            Border_BottomLeft_Radius = BorderRadius

        # -- Render the Rectangle -- #
        if not DrawLines:
            pygame.draw.rect(DISPLAY, Color, Rectangle, BorderWidth, BorderRadius, Border_TopLeft_Radius,
                             Border_TopRight_Radius, Border_BottomLeft_Radius, Border_BottomRight_Radius)
        else:
            gfxdraw.rectangle(DISPLAY, Rectangle, Color)

def Shape_Pie(DISPLAY, X, Y, Radius, StartAngle, StopAngle, Color):
    if X + Radius >= DISPLAY.get_width() or X < Radius:
        Color = FixColorRange(Color)

        gfxdraw.pie(DISPLAY, X, Y, Radius, StartAngle, StopAngle, Color)

def FixColorRange(ColorArguments):
    """
    Fix the Color Range (0 - 255)
    :param ColorArguments: Input
    :return: Output
    """
    ColorArguments = list(ColorArguments)

    if len(ColorArguments) < 4:  # -- Add the Alpha Argument
        ColorArguments.append(255)

    # -- Limit the Color Range -- #
    if int(ColorArguments[0]) < 0:  # -- R
        ColorArguments[0] = 0
    if int(ColorArguments[1]) < 0:  # -- G
        ColorArguments[1] = 0
    if int(ColorArguments[2]) < 0:  # -- B
        ColorArguments[2] = 0
    if int(ColorArguments[3]) < 0:  # -- A
        ColorArguments[3] = 0

    if int(ColorArguments[0]) > 255:  # -- R
        ColorArguments[0] = 255
    if int(ColorArguments[1]) > 255:  # -- G
        ColorArguments[1] = 255
    if int(ColorArguments[2]) > 255:  # -- B
        ColorArguments[2] = 255
    if int(ColorArguments[3]) > 255:  # -- A
        ColorArguments[3] = 255

    return ColorArguments

def GetFont_width(FontFileLocation, FontSize, Text):
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
        CurrentSize += GetFont_object(FontFileLocation, FontSize).render(l, True, (255, 255, 255)).get_width()

        if CurrentSize > TotalSize:
            TotalSize = CurrentSize

    return TotalSize


def GetFont_height(FontFileLocation, FontSize, Text):
    """
    Get the height of a font, from a specified text.
    :param FontFileLocation:FontFile Name
    :param FontSize:FontSize
    :param Text:Text
    :return:Size (int)
    """

    return GetFont_object(FontFileLocation, FontSize).render(Text, True, (255, 255, 255)).get_height() * len(
        Text.splitlines())

def GetImage_DominantColor(Surface, Number_Clusters=5):
    strFormat = 'RGBA'
    raw_str = pygame.image.tostring(Surface, strFormat)
    ConvertedImage = Image.frombytes(strFormat, Surface.get_size(), raw_str)

    ConvertedImage = ConvertedImage.resize((100, 100))  # optional, to reduce time
    ar = np.asarray(ConvertedImage)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

    codes, dist = scipy.cluster.vq.kmeans(ar, Number_Clusters)

    vecs, dist = scipy.cluster.vq.vq(ar, codes)  # assign codes
    counts, bins = scipy.histogram(vecs, len(codes))  # count occurrences

    index_max = scipy.argmax(counts)  # find most frequent
    peak = codes[index_max]
    return peak

def BlurredRectangle(DISPLAY, Rectangle,BlurAmmount=100, BlackContrast=50):
    """
    Render a blurred Rectangle, usefull for UI.
    :param DISPLAY:The surface to be blitted
    :param Rectangle:Rectangle
    :param BlurAmmount:The ammount of blur (value higher than 100 is recomended)
    :param BlackContrast:The ammount of Black Color (usefull for contrast in bright surfaces)
    :return:
    """
    # -- the Result Surface -- #
    ResultPanel = pygame.Surface((Rectangle[2], Rectangle[3]), pygame.HWSURFACE | pygame.HWACCEL)

    if not BlackContrast == 0:
        DarkerBG = pygame.Surface((Rectangle[2], Rectangle[3]), pygame.HWSURFACE | pygame.HWACCEL)
        DarkerBG.set_alpha(BlackContrast)
        DISPLAY.blit(DarkerBG, Rectangle)

    # -- Only Blur the Necessary Area -- #
    AreaToBlur = pygame.Surface((Rectangle[2], Rectangle[3]), pygame.HWSURFACE | pygame.HWACCEL)
    AreaToBlur.blit(DISPLAY, (0, 0), Rectangle)

    # -- Then Finnaly, blit the Blurred Result -- #
    ResultPanel.blit(Surface_Blur(AreaToBlur, BlurAmmount, False), (0, 0))

    DISPLAY.blit(ResultPanel, (Rectangle[0], Rectangle[1]))
