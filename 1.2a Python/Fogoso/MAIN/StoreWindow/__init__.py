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

import ENGINE.SPRITE as sprite
import Fogoso.MAIN.ClassesUtils as gameObjs
import Fogoso.MAIN as GameMain
import pygame
import ENGINE.Registry as reg
import Fogoso.MAIN.Screens.Game as GameScreen
print("Fogoso Store Window, Version 1.0")

# -- Field -- #
WindowObject = gameObjs.Window
BuyButton = gameObjs.Button
WindowSurface = pygame.Surface((0,0))
ListItems = gameObjs.VerticalListWithDescription
SelectedItemPrice = 0
SelectedItemID = 0
DownBar_BuyPanelYOffset = 0
DownBar_BuyPanelYOffsetAdder = 0
DownBar_BuyPanelAnimEnabled = True
LastClickedItem = "null"
BuyAmout = 1

def Initialize():
    global WindowObject
    global BuyButton
    global WindowSurface
    global ListItems
    global BuyAmout
    WindowObject = gameObjs.Window(pygame.Rect(100,100,350,250),"Store",True)
    WindowObject.Minimizable = False
    BuyButton = gameObjs.Button(pygame.Rect(20, 20, 50, 50), "Buy", 14)
    BuyButton.CustomColisionRectangle = True
    WindowSurface = WindowObject.WindowSurface
    ListItems = gameObjs.VerticalListWithDescription(pygame.Rect(0, 0, 350, 250))
    BuyAmout = reg.ReadKey_int("/ItemData/store/buyAmount")

    print("StoreWindowInitialize : Add Store Items")
    for x in range(-1, reg.ReadKey_int("/ItemData/store/all") + 1):
        CurrentItemRoot = "/ItemData/store/" + str(x) + "_"
        print("AddStoreItems : CurrentItem[" + CurrentItemRoot + "]")
        ListItems.AddItem(reg.ReadKey(CurrentItemRoot + "name"), reg.ReadKey(CurrentItemRoot + "description"), reg.ReadKey(CurrentItemRoot + "sprite"))

def Render(DISPLAY):
    global WindowObject
    global WindowSurface
    global BuyButton
    global ListItems
    global DownBar_BuyPanelAnimEnabled
    global DownBar_BuyPanelYOffset
    global LastClickedItem
    global SelectedItemID
    # -- Update the Surface -- #
    WindowSurface = WindowObject.WindowSurface
    # -- Update Controls -- #
    UpdateControls()

    # -- Draw the List -- #
    ListItems.Render(WindowSurface)

    # -- Render the Selected Item Text -- #
    if ListItems.LastItemClicked != "null":
        if LastClickedItem != ListItems.LastItemClicked:
            DownBar_BuyPanelAnimEnabled = True
            DownBar_BuyPanelYOffset = 0
        LastClickedItem = ListItems.LastItemClicked

        # -- Set Item Price and ID -- #
        SelectedItemPrice = GetItemPrice_ByID(GetItemID_ByName(ListItems.LastItemClicked))
        SelectedItemID = GetItemID_ByName(ListItems.LastItemClicked)

        # -- Down Panel Background -- #
        sprite.RenderRectangle(WindowSurface, (DownBar_BuyPanelYOffset - 20, DownBar_BuyPanelYOffset + 2, DownBar_BuyPanelYOffset + 19), (0, WindowSurface.get_height() - DownBar_BuyPanelYOffset, WindowSurface.get_width(), DownBar_BuyPanelYOffset))
        sprite.RenderRectangle(WindowSurface, (DownBar_BuyPanelYOffset + 16, DownBar_BuyPanelYOffset + 166, DownBar_BuyPanelYOffset + 152), (0, WindowSurface.get_height() - DownBar_BuyPanelYOffset - 1, WindowSurface.get_width(), 1))
        # -- Draw the Buy Button -- #
        BuyButton.Render(WindowSurface)
        # -- Draw the Item Title -- #
        sprite.RenderFont(WindowSurface, "/PressStart2P.ttf", 15, ListItems.LastItemClicked,(250,250,250),10,WindowSurface.get_height() - DownBar_BuyPanelYOffset + 5, reg.ReadKey_bool("/OPTIONS/font_aa"))
        # -- Draw the Item Price -- #
        sprite.RenderFont(WindowSurface,"/PressStart2P.ttf",8, "$" + str(SelectedItemPrice),(250,250,250),10,WindowSurface.get_height() - DownBar_BuyPanelYOffset + 20, reg.ReadKey_bool("/OPTIONS/font_aa"))

    WindowObject.Render(DISPLAY)
    DISPLAY.blit(WindowSurface, WindowObject.WindowSurface_Dest)

