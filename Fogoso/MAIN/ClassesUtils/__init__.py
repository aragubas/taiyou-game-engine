#!/usr/bin/ python3.6
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
from ENGINE import SPRITE as sprite
from Fogoso import MAIN as mainScript
from ENGINE import REGISTRY as reg
import pygame
import random

print("Game : Classes Utils v1.1")


class Button:
    def __init__(self, Rectangle, ButtonText, TextSize):
        self.Rectangle = Rectangle
        self.ButtonText = ButtonText
        self.TextSize = TextSize
        self.ButtonState = "INATIVE"
        self.IsButtonEnabled = True
        self.WhiteButton = False
        self.Rectangle = pygame.rect.Rect(self.Rectangle[0], self.Rectangle[1],
                                          sprite.GetText_width("/PressStart2P.ttf", self.TextSize,
                                                               self.ButtonText) + 5,
                                          sprite.GetText_height("/PressStart2P.ttf", self.TextSize,
                                                                self.ButtonText) + 3)
        self.CursorSettedToggle = False
        self.ButtonDowed = False
        self.ColisionRectangle = self.Rectangle
        self.CustomColisionRectangle = False
        self.BackgroundColor = (1, 22, 39)

    def Update(self, event):
        if not self.CustomColisionRectangle:
            self.ColisionRectangle = self.Rectangle

        if self.IsButtonEnabled:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.ColisionRectangle.collidepoint(mainScript.Cursor_Position):
                    self.ButtonState = "DOWN"
                    self.ButtonDowed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.ColisionRectangle.collidepoint(mainScript.Cursor_Position):
                    if self.ButtonDowed:
                        self.ButtonState = "UP"
                        self.ButtonDowed = False
            if event.type == pygame.MOUSEMOTION:
                if self.ColisionRectangle.collidepoint(mainScript.Cursor_Position):
                    self.CursorSettedToggle = True
                    mainScript.Cursor_CurrentLevel = 3
                else:
                    if self.CursorSettedToggle:
                        self.CursorSettedToggle = False
                        mainScript.Cursor_CurrentLevel = 0
                        self.ButtonState = "INATIVE"

        else:
            self.ButtonState = "INATIVE"

        if not self.WhiteButton:
            self.Rectangle = pygame.rect.Rect(self.Rectangle[0], self.Rectangle[1],
                                              sprite.GetText_width("/PressStart2P.ttf", self.TextSize,
                                                                   self.ButtonText) + 5,
                                              sprite.GetText_height("/PressStart2P.ttf", self.TextSize,
                                                                    self.ButtonText) + 3)

    def Set_X(self, Value):
        self.Rectangle[0] = Value

    def Set_Y(self, Value):
        self.Rectangle[1] = Value

    def Set_Width(self, Value):
        self.Rectangle[2] = Value

    def Set_Height(self, Value):
        self.Rectangle[3] = Value

    def Set_ColisionX(self, Value):
        self.ColisionRectangle[0] = Value

    def Set_ColisionY(self, Value):
        self.ColisionRectangle[1] = Value

    def Set_Text(self, Value):
        self.ButtonText = Value

    def Render(self, DISPLAY):
        # -- Render the Background -- #
        ButtonSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]), pygame.SRCALPHA)
        pygame.draw.rect(ButtonSurface, self.BackgroundColor, (0,0, self.Rectangle[2], self.Rectangle[3]))

        if not self.WhiteButton:
            if self.ButtonState == "INATIVE":
                self.BackgroundColor = (1, 22, 39, 50)

                # -- Indicator Bar -- #
                sprite.RenderRectangle(ButtonSurface, (255, 51, 102), (0, 0, self.Rectangle[2],1))

                # -- Text -- #
                sprite.RenderFont(ButtonSurface, "/PressStart2P.ttf", self.TextSize, self.ButtonText, (200, 200, 200),
                                  3, 3, reg.ReadKey_bool("/OPTIONS/font_aa"))

            else:
                # -- Background -- #
                self.BackgroundColor = (15, 27, 44, 100)
                # -- Indicator Bar -- #
                sprite.RenderRectangle(ButtonSurface, (46, 196, 182), (0, 0,self.Rectangle[2],1))

                # -- Text -- #
                sprite.RenderFont(ButtonSurface, "/PressStart2P.ttf", self.TextSize, self.ButtonText, (255, 255, 255),
                                  3, 3, reg.ReadKey_bool("/OPTIONS/font_aa"))
        else:
            if self.ButtonState == "INATIVE":
                # -- Background -- #
                self.BackgroundColor = (1, 22, 39, 50)

                # -- Indicator Bar -- #
                sprite.RenderRectangle(ButtonSurface, (255, 51, 102), (0, 0,self.Rectangle[2],4))

            else:
                # -- Background -- #
                self.BackgroundColor = (15, 27, 44, 100)
                # -- Indicator Bar -- #
                sprite.RenderRectangle(ButtonSurface, (46, 196, 182), (0, 0, self.Rectangle[2],2))

        # -- Draw the Button -- #
        DISPLAY.blit(ButtonSurface, (self.Rectangle[0], self.Rectangle[1]))
        if self.ButtonState == "UP":
            self.ButtonState = "INATIVE"




