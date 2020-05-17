#!/usr/bin/python3
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
from ENGINE import TaiyouUI as mainScript
from ENGINE import SOUND as sound
import pygame, sys

PANELS_BACKGROUND_COLOR = (4,21,32)
PANELS_INDICATOR_COLOR = (13,10,13)
PANELS_INDICATOR_SIZE = 2

def Draw_Panel(DISPLAY, Rectangle, IndicatorPosition="UP"):
    if IndicatorPosition == "BORDER":
        sprite.RenderRectangle(DISPLAY, PANELS_INDICATOR_COLOR, (Rectangle[0] - PANELS_INDICATOR_SIZE, Rectangle[1] - PANELS_INDICATOR_SIZE, Rectangle[2] + PANELS_INDICATOR_SIZE * 2, Rectangle[3] + PANELS_INDICATOR_SIZE * 2))

    sprite.RenderRectangle(DISPLAY, PANELS_BACKGROUND_COLOR, Rectangle)

    if IndicatorPosition == "DOWN":
        sprite.RenderRectangle(DISPLAY, PANELS_INDICATOR_COLOR, (Rectangle[0],Rectangle[1] + Rectangle[3] - PANELS_INDICATOR_SIZE, Rectangle[2], PANELS_INDICATOR_SIZE))

    if IndicatorPosition == "UP":
        sprite.RenderRectangle(DISPLAY, PANELS_INDICATOR_COLOR, (Rectangle[0], Rectangle[1], Rectangle[2], PANELS_INDICATOR_SIZE))

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
                                                                self.ButtonText) + 6)
        self.CursorSettedToggle = False
        self.ButtonDowed = False
        self.ColisionRectangle = self.Rectangle
        self.CustomColisionRectangle = False
        self.BackgroundColor = (1, 22, 39)
        self.ButtonSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]), pygame.SRCALPHA)
        self.SurfaceUpdated = False


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


        self.Rectangle = pygame.rect.Rect(self.Rectangle[0], self.Rectangle[1],
                                          sprite.GetText_width("/PressStart2P.ttf", self.TextSize,
                                                               self.ButtonText) + 5,
                                          sprite.GetText_height("/PressStart2P.ttf", self.TextSize,
                                                                self.ButtonText) + 6)
        if not self.SurfaceUpdated:
            self.SurfaceUpdated = True
            self.ButtonSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]), pygame.SRCALPHA)

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
        pygame.draw.rect(self.ButtonSurface, self.BackgroundColor, (0,0, self.Rectangle[2], self.Rectangle[3]))

        if not self.WhiteButton:
            if self.ButtonState == "INATIVE":
                self.BackgroundColor = (1, 22, 39, 50)

                # -- Indicator Bar -- #
                sprite.RenderRectangle(self.ButtonSurface, (255, 51, 102), (0, 0, self.Rectangle[2],1))

                # -- Text -- #
                sprite.RenderFont(self.ButtonSurface, "/PressStart2P.ttf", self.TextSize, self.ButtonText, (200, 200, 200),
                                  3, 3)

            else:
                # -- Background -- #
                self.BackgroundColor = (15, 27, 44, 100)
                # -- Indicator Bar -- #
                sprite.RenderRectangle(self.ButtonSurface, (46, 196, 182), (0, 0,self.Rectangle[2],1))

                # -- Text -- #
                sprite.RenderFont(self.ButtonSurface, "/PressStart2P.ttf", self.TextSize, self.ButtonText, (255, 255, 255),
                                  3, 3)
        else:
            if self.ButtonState == "INATIVE":
                # -- Background -- #
                self.BackgroundColor = (1, 22, 39, 50)

                # -- Indicator Bar -- #
                sprite.RenderRectangle(self.ButtonSurface, (255, 51, 102), (0, 0,self.Rectangle[2],4))

            else:
                # -- Background -- #
                self.BackgroundColor = (15, 27, 44, 100)
                # -- Indicator Bar -- #
                sprite.RenderRectangle(self.ButtonSurface, (46, 196, 182), (0, 0, self.Rectangle[2],2))

        # -- Draw the Button -- #
        DISPLAY.blit(self.ButtonSurface, (self.Rectangle[0], self.Rectangle[1]))
        if self.ButtonState == "UP":
            self.ButtonState = "INATIVE"
            sound.PlaySound("/TAIYOU_UI/HUD_Click.wav")

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
        self.SurfaceSizeFixed = False
        if not self.WindowMinimized:
            self.WindowSurface = pygame.Surface((self.WindowRectangle[2], self.WindowRectangle[3] - 20), pygame.SRCALPHA)

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

        # -- Update Window Surface Destination -- #
        if not self.WindowMinimized:
            self.WindowSurface_Dest = self.WindowRectangle[0], self.WindowRectangle[1] + 20

        # -- Clear Window Surface when is Minimized -- #
        if self.WindowMinimized:
            self.WindowSurface = pygame.Surface((0, 0))

        # -- Draw the Window Blurred Background -- #
        if not self.Window_IsBeingGrabbed:
            IndicatorLineColor = (32, 164, 243)
        else:
            IndicatorLineColor = (255, 51, 102)
        Draw_Panel(DISPLAY, self.WindowRectangle, "BORDER")

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
                              "/PressStart2P.ttf", 18, self.Title) / 2, self.TitleBarRectangle[1] + 1)


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
        if self.Window_IsBeingResized and self.Resiziable: # <- Resize the Window
            # -- Limit Window Size -- #

            if self.WindowRectangle[2] >= self.Window_MinimunW:
                self.WindowRectangle[2] = self.Cursor_Position[0] - self.WindowRectangle[0]
                self.UpdateSurface()

            if self.WindowRectangle[3] >= self.Window_MinimunH: # <- Resize the Window
                self.WindowRectangle[3] = self.Cursor_Position[1] - self.WindowRectangle[1]
                self.UpdateSurface()

        if self.WindowRectangle[2] < self.Window_MinimunW:
            self.WindowRectangle[2] = self.Window_MinimunW
            self.UpdateSurface()

            # -------------------------------------------------
        if self.WindowRectangle[3] < self.Window_MinimunH:
            self.WindowRectangle[3] = self.Window_MinimunH
            self.UpdateSurface()


    def UpdateSurface(self):
        if not self.WindowMinimized:
            self.WindowSurface = pygame.Surface((self.WindowRectangle[2], self.WindowRectangle[3] - 20), pygame.SRCALPHA)

    def ToggleMinimize(self):
        if self.WindowMinimized:
            self.WindowMinimized = False
            self.WindowRectangle = self.WindowOriginalRect
            self.Window_MinimunH = self.OriginalMinumunHeight
            self.Resiziable = self.OriginalResiziable
            self.UpdateSurface()
        else:
            self.WindowMinimized = True
            self.WindowOriginalRect = self.WindowRectangle
            self.WindowRectangle = pygame.Rect(self.WindowRectangle[0], self.WindowRectangle[1],
                                               self.WindowRectangle[2], 20)
            self.OriginalMinumunHeight = self.Window_MinimunH
            self.Window_MinimunH = 0
            self.OriginalResiziable = self.Resiziable
            self.Resiziable = False