def UpdateControls():
    global DownBar_BuyPanelYOffset
    global DownBar_BuyPanelAnimEnabled
    global DownBar_BuyPanelYOffsetAdder
    global BuyAmout
    # -- Set the Buy Button Location -- #
    BuyButton.Set_X(WindowObject.WindowRectangle[2] - BuyButton.Rectangle[2] - 5)
    BuyButton.Set_Y(WindowObject.WindowRectangle[3] - BuyButton.Rectangle[3] - DownBar_BuyPanelYOffset + 5)
    # -- Set the Buy Button Collision -- #
    BuyButton.Set_ColisionX(WindowObject.WindowRectangle[0] + BuyButton.Rectangle[0])
    BuyButton.Set_ColisionY(WindowObject.WindowRectangle[1] + BuyButton.Rectangle[1] + BuyButton.Rectangle[3])

    if BuyButton.ButtonState == "UP":
        for buyAmount in range(0, BuyAmout):
            BuyItem_ByID(SelectedItemID)

    # -- Set Items List Size -- #
    ListItems.Set_W(WindowSurface.get_width())
    ListItems.Set_H(WindowSurface.get_height())
    ListItems.ColisionXOffset = WindowObject.WindowRectangle[0]
    ListItems.ColisionYOffset = WindowObject.WindowRectangle[1] + 20

    # -- Buy Panel -- #
    if DownBar_BuyPanelAnimEnabled:
        DownBar_BuyPanelYOffsetAdder += 1
        DownBar_BuyPanelYOffset += DownBar_BuyPanelYOffsetAdder

        if DownBar_BuyPanelYOffset >= 30:
            DownBar_BuyPanelYOffset = 30
            DownBar_BuyPanelAnimEnabled = False
            DownBar_BuyPanelYOffsetAdder = 0

def RestartAnimation():
    global DownBar_BuyPanelAnimEnabled
    global DownBar_BuyPanelYOffset
    global LastClickedItem
    DownBar_BuyPanelAnimEnabled = False
    DownBar_BuyPanelYOffset = 0
    LastClickedItem = "null"

def GetItemID_ByName(ItemName):
    return reg.ReadKey("/ItemData/name/" + ItemName)

def GetItemPrice_ByID(ItemID):
    LastItemLevel = reg.ReadKey_int("/Save/item/last_level/" + str(ItemID))
    CorrectKeyName = "/ItemData/store/price/" + str(ItemID) + "_level_" + str(LastItemLevel)
    return reg.ReadKey_float(CorrectKeyName)

def BuyItem_ByID(ItemID):
    ItemPrice = GetItemPrice_ByID(ItemID)
    GameScreen.Current_Money -= ItemPrice
    ItemLevel = reg.ReadKey_int("/Save/item/last_level/" + str(ItemID))

    print("BuyItem : ItemPrice:{0}; ItemLevel{1}; ItemID:{2}".format(str(ItemPrice), str(ItemLevel), str(ItemID)))

    if ItemID == "-1":
        GameScreen.GameItemsList.append(gameObjs.Item_Nothing(ItemLevel))
        GameScreen.GameItems_TotalIndx_NegativeOne += 1
        print("BuyItem : ItemID -1")

    if ItemID == "0":
        GameScreen.GameItemsList.append(gameObjs.Item_AutoClicker(ItemLevel))
        GameScreen.GameItems_TotalIndx_0 += 1
        print("BuyItem : ItemID 0")

    GameScreen.ItemsView.AddItem(str(ItemID))

def EventUpdate(event):
    WindowObject.EventUpdate(event)
    BuyButton.Update(event)
    ListItems.Update(event)
