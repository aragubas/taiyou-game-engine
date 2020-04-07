# -- Imports -- #
import ENGINE.Registry as reg
import ENGINE.Utils as utils
import ENGINE.TGE as tge
import ENGINE.SOUND as sound
import Fogoso.MAIN.ClassesUtils as gameObjs
import Fogoso.MAIN.Screens.Settings as ScreenSettings
import Fogoso.MAIN as gameMain
import pygame, sys
import ENGINE.SPRITE as sprite
import importlib
import time
from random import randint


# -- Objects Definition -- #
GrindButton = gameObjs.Button
ReceiveLog_CloseButton = gameObjs.Button
GameOptionsButton = gameObjs.Button
SaveButton = gameObjs.Button
BackToMainMenuButton = gameObjs.Button

# -- Game -- #
Current_Money = 0.0
Current_MoneyValuePerClick = 0.2

# -- Receive Log -- #
ReceiveLog_Y_Offset = 0
ReceiveLog_Y_OffsetAdder = 0
ReceiveLog_Y_AnimEnabled = False
ReceiveLog_Y_AnimType = 0
TextGrind_Text = list()
TextGrind_X = list()
TextGrind_Y = list()
TextGrind_AliveTime = list()
TextGrind_IsGrindText = list()


def LoadGame():
    global Current_Money
    global Current_MoneyValuePerClick
    print("LoadGame : Init")
    gameMain.FadeEffectState = True
    gameMain.FadeEffectCurrentState = 0
    gameMain.FadeEffectValue = 255

    Current_Money = reg.ReadKeyWithTry_float("/Save/money",0.05)
    Current_MoneyValuePerClick = reg.ReadKeyWithTry_float("/Save/money_per_click",0.1)

    gameMain.FadeEffectState = True


def SaveGame():
    gameMain.FadeEffectState = True
    gameMain.FadeEffectCurrentState = 0
    gameMain.FadeEffectValue = 255
    print("SaveGame : Init")

    reg.WriteKey("/Save/money", str(Current_Money))
    reg.WriteKey("/Save/money_per_click", str(Current_MoneyValuePerClick))

    print("SaveGame : Game Saved")


def AddMessageText(Text, IsGrindText):
    TextGrind_Text.append(Text)
    TextGrind_X.append(gameMain.DefaultDisplay.get_width() - 355)
    TextGrind_Y.append(ReceiveLog_Y_Offset + gameMain.DefaultDisplay.get_height() - 27)
    TextGrind_AliveTime.append(0)
    TextGrind_IsGrindText.append(IsGrindText)


def Update():
    global Current_Money
    global Current_MoneyValuePerClick
    global ReceiveLog_Y_Offset
    global ReceiveLog_Y_AnimEnabled
    global ReceiveLog_Y_AnimType
    global ReceiveLog_Y_OffsetAdder
    global GameOptionsButton
    global BackToMainMenuButton

    # -- Update Buttons Click -- #
    if GrindButton.ButtonState == "UP":
        AddMessageText("+" + str(Current_MoneyValuePerClick), True)
    if ReceiveLog_CloseButton.ButtonState == "UP":
        ReceiveLog_Y_AnimEnabled = True
    if GameOptionsButton.ButtonState == "UP":
        gameMain.FadeEffectValue = 255
        gameMain.FadeEffectCurrentState = 0
        gameMain.FadeEffectState = True
        ScreenSettings.ScreenToReturn = gameMain.CurrentScreen
        ScreenSettings.Initialize()
        gameMain.CurrentScreen += 1

    if SaveButton.ButtonState == "UP":
        AddMessageText("Game Saved", False)
        SaveGame()

    if BackToMainMenuButton.ButtonState == "UP":
        AddMessageText("Welcome Back!", False)
        SaveGame()
        gameMain.CurrentScreen -= 1

    # -- Update Buttons Location -- #
    ReceiveLog_CloseButton.Rectangle = pygame.rect.Rect(gameMain.DefaultDisplay.get_width() - 30,
                                                        ReceiveLog_Y_Offset + gameMain.DefaultDisplay.get_height() - 353,
                                                        ReceiveLog_CloseButton.Rectangle[2],
                                                        ReceiveLog_CloseButton.Rectangle[3])

    GameOptionsButton.Set_X(gameMain.DefaultDisplay.get_width() - 120)
    SaveButton.Set_X(gameMain.DefaultDisplay.get_width() - 120)
    BackToMainMenuButton.Set_X(gameMain.DefaultDisplay.get_width() - 120)
    GrindButton.Rectangle[2] = 130
    GrindButton.Rectangle[3] = 150

    # -- Update the Receive Log Animation -- #
    if ReceiveLog_Y_AnimEnabled:
        if ReceiveLog_Y_AnimType == 0:
            ReceiveLog_Y_OffsetAdder += 1
            ReceiveLog_Y_Offset += ReceiveLog_Y_OffsetAdder

            if ReceiveLog_Y_Offset >= 310:
                ReceiveLog_Y_Offset = 310
                ReceiveLog_Y_OffsetAdder = 0
                ReceiveLog_Y_AnimType = 1
                ReceiveLog_Y_AnimEnabled = False
                ReceiveLog_CloseButton.ButtonText = "↑"

        if ReceiveLog_Y_AnimType == 1:
            ReceiveLog_Y_OffsetAdder += 1
            ReceiveLog_Y_Offset -= ReceiveLog_Y_OffsetAdder

            if ReceiveLog_Y_Offset <= 0:
                ReceiveLog_Y_Offset = 0
                ReceiveLog_Y_OffsetAdder = 0
                ReceiveLog_Y_AnimType = 0
                ReceiveLog_Y_AnimEnabled = False
                ReceiveLog_CloseButton.ButtonText = "↓"


