import pygame
from ENGINE import sprite as sprite
import TileEditor.MAIN.HUD as hud
import TileEditor.MAIN as mainScript
import TileEditor.MAIN.SCREEN.Editor as editorScreen
import TileEditor.MAIN.Window.Properties as propsWindow

LoadMapButton = hud.Button
NewMapButton = hud.Button
FilenameTextbox = hud.InputBox
PropertiesWindowEnabled = False

def Initialize(DISPLAY):
    global LoadMapButton
    global NewMapButton
    global FilenameTextbox
    LoadMapButton = hud.Button((5,5,5,5), "Load Map", 18)
    NewMapButton = hud.Button((5,5,5,5), "New Map", 18)
    FilenameTextbox = hud.InputBox(0,0,200,30, "Map.txt")
    propsWindow.Initialize()

def Update():
    global LoadMapButton
    global NewMapButton
    global FilenameTextbox
    global PropertiesWindowEnabled
    LoadMapButton.Set_X(mainScript.DefaultDisplay.get_width() / 2 - LoadMapButton.Rectangle[2] / 2)
    LoadMapButton.Set_Y(mainScript.DefaultDisplay.get_height() / 2 - LoadMapButton.Rectangle[3])

    NewMapButton.Set_X(mainScript.DefaultDisplay.get_width() / 2 - LoadMapButton.Rectangle[2] / 2)
    NewMapButton.Set_Y(LoadMapButton.Rectangle[1] + NewMapButton.Rectangle[3] + 5)

    FilenameTextbox.Set_X(mainScript.DefaultDisplay.get_width() / 2 - FilenameTextbox.rect[2] / 2)
    FilenameTextbox.Set_Y(NewMapButton.Rectangle[1] + FilenameTextbox.rect[3] + 40)

    mainScript.CurrentFileName = FilenameTextbox.text

    if not PropertiesWindowEnabled:
        if NewMapButton.ButtonState == "UP":
            PropertiesWindowEnabled = True

        if LoadMapButton.ButtonState == "UP":
            editorScreen.LoadMapData()
            LoadMapButton.ButtonState = "INACTIVE"
            mainScript.CurrentScreen = 1
    else:
        propsWindow.Update()

def GameDraw(DISPLAY):
    global LoadMapButton
    global NewMapButton
    global FilenameTextbox
    global PropertiesWindowEnabled
    sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 38, "Tile Editor", (240,240,240), DISPLAY.get_width() / 2 - sprite.GetText_width("/PressStart2P.ttf", 38, "Tile Editor") / 2,25)

    LoadMapButton.Render(DISPLAY)
    NewMapButton.Render(DISPLAY)

    sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 14, "Map Name:", (240, 240, 240), FilenameTextbox.rect[0], FilenameTextbox.rect[1] - 20)

    FilenameTextbox.Render(DISPLAY)

    if PropertiesWindowEnabled:
        propsWindow.Render(DISPLAY)


def EventUpdate(event):
    global LoadMapButton
    global NewMapButton
    global FilenameTextbox
    global PropertiesWindowEnabled

    if not PropertiesWindowEnabled:
        LoadMapButton.Update(event)
        NewMapButton.Update(event)
        FilenameTextbox.Update(event)
    else:
        propsWindow.EventUpdate(event)