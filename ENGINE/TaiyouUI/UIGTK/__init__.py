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
from ENGINE import UTILS as utils
from ENGINE import DEBUGGING as debug

import ENGINE as tge
import pygame, sys, importlib

# -- Panels Color -- #
Panels_BackgroundColor = (0, 12, 29)
Panels_IndicatorColor = (1, 22, 39)

# -- Slider Colors -- #
Slider_BackgroundColor = (1, 12, 29)
Slider_Borders_Color = (15, 30, 52)
Slider_Progress_Background = (100, 101, 103)
Slider_Progress_Percentage = (255, 51, 102)
Slider_Progress_Notch = (200, 200, 200)

# -- Buttons Color -- #
Button_Active_IndicatorColor = (46, 196, 182)
Button_Active_BackgroundColor = (15, 27, 44, 150)
Button_Inactive_IndicatorColor = (255, 51, 102)
Button_Inactive_BackgroundColor = (1, 22, 39, 150)
Button_BackgroundColor = (12, 22, 14)
Button_BorderRadius = 5

InputBox_ActiveColor = (1, 22, 39)
InputBox_DeactiveColor = (15, 27, 44)


# -- Panels Size -- #
Panels_Indicator_Size = 2

# -- GameSeletor Colors -- #
GameSeletor_BackgroundColor = (0, 2, 27)

# -- Font Files -- #
Button_FontFile = "/Ubuntu_Bold.ttf"
Window_Title_FontFile = "/Ubuntu_Bold.ttf"
ApplicationListList_FontFile = "/Ubuntu.ttf"
InputBox_FontFile = "/Ubuntu_Bold.ttf"
VerticalList_FontFile = "/Ubuntu_Bold.ttf"

# -- Language System -- #
CurrentLanguage = "en"
LangErrorAppered = False


def SetLang(lang):
    global CurrentLanguage
    global LangErrorAppered
    CurrentLanguage = lang
    LangErrorAppered = False
    print("TaiyouUI.GTK : Language was set to[" + lang + "]")

def GetLangText(lang_name, lang_prefix="generic"):
    global CurrentLanguage
    global LangErrorAppered
    try:
        ReturnString = reg.ReadKey("/TaiyouSystem/lang_" + str(CurrentLanguage) + "/" + str(lang_prefix) + "/" + str(lang_name), True)
        LangErrorAppered = False
        return ReturnString

    except ValueError:
        if not LangErrorAppered:
            print("\n\nTaiyou.GetLangText : The language pack [" + CurrentLanguage + "] contains errors.\nCannot find the translation for: Prefix{" + lang_prefix + "} LangName[" + lang_name + "]\n\n")
            LangErrorAppered = True

        return reg.ReadKey("/TaiyouSystem/lang_" + "en" + "/" + str(lang_prefix) + "/" + str(lang_name), True)

    except Exception as ex:
        print("Taiyou.GetLangText : An error occured while processing the request.\nRequest: Name[" + lang_name + "] Prefix[" + lang_prefix + "].")

        raise ex


def Draw_Panel(DISPLAY, Rectangle, IndicatorPosition="UP", Opacity=255):
    ResultPanel = pygame.Surface((Rectangle[2], Rectangle[3]))
    if not Opacity == 255:
        ResultPanel.set_alpha(Opacity)

    # -- Render the Background -- #
    sprite.Shape_Rectangle(ResultPanel, Panels_BackgroundColor, (0, 0, Rectangle[2], Rectangle[3]))

    if IndicatorPosition == "BORDER":
        sprite.Shape_Rectangle(ResultPanel, Panels_IndicatorColor, (0, Rectangle[3] - Panels_Indicator_Size, Rectangle[2], Panels_Indicator_Size))

    if IndicatorPosition == "DOWN":
        sprite.Shape_Rectangle(ResultPanel, Panels_IndicatorColor, (0, Rectangle[3] - Panels_Indicator_Size, Rectangle[2], Panels_Indicator_Size))

    if IndicatorPosition == "UP":
        sprite.Shape_Rectangle(ResultPanel, Panels_IndicatorColor, (0, 0, Rectangle[2], Panels_Indicator_Size))

    DISPLAY.blit(ResultPanel, (Rectangle[0], Rectangle[1]))
    del ResultPanel

