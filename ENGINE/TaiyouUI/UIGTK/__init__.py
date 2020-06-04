#!/usr/bin/python3.7
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
from ENGINE import REGISTRY as reg
from ENGINE import TaiyouUI as mainScript
from ENGINE import SOUND as sound
import ENGINE as tge
import pygame, sys, importlib

PANELS_BACKGROUND_COLOR = (4, 21, 32)
PANELS_INDICATOR_COLOR = (13, 10, 13)
PANELS_INDICATOR_SIZE = 2
BUTTONS_FONT_FILE = "/Ubuntu_Bold.ttf"
WINDOW_TITLE_TEXT_FONT_FILE = "/Ubuntu_Bold.ttf"
HORIZONTAL_LIST_FONT_FILE = "/Ubuntu_Bold.ttf"
INPUT_BOX_FONT_FILE = "/Ubuntu_Bold.ttf"
VERTICALLIST_FONT_FILE = "/Ubuntu_Bold.ttf"

CurrentLanguage = "en"


def SetLang(lang):
    global CurrentLanguage
    global LangErrorAppered
    CurrentLanguage = lang
    LangErrorAppered = False
    print("TaiyouUI.GTK : Language was set to[" + lang + "]")


LangErrorAppered = False


def GetLangText(lang_name, lang_prefix="generic"):
    global CurrentLanguage
    global LangErrorAppered
    try:
        ReturnString = reg.ReadKey("/TaiyouSystem/lang_" + str(CurrentLanguage) + "/" + str(lang_prefix) + "/" + str(lang_name))
        LangErrorAppered = False
        return ReturnString
    except ValueError:
        if not LangErrorAppered:
            print("\n\nTaiyouUI.GTK : The language pack [" + CurrentLanguage + "] contains errors.\nCannot find the translation for: Prefix{" + lang_prefix + "} LangName[" + lang_name + "]\n\n")
            LangErrorAppered = True
        return reg.ReadKey("/TaiyouSystem/lang_" + "en" + "/" + str(lang_prefix) + "/" + str(lang_name))


def Draw_Panel(DISPLAY, Rectangle, IndicatorPosition="UP", Opacity=255):
    ResultPanel = pygame.Surface((Rectangle[2], Rectangle[3]), pygame.SRCALPHA)
    ResultPanel.set_alpha(Opacity)
    ResultPanel.fill(PANELS_BACKGROUND_COLOR)

    if IndicatorPosition == "BORDER":
        pygame.draw.rect(ResultPanel, PANELS_INDICATOR_COLOR, Rectangle, PANELS_INDICATOR_SIZE)

    if IndicatorPosition == "DOWN":
        sprite.RenderRectangle(ResultPanel, PANELS_INDICATOR_COLOR, (0, Rectangle[3] - PANELS_INDICATOR_SIZE, Rectangle[2], PANELS_INDICATOR_SIZE))

    if IndicatorPosition == "UP":
        sprite.RenderRectangle(ResultPanel, PANELS_INDICATOR_COLOR, (0, 0, Rectangle[2], PANELS_INDICATOR_SIZE))

    DISPLAY.blit(ResultPanel, (Rectangle[0], Rectangle[1]))