class UpDownButton:
    def __init__(self, X, Y, TextSize):
        self.X = X
        self.Y = Y
        self.TextSize = TextSize
        self.UpButton = Button(pygame.Rect(X, Y, 20, 20), "/\\", TextSize)
        self.DownButton = Button(pygame.Rect(X + sprite.GetText_width("/PressStart2P.ttf", TextSize, "\/") + 5, Y, 20, 20), "\/", TextSize)
        self.ButtonState = "INATIVE"
        self.BackStateWaitLoop = 0
        print("ObjectCreation : UpDownButton created.")

    def Update(self, event):
        self.UpButton.Update(event)
        self.DownButton.Update(event)

        if self.UpButton.ButtonState == "UP":
            self.ButtonState = "UP"
        if self.DownButton.ButtonState == "UP":
            self.ButtonState = "DOWN"

    def Render(self, DISPLAY):
        self.UpButton.Render(DISPLAY)
        self.DownButton.Render(DISPLAY)

        if self.ButtonState == "UP" or self.ButtonState == "DOWN":
            self.BackStateWaitLoop += 1

            if self.BackStateWaitLoop >= 1:
                self.ButtonState = "INATIVE"
                self.BackStateWaitLoop = 0

    def Get_Width(self):
        return sprite.GetText_width("/PressStart2P.ttf", self.TextSize, "\/") + 4 + sprite.GetText_width(
            "/PressStart2P.ttf", self.TextSize, "/\\") + 4

    def Get_Height(self):
        return sprite.GetText_height("/PressStart2P.ttf", self.TextSize, "\/") + 4 + sprite.GetText_height(
            "/PressStart2P.ttf", self.TextSize, "/\\") + 4

    def Set_X(self, NewXValue):
        self.UpButton.Set_X(NewXValue)
        self.DownButton.Set_X(
            NewXValue + sprite.GetText_width("/PressStart2P.ttf", self.TextSize, "\/") + 5)

    def Set_Y(self, NewYValue):
        self.UpButton.Set_Y(NewYValue)
        self.DownButton.Set_Y(NewYValue)

    def Set_Size(self, NewSize):
        self.UpButton.TextSize = NewSize
        self.DownButton.TextSize = NewSize

        self.UpButton.Set_X(self.X)
        self.DownButton.Set_X(
            self.X + sprite.GetText_width("/PressStart2P.ttf", self.TextSize, "\/") + 5)