class Button:
    def __init__(self, Rectangle, ButtonText, TextSize):
        self.Rectangle = Rectangle
        self.ButtonText = ButtonText
        self.TextSize = TextSize
        self.ButtonState = 0 # 0 - INACTIVE, 1 - DOWN, 2 - UP
        self.FontFile = Button_FontFile
        self.IsButtonEnabled = True
        self.Rectangle = pygame.rect.Rect(self.Rectangle[0], self.Rectangle[1], sprite.GetFont_width(self.FontFile, self.TextSize, self.ButtonText) + 5, sprite.GetFont_height(self.FontFile, self.TextSize, self.ButtonText) + 6)
        self.LastRect = self.Rectangle
        self.CursorSettedToggle = False
        self.ButtonDowed = False
        self.ColisionRectangle = self.Rectangle
        self.CustomColisionRectangle = False
        self.BackgroundColor = Button_BackgroundColor
        self.SurfaceUpdated = False
        self.LastRect = pygame.Rect(0, 0, 0, 0)
        self.Surface = pygame.Surface((Rectangle[2], Rectangle[3]))

    def Update(self, event):
        # -- Set the Custom Colision Rectangle -- #
        if not self.CustomColisionRectangle:
            self.ColisionRectangle = self.Rectangle
        else:
            self.ColisionRectangle = pygame.Rect(self.ColisionRectangle[0], self.ColisionRectangle[1], self.Rectangle[2], self.Rectangle[3])

        if self.IsButtonEnabled:  # -- Only update the button, when is enabled.
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Set the button to the DOWN state
                if self.ColisionRectangle.collidepoint(mainScript.Cursor_Position):
                    self.ButtonState = 1
                    self.ButtonDowed = True

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Set the button to the UP state
                if self.ButtonDowed:
                    self.ButtonState = 2
                    self.ButtonDowed = False

            if event.type == pygame.MOUSEMOTION:  # Change the Cursor
                if self.ColisionRectangle.collidepoint(mainScript.Cursor_Position):
                    self.CursorSettedToggle = True
                    mainScript.Cursor_CurrentLevel = 3
                else:
                    if self.CursorSettedToggle:
                        self.CursorSettedToggle = False
                        mainScript.Cursor_CurrentLevel = 0
                        self.ButtonState = 0

        else:
            self.ButtonState = 0
            if self.CursorSettedToggle:
                self.CursorSettedToggle = False
                mainScript.Cursor_CurrentLevel = 0

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
        # -- Update the Surface -- #
        self.Rectangle = pygame.rect.Rect(self.Rectangle[0], self.Rectangle[1], sprite.GetFont_width(self.FontFile, self.TextSize, self.ButtonText) + 5, sprite.GetFont_height(self.FontFile, self.TextSize, self.ButtonText) + 6)

        # -- Update the Rect Wheen Needed -- #
        if self.Rectangle == self.LastRect:
            self.Surface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]))

        # -- Update Surface when the size is changed -- #
        if not self.LastRect == self.Rectangle:
            self.SurfaceUpdated = False
            self.LastRect = self.Rectangle

        # -- Set the Button Colors -- #
        IndicatorColor = (0, 0, 0)

        if self.ButtonState == 0:
            IndicatorColor = Button_Inactive_IndicatorColor
            self.BackgroundColor = Button_Inactive_BackgroundColor

        elif self.ButtonState == 1:
            IndicatorColor = Button_Active_IndicatorColor
            self.BackgroundColor = Button_Active_BackgroundColor

        # -- Render Background -- #
        self.Surface.fill(self.BackgroundColor)

        # -- Indicator Bar -- #
        sprite.Shape_Rectangle(self.Surface, IndicatorColor, (0, 0, self.Rectangle[2], 2), 0, 0, Button_BorderRadius, Button_BorderRadius)

        # -- Text -- #
        sprite.FontRender(self.Surface, self.FontFile, self.TextSize, self.ButtonText, (200, 200, 200), 3, 3)

        # -- Draw the Button -- #
        DISPLAY.blit(self.Surface, (self.Rectangle[0], self.Rectangle[1]))

        if self.ButtonState == 2:
            self.ButtonState = 0
            sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Click", True), 0.5, PlayOnSystemChannel=True)

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
        self.MinimizeButton.FontFile = "/PressStart2P.ttf"
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
        Draw_Panel(DISPLAY, WindowBorderRectangle, "DISABLED")

        pygame.draw.line(DISPLAY, IndicatorLineColor, (self.TitleBarRectangle[0], self.TitleBarRectangle[1] - 2 + self.TitleBarRectangle[3]), (self.TitleBarRectangle[0] + self.TitleBarRectangle[2], self.TitleBarRectangle[1] - 2 + self.TitleBarRectangle[3]), 2)

        # -- Draw the Resize Block -- #
        if self.Resiziable:
            sprite.ImageRender(DISPLAY, "/TAIYOU_UI/ICONS/resize.png", self.ResizeRectangle[0], self.ResizeRectangle[1], self.ResizeRectangle[2], self.ResizeRectangle[3])

        # -- Render the Minimize Button -- #
        if self.Minimizable:
            self.MinimizeButton.Render(DISPLAY)

        # -- Draw the window title -- #
        TextX = self.TitleBarRectangle[0] + self.TitleBarRectangle[2] / 2 - sprite.GetFont_width(Window_Title_FontFile, 18, self.Title) / 2
        sprite.FontRender(DISPLAY, Window_Title_FontFile, 18, self.Title, (250, 250, 255), TextX, self.TitleBarRectangle[1] - 2, reg.ReadKey_bool("/TaiyouSystem/CONF/font_aa", True))

    def EventUpdate(self, event):
        self.Cursor_Position = mainScript.Cursor_Position

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.TitleBarRectangle.collidepoint(self.Cursor_Position):
                self.Window_IsBeingGrabbed = True
                mainScript.Cursor_CurrentLevel = 2
            if self.ResizeRectangle.collidepoint(self.Cursor_Position) and self.Resiziable:
                self.Window_IsBeingResized = True
                mainScript.Cursor_CurrentLevel = 1
        # -------------------------------------------------------------------
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.Window_IsBeingResized:
                self.Window_IsBeingResized = False
                mainScript.Cursor_CurrentLevel = 0
            if self.Window_IsBeingGrabbed:
                self.Window_IsBeingGrabbed = False
                mainScript.Cursor_CurrentLevel = 0
        # -- Minimize Button Update -- #
        if self.Minimizable:
            self.MinimizeButton.Update(event)
            if self.MinimizeButton .ButtonState == 2:
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
        if not self.WindowRectangle[2] < self.Window_MinimunW and not self.WindowRectangle[3] < self.Window_MinimunH:
            self.WindowSurface = pygame.Surface((self.WindowRectangle[2], self.WindowRectangle[3] - 20), pygame.SRCALPHA)

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