COLOR_INACTIVE = (1, 22, 39)
COLOR_ACTIVE = (15,27,44)

class InputBox:
    def __init__(self, x, y, w, h, text='LO'):
        self.rect = pygame.Rect(x, y, w, h)
        self.colisionRect = pygame.Rect(x,y,w,h)
        self.CustomColision = False
        self.color = COLOR_INACTIVE
        self.text = text
        self.active = False
        self.DefaultText = text
        self.LastHeight = 1
        self.CustomWidth = False
        self.width = 1

    def Set_X(self, Value):
        self.rect = pygame.Rect(Value, self.rect[1], self.rect[2], self.rect[3])

    def Set_Y(self, Value):
        self.rect = pygame.Rect(self.rect[0], Value, self.rect[2], self.rect[3])

    def Update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.colisionRect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.active = not self.active
                else:
                    self.active = False
                # Change the current color of the input box.
                self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    if len(self.text) > 0:
                        self.text = self.text[:-1]
                    else:
                        self.text = self.DefaultText

                else:
                    self.text += event.unicode

    def Render(self, screen):
        # -- Resize the Textbox -- #
        try:
            if not self.CustomWidth:
                self.width = max(100, sprite.GetText_width("/PressStart2P.ttf", 10, self.text)+10)
            self.rect.w = self.width
            self.rect.h = sprite.GetText_height("/PressStart2P.ttf", 10, self.text)
            self.LastHeight = self.rect.h
        except:
            if not self.CustomWidth:
                self.rect.w = 100
            self.rect.h = self.LastHeight

        if not self.CustomColision:
            self.colisionRect = self.rect

        # Blit the rect.
        Draw_Panel(screen, self.rect, "UP")

        if self.text == self.DefaultText:
            sprite.RenderFont(screen, "/PressStart2P.ttf", 10, self.text, (140,140,140), self.rect[0],self.rect[1])
        else:
            if not self.text == "":
                sprite.RenderFont(screen, "/PressStart2P.ttf", 10, self.text, (240, 240, 240), self.rect[0], self.rect[1])

        if not self.active:
            sprite.RenderRectangle(screen, (255, 51, 102), (self.rect[0],self.rect[1] - 1,self.rect[2], 1))
        else:
            sprite.RenderRectangle(screen, (46, 196, 182), (self.rect[0],self.rect[1] - 1,self.rect[2], 1))

