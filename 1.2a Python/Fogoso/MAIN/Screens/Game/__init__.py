#!/usr/bin/env python3.7
#
#   Copyright 2020 Aragubas
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

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
import Fogoso.MAIN.StoreWindow as storeWindow
import importlib
import time
from random import randint

# -- Objects Definition -- #
GrindButton = gameObjs.Button
ReceiveLog_CloseButton = gameObjs.Button
GameOptionsButton = gameObjs.Button
SaveButton = gameObjs.Button
BackToMainMenuButton = gameObjs.Button
OpenStoreButton = gameObjs.Button

# -- Game -- #
Current_Money = 0.0
Current_MoneyValuePerClick = 0.2
CUrrent_Experience = 250

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
TextGrind_TextColor = list()
TextGrind_Value = list()

# -- Game Items Variables -- #
GameItemsList = list()
GameItemsInitialized = False
GameItems_TotalIndx_0 = 0
GameItems_TotalIndx_NegativeOne = 0

# -- Game Items View -- #
ItemsView = gameObjs.HorizontalItemsView

# -- Store Window -- #
StoreWindow_Enabled = True

# -- Unload -- #
UnloadRequested = False
UnloadDelay = 0

# -- Load/Save Functions -- #
def LoadGame():
    global Current_Money
    global Current_MoneyValuePerClick
    global GameItemsInitialized
    global ItemsView
    global GameItems_TotalIndx_0
    global GameItems_TotalIndx_NegativeOne
    print("LoadGame : Init")
    gameMain.FadeEffectState = True
    gameMain.FadeEffectCurrentState = 0
    gameMain.FadeEffectValue = 255

    Current_Money = reg.ReadKeyWithTry_float("/Save/money", 0.05)
    Current_MoneyValuePerClick = reg.ReadKeyWithTry_float("/Save/money_per_click", 0.1)

    AllKeys = 0
    ItemID0_Added = False
    ItemIDNegativeOne_Added = False
    for x in range(0,1000):
        if reg.KeyExists("/Save/item/" + str(x)):
            AllKeys += 1

    for x in range(0,AllKeys):
        KeyName = "/Save/item/" + str(x)

        SplitedLines = reg.ReadKey(KeyName).splitlines()
        print("ItemID ; " + SplitedLines[0])
        print("ItemLevel ; " + SplitedLines[1])

        if SplitedLines[0] == "-1":
            GameItems_TotalIndx_NegativeOne += 1
            GameItemsList.append(gameObjs.Item_Nothing(SplitedLines[1]))
            if not ItemIDNegativeOne_Added:
                ItemIDNegativeOne_Added = True
                ItemsView.AddItem(SplitedLines[0])
                print("ItemsView : ItemType ID_-1 added.")
            print("Item_Nothing has been created.")

        if SplitedLines[0] == "0":
            GameItems_TotalIndx_0 += 1
            GameItemsList.append(gameObjs.Item_AutoClicker(SplitedLines[1]))
            if not ItemID0_Added:
                ItemID0_Added = True
                ItemsView.AddItem(SplitedLines[0])
                print("ItemsView : ItemType ID_0 added.")
            print("Item_AutoClicker has been created.")

    print("AllKeys : " + str(AllKeys))

    GameItemsInitialized = True
    gameMain.FadeEffectState = True
    print("LoadGame : Game Loaded Sucefully")

def SaveGame():
    gameMain.FadeEffectState = True
    gameMain.FadeEffectCurrentState = 0
    gameMain.FadeEffectValue = 255
    print("SaveGame : Init")

    reg.WriteKey("/Save/money", str(Current_Money))
    reg.WriteKey("/Save/money_per_click", str(Current_MoneyValuePerClick))

    print("SaveGame : Saving Items Data...")
    for i in range(0,len(GameItemsList)):
        print("SaveItem : id:" + str(i))
        ItemStringData = str(GameItemsList[i].ItemID) + "\n" + str(GameItemsList[i].ItemLevel)
        reg.WriteKey("/Save/item/" + str(i),ItemStringData)
        print("SaveItem : Item saved.")

    print("SaveGame : Game Saved")


