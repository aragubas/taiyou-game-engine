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

print("TaiyouGameEngine Sprite Utilitary version " + tge.Get_SpriteVersion())

# -- Variables --
Sprites_Name = list()
Sprites_Data = list()
Fonts_Name = list()
Fonts_Data = list()

DefaultSprite = pygame.image.load("Taiyou/SYSTEM/SOURCE/SPRITE/default.png")

FontRenderingDisabled = False
SpriteRenderingDisabled = False
RectangleRenderingDisabled = False
SpriteTransparency = False

def LoadSpritesInFolder(FolderName):
    pygame.font.init()
    folder_name = FolderName + "/SPRITE"
    index = -1

    sprite_metadata = open(FolderName + "/SPRITE/meta.data", "r")
    sprite_meta_lines = sprite_metadata.readlines()

    print("LoadSpritesInFolder : Loading all Sprites...")

    for line in sprite_meta_lines:
        line = line.rstrip()
        if not line.startswith('#') and not line == "":
            currentLine = line.split(':')
            spriteLocation = folder_name + currentLine[0]
            print("[{0}]".format(spriteLocation))
            Sprites_Name.append(currentLine[0])

            if currentLine[1] == "True":
                try:
                    if not SpriteTransparency:
                        Sprites_Data.append(pygame.image.load(spriteLocation).convert_alpha())
                    else:
                        Sprites_Data.append(pygame.image.load(spriteLocation).convert())
                    print("Sprite.LoadFolder : ItemAdded[" + currentLine[0] + "]; Index[" + str(index) + "] Transparent: True\n")
                except FileNotFoundError:
                    print("Sprite.LoadFolder : ERROR!\nCannot find the image[" + spriteLocation + "]")
                    Sprites_Data.append(DefaultSprite)

            elif currentLine[1] == "False":
                Sprites_Data.append(pygame.image.load(spriteLocation).convert())
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

                if utils.File_Exists(DestinationDir):
                    print("Sprite.LoadFolder.CopyFontFile : FontFile \n[" + CurrentFileName + "] already exists.")
                else:
                    if not utils.File_Exists(CurrentFileName):
                        raise FileNotFoundError("The listed Font-Pack \n[" + CurrentFileName + "] does not exist.")

                    utils.FileCopy(CurrentFileName, DestinationDir)

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
            Sprites_Data.append(pygame.image.load(SpritePath).convert_alpha())
        else:
            Sprites_Data.append(pygame.image.load(SpritePath).convert())

def GetSprite(SpriteResourceName):
    try:
        return Sprites_Data[Sprites_Name.index(SpriteResourceName)]
    except:
        print("GetSprite : Sprite[" + SpriteResourceName + "] does not exist.")
        return DefaultSprite

def Unload():
    print("Sprite.Unload : Unloading Sprites...")

    Sprites_Data.clear()
    Sprites_Name.clear()

    CurrentLoadedFonts_Contents.clear()
    CurrentLoadedFonts_Name.clear()

    print("Sprite.Unload : Opearation Completed")

    # -- Reload Menu Sprites -- #
    LoadSpritesInFolder("Taiyou/SYSTEM/SOURCE")


def Reload():
    print("Sprite.Reload : Reloading Sprites...")

    Unload()

    LoadSpritesInFolder(tge.Get_GameSourceFolder())

    # -- Reload Menu Sprites -- #
    LoadSpritesInFolder("Taiyou/SYSTEM/SOURCE")

def UnloadSprite(SpriteResourceName):
    try:
        sprite_index = Sprites_Name.index(SpriteResourceName)

        print("UnloadSprite : Sprite[" + SpriteResourceName + "] unloaded sucefully.")

        del Sprites_Data[sprite_index]
    except:
        print("UnloadSprite : Sprite[" + SpriteResourceName + "] does not exist.")


def ImageRender(DISPLAY, spriteName, X, Y, Width=0, Height=0, SmoothScaling=False):
    """
    Render a Image loaded to the Sprite System
    :param DISPLAY:Surface to be rendered
    :param spriteName:Sprite Resource Name [starting with /]
    :param X:X Location
    :param Y:Y Location
    :param Width:Scale Width
    :param Height:Scale Height
    :param SmoothScaling:Smooth Pixels [This option can decrease peformace]
    :return:
    """
    if not SpriteRenderingDisabled:
        try:
            if X <= DISPLAY.get_width() and X >= 0 - Width and Y <= DISPLAY.get_height() and Y >= 0 - Height:
                if Width == 0 and Height == 0:
                    DISPLAY.blit(GetSprite(spriteName), (X, Y))
                else:
                    if not SmoothScaling:
                        DISPLAY.blit(pygame.transform.scale(GetSprite(spriteName), (Width, Height)), (X, Y))
                    else:
                        DISPLAY.blit(pygame.transform.smoothscale(GetSprite(spriteName), (Width, Height)), (X, Y))

        except Exception as ex:
            print("Sprite.Render : Error while rendering sprite;\n" + str(ex))

