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
import threading
import pygame

print("TaiyouGameEngine Sprite Utilitary version 1.0")

# -- Variables --
Sprites_Name = list()
Sprites_Data = list()
Fonts_Name = list()
Fonts_Data = list()

DefaultSprite = pygame.image.load("default.png")

def LoadSpritesInFolder(FolderName):
    pygame.font.init()
    folder_name = FolderName + "/SPRITE"
    index = -1

    sprite_metadata = open(utils.GetCurrentSourceFolder() + "/SPRITE/meta.data", "r")
    sprite_meta_lines = sprite_metadata.readlines()

    print("LoadSpritesInFolder : Loading all Sprites...")

    for line in sprite_meta_lines:
        line = line.rstrip()
        if not line.startswith('#'):
            currentLine = line.split(':')
            spriteLocation = folder_name + currentLine[0]
            print("[{0}]".format(spriteLocation))

            if currentLine[1] == "True":
                Sprites_Name.append(currentLine[0])
                Sprites_Data.append(pygame.image.load(spriteLocation).convert_alpha())
                print("LoadSpritesInFolder : ItemAdded[" + currentLine[0] + "]; Index[" + str(index) + "] Transparent: True\n")

            elif currentLine[1] == "False":
                Sprites_Name.append(currentLine[0])
                Sprites_Data.append(pygame.image.load(spriteLocation).convert())
                print("LoadSpritesInFolder : ItemAdded[" + currentLine[0] + "]; Index[" + str(index) + "] Transparent: True\n")
            else:
                print("LoadSpritesInFolder : MetadataFileError!, Value[" + line + "] is invalid.")


    print("LoadSpritesInFolder : Operation Completed.")

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

    print("Sprite.Unload : Opearation Completed")

def Reload():
    print("Sprite.Reload : Reloading Sprites...")

    Unload()

    LoadSpritesInFolder(tge.Get_GameSourceFolder + "/SPRITE")



def UnloadSprite(SpriteResourceName):
    try:
        sprite_index = Sprites_Name.index(SpriteResourceName)

        print("UnloadSprite : Sprite[" + SpriteResourceName + "] unloaded sucefully.")

        del Sprites_Data[sprite_index]
    except:
        print("UnloadSprite : Sprite[" + SpriteResourceName + "] does not exist.")

def Flip(spriteName, x_flip,y_flip):
    try:
        sprite_index = Sprites_Name.index(spriteName)

        Sprites_Data[sprite_index] = pygame.transform.flip(Sprites_Data[sprite_index], x_flip, y_flip)

    except:
        print("FlipSprite : Sprite[" + spriteName + "] does not exist.")


def Scale(spriteName,width,height):
    try:
        sprite_index = Sprites_Name.index(spriteName)

        Sprites_Data[sprite_index] = pygame.transform.scale(Sprites_Data[sprite_index], (width,height))

    except:
        print("ScaleSprite : Sprite[" + spriteName + "] does not exist.")

def Rotate(spriteName,angle):
    try:
        sprite_index = Sprites_Name.index(spriteName)

        Sprites_Data[sprite_index] = pygame.transform.Rotate(Sprites_Data[sprite_index], angle)

    except:
        print("RotateSprite : Sprite[" + spriteName + "] does not exist.")

def RotoZoom(spriteName, angle, scale):
    try:
        sprite_index = Sprites_Name.index(spriteName)

        Sprites_Data[sprite_index] = pygame.transform.rotozoom(Sprites_Data[sprite_index], angle, scale)

    except:
        print("RotoZoomSprite : Sprite[" + spriteName + "] does not exist.")

def SmoothScale(spriteName, width, height):
    try:
        sprite_index = Sprites_Name.index(spriteName)

        Sprites_Data[sprite_index] = pygame.transform.smoothscale(Sprites_Data[sprite_index], (width, height))

    except:
        print("SmoothScale : Sprite[" + spriteName + "] does not exist.")

def Chop(spriteName, rectangle):
    try:
        sprite_index = Sprites_Name.index(spriteName)

        Sprites_Data[sprite_index] = pygame.transform.chop(Sprites_Data[sprite_index], rectangle)

    except:
        print("ChopSprite : Sprite[" + spriteName + "] does not exist.")