class InputBox:
    def __init__(self, x, y, w, h, text='LO', FontSize=12):
        self.rect = pygame.Rect(x, y, w, h)
        self.colisionRect = pygame.Rect(x, y, w, h)
        self.CustomColision = False
        self.color = InputBox_DeactiveColor
        self.text = text
        self.active = False
        self.DefaultText = text
        self.LastHeight = 1
        self.CustomWidth = False
        self.width = 1
        self.FontSize = FontSize
        self.CharacterLimit = 0

    def Set_X(self, Value):
        if not self.rect[0] == Value:
            self.rect = pygame.Rect(Value, self.rect[1], self.rect[2], self.rect[3])

    def Set_Y(self, Value):
        if not self.rect[1] == Value:
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
            self.color = InputBox_ActiveColor if self.active else InputBox_DeactiveColor
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    if len(self.text) > 0:
                        self.text = self.text[:-1]
                    else:
                        self.text = self.DefaultText

                else:
                    if not self.CharacterLimit == 0:
                        if len(self.text) < self.CharacterLimit:
                            self.text += event.unicode
                    else:
                        self.text += event.unicode

    def Render(self, screen):
        # -- Resize the Textbox -- #
        try:
            if not self.CustomWidth:
                self.width = max(100, sprite.GetFont_width(InputBox_FontFile, self.FontSize, self.text) + 10)
            self.rect.w = self.width
            self.rect.h = sprite.GetFont_height(InputBox_FontFile, self.FontSize, self.text)
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
            sprite.FontRender(screen, InputBox_FontFile, self.FontSize, self.text, (140, 140, 140), self.rect[0], self.rect[1])
        else:
            if not self.text == "":
                sprite.FontRender(screen, InputBox_FontFile, self.FontSize, self.text, (240, 240, 240), self.rect[0], self.rect[1])

        if not self.active:
            sprite.Shape_Rectangle(screen, (255, 51, 102), (self.rect[0], self.rect[1] - 1, self.rect[2], 1))
        else:
            sprite.Shape_Rectangle(screen, (46, 196, 182), (self.rect[0], self.rect[1] - 1, self.rect[2], 1))


