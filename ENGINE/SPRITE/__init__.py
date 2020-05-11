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
import sys

print("TaiyouGameEngine Sprite Utilitary version " + tge.Get_SpriteVersion())

# -- Variables --
Sprites_Name = list()
Sprites_Data = list()
Fonts_Name = list()
Fonts_Data = list()

DefaultSprite = pygame.image.load("Taiyou/HOME/SOURCE/SPRITE/default.png")

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

    try:
        for line in sprite_meta_lines:
            line = line.rstrip()
            if not line.startswith('#'):
                currentLine = line.split(':')
                spriteLocation = folder_name + currentLine[0]
                print("[{0}]".format(spriteLocation))

                if currentLine[1] == "True":
                    Sprites_Name.append(currentLine[0])
                    if not SpriteTransparency:
                        Sprites_Data.append(pygame.image.load(spriteLocation).convert_alpha())
                    else:
                        Sprites_Data.append(pygame.image.load(spriteLocation).convert())
                    print("Sprite.LoadFolder : ItemAdded[" + currentLine[0] + "]; Index[" + str(index) + "] Transparent: True\n")

                elif currentLine[1] == "False":
                    Sprites_Name.append(currentLine[0])
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
                    DestinationDir = "Taiyou/HOME/SOURCE/FONT" + font

                    if utils.File_Exists(DestinationDir):
                        print("Sprite.LoadFolder.CopyFontFile : FontFile [" + CurrentFileName + "] already exists.")
                    else:
                        if not utils.File_Exists(CurrentFileName):
                            raise FileNotFoundError("The listed Font-Pack [" + CurrentFileName + "] does not exist.")

                        utils.FileCopy(CurrentFileName, DestinationDir)

                        if not utils.File_Exists(DestinationDir):
                            raise FileNotFoundError("An error occoured while copying the [" + CurrentFileName + "] font file.")
                        else:
                            print("Sprite.LoadFolder.CopyFontFile : Font[" + CurrentFileName + "] copied sucefully.")

        else:
            print("Sprite.LoadFolder : Directory does not have Font Packs to be installed.")

    except FileNotFoundError as ex:
        print("\n\nFILE_NOT_FOUND_ERROR:\n" + str(ex))
        sys.exit()

    print("Sprite.LoadFolder : Operation Completed.")

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

def Reload():
    print("Sprite.Reload : Reloading Sprites...")

    Unload()

    LoadSpritesInFolder(tge.Get_GameSourceFolder())

def UnloadSprite(SpriteResourceName):
    try:
        sprite_index = Sprites_Name.index(SpriteResourceName)

        print("UnloadSprite : Sprite[" + SpriteResourceName + "] unloaded sucefully.")

        del Sprites_Data[sprite_index]
    except:
        print("UnloadSprite : Sprite[" + SpriteResourceName + "] does not exist.")

def Render(DISPLAY, spriteName, X, Y, Width, Height):
    if SpriteRenderingDisabled:
        return
    if X <= DISPLAY.get_width() and X >= 0 - Width and Y <= DISPLAY.get_height() and Y >= 0 - Height:
        DISPLAY.blit(pygame.transform.scale(GetSprite(spriteName), (Width, Height)), (X, Y))
    else:
        return

CurrentLoadedFonts_Name = list()
CurrentLoadedFonts_Contents = list()
def RenderFont(DISPLAY, FontFileLocation, Size, Text, ColorRGB, X, Y, atialias=True):
    if FontRenderingDisabled:
        return
    try:
        if X <= DISPLAY.get_width() and Y <= DISPLAY.get_height() and X >= -GetText_width(FontFileLocation,Size,Text) and Y >= -GetText_height(FontFileLocation,Size,Text):
            for i, l in enumerate(Text.splitlines()):
                DISPLAY.blit(CurrentLoadedFonts_Contents[CurrentLoadedFonts_Name.index("Taiyou/HOME/SOURCE/FONT" + FontFileLocation + ",S:" + str(Size))].render(l, atialias, ColorRGB), (X, Y + Size * i))
        else:
            return

    except Exception as ex:
        CurrentLoadedFonts_Name.append("Taiyou/HOME/SOURCE/FONT" + FontFileLocation + ",S:" + str(Size))
        CurrentLoadedFonts_Contents.append(pygame.font.Font("Taiyou/HOME/SOURCE/FONT" + FontFileLocation, Size))
        print("RenderFont ; LoadedFont: " + "Taiyou/HOME/SOURCE/FONT" + FontFileLocation + ",S:" + str(Size))
        print("RenderFont ; Detailed Error: " + str(ex))

