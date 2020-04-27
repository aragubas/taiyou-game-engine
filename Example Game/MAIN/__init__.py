from ENGINE import SPRITE as sprite
from ENGINE import REGISTRY as reg
import pygame
from math import *

# -- Game Engine Messages -- #
Messages = list()


CursorPosition = 0,0

MapData = list()
Cursor_MapX = 0
Cursor_MapY = 0
Map_X = 0
Map_Y = 0
Map_SizeW = 32
Map_SizeH = 32
Map_TileSize = 32
Viewport_TilesW = 25
Viewport_TilesH = 17
CurrentSelectedTile = 1
CurrentTileSet = 0
MouseIsHeldDown = False
CurrentMessage = "Ready!"
def Initialize(DISPLAY):
    global MapData
    pygame.display.set_caption("Example Game")
    pygame.mouse.set_visible(False)

    Messages.append("SET_FPS:0")

    # -- Load the Map -- #
    LoadMapData()

def LoadMapData():
    global MapData
    global CurrentTileSet
    global Map_TileSize
    global Map_SizeW
    global Map_SizeH

    f = open('map.txt', "r")

    IsInitializationLines = True
    InfosLoaded = 0
    for line in f:
        line = line.rstrip()
        print(line)

        if line.startswith(";"):
            IsInitializationLines = True

        if not IsInitializationLines:
            if not line.startswith("#"):
                SplitedData = line.split(',')
                print("Fill Map Data:")
                MapData[int(SplitedData[0])][int(SplitedData[1])] = int(SplitedData[2])

        if IsInitializationLines:
            SplitedParameters = line.split(':')

            if SplitedParameters[0] == "tileset":
                InfosLoaded += 1
                CurrentTileSet = int(SplitedParameters[1])
                print("Tileset set to: [{0}].".format(CurrentTileSet))

            if SplitedParameters[0] == "tile_size":
                InfosLoaded += 1
                Map_TileSize = int(SplitedParameters[1])
                print("Tilesize set to: [{0}].".format(Map_TileSize))

            if SplitedParameters[0] == "map_width":
                InfosLoaded += 1
                Map_SizeW = int(SplitedParameters[1])
                print("Map Width set to: [{0}].".format(Map_SizeW))

            if SplitedParameters[0] == "map_height":
                InfosLoaded += 1
                Map_SizeH = int(SplitedParameters[1])
                print("Map Height set to: [{0}].".format(Map_SizeH))

            if InfosLoaded >= 4:
                IsInitializationLines = False
                w, h = Map_SizeW, Map_SizeH
                MapData = [[0 for x in range(w)] for y in range(h)]

                print("Map Info Loaded, Loading Map Data...")


def SaveMapData():
    global MapData
    global CurrentTileSet
    global Map_TileSize
    global Map_SizeW
    global Map_SizeH
    global CurrentMessage

    f = open('map.txt', 'w')
    f.write("; -- MAP INFO -- ;\ntileset:" + str(CurrentTileSet) + "\n")
    f.write("tile_size:" + str(Map_TileSize) + "\n")
    f.write("map_width:" + str(Map_SizeW) + "\n")
    f.write("map_height:" + str(Map_SizeH) + "\n")

    f.write("# -- BEGIN MAP DATA -- #\n")

    for xData in range(0, Map_SizeW):
        for yData in range(0, Map_SizeH):
            f.write(str(xData) + "," + str(yData) + "," + str(MapData[xData][yData]) + "\n")  # python will convert \n to os.linesep

    f.write("# - END MAP DATA -- #")

    f.close()  # you can omit in most cases as the destructor will call it
    CurrentMessage = "Map Saved."

def GameDraw(DISPLAY):
    global MapData
    global Map_SizeHP
    global Map_SizeW
    global Map_TileSize
    global Viewport_TilesW
    global Viewport_TilesH
    global CurrentMessage
    DISPLAY.fill((220, 220, 220))


    for x in range(0, Viewport_TilesW):
        for y in range(0, Viewport_TilesH):
            try:
                sprite.Render(DISPLAY, "/{0}/{1}.png".format(str(CurrentTileSet),MapData[Map_X + x][Map_Y + y]), x * Map_TileSize,y * Map_TileSize,Map_TileSize,Map_TileSize)
            except:
                sprite.RenderRectangle(DISPLAY, (0,0,0), (x * Map_TileSize, y * Map_TileSize, Map_TileSize, Map_TileSize))


    HUD_Selector = pygame.Surface((Map_TileSize, Map_TileSize), pygame.SRCALPHA)
    sprite.RenderRectangle(HUD_Selector, (100, 20, 20, 150), (0,0, Map_TileSize, Map_TileSize))

    DISPLAY.blit(HUD_Selector, (floor(CursorPosition[0] / Map_TileSize) * Map_TileSize, floor(CursorPosition[1] / Map_TileSize) * Map_TileSize))

    HUD_Surface = pygame.Surface((DISPLAY.get_width(), 55), pygame.SRCALPHA)
    sprite.RenderRectangle(HUD_Surface, (0,0,0,150), (0,0,HUD_Surface.get_width(), HUD_Surface.get_height()))

    sprite.RenderFont(HUD_Surface, "/PressStart2P.ttf", 10, "Cursor[X{0}, Y{1}]\nMap[X:{2}, Y:{3}\nTile[Tile:{4}, W:{5}, H:{6}]".format(str(Cursor_MapX), str(Cursor_MapY), str(Map_X), str(Map_Y), str(Map_TileSize), str(Map_SizeW), str(Map_SizeH)), (255, 255, 255), 10, 2, True)
    sprite.RenderFont(HUD_Surface, "/PressStart2P.ttf", 10, "Tile: {0}\nTileset{1}".format(str(CurrentSelectedTile), str(CurrentTileSet)), (255, 255, 255), 280, 2, True)
    sprite.Render(HUD_Surface, "/{0}/{1}.png".format(CurrentTileSet, CurrentSelectedTile), 380, 2, 32, 32)

    sprite.RenderFont(HUD_Surface, "/PressStart2P.ttf", 10, CurrentMessage, (240, 240, 240), HUD_Surface.get_width() - sprite.GetText_width("/PressStart2P.ttf", 10, CurrentMessage) - 10, 20)

    DISPLAY.blit(HUD_Surface, (0, DISPLAY.get_height() - 55))

    # -- render da cursor #
    sprite.Render(DISPLAY, "/0.png", CursorPosition[0], CursorPosition[1], 15, 22)

    pygame.display.update()