class Button:
    def __init__(self, Rectangle, ButtonText, TextSize):
        self.Rectangle = Rectangle
        self.ButtonText = ButtonText
        self.TextSize = TextSize
        self.ButtonState = "INATIVE"
        self.IsButtonEnabled = True
        self.WhiteButton = False
        self.Rectangle = pygame.rect.Rect(self.Rectangle[0], self.Rectangle[1], sprite.GetText_width("/PressStart2P.ttf", self.TextSize, self.ButtonText) + 5, sprite.GetText_height("/PressStart2P.ttf", self.TextSize, self.ButtonText) + 6)
        self.CursorSettedToggle = False
        self.ButtonDowed = False
        self.ColisionRectangle = self.Rectangle
        self.CustomColisionRectangle = False
        self.BackgroundColor = (1, 22, 39)
        self.ButtonSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]), pygame.SRCALPHA)
        self.SurfaceUpdated = False
        self.LastRect = pygame.Rect(0, 0, 0, 0)

    def Update(self, event):
        if not self.CustomColisionRectangle:
            self.ColisionRectangle = self.Rectangle
        else:
            self.ColisionRectangle = pygame.Rect(self.ColisionRectangle[0], self.ColisionRectangle[1], self.Rectangle[2], self.Rectangle[3])

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
        pygame.draw.rect(self.ButtonSurface, self.BackgroundColor, (0, 0, self.Rectangle[2], self.Rectangle[3]))

        # -- Update Surface when the size is changed -- #
        if not self.LastRect == self.Rectangle:
            self.SurfaceUpdated = False
            self.LastRect = self.Rectangle

        # -- Update the Surface -- #
        self.Rectangle = pygame.rect.Rect(self.Rectangle[0], self.Rectangle[1], sprite.GetText_width(BUTTONS_FONT_FILE, self.TextSize, self.ButtonText) + 5, sprite.GetText_height(BUTTONS_FONT_FILE, self.TextSize, self.ButtonText) + 6)
        if not self.SurfaceUpdated:
            self.SurfaceUpdated = True
            self.ButtonSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]), pygame.SRCALPHA)

        if not self.WhiteButton:
            if self.ButtonState == "INATIVE":
                self.BackgroundColor = (1, 22, 39, 50)

                # -- Indicator Bar -- #
                sprite.RenderRectangle(self.ButtonSurface, (255, 51, 102), (0, 0, self.Rectangle[2], 1))

                # -- Text -- #
                sprite.RenderFont(self.ButtonSurface, BUTTONS_FONT_FILE, self.TextSize, self.ButtonText, (200, 200, 200), 3, 3)

            else:
                # -- Background -- #
                self.BackgroundColor = (15, 27, 44, 100)
                # -- Indicator Bar -- #
                sprite.RenderRectangle(self.ButtonSurface, (46, 196, 182), (0, 0, self.Rectangle[2], 1))

                # -- Text -- #
                sprite.RenderFont(self.ButtonSurface, BUTTONS_FONT_FILE, self.TextSize, self.ButtonText, (255, 255, 255), 3, 3)
        else:
            if self.ButtonState == "INATIVE":
                # -- Background -- #
                self.BackgroundColor = (1, 22, 39, 50)

                # -- Indicator Bar -- #
                sprite.RenderRectangle(self.ButtonSurface, (255, 51, 102), (0, 0, self.Rectangle[2], 4))

            else:
                # -- Background -- #
                self.BackgroundColor = (15, 27, 44, 100)
                # -- Indicator Bar -- #
                sprite.RenderRectangle(self.ButtonSurface, (46, 196, 182), (0, 0, self.Rectangle[2], 2))

        # -- Draw the Button -- #
        DISPLAY.blit(self.ButtonSurface, (self.Rectangle[0], self.Rectangle[1]))
        if self.ButtonState == "UP":
            self.ButtonState = "INATIVE"
            sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Click"))


