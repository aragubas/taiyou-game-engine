# -- Imports -- #
import ENGINE.Registry as reg
import ENGINE.Utils as utils
import ENGINE.TGE as tge
import ENGINE.SOUND as sound
import Fogoso.MAIN.ClassesUtils as gameObjs
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
OptionsScreen_CloseButton = gameObjs.Button
OptionsScreen_ChangeFps = gameObjs.UpDownButton
OptionsScreen_ChangeWindowSize = gameObjs.UpDownButton
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

# -- Options Screen -- #
Menu_Background = pygame.Surface
OptionsScreen_AnimToggle = False
OptionsScreen_AnimType = 0
OptionsScreen_AnimValue = 0
OptionsScreen_AnimAdder = 0
OptionsScreen_Enabled = False


def LoadGame():
    global Current_Money
    global Current_MoneyValuePerClick
    print("LoadGame : Init")
    gameMain.FadeEffectState = True
    gameMain.FadeEffectCurrentState = 0
    gameMain.FadeEffectValue = 255

    Current_Money = reg.ReadKeyWithTry_float("/Save/money",0.05)
    Current_MoneyValuePerClick = reg.ReadKeyWithTry_float("/Save/money_per_click",0.1)

    gameMain.Cursor_CurrentLevel = 1
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
    global Menu_Background
    global OptionsScreen_AnimToggle
    global OptionsScreen_AnimType
    global OptionsScreen_AnimAdder
    global OptionsScreen_AnimValue
    global GameOptionsButton
    global OptionsScreen_Enabled
    global OptionsScreen_CloseButton
    global BackToMainMenuButton
    Menu_Background = pygame.Surface((gameMain.DefaultDisplay.get_width(), gameMain.DefaultDisplay.get_height()))

    # -- Update Buttons Click -- #
    if not OptionsScreen_Enabled:
        if GrindButton.ButtonState == "UP":
            AddMessageText("+" + str(Current_MoneyValuePerClick), True)
        if ReceiveLog_CloseButton.ButtonState == "UP":
            ReceiveLog_Y_AnimEnabled = True
        if GameOptionsButton.ButtonState == "UP":
            OptionsScreen_AnimToggle = True
            gameMain.Cursor_CurrentLevel = 0

        if SaveButton.ButtonState == "UP":
            AddMessageText("Game Saved", False)
            SaveGame()

        if BackToMainMenuButton.ButtonState == "UP":
            AddMessageText("Welcome Back!", False)
            SaveGame()
            gameMain.CurrentScreen -= 1

    else:
        if OptionsScreen_CloseButton.ButtonState == "UP":
            gameMain.Cursor_CurrentLevel = 1
            OptionsScreen_AnimToggle = True

        if OptionsScreen_ChangeFps.ButtonState == "UP":
            print("MaxFPS is [" + str(gameMain.Engine_MaxFPS) + "]")
            if gameMain.Engine_MaxFPS == 120:
                gameMain.Engine_MaxFPS = 60
            elif gameMain.Engine_MaxFPS == 75:
                gameMain.Engine_MaxFPS = 120
            elif gameMain.Engine_MaxFPS == 60:
                gameMain.Engine_MaxFPS = 75
            gameMain.Messages.append("SET_FPS:" + str(gameMain.Engine_MaxFPS))
            reg.WriteKey("/OPTIONS/maxFPS", str(gameMain.Engine_MaxFPS))
            print("MaxFPS is now set to[" + str(gameMain.Engine_MaxFPS) + "]")

        if OptionsScreen_ChangeFps.ButtonState == "DOWN":
            print("MaxFPS is [" + str(gameMain.Engine_MaxFPS) + "]")
            if gameMain.Engine_MaxFPS == 120:
                gameMain.Engine_MaxFPS = 75
            elif gameMain.Engine_MaxFPS == 75:
                gameMain.Engine_MaxFPS = 60
            elif gameMain.Engine_MaxFPS == 60:
                gameMain.Engine_MaxFPS = 120
            gameMain.Messages.append("SET_FPS:" + str(gameMain.Engine_MaxFPS))
            reg.WriteKey("/OPTIONS/maxFPS", str(gameMain.Engine_MaxFPS))
            print("MaxFPS is now set to[" + str(gameMain.Engine_MaxFPS) + "]")

        if OptionsScreen_ChangeWindowSize.ButtonState == "UP":
            CurrentW, CurrentH = gameMain.DefaultDisplay.get_size()
            print("OldResolution : " + str(CurrentW) + "x" + str(CurrentH))

            if CurrentW == 1280 and CurrentH == 1024:
                CurrentW = 800
                CurrentH = 600
            elif CurrentW == 1280 and CurrentH == 768:
                CurrentW = 1280
                CurrentH = 1024
            elif CurrentW == 800 and CurrentH == 600:
                CurrentW = 1280
                CurrentH = 768

            print("New Resolution : " + str(CurrentW) + "x" + str(CurrentH))
            reg.WriteKey("/OPTIONS/resW", str(CurrentW))
            reg.WriteKey("/OPTIONS/resH", str(CurrentH))
            gameMain.Messages.append("SET_RESOLUTION:" + str(CurrentW) + ":" + str(CurrentH))

        if OptionsScreen_ChangeWindowSize.ButtonState == "DOWN":
            CurrentW, CurrentH = gameMain.DefaultDisplay.get_size()
            print("OldResolution : " + str(CurrentW) + "x" + str(CurrentH))

            if CurrentW == 1280 and CurrentH == 1024:
                CurrentW = 1280
                CurrentH = 768
            elif CurrentW == 1280 and CurrentH == 768:
                CurrentW = 800
                CurrentH = 600
            elif CurrentW == 800 and CurrentH == 600:
                CurrentW = 1280
                CurrentH = 1024

            print("New Resolution : " + str(CurrentW) + "x" + str(CurrentH))
            reg.WriteKey("/OPTIONS/resW", str(CurrentW))
            reg.WriteKey("/OPTIONS/resH", str(CurrentH))
            gameMain.Messages.append("SET_RESOLUTION:" + str(CurrentW) + ":" + str(CurrentH))


    # -- Set Buttons Enabled State -- #
    ReceiveLog_CloseButton.IsButtonEnabled = not OptionsScreen_Enabled
    GrindButton.IsButtonEnabled = not OptionsScreen_Enabled
    GameOptionsButton.IsButtonEnabled = not OptionsScreen_Enabled
    OptionsScreen_CloseButton.IsButtonEnabled = OptionsScreen_Enabled
    OptionsScreen_ChangeFps.IsButtonEnabled = OptionsScreen_Enabled
    SaveButton.IsButtonEnabled = not OptionsScreen_Enabled
    BackToMainMenuButton.IsButtonEnabled = not OptionsScreen_Enabled
    OptionsScreen_ChangeWindowSize.IsButtonEnabled = OptionsScreen_Enabled
    # -- Update Buttons Location -- #
    ReceiveLog_CloseButton.Rectangle = pygame.rect.Rect(gameMain.DefaultDisplay.get_width() - 30,
                                                        ReceiveLog_Y_Offset + gameMain.DefaultDisplay.get_height() - 353,
                                                        ReceiveLog_CloseButton.Rectangle[2],
                                                        ReceiveLog_CloseButton.Rectangle[3])
    GameOptionsButton.Set_X(gameMain.DefaultDisplay.get_width() - 120)
    OptionsScreen_CloseButton.Set_X(gameMain.DefaultDisplay.get_width() - 120)
    SaveButton.Set_X(gameMain.DefaultDisplay.get_width() - 120)
    BackToMainMenuButton.Set_X(gameMain.DefaultDisplay.get_width() - 120)
    if OptionsScreen_AnimToggle:
        if OptionsScreen_AnimType == 0:
            OptionsScreen_AnimAdder += 1
            OptionsScreen_AnimValue += OptionsScreen_AnimAdder

            if OptionsScreen_AnimValue >= 255:
                OptionsScreen_AnimValue = 255
                OptionsScreen_AnimType = 1
                OptionsScreen_AnimAdder = 0
                OptionsScreen_AnimToggle = False
                OptionsScreen_Enabled = True
        if OptionsScreen_AnimType == 1:
            OptionsScreen_AnimAdder += 1
            OptionsScreen_AnimValue -= OptionsScreen_AnimAdder

            if OptionsScreen_AnimValue <= 0:
                OptionsScreen_AnimValue = 0
                OptionsScreen_AnimType = 0
                OptionsScreen_AnimAdder = 0
                OptionsScreen_AnimToggle = False
                OptionsScreen_Enabled = False

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
                              (255, 255, 255), TextGrind_X[x], TextGrind_Y[x])

        if not OptionsScreen_Enabled:
            TextGrind_Y[x] -= 3
            TextGrind_AliveTime[x] += 1
            if TextGrind_AliveTime[x] >= 1500 or TextGrind_Y[x] <= ReceiveLog_Y_Offset + DISPLAY.get_height() - 350:
                if TextGrind_IsGrindText[x]:
                    Current_Money += Current_MoneyValuePerClick
                del TextGrind_Text[x]
                del TextGrind_X[x]
                del TextGrind_Y[x]
                del TextGrind_AliveTime[x]
                del TextGrind_IsGrindText[x]
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
    global OptionsScreen_Enabled
    global OptionsScreen_ChangeWindowSize
    global Menu_Background
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

    # -- Render the Options Menu Background -- #
    Menu_Background.fill((150, 150, 150))
    ElementsX = Menu_Background.get_width() / 2 - 275
    ElementsY = Menu_Background.get_height() / 2 - 125
    sprite.RenderRectangle(Menu_Background, (10, 20, 17), (ElementsX - 4, ElementsY - 4, 558, 258))
    sprite.RenderRectangle(Menu_Background,(30,40,47),(ElementsX,ElementsY,550,250))

    # -- Render The Title Text --
    sprite.RenderFont(Menu_Background, "/PressStart2P.ttf", 28, "-- Options --", (255, 255, 255), ElementsX + 95,
                      ElementsY + 5)

    OptionsScreen_CloseButton.Render(Menu_Background)
    # -- Change Max FPS Option --
    OptionsScreen_ChangeFps.Render(Menu_Background)
    OptionsScreen_ChangeFps.Set_X(ElementsX + 20)
    OptionsScreen_ChangeFps.Set_Y(ElementsY + 100)
    sprite.RenderFont(Menu_Background, "/PressStart2P.ttf", 14, "Max FPS:" + str(gameMain.Engine_MaxFPS),
                      (255, 255, 255), ElementsX + 115, ElementsY + 103)

    # -- Change Resolution Option -- #
    OptionsScreen_ChangeWindowSize.Render(Menu_Background)
    OptionsScreen_ChangeWindowSize.Set_X(ElementsX + 20)
    OptionsScreen_ChangeWindowSize.Set_Y(ElementsY + 130)

    ResName = "Invalid"
    if gameMain.DefaultDisplay.get_width() == 800 and DISPLAY.get_height() == 600:
        ResName = "SVGA,4:3"
    if gameMain.DefaultDisplay.get_width() == 1280 and DISPLAY.get_height() == 768:
        ResName = "XGA,4:3"
    if gameMain.DefaultDisplay.get_width() == 1280 and DISPLAY.get_height() == 1024:
        ResName = "SXGA,5:3"
    sprite.RenderFont(Menu_Background, "/PressStart2P.ttf", 14,
                      "Resolution:" + str(DISPLAY.get_width()) + "x" + str(
                          DISPLAY.get_height()) + "[{0}]".format(ResName),
                      (255, 255, 255), ElementsX + 115, ElementsY + 133)

    Menu_Background.set_alpha(OptionsScreen_AnimValue)
    DISPLAY.blit(Menu_Background, (0, 0))