def EventUpdate(event):
    global CursorPosition
    global Map_X
    global Map_Y
    global Map_SizeW
    global Map_SizeH
    global Map_TileSize
    global Viewport_TilesW
    global Viewport_TilesH
    global CurrentSelectedTile
    global CurrentTileSet
    global MouseIsHeldDown
    global MapData
    global CurrentMessage

    # -- Move the Map -- #
    if event.type == pygame.KEYUP and event.key == pygame.K_w:
        if Map_Y >= 1:
            Map_Y -= 1
    if event.type == pygame.KEYUP and event.key == pygame.K_s:
        Map_Y += 1
    if event.type == pygame.KEYUP and event.key == pygame.K_a:
        if Map_X >= 1:
            Map_X -= 1
    if event.type == pygame.KEYUP and event.key == pygame.K_d:
        Map_X += 1

    # -- Change the Selected Tile -- #
    if event.type == pygame.KEYUP and event.key == pygame.K_q:
        if CurrentSelectedTile > 0:
            CurrentSelectedTile -= 1
    if event.type == pygame.KEYUP and event.key == pygame.K_e:
        CurrentSelectedTile += 1

    # -- Change Viewport Size -- #
    if event.type == pygame.KEYUP and event.key == pygame.K_j:
        if Viewport_TilesW > 16:
            Viewport_TilesW -= 1
        else:
            CurrentMessage = "Viewport Width cannot be\nlower than 16."
    if event.type == pygame.KEYUP and event.key == pygame.K_l:
        if Viewport_TilesW < Map_SizeW:
            Viewport_TilesW += 1
        else:
            CurrentMessage = "Viewport Width cannot be\nhigher than map width."
    if event.type == pygame.KEYUP and event.key == pygame.K_k:
        if Viewport_TilesH < Map_SizeH:
            Viewport_TilesH += 1
        else:
            CurrentMessage = "Viewport Height cannot be\nhigher than map height."
    if event.type == pygame.KEYUP and event.key == pygame.K_i:
        if Viewport_TilesH > 16:
            Viewport_TilesH -= 1
        else:
            CurrentMessage = "Viewport Height cannot be\nlower than 16.."


    # -- Change the Selected Tileset -- #
    if event.type == pygame.KEYUP and event.key == pygame.K_z:
        if CurrentTileSet > 0:
            CurrentTileSet -= 1
    if event.type == pygame.KEYUP and event.key == pygame.K_c:
        CurrentTileSet += 1

    # -- I/O Buttons -- #
    if event.type == pygame.KEYUP and event.key == pygame.K_x:
        SaveMapData()
    if event.type == pygame.KEYUP and event.key == pygame.K_n:
        NewMap()

    # -- Detect Mouse Motion -- #
    if event.type == pygame.MOUSEMOTION:
        CursorPosition = pygame.mouse.get_pos()

    # -- Detect Mouse Down -- #
    if event.type == pygame.MOUSEBUTTONDOWN:
        MouseIsHeldDown = True
    if event.type == pygame.MOUSEBUTTONUP:
        MouseIsHeldDown = False

def NewMap():
    global MapData
    global CurrentMessage
    w, h = Map_SizeW, Map_SizeH;
    MapData = [[0 for x in range(w)] for y in range(h)]

    SaveMapData()
    CurrentMessage = "New Map"

def Update():
    global TextToShow
    global Cursor_MapX
    global Cursor_MapY
    global Map_X
    global Map_Y
    global Map_TileSize
    global CurrentMessage
    # -- Set Cursor Map Location -- #
    Cursor_MapX = Map_X + floor(CursorPosition[0] / Map_TileSize)
    Cursor_MapY = Map_Y + floor(CursorPosition[1] / Map_TileSize)

    if Cursor_MapX <= -Map_SizeW:
        Cursor_MapX = -Map_SizeW
    if Cursor_MapY <= -Map_SizeH:
        Cursor_MapY = -Map_SizeH

    # -- Key Events -- #
    PressedKeys = pygame.key.get_pressed()
    if PressedKeys[pygame.K_1]:
        if Map_TileSize > 1:
            Map_TileSize -= 1
    if PressedKeys[pygame.K_2]:
        Map_TileSize += 1

    # -- Place Tiles -- #
    if MouseIsHeldDown:
        try:
            MapData[Cursor_MapX][Cursor_MapY] = CurrentSelectedTile
            CurrentMessage = "Tile[{0},{1}] = {2}".format(str(Cursor_MapX), str(Cursor_MapY), str(CurrentSelectedTile))
        except:
            CurrentMessage = "Tiles cannot be place outside\nthe map."


# -- Send the messages on the Message Quee to the Game Engine -- #
def ReadCurrentMessages():
    try:
        for x in Messages:
            Messages.remove(x)
            print("Game : MessageSent[" + x + "]")
            return x
    except:
        return ""

