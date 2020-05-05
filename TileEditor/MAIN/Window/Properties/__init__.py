import pygame
import TileEditor.MAIN as mainScript
import TileEditor.MAIN.SCREEN.Menu as menuScreen
import TileEditor.MAIN.SCREEN.Editor as editorScreen
import TileEditor.MAIN.HUD as hud
from ENGINE import sprite as sprite

WindowObject = hud.Window
WindowSurface = pygame.Surface
MapWidthInput = hud.InputBox
MapHeightInput = hud.InputBox
CreateMapButton = hud.Button
MapTileSizeInput = hud.InputBox


def Initialize():
    global WindowObject
    global MapWidthInput
    global MapHeightInput
    global CreateMapButton
    global MapTileSizeInput
    WindowObject = hud.Window(pygame.Rect(50,50,350,250), "Map Properties", False)
    WindowObject.Minimizable = False
    MapWidthInput = hud.InputBox(5,50,150,18,"64")
    MapHeightInput = hud.InputBox(5,80,150, 18, "64")
    CreateMapButton = hud.Button((0,0,0,0), "Create Map", 14)
    MapTileSizeInput = hud.InputBox(5,110, 150, 18, "32")

    MapWidthInput.CustomColision = True
    MapHeightInput.CustomColision = True
    CreateMapButton.CustomColisionRectangle = True
    MapTileSizeInput.CustomColision = True

def Render(DISPLAY):
    global WindowObject
    global WindowSurface
    global MapWidthInput
    global MapHeightInput
    global CreateMapButton
    global MapTileSizeInput
    WindowSurface = WindowObject.WindowSurface

    # -- Map Size Category -- #
    sprite.RenderFont(WindowSurface, "/PressStart2P.ttf", 18, "Map Dimensions", (240,240,240), 15, 7)

    # -- Render the Width Textbox -- #
    MapWidthInput.Render(WindowSurface)
    sprite.RenderFont(WindowSurface, "/PressStart2P.ttf", 12, "Width", (240,240,240), 5, 35)

    # -- Render Height Textbox -- #
    MapHeightInput.Render(WindowSurface)
    sprite.RenderFont(WindowSurface, "/PressStart2P.ttf", 12, "Height", (240,240,240), 5, 65)

    # -- Render Tile Size -- #
    MapTileSizeInput.Render(WindowSurface)
    sprite.RenderFont(WindowSurface, "/PressStart2P.ttf", 12, "Tile", (240,240,240), 5, 95)


    # -- Render Create Map Button -- #
    CreateMapButton.Render(WindowSurface)


    WindowObject.Render(DISPLAY)
    DISPLAY.blit(WindowSurface, WindowObject.WindowSurface_Dest)

    #sprite.RenderRectangle(DISPLAY, (255,0,0), CreateMapButton.ColisionRectangle)


def Update():
    global MapWidthInput
    global WindowObject
    global MapHeightInput
    global CreateMapButton
    global MapTileSizeInput

    CreateMapButton.Set_X(WindowSurface.get_width() - CreateMapButton.Rectangle[2] - 5)
    CreateMapButton.Set_Y(WindowSurface.get_height() - CreateMapButton.Rectangle[3] - 8)

    MapWidthInput.colisionRect = pygame.Rect(WindowObject.WindowRectangle[0] + MapWidthInput.rect[0], WindowObject.WindowRectangle[1] + MapWidthInput.rect[1] + 20, MapWidthInput.rect[2], MapWidthInput.rect[3])
    MapHeightInput.colisionRect = pygame.Rect(WindowObject.WindowRectangle[0] + MapHeightInput.rect[0], WindowObject.WindowRectangle[1] + MapHeightInput.rect[1] + 20, MapHeightInput.rect[2], MapHeightInput.rect[3])
    MapTileSizeInput.colisionRect = pygame.Rect(WindowObject.WindowRectangle[0] + MapTileSizeInput.rect[0], WindowObject.WindowRectangle[1] + MapTileSizeInput.rect[1] + 20, MapTileSizeInput.rect[2], MapTileSizeInput.rect[3])
    CreateMapButton.Set_ColisionX(WindowObject.WindowRectangle[0] + CreateMapButton.Rectangle[0])
    CreateMapButton.Set_ColisionY(WindowObject.WindowRectangle[1] + CreateMapButton.Rectangle[1] + 20)
    CreateMapButton.ColisionRectangle[2] = CreateMapButton.Rectangle[2]
    CreateMapButton.ColisionRectangle[3] = CreateMapButton.Rectangle[3]

    if CreateMapButton.ButtonState == "UP":
        menuScreen.PropertiesWindowEnabled = False
        # -- Set the map Properties -- #
        editorScreen.Map_SizeW = int(MapWidthInput.text)
        editorScreen.Map_SizeH = int(MapHeightInput.text)
        editorScreen.Map_TileSize = int(MapTileSizeInput.text)

        # -- 0 Fill the map Matrix -- #
        editorScreen.NewMap()
        # -- And finnaly, go to Editor Screen -- #
        mainScript.CurrentScreen = 1


def EventUpdate(event):
    global WindowObject
    global MapWidthInput
    global MapHeightInput
    global CreateMapButton
    global MapTileSizeInput
    WindowObject.EventUpdate(event)
    MapWidthInput.Update(event)
    MapHeightInput.Update(event)
    CreateMapButton.Update(event)
    MapTileSizeInput.Update(event)