class HorizontalItemsView:
    def __init__(self, Rectangle):
        self.Rectangle = Rectangle
        # -- Selected item Vars -- #
        self.GameName = list()
        self.GameID = list()
        self.GameVersion = list()
        self.GameSourceFolder = list()
        self.GameBanner = list()
        self.GameFolderName = list()

        self.ItemSelected = list()
        self.SelectedItem = "Select a game below"
        self.SelectedGameID = ""
        self.SelectedGameFolderName = ""
        self.SelectedItemIndex = -1

        self.ScrollX = 0
        self.ListSurface = pygame.Surface
        self.ButtonLeftRectangle = pygame.Rect(0, 0, 32, 32)
        self.ButtonRightRectangle = pygame.Rect(34, 0, 32, 32)
        self.ListSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]), pygame.SRCALPHA)
        self.ListSurfaceUpdated = False
        self.SurfaceOpacity = 255

    def Render(self, DISPLAY):
        if not self.ListSurfaceUpdated:
            self.ListSurfaceUpdated = True
            self.ListSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]), pygame.SRCALPHA)
        self.ListSurface.set_alpha(self.SurfaceOpacity)

        # -- Render the Selected Item text -- #
        sprite.RenderFont(self.ListSurface, "/PressStart2P.ttf", 12, self.SelectedItem, (250, 250, 250), 5, 5)

        for i, itemNam in enumerate(self.GameName):
            ItemWidth = 256
            ItemX = self.ScrollX + ItemWidth * i
            ItemRect = (ItemX, self.Rectangle[3] / 2 - 145 / 2, ItemWidth - 5, 155)

            if self.ItemSelected[i]:
                Draw_Panel(self.ListSurface, (ItemRect[0], ItemRect[1], ItemRect[2], ItemRect[3] + 8), "BORDER")

            if self.SelectedItemIndex == i:
                self.ItemSelected[i] = True
            else:
                self.ItemSelected[i] = False
            # -- Render the Item Sprite -- #

            if self.ItemSelected[i]:
                self.ListSurface.blit(pygame.transform.scale(self.GameBanner[i], (244, 154)), (ItemRect[0] + 3, ItemRect[1] + 5))
            else:
                self.ListSurface.blit(pygame.transform.scale(self.GameBanner[i], (240, 150)), (ItemRect[0] + 4, ItemRect[1] + 9))


        DISPLAY.blit(self.ListSurface, (self.Rectangle[0], self.Rectangle[1]))
        self.ListSurface.fill((0,0,0,0))


    def Update(self, event):
        if event.type == pygame.KEYUP and event.key == pygame.K_q:
            # -- Scroll the Selected Item -- #
            self.SelectedItemIndex -= 1
            sound.PlaySound("/TAIYOU_UI/HUD_Select.wav")

            # -- Limit the Scrolling -- #
            if self.SelectedItemIndex < 0:
                self.SelectedItemIndex = 0
                sound.PlaySound("/TAIYOU_UI/HUD_ListEnd.wav")

        if event.type == pygame.KEYUP and event.key == pygame.K_e:
            # -- Scroll the Selected Item -- #
            self.SelectedItemIndex += 1
            sound.PlaySound("/TAIYOU_UI/HUD_Select.wav")

            # -- Limit the Scrolling -- #
            if self.SelectedItemIndex >= len(self.GameName):
                self.SelectedItemIndex -= 1
                sound.PlaySound("/TAIYOU_UI/HUD_ListEnd.wav")


        # -- Mouse Whell -- #
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.ScrollX += 5
            if event.button == 5:
                self.ScrollX -= 5

        for i, itemNam in enumerate(self.GameName):
            ItemWidth = 256
            ItemX = self.ScrollX + ItemWidth * i
            ItemRect = pygame.Rect(ItemX, self.Rectangle[3] / 2 - 155 / 2, ItemWidth - 5, 155)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 or self.SelectedItemIndex == i and self.ItemSelected[i] == False:
                if ItemRect.collidepoint(pygame.mouse.get_pos()) or self.SelectedItemIndex == i:
                    self.SelectedItem = itemNam
                    self.SelectedGameID = self.GameID[i]
                    self.SelectedGameFolderName = self.GameFolderName[i]
                    self.ItemSelected[i] = True
                    self.SelectedItemIndex = i
                    sound.PlaySound("/TAIYOU_UI/HUD_Select.wav")
                else:
                    self.ItemSelected[i] = False

    def Set_X(self, Value):
        self.Rectangle[0] = float(Value)

    def Set_Y(self, Value):
        self.Rectangle[1] = float(Value)

    def Set_W(self, Value):
        self.Rectangle[2] = float(Value)

    def Set_H(self, Value):
        self.Rectangle[3] = float(Value)

    def AddItem(self, GameDir):
        self.ItemSelected.append(False)

        # -- Read Meta Data File -- #
        LineNumber = -1 # Line 0 == Game Name; Line 1 == Game ID; Line 2 == Game Version; Line 3 == Game Source Folder
        MetaFile = GameDir + "/meta.data"
        with open(MetaFile) as file_in:
            for line in file_in:
                LineNumber += 1

                if LineNumber == 0: # -- Game Name
                    self.GameName.append(line)

                if LineNumber == 1: # -- Game ID
                    self.GameID.append(line)

                if LineNumber == 2: # -- Game Version
                    self.GameVersion.append(line)

                if LineNumber == 3: # -- Game Source Folder
                    self.GameSourceFolder.append(line)

                if LineNumber == 4: # -- Game Folder Name
                    self.GameFolderName.append(line)

        # -- Load the Game Icon -- #
        self.GameBanner.append(pygame.image.load(GameDir + "/icon.png").convert())

        if LineNumber < 3:
            # -- Add Game Icon -- #

            raise NotADirectoryError("The game [" + GameDir + "] is not a valid Taiyou Game.")
