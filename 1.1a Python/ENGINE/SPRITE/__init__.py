# -- Imports --
import ENGINE.Utils as utils
import pygame

print("TaiyouGameEngine Sprite Utilitary version 1.0")

# -- Variables --
Sprites_Name = list()
Sprites_Data = list()
Fonts_Name = list()
Fonts_Data = list()
Movies_Name = list()
Movies_Data = list()

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

        CorrectKeyName = x.replace(FolderName,"")
        Sprites_Name.append(CorrectKeyName)
        Sprites_Data.append(pygame.image.load(x))

        print("LoadSpritesInFolder : ItemAdded[" + CorrectKeyName + "]; Index[" + str(index) + "]\n")



    print("LoadSpritesInFolder : Loading all Fonts...")
    index = -1
    for f in temp_font_files:
        index += 1
        print("\nLoadFontInFolder : File[" + f + "] detected; Index[" + str(index) + "]")

        CorrectKeyName = f.replace(FontFolderName,"")
        Fonts_Name.append(CorrectKeyName)
        Fonts_Data.append(pygame.font.Font(f, 16))

        print("LoadFontsInFolder : ItemAdded[" + CorrectKeyName + "]; Index[" + str(index) + "]\n")

    print("LoadSpritesInFolder : Operation Completed.")

def GetSprite(SpriteResourceName,Width=0,Height=0):
    try:
        sprite_index = Sprites_Name.index(SpriteResourceName)
        spriteData = Sprites_Data[sprite_index]
        if Width > 0:
            spriteData = pygame.transform.scale(spriteData, (Height, Width))

        return spriteData
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

def RotoZoom(spriteName,angle,scale):
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

def Render(DISPLAY, spriteName, X, Y, Width, Height):
    try:

        DISPLAY.blit(pygame.transform.scale(Sprites_Data[Sprites_Name.index(spriteName)], (Width, Height)), (X, Y, Width, Height))

    except:
        print("GetSprite : Sprite[" + spriteName + "] does not exist.")
        DISPLAY.blit(DefaultSprite, (X, Y, Width, Height))


CurrentLoadedFonts_Name = list()
CurrentLoadedFonts_Contents = list()
def RenderFont(DISPLAY, FontFileLocation, Size, Text, ColorRGB, X, Y, atialias=True):
    try:
        fontRender = CurrentLoadedFonts_Contents[CurrentLoadedFonts_Name.index(utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation + ",S:" + str(Size))].render(Text, atialias,ColorRGB)

        DISPLAY.blit(fontRender, (X, Y))
    except:
        CurrentLoadedFonts_Name.append(utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation + ",S:" + str(Size))
        CurrentLoadedFonts_Contents.append(pygame.font.Font(utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation,Size))
        print("RenderFont ; LoadedFont: " + utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation + ",S:" + str(Size))
        font = pygame.font.SysFont('random', Size, True, False)
        text = font.render(Text, atialias, ColorRGB)

        DISPLAY.blit(text,(X,Y))
def RenderRectangle(DISPLAY,Color,Rectangle):
    pygame.draw.rect(DISPLAY, Color, Rectangle)

def GetText_width(FontFileLocation, FontSize, Text):
    try:
        fontRender = CurrentLoadedFonts_Contents[CurrentLoadedFonts_Name.index(utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation + ",S:" + str(FontSize))].render(Text, True, (255,255,255))
        return fontRender.get_width()
    except:
        CurrentLoadedFonts_Name.append(utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation + ",S:" + str(FontSize))
        CurrentLoadedFonts_Contents.append(pygame.font.Font(utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation, FontSize))
        fontRender = CurrentLoadedFonts_Contents[CurrentLoadedFonts_Name.index(utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation + ",S:" + str(FontSize))].render(Text, True, (255, 255, 255))
        print("GetText_width ; LoadedFont: " + utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation + ",S:" + str(FontSize))
        return fontRender.get_width()

def GetText_height(FontFileLocation, FontSize, Text):
    try:
        fontRender = CurrentLoadedFonts_Contents[CurrentLoadedFonts_Name.index(utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation + ",S:" + str(FontSize))].render(Text, True, (255,255,255))
        return fontRender.get_height()
    except:
        CurrentLoadedFonts_Name.append(utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation + ",S:" + str(FontSize))
        CurrentLoadedFonts_Contents.append(pygame.font.Font(utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation, FontSize))
        fontRender = CurrentLoadedFonts_Contents[CurrentLoadedFonts_Name.index(utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation + ",S:" + str(FontSize))].render(Text, True, (255, 255, 255))
        print("GetText_height ; LoadedFont:" + utils.GetCurrentSourceFolder() + "/FONT" + FontFileLocation + ",S:" + str(FontSize))
        return fontRender.get_height()