class InstalledApplicationList:
    def __init__(self, Rectangle):
        self.Rectangle = Rectangle
        self.SetObjects()

    def Render(self, DISPLAY):
        Surface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]), pygame.SRCALPHA)
        Surface.set_alpha(self.SurfaceOpacity)

        # -- Render the Selected Item text -- #
        sprite.FontRender(Surface, ApplicationListList_FontFile, 24, self.SelectedItem, (250, 250, 250), 3, 1)

        for i, itemNam in enumerate(self.ApplicationName):
            if self.SelectedItemIndex == i:
                self.ItemSelected[i] = True
            else:
                self.ItemSelected[i] = False

            ItemRect = pygame.Rect((self.ScrollX + 245 * i), 30, 240, 150)
            ItemSurface = pygame.Surface((ItemRect[2], ItemRect[3]))

            AnimationSpeed = 15
            if not self.ItemSelected[i]:
                OpctMax = 30
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

            # -- Set Surface Alpha -- #
            ItemSurface.set_alpha(self.ItemApperAnimationNumb[i])

            if self.ItemSelected[i]:  # -- Update Item Animation, only when Selected -- #
                self.ItemSelectedCurrentFrameUpdateDelay[i] += 1

                if self.ItemSelectedCurrentFrameUpdateDelay[i] >= self.ApplicationBannerAnimationFrameDelay[i]:
                    self.ItemSelectedCurrentFrame[i] += 1
                    if self.ItemSelectedCurrentFrame[i] >= self.ApplicationBannerAnimationAmount[i]:
                        self.ItemSelectedCurrentFrame[i] = 0

                    self.ItemSelectedCurrentFrameUpdateDelay[i] = 0

                ItemSurface.blit(self.ApplicationBannerAnimation[i][self.ItemSelectedCurrentFrame[i]], (0, 0))

                # -- Scroll the List -- #
                if self.ScrollEnabled:
                    if ItemRect[0] + ItemRect[2] * 2 > Surface.get_width() - self.ScrollMultiplier and self.ScrollMode == 1 and self.ScrollEnabled:
                        self.ScrollMode = 0
                        self.ScrollMultiplier = 1.5
                        self.ScrollEnabled = False

                    if ItemRect[0] - ItemRect[2] < -self.ScrollMultiplier and self.ScrollMode == 0 and self.ScrollEnabled:
                        self.ScrollMode = 0
                        self.ScrollMultiplier = 1.5
                        self.ScrollEnabled = False

                    if self.ScrollMode == 0 and self.ScrollEnabled:
                        self.ScrollMultiplier += 1.5
                        self.ScrollX -= self.ScrollMultiplier

                    elif self.ScrollMode == 1 and self.ScrollEnabled:
                        self.ScrollMultiplier += 1.5
                        self.ScrollX += self.ScrollMultiplier

            else:  # -- Draw the Game Icon only -- #
                self.ItemSelectedCurrentFrame[i] = 0
                ItemSurface.blit(self.ApplicationBanner[i], (0, 0))

            # -- Render the Item to the Surface -- #
            Surface.blit(ItemSurface, (ItemRect[0], ItemRect[1]))

        DISPLAY.blit(Surface, (self.Rectangle[0], self.Rectangle[1]))

        if self.ScrollSlowdownEnabled:
            self.ScrollSlowdown += 1

            if self.ScrollSlowdown > 10:
                self.ScrollSlowdown = 0
                self.ScrollSlowdownEnabled = False

    def ClearItems(self):
        utils.GarbageCollector_Collect()

        # -- Selected item Vars -- #
        del self.ApplicationName
        del self.ApplicationID
        del self.ApplicationVersion
        del self.ApplicationSourceFolder
        del self.ApplicationBanner
        del self.ApplicationFolderName
        del self.ApplicationFolderInfos
        del self.ItemApperAnimationEnabled
        del self.ItemApperAnimationNumb
        del self.ItemApperAnimationMode
        del self.ItemApperAnimationToggle
        del self.ItemSurface
        del self.ApplicationBannerAnimation
        del self.ApplicationBannerAnimationAmount
        del self.ItemSelectedCurrentFrame
        del self.ItemSelectedCurrentFrameUpdateDelay
        del self.ApplicationBannerAnimationFrameDelay
        utils.GarbageCollector_Collect()

        del self.ItemSelected
        del self.SelectedItem
        del self.SelectedApplicationID
        del self.SelectedApplicationVersion
        del self.SelectedApplicationFolderName
        del self.SelectedItemIndex
        del self.SelectedApplicationFolderInfos
        del self.SelectedApplicationIcon
        utils.GarbageCollector_Collect()

        del self.ScrollX
        del self.ScrollMode
        del self.ScrollEnabled
        del self.ScrollMultiplier
        utils.GarbageCollector_Collect()

        del self.ButtonLeftRectangle
        del self.ButtonRightRectangle
        del self.SurfaceOpacity
        del self.ScrollSlowdown
        del self.ScrollSlowdownEnabled
        utils.GarbageCollector_Collect()

        self.SetObjects()

    def SetObjects(self):
        utils.GarbageCollector_Collect()

        # -- Selected item Vars -- #
        self.ApplicationName = list()
        self.ApplicationID = list()
        self.ApplicationVersion = list()
        self.ApplicationSourceFolder = list()
        self.ApplicationBanner = list()
        self.ApplicationFolderName = list()
        self.ApplicationFolderInfos = list()
        self.ItemApperAnimationEnabled = list()
        self.ItemApperAnimationNumb = list()
        self.ItemApperAnimationMode = list()
        self.ItemApperAnimationToggle = list()
        self.ItemSurface = list()
        self.ApplicationBannerAnimation = list()
        self.ApplicationBannerAnimationAmount = list()
        self.ItemSelectedCurrentFrame = list()
        self.ItemSelectedCurrentFrameUpdateDelay = list()
        self.ApplicationBannerAnimationFrameDelay = list()
        utils.GarbageCollector_Collect()

        self.ItemSelected = list()
        self.SelectedItem = GetLangText("horizontal_items_view_default_text", "gtk")
        self.SelectedApplicationID = ""
        self.SelectedApplicationVersion = ""
        self.SelectedApplicationFolderName = ""
        self.SelectedItemIndex = -1
        self.SelectedApplicationFolderInfos = None
        self.SelectedApplicationIcon = sprite.DefaultSprite
        utils.GarbageCollector_Collect()

        self.ScrollX = 0
        self.ScrollMode = 0
        self.ScrollEnabled = False
        self.ScrollMultiplier = 1
        utils.GarbageCollector_Collect()

        self.ButtonLeftRectangle = pygame.Rect(0, 0, 32, 32)
        self.ButtonRightRectangle = pygame.Rect(34, 0, 32, 32)
        self.SurfaceOpacity = 255
        self.ScrollSlowdown = 0
        self.ScrollSlowdownEnabled = False
        utils.GarbageCollector_Collect()

    def ScrollIndexUp(self):
        # -- Scroll the Selected Item -- #
        self.SelectedItemIndex += 1

        # -- Limit the Scrolling -- #
        if self.SelectedItemIndex >= len(self.ApplicationName):
            self.SelectedItemIndex -= 1
            sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/ListEnd", True), PlayOnSystemChannel=True)

        else:
            sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Select", True), PlayOnSystemChannel=True)

        self.ScrollSlowdownEnabled = True

        self.ScrollEnabled = True
        self.ScrollMode = 0
        self.ScrollMultiplier = 1.5

    def ScrollIndexDown(self):
        # -- Scroll the Selected Item -- #
        self.SelectedItemIndex -= 1

        # -- Limit the Scrolling -- #
        if self.SelectedItemIndex < 0:
            self.SelectedItemIndex = 0
            sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/ListEnd", True), PlayOnSystemChannel=True)

        else:
            sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Select", True), PlayOnSystemChannel=True)

        self.ScrollSlowdownEnabled = True

        self.ScrollEnabled = True
        self.ScrollMode = 1
        self.ScrollMultiplier = 1.5

    def Update(self, event):
        # -- Only Run Events when needed. -- #
        if self.Rectangle.collidepoint(pygame.mouse.get_pos()):
            if not self.ScrollSlowdownEnabled:
                if event.type == pygame.KEYUP and event.key == pygame.K_q:
                    self.ScrollIndexDown()

                if event.type == pygame.KEYUP and event.key == pygame.K_e:
                    self.ScrollIndexUp()

                if event.type == pygame.KEYUP and event.key == pygame.K_HOME:
                    self.SelectedItemIndex = len(self.ApplicationName) - 1
                    self.ScrollX = -self.SelectedItemIndex * 240
                    sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/ListEnd", True), PlayOnSystemChannel=True)

                if event.type == pygame.KEYUP and event.key == pygame.K_END:
                    self.ScrollX = 128
                    self.SelectedItemIndex = 0
                    sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/ListEnd", True), PlayOnSystemChannel=True)

                # -- Mouse Whell -- #
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.ScrollIndexUp()

                    if event.button == 5:
                        self.ScrollIndexDown()

            for i, itemNam in enumerate(self.ApplicationName):
                if self.SelectedItemIndex == i:
                    self.SelectedApplicationFolderInfos = self.ApplicationFolderInfos[i]
                    self.SelectedItem = itemNam
                    self.SelectedApplicationID = self.ApplicationID[i]
                    self.SelectedApplicationFolderName = self.ApplicationFolderName[i]
                    self.ItemSelected[i] = True
                    self.SelectedItemIndex = i
                    self.SelectedApplicationVersion = self.ApplicationVersion[i]
                    self.SelectedApplicationID = self.ApplicationID[i]
                    self.SelectedApplicationIcon = self.ApplicationBanner[i]

                else:
                    self.ItemSelected[i] = False


    def Set_X(self, Value):
        if not self.Rectangle[0] == Value:
            self.Rectangle[0] = float(Value)

    def Set_Y(self, Value):
        if not self.Rectangle[1] == Value:
            self.Rectangle[1] = float(Value)

    def Set_W(self, Value):
        if not self.Rectangle[2] == Value:
            self.Rectangle[2] = float(Value)

    def Set_H(self, Value):
        if not self.Rectangle[3] == Value:
            self.Rectangle[3] = float(Value)

    def AddItem(self, ApplicationDir):
        # -- Convert Name to String -- #
        ApplicationDir = str(ApplicationDir)

        # -- Check if Folder Exists -- #
        if not utils.Directory_Exists(ApplicationDir):
            raise FileNotFoundError("Cannot locate the application folder: " + ApplicationDir)

        # -- Read Meta Data File -- #
        LineNumber = -1
        AnimationTotalFrames = 0
        AnimationFramesDelay = 0

        MetaFile = ApplicationDir + "/meta.data"
        FolderName = ""
        with open(MetaFile) as file_in:
            for line in file_in:
                line = line.rstrip()

                if not line == "" and not line.startswith('#'):
                    LineNumber += 1

                    if LineNumber == 0:  # -- Application Name
                        self.ApplicationName.append(line)

                    if LineNumber == 1:  # -- Application ID
                        self.ApplicationID.append(line)

                    if LineNumber == 2:  # -- Application Version
                        self.ApplicationVersion.append(line)

                    if LineNumber == 3:  # -- Application Folder Name
                        self.ApplicationFolderName.append(line)
                        FolderName = line.rstrip()

                    if LineNumber == 4:  # -- Animation Banner Frames
                        AnimationTotalFrames = int(line)

                    if LineNumber == 5:  # -- Animation Banner Frames Delay
                        AnimationFramesDelay = int(line)

        if LineNumber < 5: # -- Detect if the Game Folder is invalid
            raise NotADirectoryError("The Application [" + ApplicationDir + "] is not a valid Taiyou Application.\nMETADATA_FILE_READ_ERROR")

        # -- Load the Game Icon and Banner Animation -- #
        try:
            self.ApplicationBanner.append(pygame.transform.scale(pygame.image.load(ApplicationDir + "/icon.png").convert(), (240, 150)))

        except FileNotFoundError:
            self.ApplicationBanner.append(sprite.GetSprite("/TAIYOU_UI/no_icon.png"))
            print("Taiyou.InstalledGamesSelecter.AddItem : Cannot Locate Application icon.")

        # -- Add Item Variables -- #
        self.ItemApperAnimationEnabled.append(True)
        self.ItemApperAnimationNumb.append(0)
        self.ItemApperAnimationMode.append(0)
        self.ItemSelectedCurrentFrame.append(0)
        self.ItemApperAnimationToggle.append(False)
        self.ItemSelectedCurrentFrameUpdateDelay.append(0)
        self.ItemSelected.append(False)

        # - Load Folder Metadata -- #
        ApplicationFolderInfos = list()

        ApplicationFolderInfos.append(tge.utils.FormatNumber(tge.utils.Calculate_FolderSize(FolderName), 2, ['B', 'Kb', 'MB', 'GB', 'TB']))
        ApplicationFolderInfos.append(tge.utils.Get_DirectoryTotalOfFiles(FolderName))

        self.ApplicationFolderInfos.append(ApplicationFolderInfos)

        # -- Add the Animation Frames -- #
        FiltredGameDir = ApplicationDir.replace("./", "")

        if utils.File_Exists(FiltredGameDir + "/SELETOR/0.png"):
            if AnimationTotalFrames > 1:
                AnimationFrames = list()
                for frame in range(0, AnimationTotalFrames):
                    path = FiltredGameDir + "/SELETOR/" + str(frame) + ".png"

                    print("Frame : [" + path + "]")
                    AnimationFrames.append(pygame.transform.scale(pygame.image.load(path).convert(), (240, 150)))

                # -- Add Values to the List -- #
                self.ApplicationBannerAnimation.append(AnimationFrames)
                self.ApplicationBannerAnimationAmount.append(AnimationTotalFrames)
                self.ApplicationBannerAnimationFrameDelay.append(AnimationFramesDelay)
            else:
                AnimationFrames = list()
                AnimationFrames.append(pygame.transform.scale(pygame.image.load(ApplicationDir + "/icon.png").convert(), (240, 150)))

                self.ApplicationBannerAnimation.append(AnimationFrames)
                self.ApplicationBannerAnimationAmount.append(0)
                self.ApplicationBannerAnimationFrameDelay.append(0)


        else:
            AnimationFrames = list()
            AnimationFrames.append(sprite.GetSprite("/TAIYOU_UI/no_icon.png"))

            self.ApplicationBannerAnimation.append(AnimationFrames)
            self.ApplicationBannerAnimationAmount.append(0)
            self.ApplicationBannerAnimationFrameDelay.append(0)
            print("Taiyou.InstalledGamesSelecter.AddItem : Cannot Locate Application Banner Frames.")


