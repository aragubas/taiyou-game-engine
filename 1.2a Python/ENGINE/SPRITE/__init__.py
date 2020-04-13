#!/usr/bin/env python3.7
# -- Imports --
import ENGINE.Utils as utils
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
    FontFolderName = FolderName + "/FONT"
    FolderName = FolderName + "/SPRITE"
    temp_sprites_files = utils.GetFileInDir(FolderName)
    temp_font_files = utils.GetFileInDir(FontFolderName)
    index = -1

    print("LoadSpritesInFolder : Loading all Sprites...")
    for x in temp_sprites_files:
        index += 1
        print("\nLoadSpritesInFolder : File[" + x + "] detected; Index[" + str(index) + "]")

        CorrectKeyName = x.replace(FolderName, "")
        Sprites_Name.append(CorrectKeyName)
        Sprites_Data.append(pygame.image.load(x))

        print("LoadSpritesInFolder : ItemAdded[" + CorrectKeyName + "]; Index[" + str(index) + "]\n")

    print("LoadSpritesInFolder : Operation Completed.")

def GetSprite(SpriteResourceName):
    try:
        return Sprites_Data[Sprites_Name.index(SpriteResourceName)]
    except:
        print("GetSprite : Sprite[" + SpriteResourceName + "] does not exist.")
        return DefaultSprite


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
def Render(DISPLAY, spriteName, X, Y, Width=0, Height=0):
    try:
        if X <= DISPLAY.get_width() and X >= 0 - Width and Y <= DISPLAY.get_height() and Y >= 0 - Height:
            TransformedID = TransformedSpriteCache_Name.index(spriteName + " [{0},{1}]".format(str(Width), str(Height)))
            DISPLAY.blit(TransformedSpriteCache[TransformedID], (X, Y))
        else:
            return

    except:
        TransformedSpriteCache_Name.append(spriteName + " [{0},{1}]".format(str(Width),str(Height)))
        TransformedSpriteCache.append(pygame.transform.scale(Sprites_Data[Sprites_Name.index(spriteName)], (Width, Height)))
        print("GetSprite : Sprite [{0}] added to the Transform Cache.".format(spriteName))


CurrentLoadedFonts_Name = list()
CurrentLoadedFonts_Contents = list()
def RenderFont(DISPLAY, FontFileLocation, Size, Text, ColorRGB, X, Y, atialias=True):
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

def RenderRectangle(DISPLAY, Color, Rectangle):
    if Rectangle[0] <= DISPLAY.get_width() and Rectangle[0] >= 0 - Rectangle[2] and Rectangle[1] <= DISPLAY.get_height() and Rectangle[1] >= 0 - Rectangle[3]:
        Color = list(Color)
        if Color[0] <= 0:
            Color[0] = 0
        if Color[1] <= 0:
            Color[1] = 0
        if Color[2] <= 0:
            Color[2] = 0
        pygame.draw.rect(DISPLAY, Color, Rectangle)


def GetText_width(FontFileLocation, FontSize, Text):
    try:
        for i, l in enumerate(Text.splitlines()):
            return CurrentLoadedFonts_Contents[CurrentLoadedFonts_Name.index(utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation + ",S:" + str(FontSize))].render(l, True, (255,255,255)).get_width()
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