def AddMessageText(Text, IsGrindText, TextColor, Value=0):
    TextGrind_Text.append(Text)
    TextGrind_X.append(gameMain.DefaultDisplay.get_width() - 355 + 5)
    TextGrind_Y.append(ReceiveLog_Y_Offset + gameMain.DefaultDisplay.get_height() - 27)
    TextGrind_AliveTime.append(0)
    TextGrind_IsGrindText.append(IsGrindText)
    TextGrind_TextColor.append(TextColor)
    TextGrind_Value.append(Value)

def Update():
    global Current_Money
    global Current_MoneyValuePerClick
    global ReceiveLog_Y_Offset
    global ReceiveLog_Y_AnimEnabled
    global ReceiveLog_Y_AnimType
    global ReceiveLog_Y_OffsetAdder
    global GameOptionsButton
    global BackToMainMenuButton
    global GameItemsList
    global GameItemsInitialized
    global OpenStoreButton
    global StoreWindow_Enabled
    global ItemsView
    global UnloadDelay
    global UnloadRequested
    if GameItemsInitialized:
        for x in GameItemsList:
            x.Update()

    ItemsView.Set_X(5)
    ItemsView.Set_Y(gameMain.DefaultDisplay.get_height() - 130)

    # -- Update Buttons Click -- #
    if GrindButton.ButtonState == "UP":
        AddMessageText("+" + str(Current_MoneyValuePerClick), True, (20,150,25), Current_MoneyValuePerClick)
    if ReceiveLog_CloseButton.ButtonState == "UP":
        ReceiveLog_Y_AnimEnabled = True
    if GameOptionsButton.ButtonState == "UP":
        gameMain.FadeEffectValue = 255
        gameMain.FadeEffectCurrentState = 0
        gameMain.FadeEffectState = True
        ScreenSettings.ScreenToReturn = gameMain.CurrentScreen
        ScreenSettings.Initialize()
        storeWindow.RestartAnimation()
        gameMain.CurrentScreen += 1

    if SaveButton.ButtonState == "UP":
        AddMessageText("Game Saved", False, (255,255,255))
        SaveGame()

    if BackToMainMenuButton.ButtonState == "UP":
        gameMain.FadeEffectState = 0
        gameMain.FadeEffectValue = 255
        gameMain.FadeEffectState = True
        UnloadRequested = True

    if UnloadRequested:
        UnloadDelay += 1

        if UnloadDelay >= 3:
            Unload()
            gameMain.CurrentScreen -= 1

    if OpenStoreButton.ButtonState == "UP":
        if StoreWindow_Enabled:
            StoreWindow_Enabled = False
            storeWindow.RestartAnimation()
        else:
            StoreWindow_Enabled = True

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

    # -- Update the Receive Log Hide Animation -- #
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
    sprite.RenderRectangle(DISPLAY, (4, 21, 32), (GlobalX, GlobalY, 350, 350)) # -- Container Background -- #
    sprite.RenderRectangle(DISPLAY, (66, 75, 84), (GlobalX + 2, GlobalY + 2, 350 - 4, 350 - 4)) # -- Container Border -- #

    global Current_Money
    for x, TextGrind_TxT in enumerate(TextGrind_Text):
        sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 20, TextGrind_TxT, TextGrind_TextColor[x], TextGrind_X[x], TextGrind_Y[x])

        TextGrind_Y[x] -= 3
        if TextGrind_IsGrindText[x]:
            TextGrind_X[x] += TextGrind_AliveTime[x] / 256

        TextGrind_AliveTime[x] += 1
        if TextGrind_AliveTime[x] >= 500 + x or TextGrind_Y[x] <= ReceiveLog_Y_Offset + DISPLAY.get_height() - 350:
            if TextGrind_IsGrindText[x]:
                Current_Money += float(TextGrind_Value[x])
            TextGrind_Text.pop(x)
            TextGrind_X.pop(x)
            TextGrind_Y.pop(x)
            TextGrind_AliveTime.pop(x)
            TextGrind_IsGrindText.pop(x)
            TextGrind_TextColor.pop(x)
            TextGrind_Value.pop(x)


    # -- Render the Container Title -- #
    sprite.RenderRectangle(DISPLAY, (13, 10, 13), (GlobalX + 2, GlobalY + 2, 350 - 4, 24 - 4))
    sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 18, "Receiving Log", (250, 250, 255), GlobalX + 3,
                      GlobalY + 3)

    ReceiveLog_CloseButton.Render(DISPLAY)