class Window:
    def __init__(self, Rectangle, Title, Resiziable):
        self.WindowRectangle = Rectangle
        self.Title = Title
        self.TitleBarRectangle = pygame.Rect(self.WindowRectangle[0], self.WindowRectangle[1], self.WindowRectangle[2],
                                             20)
        self.ResizeRectangle = pygame.Rect(self.WindowRectangle[0] + self.WindowRectangle[3] - 16,
                                           self.WindowRectangle[1] + self.WindowRectangle[3] - 16, 16, 16)
        self.Cursor_Position = mainScript.Cursor_Position
        self.Window_IsBeingGrabbed = False
        self.Window_IsBeingResized = False
        self.Window_MinimunW = Rectangle[2]
        self.Window_MinimunH = Rectangle[3]
        self.MinimizeButton = Button(pygame.Rect(self.WindowRectangle[0] + self.WindowRectangle[2] - 20, self.WindowRectangle[1], 16, 20),"↑",16)
        self.WindowSurface = pygame.Surface((self.WindowRectangle[0], self.WindowRectangle[1] + 20), pygame.SRCALPHA)
        self.WindowMinimized = False
        self.Resiziable = Resiziable
        self.WindowOriginalRect = pygame.Rect(0, 0, 0, 0)
        self.OriginalMinumunHeight = 0
        self.OriginalResiziable = False
        self.WindowSurface_Dest = (0, 0)
        self.Minimizable = True

    def Render(self, DISPLAY):
        # -- Window Rectangle -- #
        self.WindowRectangle[0] = self.TitleBarRectangle[0]
        self.WindowRectangle[1] = self.TitleBarRectangle[1]
        # -- Title Bar Rectangle -- #
        if self.Minimizable:
            self.TitleBarRectangle = pygame.Rect(self.WindowRectangle[0], self.WindowRectangle[1],
                                                 self.WindowRectangle[2] - 21, 20)
        else:
            self.TitleBarRectangle = pygame.Rect(self.WindowRectangle[0], self.WindowRectangle[1],
                                                 self.WindowRectangle[2], 20)
        # -- Resize Button Rectangle -- #
        if self.Resiziable:
            self.ResizeRectangle = pygame.Rect(self.WindowRectangle[0] + self.WindowRectangle[2] - 10,
                                               self.WindowRectangle[1] + self.WindowRectangle[3], 10, 10)
        # -- Minimize Button Location -- #
        if self.Minimizable:
            self.MinimizeButton.Set_X(self.WindowRectangle[0] + self.WindowRectangle[2] - 21)
            self.MinimizeButton.Set_Y(self.WindowRectangle[1])
        # -- Window Surface -- #
        if not self.WindowMinimized:
            self.WindowSurface = pygame.Surface((self.WindowRectangle[2], self.WindowRectangle[3] - 20), pygame.SRCALPHA)
        # -- Update Window Surface Destination -- #
        if not self.WindowMinimized:
            self.WindowSurface_Dest = self.WindowRectangle[0], self.WindowRectangle[1] + 20

        # -- Update Window Border -- #
        if not self.Resiziable:
            WindowBorderRectangle = (
                self.WindowRectangle[0] - 2, self.WindowRectangle[1] - 2, self.WindowRectangle[2] + 4,
                self.WindowRectangle[3] + 4)
        else:
            WindowBorderRectangle = (
                self.WindowRectangle[0] - 2, self.WindowRectangle[1] - 2, self.WindowRectangle[2] + 4,
                self.WindowRectangle[3] + 12)

        # -- Draw the Window Blurred Background -- #
        if not self.Window_IsBeingGrabbed:
            IndicatorLineColor = (32, 164, 243)
        else:
            IndicatorLineColor = (255, 51, 102)
        if reg.ReadKey_bool("/OPTIONS/window_blur_bg"):
            BackContrast = pygame.Surface((self.WindowRectangle[2], self.WindowRectangle[3]), pygame.SRCALPHA)
            pygame.draw.rect(BackContrast, (0, 0, 0, 150), (0,0, self.WindowRectangle[2], self.WindowRectangle[3]))
            DISPLAY.blit(BackContrast, (self.WindowRectangle[0], self.WindowRectangle[1]))

            DISPLAY.blit(sprite.Surface_Blur(DISPLAY, reg.ReadKey_float("/OPTIONS/window_blur_amount")), (WindowBorderRectangle[0], WindowBorderRectangle[1]), WindowBorderRectangle)

        else:
            sprite.RenderRectangle(DISPLAY, (6, 27, 45), WindowBorderRectangle)
        pygame.draw.line(DISPLAY, IndicatorLineColor, (self.TitleBarRectangle[0], self.TitleBarRectangle[1] - 2 + self.TitleBarRectangle[3]), (self.TitleBarRectangle[0] + self.TitleBarRectangle[2], self.TitleBarRectangle[1] - 2 + self.TitleBarRectangle[3]), 2)

        # -- Draw the Resize Block -- #
        if self.Resiziable:
            sprite.Render(DISPLAY, "/window/resize.png", self.ResizeRectangle[0], self.ResizeRectangle[1],
                          self.ResizeRectangle[2], self.ResizeRectangle[3])

        # -- Render the Minimize Button -- #
        if self.Minimizable:
            self.MinimizeButton.Render(DISPLAY)

        # -- Draw the window title -- #
        sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 18, self.Title, (250, 250, 255),
                          self.TitleBarRectangle[0] + self.TitleBarRectangle[2] / 2 - sprite.GetText_width(
                              "/PressStart2P.ttf", 18, self.Title) / 2, self.TitleBarRectangle[1] + 1, reg.ReadKey_bool("/OPTIONS/font_aa"))


    def EventUpdate(self, event):
        self.Cursor_Position = mainScript.Cursor_Position

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.TitleBarRectangle.collidepoint(self.Cursor_Position):
                self.Window_IsBeingGrabbed = True
                mainScript.Cursor_CurrentLevel = 2
            if self.ResizeRectangle.collidepoint(self.Cursor_Position) and self.Resiziable:
                self.Window_IsBeingResized = True
                mainScript.Cursor_CurrentLevel = 1
        # -------------------------------------------------------------------
        if event.type == pygame.MOUSEBUTTONUP:
            if self.Window_IsBeingResized:
                self.Window_IsBeingResized = False
                mainScript.Cursor_CurrentLevel = 0
            if self.Window_IsBeingGrabbed:
                self.Window_IsBeingGrabbed = False
                mainScript.Cursor_CurrentLevel = 0
        # -- Minimize Button Update -- #
        if self.Minimizable:
            self.MinimizeButton.Update(event)
            if self.MinimizeButton.ButtonState == "UP":
                self.ToggleMinimize()
            if not self.WindowMinimized:
                self.MinimizeButton.Set_Text("↑")
            else:
                self.MinimizeButton.Set_Text("↓")

        # -- Grab Window -- #
        if self.Window_IsBeingGrabbed:
            self.TitleBarRectangle[0] = self.Cursor_Position[0] - self.WindowRectangle[2] / 2
            self.TitleBarRectangle[1] = self.Cursor_Position[1] - self.TitleBarRectangle[3] / 2
        # -- Resize Window -- #
        if self.Window_IsBeingResized and self.Resiziable:
            if self.WindowRectangle[2] >= self.Window_MinimunW:
                self.WindowRectangle[2] = self.Cursor_Position[0] - self.WindowRectangle[0]

            if self.WindowRectangle[3] >= self.Window_MinimunH:
                self.WindowRectangle[3] = self.Cursor_Position[1] - self.WindowRectangle[1]

        if self.WindowRectangle[2] <= self.Window_MinimunW:
            self.WindowRectangle[2] = self.Window_MinimunW
        # -------------------------------------------------
        if self.WindowRectangle[3] <= self.Window_MinimunH:
            self.WindowRectangle[3] = self.Window_MinimunH

    def ToggleMinimize(self):
        if self.WindowMinimized:
            self.WindowMinimized = False
            self.WindowRectangle = self.WindowOriginalRect
            self.Window_MinimunH = self.OriginalMinumunHeight
            self.Resiziable = self.OriginalResiziable
        else:
            self.WindowMinimized = True
            self.WindowOriginalRect = self.WindowRectangle
            self.WindowRectangle = pygame.Rect(self.WindowRectangle[0], self.WindowRectangle[1],
                                               self.WindowRectangle[2], 20)
            self.OriginalMinumunHeight = self.Window_MinimunH
            self.Window_MinimunH = 0
            self.OriginalResiziable = self.Resiziable
            self.Resiziable = False