class VerticalListWithDescription:
    def __init__(self, Rectangle):
        self.Rectangle = Rectangle
        self.ItemsName = list()
        self.ItemsDescription = list()
        self.ItemSprite = list()
        self.ItemSelected = list()
        self.Selected_Name = "null"
        self.Selected_Index = -1
        self.ScrollY = 0
        self.ClickedItem = ""
        self.ColisionXOffset = 0
        self.ColisionYOffset = 0
        self.ButtonUpRectangle = pygame.Rect(0, 0, 32, 32)
        self.ButtonDownRectangle = pygame.Rect(34, 0, 32, 32)

    def Render(self, DISPLAY):
        ListSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]), pygame.SRCALPHA)

        ListSurface.fill((0,0,0,0))
        for i, itemNam in enumerate(self.ItemsName):
            ItemRect = (0, self.ScrollY + 42 * i, self.Rectangle[2], 40)

            # -- When the item is not clicked -- #
            if not self.ItemSelected[i]:
                if self.Selected_Name == itemNam:
                    # -- Background -- #
                    sprite.Shape_Rectangle(ListSurface, (20, 42, 59, 100), ItemRect)
                    # -- Indicator Bar -- #
                    sprite.Shape_Rectangle(ListSurface, (46, 196, 182), (ItemRect[0], ItemRect[1], ItemRect[2], 1))
                else:
                    # -- Background -- #
                    sprite.Shape_Rectangle(ListSurface, (20, 42, 59, 50), ItemRect)
                    # -- Indicator Bar -- #
                    sprite.Shape_Rectangle(ListSurface, (32, 164, 243), (ItemRect[0], ItemRect[1], ItemRect[2], 1))

            else:
                # -- Background -- #
                sprite.Shape_Rectangle(ListSurface, (30, 52, 69, 150), ItemRect)
                # -- Indicator Bar -- #
                sprite.Shape_Rectangle(ListSurface, (255, 51, 102), (ItemRect[0], ItemRect[1], ItemRect[2], 1))

            # -- Render the Item Name and Description -- #
            sprite.FontRender(ListSurface, VerticalList_FontFile, 18, itemNam, (250, 250, 250), ItemRect[0] + 5, ItemRect[1] + 5, reg.ReadKey_bool("TaiyouSystem/CONF/font_aa", True))
            sprite.FontRender(ListSurface, VerticalList_FontFile, 12, self.ItemsDescription[i], (250, 250, 250), ItemRect[0] + 3, ItemRect[1] + 28, reg.ReadKey_bool("TaiyouSystem/CONF/font_aa", True))

        DISPLAY.blit(ListSurface, (self.Rectangle[0], self.Rectangle[1]))

    def Update(self, event):
        ColisionRect = pygame.Rect(self.Rectangle[0] + self.ColisionXOffset, self.Rectangle[1] + self.ColisionYOffset, self.Rectangle[2], self.Rectangle[3])

        if ColisionRect.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:
                    self.ScrollY += 5

                if event.button == 4:
                    self.ScrollY -= 5

            # -- Select the Clicked Item -- #
            for i, itemNam in enumerate(self.ItemsName):
                ItemRect = pygame.Rect(self.ColisionXOffset + self.Rectangle[0], self.ColisionYOffset + self.ScrollY + self.Rectangle[1] + 42 * i, self.Rectangle[2], 40)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if ItemRect.collidepoint(pygame.mouse.get_pos()):
                        self.Selected_Name = itemNam
                        self.ItemSelected[i] = True
                        self.Selected_Index = i

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

    def ClearList(self):
        self.ItemsName.clear()
        self.ItemsDescription.clear()
        self.ItemSprite.clear()
        self.ItemSelected.clear()
        self.ScrollY = 0
        self.Selected_Name = "null"
        self.Selected_Index = -1