CurrentLoadedFonts_Name = list()
CurrentLoadedFonts_Contents = list()
def FontRender(DISPLAY, FontFileLocation, Size, Text, ColorRGB, X, Y, antialias=True, backgroundColor=(-1, -1, -1)):
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
        if X <= DISPLAY.get_width() and Y <= DISPLAY.get_height() and X >= -GetFont_width(FontFileLocation, Size, Text) and Y >= -GetFont_height(FontFileLocation, Size, Text) and not Text == "" or not Text == " ":
            # -- Only Render Multiple Lines when needed -- #
            if len(Text.splitlines()) > 1:
                for i, l in enumerate(Text.splitlines()):
                    if not backgroundColor == (-1, -1, -1):
                        DISPLAY.blit(GetFont_object(FontFileLocation, Size).render(l, antialias, ColorRGB, backgroundColor), (X, Y + Size * i))
                    else:
                        DISPLAY.blit(GetFont_object(FontFileLocation, Size).render(l, antialias, ColorRGB), (X, Y + Size * i))

            else:
                if not backgroundColor == (-1, -1, -1):
                    DISPLAY.blit(GetFont_object(FontFileLocation, Size).render(Text, antialias, ColorRGB, backgroundColor), (X, Y))
                else:
                    DISPLAY.blit(GetFont_object(FontFileLocation, Size).render(Text, antialias, ColorRGB), (X, Y))

def GetFont_object(FontFileLocation, Size):
    """
    Returns a Font Object on the Taiyou Font Cache
    :param FontFileLocation:The name of font file [starting with /]
    :param Size:Font Object Size
    :return:Font Object
    """
    if not FontRenderingDisabled:
        FontCacheName = FontFileLocation + ":" + str(Size)
        try:
            return CurrentLoadedFonts_Contents[CurrentLoadedFonts_Name.index(FontCacheName)]

        except ValueError: # -- Add font to the FontCache if was not found -- #
            print("Sprite.GetFontObject ; Creating Font Cache Object")

            CurrentLoadedFonts_Name.append(FontCacheName)
            CurrentLoadedFonts_Contents.append(pygame.font.Font("Taiyou/SYSTEM/SOURCE/FONT" + FontFileLocation, Size))

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
    scale = 1.0/float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
    if not fast_scale:
        surf = pygame.transform.smoothscale(surface, scale_size)
        surf = pygame.transform.smoothscale(surf, surf_size)
    else:
        surf = pygame.transform.scale(surface, scale_size)
        surf = pygame.transform.scale(surf, surf_size)
    return surf

def Shape_Rectangle(DISPLAY, Color, Rectangle, BorderWidth=0, BorderRadius=0, Border_TopLeft_Radius=0, Border_TopRight_Radius=0, Border_BottomLeft_Radius=0, Border_BottomRight_Radius=0):
    if RectangleRenderingDisabled:
        return
    if Rectangle[0] <= DISPLAY.get_width() and Rectangle[0] >= 0 - Rectangle[2] and Rectangle[1] <= DISPLAY.get_height() and Rectangle[1] >= 0 - Rectangle[3]:
        Color = list(Color)
        # -- Fix Color RGBA RGB Confusion -- #
        if len(Color) < 4:
            Color.append(255)
        if Color[0] <= 0:
            Color[0] = 0
        if Color[1] <= 0:
            Color[1] = 0
        if Color[2] <= 0:
            Color[2] = 0
        if Color[3] <= 0:
            Color[3] = 0

        # -- Border Radius-- #
        if BorderRadius > 0 and Border_TopRight_Radius == 0 and Border_TopLeft_Radius == 0 and Border_BottomLeft_Radius == 0 and Border_BottomRight_Radius == 0:
            Border_TopRight_Radius = BorderRadius
            Border_TopLeft_Radius = BorderRadius
            Border_BottomRight_Radius = BorderRadius
            Border_BottomLeft_Radius = BorderRadius

        # -- Render the Rectangle -- #
        pygame.draw.rect(DISPLAY, Color, Rectangle, BorderWidth, BorderRadius, Border_TopLeft_Radius, Border_TopRight_Radius, Border_BottomLeft_Radius, Border_BottomRight_Radius)

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

    return GetFont_object(FontFileLocation, FontSize).render(Text, True, (255, 255, 255)).get_height() * len(Text.splitlines())