class VerticalListWithDescription:
    def __init__(self, Rectangle):
        self.Rectangle = Rectangle
        self.ItemsName = list()
        self.ItemsDescription = list()
        self.ItemSprite = list()
        self.ItemSelected = list()
        self.LastItemClicked = "null"
        self.ScrollY = 0
        self.ListSurface = pygame.Surface
        self.ClickedItem = ""
        self.ColisionXOffset = 0
        self.ColisionYOffset = 0
        self.ButtonUpRectangle = pygame.Rect(0, 0, 32, 32)
        self.ButtonDownRectangle = pygame.Rect(34, 0, 32, 32)
        self.Cursor_Position = mainScript.Cursor_Position

    def Render(self,DISPLAY):
        self.ListSurface = pygame.Surface((self.Rectangle[2],self.Rectangle[3]), pygame.SRCALPHA)

        for i, itemNam in enumerate(self.ItemsName):
            ItemRect = (self.Rectangle[0],self.ScrollY + self.Rectangle[1] + 42 * i,self.Rectangle[2],40)

            # -- When the item is not clicked -- #
            if not self.ItemSelected[i]:
                if self.LastItemClicked == itemNam:
                    # -- Background -- #
                    sprite.RenderRectangle(self.ListSurface, (20, 42, 59, 100), ItemRect)
                    # -- Indicator Bar -- #
                    sprite.RenderRectangle(self.ListSurface, (46, 196, 182), (ItemRect[0], ItemRect[1], ItemRect[2], 1))
                else:
                    # -- Background -- #
                    sprite.RenderRectangle(self.ListSurface, (20, 42, 59, 50), ItemRect)
                    # -- Indicator Bar -- #
                    sprite.RenderRectangle(self.ListSurface, (32, 164, 243), (ItemRect[0],ItemRect[1],ItemRect[2],1))
            else:
                # -- Background -- #
                sprite.RenderRectangle(self.ListSurface, (30, 52, 69, 150), ItemRect)
                # -- Indicator Bar -- #
                sprite.RenderRectangle(self.ListSurface, (255, 51, 102), (ItemRect[0],ItemRect[1],ItemRect[2],1))

            # -- Render the Item Name and Description -- #
            if not self.ItemSelected[i]:
                sprite.RenderFont(self.ListSurface, "/PressStart2P.ttf", 12, itemNam, (250, 250, 250), ItemRect[0] + 45, ItemRect[1] + 5, reg.ReadKey_bool("/OPTIONS/font_aa"))
                sprite.RenderFont(self.ListSurface, "/PressStart2P.ttf", 10, self.ItemsDescription[i], (250, 250, 250), ItemRect[0] + 45,ItemRect[1] + 30, reg.ReadKey_bool("/OPTIONS/font_aa"))
            else:
                sprite.RenderFont(self.ListSurface, "/PressStart2P.ttf", 12, itemNam, (255, 255, 255), ItemRect[0] + 45, ItemRect[1] + 5, reg.ReadKey_bool("/OPTIONS/font_aa"))
                sprite.RenderFont(self.ListSurface, "/PressStart2P.ttf", 10, self.ItemsDescription[i], (255, 255, 255), ItemRect[0] + 45, ItemRect[1] + 30, reg.ReadKey_bool("/OPTIONS/font_aa"))

            # -- Render the Item Sprite -- #
            if self.ItemSprite[i] != "null":
                sprite.Render(self.ListSurface,self.ItemSprite[i],ItemRect[0] + 4,ItemRect[1] + 4,36, 32)

        DISPLAY.blit(self.ListSurface,(self.Rectangle[0], self.Rectangle[1]))

    def Update(self, event):
        self.Cursor_Position = mainScript.Cursor_Position

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                self.ScrollY += 5
            if event.key == pygame.K_e:
                self.ScrollY -= 5

        # -- Select the Clicked Item -- #
        for i, itemNam in enumerate(self.ItemsName):
            ItemRect = pygame.Rect(self.ColisionXOffset + self.Rectangle[0], self.ColisionYOffset + self.ScrollY + self.Rectangle[1] + 42 * i, self.Rectangle[2], 40)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if ItemRect.collidepoint(self.Cursor_Position):
                    self.LastItemClicked = itemNam
                    self.ItemSelected[i] = True
                    print("LastClickedItem : " + self.LastItemClicked)
            if event.type == pygame.MOUSEBUTTONUP:
                self.ItemSelected[i] = False

    def Set_X(self, Value):
        self.Rectangle[0] = int(Value)

    def Set_Y(self, Value):
        self.Rectangle[1] = int(Value)

    def Set_W(self, Value):
        self.Rectangle[2] = int(Value)

    def Set_H(self, Value):
        self.Rectangle[3] = int(Value)

    def AddItem(self,ItemName, ItemDescription, ItemSprite="null"):
        self.ItemsName.append(ItemName)
        self.ItemsDescription.append(ItemDescription)
        self.ItemSprite.append(ItemSprite)
        self.ItemSelected.append(False)