def GetFontObject(FontFileLocation, Size):
    if FontRenderingDisabled:
        return

    try:
        return CurrentLoadedFonts_Contents[CurrentLoadedFonts_Name.index("Taiyou/HOME/SOURCE/FONT" + FontFileLocation + ",S:" + str(Size))]
    except Exception as ex:
        CurrentLoadedFonts_Name.append("Taiyou/HOME/SOURCE/FONT" + FontFileLocation + ",S:" + str(Size))
        CurrentLoadedFonts_Contents.append(pygame.font.Font("Taiyou/HOME/SOURCE/FONT" + FontFileLocation, Size))
        print("RenderFont ; LoadedFont: " + "Taiyou/HOME/SOURCE/FONT" + FontFileLocation + ",S:" + str(Size))
        print("RenderFont ; Detailed Error: " + str(ex))

        return CurrentLoadedFonts_Contents[CurrentLoadedFonts_Name.index("Taiyou/HOME/SOURCE/FONT" + FontFileLocation + ",S:" + str(Size))]

def RenderWrappedFont(text, font, colour, x, y, screen, allowed_width):
    words = text.split()
    lines = []
    while len(words) > 0:
        # get as many words as will fit within allowed_width
        line_words = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw, fh = font.size(' '.join(line_words + words[:1]))
            if fw > allowed_width:
                break

        # add a line consisting of those words
        line = ' '.join(line_words)
        lines.append(line)

    y_offset = 0
    for line in lines:
        fw, fh = font.size(line)
        ty = y + y_offset

        font_surface = font.render(line, True, colour)
        screen.blit(font_surface, (x, ty))

        y_offset += fh


def Surface_Blur(surface, amt):
    if amt < 1.0:
        print("Surface_Blue : Invalid Blur Amount.")
        return surface
    scale = 1.0/float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf

def Surface_Pixalizate(surface, amt):
    if amt < 1.0:
        print("Surface_Blue : Invalid Blur Amount.")
        return surface
    scale = 1.0/float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
    surf = pygame.transform.scale(surface, scale_size)
    surf = pygame.transform.scale(surf, surf_size)
    return surf

def RenderRectangle(DISPLAY, Color, Rectangle):
    if RectangleRenderingDisabled:
        return
    if Rectangle[0] <= DISPLAY.get_width() and Rectangle[0] >= 0 - Rectangle[2] and Rectangle[1] <= DISPLAY.get_height() and Rectangle[1] >= 0 - Rectangle[3]:
        Color = list(Color)
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
        pygame.draw.rect(DISPLAY, Color, Rectangle)

def GetText_width(FontFileLocation, FontSize, Text):
    try:
        for i, l in enumerate(Text.splitlines()):
            return CurrentLoadedFonts_Contents[CurrentLoadedFonts_Name.index("Taiyou/HOME/SOURCE/FONT" + FontFileLocation + ",S:" + str(FontSize))].render(l, True, (255, 255, 255)).get_width()

    except:
        CurrentLoadedFonts_Name.append("Taiyou/HOME/SOURCE/FONT" + FontFileLocation + ",S:" + str(FontSize))
        CurrentLoadedFonts_Contents.append(pygame.font.Font("Taiyou/HOME/SOURCE/FONT" + FontFileLocation, FontSize))
        print("GetText_width ; LoadedFont: " + "Taiyou/HOME/SOURCE/FONT" + FontFileLocation + ",S:" + str(FontSize))
        return 0


def GetText_height(FontFileLocation, FontSize, Text):
    try:
        return CurrentLoadedFonts_Contents[CurrentLoadedFonts_Name.index("Taiyou/HOME/SOURCE/FONT" + FontFileLocation + ",S:" + str(FontSize))].render(Text, True, (255,255,255)).get_height() * len(Text.splitlines())
    except:
        CurrentLoadedFonts_Name.append("Taiyou/HOME/SOURCE/FONT" + FontFileLocation + ",S:" + str(FontSize))
        CurrentLoadedFonts_Contents.append(pygame.font.Font("Taiyou/HOME/SOURCE/FONT" + FontFileLocation, FontSize))
        print("GetText_height ; LoadedFont:" + "Taiyou/HOME/SOURCE/FONT" + FontFileLocation + ",S:" + str(FontSize))
        return 0
