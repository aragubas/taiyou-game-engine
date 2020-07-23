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
from ENGINE.TaiyouUI import OverlayManager
from ENGINE.TaiyouUI import UIGTK as gtk
from ENGINE import TaiyouUI as taiyouUI
import pygame

Animation_Y = 0
Animation_Speed = 0
Animation_Enabled = True
Animation_Rectangle = pygame.Rect(0, 0, 0, 0)
Animation_Mode = True
DeltaTime = 0
DeltaTimeMax = 50
Surface = None
MinWidth = 150
Width = MinWidth

# -- NotificationPopup Message Related -- #
Message = "undefined_message"
Title = "undefined_title"
Icon = "null"

def Update():
    global Animation_Y
    global Animation_Enabled
    global Animation_Rectangle
    global Animation_Mode
    global Surface
    global Animation_Speed
    global DeltaTime
    global DeltaTimeMax
    global Width

    if Animation_Enabled:
        if Animation_Mode:
            Animation_Speed += 1
            Animation_Y += Animation_Speed

            if Animation_Y > 0:
                Animation_Y = 0
                Animation_Mode = False
                Animation_Enabled = False

        else:
            Animation_Speed += 1
            Animation_Y -= Animation_Speed

            if Animation_Y < -150:
                Animation_Y = -150
                Animation_Mode = True
                Animation_Speed = 0
                Animation_Enabled = False
                taiyouUI.NotificationPopupEnabled = False

    # -- Update Rectangle -- #
    Animation_Rectangle = pygame.Rect((OverlayManager.CommonDisplay.get_width() / 2) - (Width / 2), Animation_Y, Width, 100)

    if not Animation_Enabled:
        if DeltaTime < DeltaTimeMax:
            DeltaTime += 1
        else:
            Animation_Enabled = True
            DeltaTime = 0

    if Surface is None:
        Surface = pygame.Surface((Animation_Rectangle[2], Animation_Rectangle[3]))

def Draw(DISPLAY):
    global Animation_Rectangle
    global Surface
    global Message
    global Title
    global Icon
    if not Surface is None:
        Surface.set_alpha(255 - Animation_Y)
        BlurBackground(Surface, (0, 0, Animation_Rectangle[2], Animation_Rectangle[3]), DISPLAY, 35, 100, (Animation_Rectangle[0], Animation_Rectangle[1]))

        sprite.Shape_Rectangle(Surface, (200, 200, 200), (0, 0, Animation_Rectangle[2], Animation_Rectangle[3]), 3, 2)

        if not Icon is "null":
            GlobalX = 102

            # -- Render NotificationPopup Icon -- #
            sprite.ImageRender(Surface, Icon, 9, 6, 90, Animation_Rectangle[3] - 12, True, ImageNotLoaded=True)
        else:
            GlobalX = 6

        # -- Render Title -- #
        sprite.FontRender(Surface, gtk.Notification_TitleFont, 22, Title, (230, 230, 230), GlobalX, 6)

        # -- Render Text -- #
        sprite.FontRender(Surface, gtk.Notification_TextFont, 14, Message, (230, 230, 230), GlobalX, 32)

        DISPLAY.blit(Surface, (Animation_Rectangle[0], Animation_Rectangle[1]))

def SetNotification(title, text, icon=None, DeltaMax=300):
    global Title
    global Message
    global Icon
    global Animation_Enabled
    global Animation_Mode
    global Animation_Y
    global DeltaTimeMax
    global Width
    global Animation_Speed
    global Surface
    global MinWidth

    Title = title
    Message = text
    Icon = icon

    Animation_Enabled = True
    Animation_Mode = True
    Animation_Y = -150
    DeltaTimeMax = DeltaMax
    Animation_Speed = 0
    Surface = None

    Width = MinWidth

    TitleWidth = sprite.GetFont_width(gtk.Notification_TitleFont, 22, Title) + 8
    TextWidth = sprite.GetFont_width(gtk.Notification_TextFont, 18, text) + 8

    if TitleWidth > Width:
        Width += TitleWidth

    if TextWidth > Width:
        Width += TextWidth - MinWidth / 2

    taiyouUI.NotificationPopupEnabled = True

def BlurBackground(DISPLAY, Rectangle, SourceSurface, BlurAmmount=100, BlackContrast=50, Offset=(0, 0)):
    """
    Render a blurred Rectangle, usefull for UI.
    :param DISPLAY:The surface to be blitted
    :param Rectangle:Rectangle
    :param BlurAmmount:The ammount of blur (value higher than 100 is recomended)
    :param BlackContrast:The ammount of Black Color (usefull for contrast in bright surfaces)
    :return:
    """
    # -- the Result Surface -- #
    ResultPanel = pygame.Surface((Rectangle[2], Rectangle[3]), pygame.HWACCEL | pygame.HWSURFACE)

    if not BlackContrast == 0:
        DarkerBG = pygame.Surface((Rectangle[2], Rectangle[3]), pygame.HWACCEL | pygame.HWSURFACE)
        DarkerBG.set_alpha(BlackContrast)
        SourceSurface.blit(DarkerBG, (Rectangle[0] + Offset[0], Rectangle[1] + Offset[1], Rectangle[2], Rectangle[3]))

    # -- Only Blur the Necessary Area -- #
    AreaToBlur = pygame.Surface((Rectangle[2], Rectangle[3]), pygame.HWACCEL | pygame.HWSURFACE)
    AreaToBlur.blit(SourceSurface, (0, 0), (Offset[0], Offset[1], Rectangle[2], Rectangle[3]))

    # -- Then Finnaly, blit the Blurred Result -- #
    ResultPanel.blit(sprite.Surface_Blur(AreaToBlur, BlurAmmount, False), (0, 0))

    DISPLAY.blit(ResultPanel, (Rectangle[0], Rectangle[1]))