class HorizontalItemsView:
    def __init__(self, Rectangle):
        self.Rectangle = Rectangle
        self.ItemsName = list()
        self.ItemSprite = list()
        self.ItemSelected = list()
        self.ScrollX = 0
        self.ListSurface = pygame.Surface
        self.ButtonLeftRectangle = pygame.Rect(0, 0, 32, 32)
        self.ButtonRightRectangle = pygame.Rect(34, 0, 32, 32)

    def Render(self, DISPLAY):
        self.ListSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]))
        self.ListSurface.fill((1, 22, 39))

        for i, itemNam in enumerate(self.ItemsName):
            ItemName = reg.ReadKey("/ItemData/store/" + str(itemNam) + "_name")
            ItemWidth = 195

            ItemX = self.ScrollX + ItemWidth * i
            ItemRect = (ItemX, 0, ItemWidth - 5, self.Rectangle[3])
            #ItemRect = (self.Rectangle[0],self.ScrollY + self.Rectangle[1] + 42 * i,self.Rectangle[2],40)

            # -- Background -- #
            sprite.RenderRectangle(self.ListSurface, (120, 142, 159), ItemRect)
            # -- Indicator Bar -- #
            sprite.RenderRectangle(self.ListSurface, (46, 196, 182), (ItemRect[0], ItemRect[1], ItemRect[2], 1))

            # -- Render the Item Title -- #
            sprite.RenderFont(self.ListSurface, "/PressStart2P.ttf", 12, ItemName, (250, 250, 250), ItemRect[0] + ItemRect[2] / 2 - sprite.GetText_width("/PressStart2P.ttf", 12, ItemName) / 2, ItemRect[1], reg.ReadKey_bool("/OPTIONS/font_aa"))

            # -- Render the Item Sprite -- #
            sprite.Render(self.ListSurface, reg.ReadKey("/ItemData/store/" + str(itemNam) + "_sprite"), ItemRect[0] + 4, ItemRect[1] + 6, 100, 100)

            # -- Render the Item Little Info -- #
            LittleInfoText = "CANNOT OBTAIN\nITEM DATA."
            if self.ItemsName[i] == "-1":
                LittleInfoText = "Count:\n{0}\nLevel:\n{1}".format(str(mainScript.ScreenGame.GameItems_TotalIndx_NegativeOne), str(reg.ReadKey("/Save/item/last_level/" + str(itemNam))))
            if self.ItemsName[i] == "0":
                LittleInfoText = "Count:\n{0}\nLevel:\n{1}".format(str(mainScript.ScreenGame.GameItems_TotalIndx_0), str(reg.ReadKey("/Save/item/last_level/" + str(itemNam))))

            sprite.RenderFont(self.ListSurface, "/PressStart2P.ttf", 10, LittleInfoText, (250, 250, 250), ItemRect[0] + 105, ItemRect[1] + 12, reg.ReadKey_bool("/OPTIONS/font_aa"))
            # -- Spacer Bar -- #
            #sprite.RenderRectangle(self.ListSurface, (1, 22, 39), (ItemRect[0] + ItemRect[2] - 5, ItemRect[1], ItemRect[2], ItemRect[3]))

        DISPLAY.blit(self.ListSurface, (self.Rectangle[0], self.Rectangle[1]))

    def Update(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                self.ScrollX += 5
            if event.key == pygame.K_e:
                self.ScrollX -= 5

    def Set_X(self, Value):
        self.Rectangle[0] = float(Value)

    def Set_Y(self, Value):
        self.Rectangle[1] = float(Value)

    def Set_W(self, Value):
        self.Rectangle[2] = float(Value)

    def Set_H(self, Value):
        self.Rectangle[3] = float(Value)

    def AddItem(self, ItemName, ItemSprite="null"):
        try:
            Index = self.ItemsName.index(ItemName)
            ItemAlreadyExists = True
        except:
            ItemAlreadyExists = False

        if not ItemAlreadyExists:
            self.ItemsName.append(ItemName)
            self.ItemSprite.append(ItemSprite)
            self.ItemSelected.append(False)


class Item_AutoClicker:
    def __init__(self, ItemLevel):
        self.ItemClickPerSecound = reg.ReadKey("/ItemData/0/lv_" + str(ItemLevel) + "_click")
        self.ItemLevel = ItemLevel
        self.DeltaTime = 0
        self.InternalDelay = 0
        self.DeltaTimeAction = int(reg.ReadKey("/ItemData/0/lv_" + str(ItemLevel) + "_delta"))
        self.ItemID = 0
        self.maintenance_cost = reg.ReadKey_float("/ItemData/0/lv_" + str(ItemLevel) + "_cost_maintenance")

    def Update(self):
        self.DeltaTime += 1

        if int(self.DeltaTime) >= int(self.DeltaTimeAction):
            self.InternalDelay += 1

            if self.InternalDelay >= random.randint(100, int(self.DeltaTimeAction)):
                mainScript.ScreenGame.AddMessageText("+" + str(self.ItemClickPerSecound), True, (100, 210, 100), self.ItemClickPerSecound)
                self.DeltaTime = 0
                self.InternalDelay = 0

class Item_ExperienceStore:
    def __init__(self, ItemLevel):
        self.ItemClickPerSecound = reg.ReadKey("/ItemData/-1/lv_" + str(ItemLevel) + "_click")
        self.ItemLevel = ItemLevel
        self.DeltaTime = 0
        self.DeltaTimeAction = reg.ReadKey("/ItemData/-1/lv_" + str(ItemLevel) + "_delta")
        self.ItemID = -1
        self.maintenance_cost = reg.ReadKey_float("/ItemData/-1/lv_" + str(ItemLevel) + "_cost_maintenance")


    def Update(self):
        self.DeltaTime += 1

        if int(self.DeltaTime) >= int(self.DeltaTimeAction):
            mainScript.ScreenGame.AddMessageText("+" + str(self.ItemClickPerSecound), True, (100, 210, 100), self.ItemClickPerSecound)
            self.DeltaTime = 0