def DrawGrindText(DISPLAY):
    # -- Render the Window Background -- #
    GlobalX = DISPLAY.get_width() - 355
    GlobalY = ReceiveLog_Y_Offset + DISPLAY.get_height() - 355
    sprite.RenderRectangle(DISPLAY, (64, 78, 124), (GlobalX, GlobalY, 350, 350))
    sprite.RenderRectangle(DISPLAY, (37, 31, 37), (GlobalX + 2, GlobalY + 2, 350 - 4, 350 - 4))

    global Current_Money
    global Current_MoneyValuePerClick
    for x in range(len(TextGrind_Text)):
        if TextGrind_IsGrindText[x]:
            sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 20, TextGrind_Text[x],
                              (134, 203, 146), TextGrind_X[x], TextGrind_Y[x])
        else:
            sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 20, TextGrind_Text[x],
                              (200 + x, 200 + x, 200 + x), TextGrind_X[x], TextGrind_Y[x])

        TextGrind_Y[x] -= 3
        TextGrind_AliveTime[x] += 1
        if TextGrind_AliveTime[x] >= 1500 or TextGrind_Y[x] <= ReceiveLog_Y_Offset + DISPLAY.get_height() - 350:
            if TextGrind_IsGrindText[x]:
                Current_Money += Current_MoneyValuePerClick
            TextGrind_Text.pop(x)
            TextGrind_X.pop(x)
            TextGrind_Y.pop(x)
            TextGrind_AliveTime.pop(x)
            TextGrind_IsGrindText.pop(x)
            print("GrindText; Index: " + str(x) + ", removed.")
            break
# -- Render the Window Title -- #
    sprite.RenderRectangle(DISPLAY, (38, 15, 38), (GlobalX, GlobalY, 350, 24))
    sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 18, "===================", (100, 100, 100),
                      GlobalX + 3, GlobalY + 3)
    sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 18, "Receiving Log", (255, 255, 255), GlobalX + 3,
                      GlobalY + 3)

    ReceiveLog_CloseButton.Render(DISPLAY)


def GameDraw(DISPLAY):
    global BackToMainMenuButton
    # -- Draw the Grind Text -- #
    DrawGrindText(DISPLAY)
    # -- Draw the Grind Button -- #
    GrindButton.Render(DISPLAY)
    # -- Draw the Options Button -- #
    GameOptionsButton.Render(DISPLAY)
    # -- Draw the Save Button -- #
    SaveButton.Render(DISPLAY)
    # -- Draw the BackToMenu button -- #
    BackToMainMenuButton.Render(DISPLAY)

    # -- Render Money Text -- #
    sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 18, "Money: " + str(Current_Money),
                      (255, 255, 255), 10, 20)


def Initialize(DISPLAY):
    # -- Set Buttons -- #
    global ReceiveLog_CloseButton
    global SaveButton
    global GameOptionsButton
    global GrindButton
    global BackToMainMenuButton
    GrindButton = gameObjs.Button(pygame.rect.Rect(15, 115, 130, 150), "This text is not ment to be visible.", 18)
    GrindButton.WhiteButton = True
    ReceiveLog_CloseButton = gameObjs.Button(pygame.rect.Rect(320, 0, 0, 0), "↓", 16)
    GameOptionsButton = gameObjs.Button(pygame.rect.Rect(DISPLAY.get_width() - 120, 5, 0, 0), "OPTIONS", 12)
    SaveButton = gameObjs.Button(pygame.rect.Rect(DISPLAY.get_width() - 120, 20, 0, 0), "Save", 12)
    BackToMainMenuButton = gameObjs.Button(pygame.Rect(DISPLAY.get_width() - 120,35,0,0),"Main Menu",12)
    # -- Load Saved Values -- #
    LoadGame()
    print("GameScreen : All objects initialized.")


def EventUpdate(event):
    # -- Update all buttons -- #
    global GrindButton
    global ReceiveLog_CloseButton
    global GameOptionsButton
    global SaveButton
    global BackToMainMenuButton
    GrindButton.Update(event)
    ReceiveLog_CloseButton.Update(event)
    GameOptionsButton.Update(event)
    SaveButton.Update(event)
    BackToMainMenuButton.Update(event)