class LoadingSquare:
    def __init__(self, X, Y, AnimationSelected=0):
        self.X = X
        self.Y = Y
        self.FramesPrefix = reg.ReadKey("/TaiyouSystem/GTK/animation_" + str(AnimationSelected) + "/frames_prefix", True)
        self.CurrentFrame = 1
        self.UpdateAnimDelay = 0
        self.Opacity = 255
        self.OpacityAddMode = 0
        self.Animation = AnimationSelected
        self.AnimationTotalFrames = reg.ReadKey_int("/TaiyouSystem/GTK/animation_" + str(AnimationSelected) + "/total_frames", True)
        self.AnimationFramesDelay = reg.ReadKey_int("/TaiyouSystem/GTK/animation_" + str(AnimationSelected) + "/frames_delay", True)
        self.LastFrameLock =  reg.ReadKey_int("/TaiyouSystem/GTK/animation_" + str(AnimationSelected) + "/last_frame_lock", True)
        self.IsLastFrame = False
        self.LastFrameDelay = 0

    def Update(self):
        # -- Do the Aniamtion Loop -- #
        if not self.IsLastFrame:
            self.UpdateAnimDelay += 1
        else:
            self.LastFrameDelay += 1

            if self.LastFrameDelay >= self.LastFrameLock:
                self.LastFrameDelay = 0
                self.IsLastFrame = False
                self.CurrentFrame = 1

        if self.UpdateAnimDelay >= self.AnimationFramesDelay and not self.IsLastFrame:
            self.CurrentFrame += 1

            if self.CurrentFrame >= self.AnimationTotalFrames:
                self.IsLastFrame = True
                self.CurrentFrame = self.AnimationTotalFrames # -- Set to the last frame

            self.UpdateAnimDelay = 0

    def Set_X(self, NewValue):
        self.X = NewValue

    def Set_Y(self, NewValue):
        self.Y = NewValue

    def Render(self, DISPLAY):
        AnimSurface = pygame.Surface((32, 32), pygame.SRCALPHA)
        AnimSurface.set_alpha(self.Opacity)

        sprite.ImageRender(AnimSurface, self.FramesPrefix + str(self.CurrentFrame) + ".png", 0, 0, 32, 32)

        DISPLAY.blit(AnimSurface, (self.X, self.Y))