class Window:
    def __init__(self, Rectangle, Title, Resiziable):
        self.WindowRectangle = Rectangle
        self.Title = Title
        self.TitleBarRectangle = pygame.Rect(self.WindowRectangle[0], self.WindowRectangle[1], self.WindowRectangle[2], 20)
        self.ResizeRectangle = pygame.Rect(self.WindowRectangle[0] + self.WindowRectangle[3] - 16, self.WindowRectangle[1] + self.WindowRectangle[3] - 16, 16, 16)
        self.Cursor_Position = mainScript.Cursor_Position
        self.Window_IsBeingGrabbed = False
        self.Window_IsBeingResized = False
        self.Window_MinimunW = Rectangle[2]
        self.Window_MinimunH = Rectangle[3]
        self.MinimizeButton = Button(pygame.Rect(self.WindowRectangle[0] + self.WindowRectangle[2] - 20, self.WindowRectangle[1], 16, 20), "↑", 16)
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
            self.TitleBarRectangle = pygame.Rect(self.WindowRectangle[0], self.WindowRectangle[1], self.WindowRectangle[2] - 21, 20)
        else:
            self.TitleBarRectangle = pygame.Rect(self.WindowRectangle[0], self.WindowRectangle[1], self.WindowRectangle[2], 20)
        # -- Resize Button Rectangle -- #
        if self.Resiziable:
            self.ResizeRectangle = pygame.Rect(self.WindowRectangle[0] + self.WindowRectangle[2] - 10, self.WindowRectangle[1] + self.WindowRectangle[3], 10, 10)
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
            sprite.Render(DISPLAY, "/window/resize.png", self.ResizeRectangle[0], self.ResizeRectangle[1], self.ResizeRectangle[2], self.ResizeRectangle[3])

        # -- Render the Minimize Button -- #
        if self.Minimizable:
            self.MinimizeButton.Render(DISPLAY)

        # -- Draw the window title -- #
        sprite.RenderFont(DISPLAY, WINDOW_TITLE_TEXT_FONT_FILE, 18, self.Title, (250, 250, 255), self.TitleBarRectangle[0] + self.TitleBarRectangle[2] / 2 - sprite.GetText_width(WINDOW_TITLE_TEXT_FONT_FILE, 18, self.Title) / 2, self.TitleBarRectangle[1] + 1)

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
                self.MinimizeButton.Set_Text("S")
            else:
                self.MinimizeButton.Set_Text("W")

        # -- Grab Window -- #
        if self.Window_IsBeingGrabbed:
            self.TitleBarRectangle[0] = self.Cursor_Position[0] - self.WindowRectangle[2] / 2
            self.TitleBarRectangle[1] = self.Cursor_Position[1] - self.TitleBarRectangle[3] / 2

        # -- Resize Window -- #
        if self.Window_IsBeingResized and self.Resiziable:  # <- Resize the Window
            # -- Limit Window Size -- #

            if self.WindowRectangle[2] >= self.Window_MinimunW:
                self.WindowRectangle[2] = self.Cursor_Position[0] - self.WindowRectangle[0]
                self.UpdateSurface()

            if self.WindowRectangle[3] >= self.Window_MinimunH:  # <- Resize the Window
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
            self.WindowRectangle = pygame.Rect(self.WindowRectangle[0], self.WindowRectangle[1], self.WindowRectangle[2], 20)
            self.OriginalMinumunHeight = self.Window_MinimunH
            self.Window_MinimunH = 0
            self.OriginalResiziable = self.Resiziable
            self.Resiziable = False


COLOR_INACTIVE = (1, 22, 39)
COLOR_ACTIVE = (15, 27, 44)