def GameDraw(DISPLAY):
    global BackToMainMenuButton
    global OpenStoreButton
    global StoreWindow_Enabled
    global ItemsView
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
    # -- Draw the Store Button -- #
    OpenStoreButton.Render(DISPLAY)
    # -- Draw the Items View -- #
    ItemsView.Render(DISPLAY)

    # -- Render Money Text -- #
    sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 18, "Money: " + str(Current_Money),
                      (255, 255, 255), 10, 20)

    # -- Draw the Store Window -- #
    if StoreWindow_Enabled:
        storeWindow.Render(DISPLAY)


def Initialize(DISPLAY):
    # -- Set Buttons -- #
    global ReceiveLog_CloseButton
    global SaveButton
    global GameOptionsButton
    global GrindButton
    global BackToMainMenuButton
    global OpenStoreButton
    global ItemsView
    # -- Initialize Buttons -- #
    GrindButton = gameObjs.Button(pygame.rect.Rect(15, 115, 130, 150), "This text is not ment to be visible.", 18)
    GrindButton.WhiteButton = True
    ReceiveLog_CloseButton = gameObjs.Button(pygame.rect.Rect(320, 0, 0, 0), "↓", 16)
    GameOptionsButton = gameObjs.Button(pygame.rect.Rect(DISPLAY.get_width() - 120, 5, 0, 0), "OPTIONS", 12)
    SaveButton = gameObjs.Button(pygame.rect.Rect(DISPLAY.get_width() - 120, 20, 0, 0), "Save", 12)
    BackToMainMenuButton = gameObjs.Button(pygame.Rect(DISPLAY.get_width() - 120,35,0,0),"Main Menu",12)
    OpenStoreButton = gameObjs.Button(pygame.Rect(5,DISPLAY.get_height() - 25,0,0),"Store",14)

    ItemsView = gameObjs.HorizontalItemsView(pygame.Rect(5, 500, 430, 100))

    # -- Load Saved Values -- #
    LoadGame()
    print("GameScreen : All objects initialized.")

    # -- Initialize Objects -- #
    storeWindow.Initialize()

def Unload():
    global Current_Money
    global Current_MoneyValuePerClick
    global CUrrent_Experience
    global storeWindow
    global GameItemsList
    global GameItemsInitialized
    global GameItems_TotalIndx_NegativeOne
    global GameItems_TotalIndx_0
    global TextGrind_Y
    global TextGrind_X
    global TextGrind_AliveTime
    global TextGrind_IsGrindText
    global TextGrind_Value
    global TextGrind_Text
    global TextGrind_TextColor
    global StoreWindow_Enabled
    global UnloadDelay
    global UnloadRequested


    # -- Restart Current Money -- #
    print("GameScreen : Restart User Data")
    Current_Money = 0
    Current_MoneyValuePerClick = 0
    CUrrent_Experience = 0

    # -- Clear Game Items -- #
    print("GameScreen : Clear Game Items")
    GameItemsList.clear()
    GameItemsInitialized = False
    GameItems_TotalIndx_0 = 0
    GameItems_TotalIndx_NegativeOne = 0
    StoreWindow_Enabled = False

    # -- Clear Receiving Log -- #
    print("GameScreen : Clear Receiving Log")
    TextGrind_Y.clear()
    TextGrind_X.clear()
    TextGrind_AliveTime.clear()
    TextGrind_IsGrindText.clear()
    TextGrind_Value.clear()
    TextGrind_Text.clear()
    TextGrind_TextColor.clear()

    print("GameScreen : Restart storeWindow")
    storeWindow.RestartAnimation()

    print("GameScreen : Restart Unload Variables")
    UnloadRequested = False
    UnloadDelay = 0

def EventUpdate(event):
    # -- Update all buttons -- #
    global GrindButton
    global ReceiveLog_CloseButton
    global GameOptionsButton
    global SaveButton
    global BackToMainMenuButton
    global OpenStoreButton
    global StoreWindow_Enabled
    global ItemsView
    GrindButton.Update(event)
    ReceiveLog_CloseButton.Update(event)
    GameOptionsButton.Update(event)
    SaveButton.Update(event)
    BackToMainMenuButton.Update(event)
    OpenStoreButton.Update(event)
    ItemsView.Update(event)

    # -- Update store Window -- #
    if StoreWindow_Enabled:
        storeWindow.EventUpdate(event)