TransformedSpriteCache_Name = list()
TransformedSpriteCache = list()
def Render(DISPLAY, spriteName, X, Y, Width, Height):
    RenderProcess = threading.Thread(target=RealRender(DISPLAY, spriteName, X, Y, Width, Height))
    RenderProcess.daemon = True
    RenderProcess.run()


def RealRender(DISPLAY, spriteName, X, Y, Width, Height):
    try:
        if X <= DISPLAY.get_width() and X >= 0 - Width and Y <= DISPLAY.get_height() and Y >= 0 - Height:
            TransformedID = TransformedSpriteCache_Name.index(spriteName + " [{0},{1}]".format(str(Width), str(Height)))
            DISPLAY.blit(TransformedSpriteCache[TransformedID], (X, Y))
        else:
            return

    except:
        TransformedSpriteCache_Name.append(spriteName + " [{0},{1}]".format(str(Width),str(Height)))
        TransformedSpriteCache.append(pygame.transform.scale(GetSprite(spriteName), (Width, Height)))
        print("Render : Sprite [{0}] added to the Transform Cache.".format(spriteName))

CurrentLoadedFonts_Name = list()
CurrentLoadedFonts_Contents = list()
def RenderFont(DISPLAY, FontFileLocation, Size, Text, ColorRGB, X, Y, atialias=True):
    RenderProcess = threading.Thread(target=RealRenderFont(DISPLAY, FontFileLocation, Size, Text, ColorRGB, X, Y, atialias))
    RenderProcess.daemon = True
    RenderProcess.run()

def RealRenderFont(DISPLAY, FontFileLocation, Size, Text, ColorRGB, X, Y, atialias=True):
    try:
        if X <= DISPLAY.get_width() and Y <= DISPLAY.get_height() and X >= -GetText_width(FontFileLocation,Size,Text) and Y >= -GetText_height(FontFileLocation,Size,Text):
            for i, l in enumerate(Text.splitlines()):
                DISPLAY.blit(CurrentLoadedFonts_Contents[CurrentLoadedFonts_Name.index(utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation + ",S:" + str(Size))].render(l, atialias, ColorRGB), (X, Y + Size * i))
        else:
            return

    except Exception as ex:
        CurrentLoadedFonts_Name.append(utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation + ",S:" + str(Size))
        CurrentLoadedFonts_Contents.append(pygame.font.Font(utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation, Size))
        print("RenderFont ; LoadedFont: " + utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation + ",S:" + str(Size))
        print("RenderFont ; Detailed Error: " + str(ex))

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
    RenderProcess = threading.Thread(target=RealRenderRectangle(DISPLAY, Color, Rectangle))
    RenderProcess.daemon = True
    RenderProcess.run()

def RealRenderRectangle(DISPLAY, Color, Rectangle):
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
            return CurrentLoadedFonts_Contents[CurrentLoadedFonts_Name.index(utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation + ",S:" + str(FontSize))].render(l, True, (255, 255, 255)).get_width()

    except:
        CurrentLoadedFonts_Name.append(utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation + ",S:" + str(FontSize))
        CurrentLoadedFonts_Contents.append(pygame.font.Font(utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation, FontSize))
        print("GetText_width ; LoadedFont: " + utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation + ",S:" + str(FontSize))
        return 0


def GetText_height(FontFileLocation, FontSize, Text):
    try:
        return CurrentLoadedFonts_Contents[CurrentLoadedFonts_Name.index(utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation + ",S:" + str(FontSize))].render(Text, True, (255,255,255)).get_height() * len(Text.splitlines())
    except:
        CurrentLoadedFonts_Name.append(utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation + ",S:" + str(FontSize))
        CurrentLoadedFonts_Contents.append(pygame.font.Font(utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation, FontSize))
        print("GetText_height ; LoadedFont:" + utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation + ",S:" + str(FontSize))
        return 0