class InputBox:
    def __init__(self, x, y, w, h, text='LO'):
        self.rect = pygame.Rect(x, y, w, h)
        self.colisionRect = pygame.Rect(x, y, w, h)
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
                self.width = max(100, sprite.GetText_width(INPUT_BOX_FONT_FILE, 10, self.text) + 10)
            self.rect.w = self.width
            self.rect.h = sprite.GetText_height(INPUT_BOX_FONT_FILE, 10, self.text)
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
            sprite.RenderFont(screen, INPUT_BOX_FONT_FILE, 10, self.text, (140, 140, 140), self.rect[0], self.rect[1])
        else:
            if not self.text == "":
                sprite.RenderFont(screen, INPUT_BOX_FONT_FILE, 10, self.text, (240, 240, 240), self.rect[0], self.rect[1])

        if not self.active:
            sprite.RenderRectangle(screen, (255, 51, 102), (self.rect[0], self.rect[1] - 1, self.rect[2], 1))
        else:
            sprite.RenderRectangle(screen, (46, 196, 182), (self.rect[0], self.rect[1] - 1, self.rect[2], 1))


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
        self.GameFolderInfos = list()
        self.ItemApperAnimationEnabled = list()
        self.ItemApperAnimationNumb = list()
        self.ItemApperAnimationMode = list()
        self.ItemApperAnimationToggle = list()
        self.ItemSurface = list()
        self.GameBannerAnimation = list()
        self.GameBannerAnimationAmount = list()
        self.ItemSelectedCurrentFrame = list()
        self.ItemSelectedCurrentFrameUpdateDelay = list()
        self.GameBannerAnimationFrameDelay = list()

        self.ItemSelected = list()
        self.SelectedItem = GetLangText("horizontal_items_view_default_text", "gtk")
        self.SelectedGameID = ""
        self.SelectedGameVersion = ""
        self.SelectedGameFolderName = ""
        self.SelectedItemIndex = -1
        self.SelectedGameFolderInfos = None
        self.SelectedGameIcon = sprite.DefaultSprite

        self.ScrollX = 0
        self.ScrollSpeed = 0
        self.ListSurface = pygame.Surface
        self.ButtonLeftRectangle = pygame.Rect(0, 0, 32, 32)
        self.ButtonRightRectangle = pygame.Rect(34, 0, 32, 32)
        self.ListSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]), pygame.SRCALPHA)
        self.ListSurfaceUpdated = False
        self.SurfaceOpacity = 255
        self.ScrollSlowdown = 0
        self.ScrollSlowdownEnabled = False

    def Render(self, DISPLAY):
        if not self.ListSurfaceUpdated:
            self.ListSurfaceUpdated = True
            self.ListSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]), pygame.SRCALPHA)
        self.ListSurface.set_alpha(self.SurfaceOpacity)

        # -- Render the Selected Item text -- #
        sprite.RenderFont(self.ListSurface, HORIZONTAL_LIST_FONT_FILE, 24, self.SelectedItem, (250, 250, 250), 3, 3)

        for i, itemNam in enumerate(self.GameName):
            if self.SelectedItemIndex == i:
                self.ItemSelected[i] = True
            else:
                self.ItemSelected[i] = False

            ItemRect = pygame.Rect((self.ScrollX + 256 * i), 30, 256 - 5, 165)
            ItemSurface = pygame.Surface((ItemRect[2], ItemRect[3]), pygame.SRCALPHA)

            AnimationSpeed = 15
            if not self.ItemSelected[i]:
                OpctMax = 150
                self.ItemApperAnimationEnabled[i] = True
                self.ItemApperAnimationMode[i] = 0
                self.ItemApperAnimationToggle[i] = False
            else:
                OpctMax = 255
                if not self.ItemApperAnimationToggle[i]:
                    self.ItemApperAnimationEnabled[i] = True
                    self.ItemApperAnimationMode[i] = 0
                    self.ItemApperAnimationToggle[i] = True

            # -- Run the Animation -- #
            if self.ItemApperAnimationEnabled[i]:
                if self.ItemApperAnimationMode[i] == 0:
                    self.ItemApperAnimationNumb[i] += AnimationSpeed

                    if self.ItemApperAnimationNumb[i] >= OpctMax:
                        self.ItemApperAnimationNumb[i] = OpctMax
                        self.ItemApperAnimationEnabled[i] = False
                        self.ItemApperAnimationMode[i] = 1

                if self.ItemApperAnimationMode[i] == 1:
                    self.ItemApperAnimationNumb[i] -= AnimationSpeed

                    if self.ItemApperAnimationNumb[i] <= 0:
                        self.ItemApperAnimationNumb[i] = 0
                        self.ItemApperAnimationEnabled[i] = False
                        self.ItemApperAnimationMode[i] = 0

            ItemSurface.set_alpha(self.ItemApperAnimationNumb[i])

            # -- Render the Item Sprite -- #
            if self.ItemSelected[i]:
                if self.ItemSelected[i]:
                    Draw_Panel(ItemSurface, (PANELS_INDICATOR_SIZE, PANELS_INDICATOR_SIZE, ItemRect[2] - PANELS_INDICATOR_SIZE * 2, ItemRect[3] - PANELS_INDICATOR_SIZE * 2), "BORDER")

                self.ItemSelectedCurrentFrameUpdateDelay[i] += 1

                if self.ItemSelectedCurrentFrameUpdateDelay[i] >= self.GameBannerAnimationFrameDelay[i]:
                    self.ItemSelectedCurrentFrame[i] += 1
                    if self.ItemSelectedCurrentFrame[i] >= self.GameBannerAnimationAmount[i]:
                        self.ItemSelectedCurrentFrame[i] = 0

                    self.ItemSelectedCurrentFrameUpdateDelay[i] = 0

                ItemSurface.blit(pygame.transform.scale(self.GameBannerAnimation[i][self.ItemSelectedCurrentFrame[i]], (244, 154)), (3, 5))

                # -- Scroll the List -- #
                if ItemRect[0] + ItemRect[2] * 2 > self.ListSurface.get_width():
                    self.ScrollX -= ItemRect[2] / 32 + self.ScrollSpeed

                if ItemRect[0] - ItemRect[2] + 3 < 0:
                    self.ScrollX += ItemRect[2] / 32 + self.ScrollSpeed

            else:
                self.ItemSelectedCurrentFrame[i] = 0
                ItemSurface.blit(pygame.transform.scale(self.GameBanner[i], (240, 150)), (4, 9))

            self.ListSurface.blit(ItemSurface, (ItemRect[0], ItemRect[1]))

        DISPLAY.blit(self.ListSurface, (self.Rectangle[0], self.Rectangle[1]))
        self.ListSurface.fill((0, 0, 0, 0))

        if self.ScrollSlowdownEnabled:
            self.ScrollSlowdown += 1

            if self.ScrollSlowdown > 10:
                self.ScrollSlowdown = 0
                self.ScrollSlowdownEnabled = False


    def ClearItems(self):
        self.GameName.clear()
        self.GameID.clear()
        self.GameVersion.clear()
        self.GameSourceFolder.clear()
        self.GameBanner.clear()
        self.GameFolderName.clear()
        self.GameBannerAnimation.clear()
        self.GameBannerAnimationAmount.clear()
        self.ItemApperAnimationEnabled.clear()
        self.ItemApperAnimationNumb.clear()
        self.ItemApperAnimationMode.clear()
        self.ItemApperAnimationToggle.clear()
        self.GameBannerAnimation.clear()
        self.GameBannerAnimationAmount.clear()
        self.GameBannerAnimationFrameDelay.clear()
        self.ItemSelected.clear()

        self.SelectedItem = GetLangText("horizontal_items_view_default_text", "gtk")
        self.SelectedGameID = ""
        self.SelectedGameFolderName = ""
        self.SelectedItemIndex = -1
        self.SelectedGameFolderInfos = None
        self.SelectedGameIcon = sprite.DefaultSprite

        self.ScrollX = 0

    def ScrollIndexUp(self):
        # -- Scroll the Selected Item -- #
        self.SelectedItemIndex += 1

        # -- Limit the Scrolling -- #
        if self.SelectedItemIndex >= len(self.GameName):
            self.SelectedItemIndex -= 1
            sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/ListEnd"))

        else:
            sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Select"))

        self.ScrollSlowdownEnabled = True

    def ScrollIndexDown(self):
        # -- Scroll the Selected Item -- #
        self.SelectedItemIndex -= 1

        # -- Limit the Scrolling -- #
        if self.SelectedItemIndex < 0:
            self.SelectedItemIndex = 0
            sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/ListEnd"))

        else:
            sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Select"))

        self.ScrollSlowdownEnabled = True

    def Update(self, event):
        if not self.ScrollSlowdownEnabled:
            if event.type == pygame.KEYUP and event.key == pygame.K_q:
                self.ScrollIndexDown()

            if event.type == pygame.KEYUP and event.key == pygame.K_e:
                self.ScrollIndexUp()

            if event.type == pygame.KEYUP and event.key == pygame.K_HOME:
                self.SelectedItemIndex = len(self.GameName) - 1
                self.ScrollX = self.SelectedItemIndex / 1.02
                sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/ListEnd"))

            if event.type == pygame.KEYUP and event.key == pygame.K_END:
                self.ScrollX = 256
                self.SelectedItemIndex = 0
                sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/ListEnd"))

            # -- Mouse Whell -- #
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.ScrollIndexUp()
                if event.button == 5:
                    self.ScrollIndexDown()

        for i, itemNam in enumerate(self.GameName):
            ItemRect = pygame.Rect((self.ScrollX + 256 * i), 30, 256 - 5, 205)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and ItemRect.collidepoint(pygame.mouse.get_pos()):
                if not self.SelectedItemIndex == i:
                    sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Select"))
                    self.SelectedItemIndex = i

            if self.SelectedItemIndex == i:
                self.SelectedGameFolderInfos = self.GameFolderInfos[i]
                self.SelectedItem = itemNam
                self.SelectedGameID = self.GameID[i]
                self.SelectedGameFolderName = self.GameFolderName[i]
                self.ItemSelected[i] = True
                self.SelectedItemIndex = i
                self.SelectedGameVersion = self.GameVersion[i]
                self.SelectedGameID = self.GameID[i]
                self.SelectedGameIcon = self.GameBanner[i]
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
        LineNumber = -1  # Line 0 == Game Name; Line 1 == Game ID; Line 2 == Game Version; Line 3 == Game Source Folder
        GameBannerAnimAmountFrames = 0
        MetaFile = GameDir + "/meta.data"
        FolderName = ""
        with open(MetaFile) as file_in:
            for line in file_in:
                if not line == "":
                    LineNumber += 1

                    if LineNumber == 0:  # -- Game Name
                        self.GameName.append(line)

                    if LineNumber == 1:  # -- Game ID
                        self.GameID.append(line)

                    if LineNumber == 2:  # -- Game Version
                        self.GameVersion.append(line)

                    if LineNumber == 3:  # -- Game Source Folder
                        self.GameSourceFolder.append(line)

                    if LineNumber == 4:  # -- Game Folder Name
                        self.GameFolderName.append(line)
                        FolderName = line.rstrip()

                    if LineNumber == 5:  # -- Animation Banner Frames
                        self.GameBannerAnimationAmount.append(int(line))
                        GameBannerAnimAmountFrames = int(line)

                    if LineNumber == 6:  # -- Animation Banner Frames Delay
                        self.GameBannerAnimationFrameDelay.append(int(line))

        # -- Load the Game Icon and Banner Animation -- #
        self.GameBanner.append(pygame.image.load(GameDir + "/icon.png").convert())
        self.ItemApperAnimationEnabled.append(True)
        self.ItemApperAnimationNumb.append(0)
        self.ItemApperAnimationMode.append(0)
        self.ItemSelectedCurrentFrame.append(0)
        self.ItemApperAnimationToggle.append(False)
        self.ItemSelectedCurrentFrameUpdateDelay.append(0)

        # - Load Folder Metadata -- #
        GameFolderInfos = list()

        GameFolderInfos.append(tge.utils.FormatNumber(tge.utils.Calculate_FolderSize(FolderName), 2, ['B', 'Kb', 'MB', 'GB', 'TB']))
        GameFolderInfos.append(tge.utils.Get_DirectoryTotalOfFiles(FolderName))

        self.GameFolderInfos.append(GameFolderInfos)

        AnimationFrames = list()
        for frame in range(0, GameBannerAnimAmountFrames):
            FiltredGameDir = GameDir.replace("./", "")
            path = FiltredGameDir + "/SELETOR/" + str(frame) + ".png"

            print("Frame : [" + path + "]")
            AnimationFrames.append(pygame.image.load(path).convert())

        self.GameBannerAnimation.append(AnimationFrames)

        if LineNumber < 6 or LineNumber > 8: # -- Detect if the Game Folder is invalid
            raise NotADirectoryError("The game [" + GameDir + "] is not a valid Taiyou Game.\nThis metadata file contains: " + str(LineNumber) + " lines.")


