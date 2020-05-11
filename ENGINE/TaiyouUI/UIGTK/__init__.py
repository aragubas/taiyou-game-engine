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
import pygame

PANELS_BACKGROUND_COLOR = (64,78,124)
PANELS_INDICATOR_COLOR = (37,31,72)
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
                                  3, 3, False)

            else:
                # -- Background -- #
                self.BackgroundColor = (15, 27, 44, 100)
                # -- Indicator Bar -- #
                sprite.RenderRectangle(ButtonSurface, (46, 196, 182), (0, 0,self.Rectangle[2],1))

                # -- Text -- #
                sprite.RenderFont(ButtonSurface, "/PressStart2P.ttf", self.TextSize, self.ButtonText, (255, 255, 255),
                                  3, 3, False)
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
        else:
            self.WindowSurface = pygame.Surface((0,0))
        # -- Update Window Surface Destination -- #
        if not self.WindowMinimized:
            self.WindowSurface_Dest = self.WindowRectangle[0], self.WindowRectangle[1] + 20

        # -- Draw the Window Background -- #
        Draw_Panel(DISPLAY, self.WindowRectangle, "BORDER")

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
                              "/PressStart2P.ttf", 18, self.Title) / 2, self.TitleBarRectangle[1] + 1, False)


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