class Slider():
    def __init__(self, Xloc, Yloc, Value):
        self.Rectangle = pygame.Rect(Xloc, Yloc, 32, 132)
        self.Value = Value
        self.LastCursorPos = (0, 0)
        self.IsBeingMoved = False
        self.SliderRectangle = pygame.Rect(self.Rectangle[0] + 5, (self.Rectangle[1] + 5) + 0 - (self.Rectangle[1] + 5), self.Rectangle[2] - 10, 10)
        self.Opacity = 255
        self.Surface = pygame.Surface((32, 138), pygame.SRCALPHA)
        self.UpdateValue = True
        self.DrawEnabled = False

    def Render(self, Display):
        # -- Update Rectangles -- #
        self.SliderRectangle = pygame.Rect(self.Rectangle[0] + 5, (self.Rectangle[1] + 5) + self.LastCursorPos[1] - (self.Rectangle[1] + 5), self.Rectangle[2] - 10, 10)

        # -- Update Slider Controller -- #
        if self.SliderRectangle[1] <= self.Rectangle[1] + 10:
            self.SliderRectangle[1] = self.Rectangle[1] + 10

        if self.SliderRectangle[1] >= self.Rectangle[1] + self.Rectangle[3] - 12:
            self.SliderRectangle[1] = self.Rectangle[1] + self.Rectangle[3] - 12

        # -- Render Background -- #
        if self.DrawEnabled:
            self.DrawObject()

        # -- Set Surface Opacity -- #
        self.Surface.set_alpha(self.Opacity)

        Display.blit(self.Surface, (self.Rectangle[0], self.Rectangle[1]))

    def DrawObject(self):
        self.Surface.fill(Slider_BackgroundColor)

        # -- Render the Borders -- #
        sprite.Shape_Rectangle(self.Surface, Slider_Borders_Color, (0, 0, 32, 137), Panels_Indicator_Size)

        # -- Render the Slider Background -- #
        sprite.Shape_Rectangle(self.Surface, Slider_Progress_Background, (11, 10, 10, self.Rectangle[3] - 15), 0, 5)

        # -- Render the Slider Percentage -- #
        sprite.Shape_Rectangle(self.Surface, Slider_Progress_Percentage, (11, 10, 10, (self.SliderRectangle[1] - self.Rectangle[1]) - self.SliderRectangle[3]), 0, 0, 5, 5)

        # -- Render the Slider Notch -- #
        sprite.Shape_Rectangle(self.Surface, Slider_Progress_Notch, (5, self.SliderRectangle[1] - self.Rectangle[1], self.SliderRectangle[2], 10), 0, 10)

    def Set_X(self, Value):
        self.Rectangle[0] = Value

    def Set_Y(self, Value):
        self.Rectangle[1] = Value

    def Set_Opacity(self, Value):
        self.Opacity = Value

    def SetValue(self, value):
        self.LastCursorPos = (self.LastCursorPos[0], self.SliderRectangle[1] + value)
        self.Value = value

    def EventUpdate(self, event):
        if self.Opacity > 1:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.SliderRectangle.collidepoint(mainScript.Cursor_Position):
                    self.IsBeingMoved = True

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.IsBeingMoved = False
                if self.SliderRectangle.collidepoint(mainScript.Cursor_Position):
                    sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Click", True), 0.5, PlayOnSystemChannel=True)

            if self.IsBeingMoved:
                self.LastCursorPos = (mainScript.Cursor_Position[0], mainScript.Cursor_Position[1])
                self.UpdateValue = True
            else:
                try:
                    if self.UpdateValue:
                        self.UpdateValue = False
                        # -- Update Bar Value -- #
                        self.Value = min((self.SliderRectangle[1] - self.SliderRectangle[3]) - (self.Rectangle[1]), 100)

                except TypeError:
                    pass