def Initialize(DISPLAY):
    # -- Set Buttons -- #
    global ReceiveLog_CloseButton
    global SaveButton
    global GameOptionsButton
    global OptionsScreen_CloseButton
    global OptionsScreen_ChangeFps
    global OptionsScreen_ChangeWindowSize
    global GrindButton
    global BackToMainMenuButton
    GrindButton = gameObjs.Button(pygame.rect.Rect(15, 115, 130, 150), "This text is not ment to be visible.", 18)
    GrindButton.WhiteButton = True
    ReceiveLog_CloseButton = gameObjs.Button(pygame.rect.Rect(320, 0, 0, 0), "↓", 16)
    GameOptionsButton = gameObjs.Button(pygame.rect.Rect(DISPLAY.get_width() - 120, 5, 0, 0), "OPTIONS", 12)
    SaveButton = gameObjs.Button(pygame.rect.Rect(DISPLAY.get_width() - 120, 20, 0, 0), "Save", 12)
    OptionsScreen_CloseButton = gameObjs.Button(pygame.rect.Rect(0,10,0,0),"Back", 14)
    OptionsScreen_ChangeFps = gameObjs.UpDownButton(20, 100, 14)
    OptionsScreen_ChangeWindowSize = gameObjs.UpDownButton(20, 130, 14)
    BackToMainMenuButton = gameObjs.Button(pygame.Rect(DISPLAY.get_width() - 120,35,0,0),"Main Menu",12)
    # -- Load Saved Values -- #
    LoadGame()
    print("GameScreen : All objects initialized.")


def EventUpdate(event):
    # -- Update all buttons -- #
    global GrindButton
    global ReceiveLog_CloseButton
    global GameOptionsButton
    global OptionsScreen_CloseButton
    global OptionsScreen_ChangeFps
    global OptionsScreen_ChangeWindowSize
    global SaveButton
    global BackToMainMenuButton
    GrindButton.Update(event)
    ReceiveLog_CloseButton.Update(event)
    GameOptionsButton.Update(event)
    SaveButton.Update(event)
    BackToMainMenuButton.Update(event)
    if OptionsScreen_Enabled:
        OptionsScreen_CloseButton.Update(event)
        OptionsScreen_ChangeFps.Update(event)
        OptionsScreen_ChangeWindowSize.Update(event)