class VerticalListWithDescription:
    def __init__(self, Rectangle):
        self.Rectangle = Rectangle
        self.ItemsName = list()
        self.ItemsDescription = list()
        self.ItemSprite = list()
        self.ItemSelected = list()
        self.LastItemClicked = "null"
        self.SelectedItemIndex = -1
        self.ScrollY = 0
        self.ListSurface = pygame.Surface((Rectangle[2], Rectangle[3]))
        self.ClickedItem = ""
        self.ColisionXOffset = 0
        self.ColisionYOffset = 0
        self.ButtonUpRectangle = pygame.Rect(0, 0, 32, 32)
        self.ButtonDownRectangle = pygame.Rect(34, 0, 32, 32)
        self.Cursor_Position = mainScript.Cursor_Position
        self.ListSurfaceUpdated = False

    def Render(self, DISPLAY):
        if not self.ListSurfaceUpdated:
            self.ListSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]), pygame.SRCALPHA)
            self.ListSurfaceUpdated = True

        self.ListSurface.fill((0,0,0,0))
        for i, itemNam in enumerate(self.ItemsName):
            ItemRect = (0, self.ScrollY + 42 * i, self.Rectangle[2], 40)

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
                    sprite.RenderRectangle(self.ListSurface, (32, 164, 243), (ItemRect[0], ItemRect[1], ItemRect[2], 1))

            else:
                # -- Background -- #
                sprite.RenderRectangle(self.ListSurface, (30, 52, 69, 150), ItemRect)
                # -- Indicator Bar -- #
                sprite.RenderRectangle(self.ListSurface, (255, 51, 102), (ItemRect[0], ItemRect[1], ItemRect[2], 1))

            # -- Render the Item Name and Description -- #
            sprite.RenderFont(self.ListSurface, VERTICALLIST_FONT_FILE, 18, itemNam, (250, 250, 250), ItemRect[0] + 5, ItemRect[1] + 5, reg.ReadKey_bool("TaiyouSystem/CONF/font_aa"))
            sprite.RenderFont(self.ListSurface, VERTICALLIST_FONT_FILE, 12, self.ItemsDescription[i], (250, 250, 250), ItemRect[0] + 3, ItemRect[1] + 28, reg.ReadKey_bool("TaiyouSystem/CONF/font_aa"))

        DISPLAY.blit(self.ListSurface, (self.Rectangle[0], self.Rectangle[1]))

        # -- Keyup List Scrolling -- #
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_a]:
            self.ScrollY += 1

        if pressed[pygame.K_d]:
            self.ScrollY -= 1

    def Update(self, event):
        self.Cursor_Position = mainScript.Cursor_Position

        # -- Select the Clicked Item -- #
        for i, itemNam in enumerate(self.ItemsName):
            ItemRect = pygame.Rect(self.ColisionXOffset + self.Rectangle[0], self.ColisionYOffset + self.ScrollY + self.Rectangle[1] + 42 * i, self.Rectangle[2], 40)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if ItemRect.collidepoint(self.Cursor_Position):
                    self.LastItemClicked = itemNam
                    self.ItemSelected[i] = True
                    self.SelectedItemIndex = i
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

    def AddItem(self, ItemName, ItemDescription, ItemSprite="null"):
        self.ItemsName.append(ItemName)
        self.ItemsDescription.append(ItemDescription)
        self.ItemSprite.append(ItemSprite)
        self.ItemSelected.append(False)


class LoadingSquare:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.FramesPrefix = "/FRAMES/loading/"
        self.CurrentFrame = 1
        self.UpdateAnimDelay = 0
        self.Opacity = 255
        self.OpacityAddMode = 0

    def Update(self):
        # -- Do the Aniamtion Loop -- #
        self.UpdateAnimDelay += 1
        if self.UpdateAnimDelay >= 2:
            self.CurrentFrame += 1

            if self.CurrentFrame >= 39:
                self.CurrentFrame = 1

            self.UpdateAnimDelay = 0

    def Set_X(self, NewValue):
        self.X = NewValue

    def Set_Y(self, NewValue):
        self.Y = NewValue


    def Render(self, DISPLAY):
        AnimSurface = pygame.Surface((32, 32), pygame.SRCALPHA)
        AnimSurface.set_alpha(self.Opacity)

        sprite.Render(AnimSurface, self.FramesPrefix + str(self.CurrentFrame) + ".png", 0, 0, 32, 32)

        DISPLAY.blit(AnimSurface, (self.X, self.Y))