class SpriteButton:
    def __init__(self, Rectangle, Sprite):
        self.Rectangle = Rectangle
        self.Sprite = Sprite
        self.ButtonState = 0  # 0 - Inactive, 1 - DOWN, 2 - UP
        self.CursorSettedToggle = False
        self.CustomColisionRectangle = False
        self.ButtonDowed = False
        self.ColisionRectangle = pygame.Rect(0, 0, 0, 0)
        self.LastRect = pygame.Rect(0, 0, 0, 0)
        self.Surface = pygame.Surface((Rectangle[2], Rectangle[3]))
        self.Surface.set_colorkey((0, 255, 0))
        self.Surface.fill((0, 255, 0))

    def Render(self, DISPLAY):
        IndicatorColor = (0, 0, 0)

        if not self.LastRect == self.Rectangle:  # -- Update the Surface When Needed.
            self.Surface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]))

        # -- Update Buttons Color -- #
        if self.ButtonState == 0:  # -- Inactive State
            self.BackgroundColor = Button_Inactive_BackgroundColor
            IndicatorColor = Button_Inactive_IndicatorColor

        elif self.ButtonState == 1:  # -- DOWN State
            self.BackgroundColor = Button_Active_BackgroundColor
            IndicatorColor = Button_Active_IndicatorColor

        # -- Render the Background -- #
        self.Surface.fill(self.BackgroundColor)

        # -- Render Indicator Bar -- #
        sprite.Shape_Rectangle(self.Surface, IndicatorColor, (0, 0, self.Rectangle[2], 2), 0, 0, Button_BorderRadius, Button_BorderRadius)

        # -- Render the Sprite
        sprite.ImageRender(self.Surface, self.Sprite, 0, 2, self.Rectangle[2], self.Rectangle[3] - 2, True)

        # -- Render the Button -- #
        DISPLAY.blit(self.Surface, self.Rectangle)

        if self.ButtonState == 2:
            self.ButtonState = 0

    def EventUpdate(self, event):
        if not self.CustomColisionRectangle:
            self.ColisionRectangle = self.Rectangle

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # -- Set the Button to DOWN State -- #
            if self.ColisionRectangle.collidepoint(mainScript.Cursor_Position):
                self.ButtonState = 1
                self.ButtonDowed = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # -- Set the Button to UP state -- #
            if self.ColisionRectangle.collidepoint(mainScript.Cursor_Position):
                if self.ButtonDowed:
                    self.ButtonState = 2
                    self.ButtonDowed = False
                    sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Click", True), 0.5, PlayOnSystemChannel=True)

    def Set_X(self, Value):
        self.Rectangle[0] = Value

    def Set_Y(self, Value):
        self.Rectangle[1] = Value

    def Set_W(self, Value):
        self.Rectangle[2] = Value

    def Set_H(self, Value):
        self.Rectangle[3] = Value

    def Set_Sprite(self, Value):
        self.Sprite = Value
