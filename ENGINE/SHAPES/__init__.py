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
import pygame
from ENGINE import UTILS as utils
from ENGINE import CONTENT_MANAGER as cntMng
import ENGINE as tge

print("Taiyou SHAPE version: " + tge.Get_ShapeVersion())


def Shape_Rectangle(DISPLAY, Color, Rectangle, BorderWidth=0, BorderRadius=0, Border_TopLeft_Radius=0, Border_TopRight_Radius=0, Border_BottomLeft_Radius=0, Border_BottomRight_Radius=0, DrawLines=False):
    if cntMng.RectangleRenderingDisabled:
        return
    if Rectangle[0] <= DISPLAY.get_width() and Rectangle[0] >= 0 - Rectangle[2] and Rectangle[1] <= DISPLAY.get_height() and Rectangle[1] >= 0 - Rectangle[3]:
        # -- Fix the Color Range -- #
        Color = utils.FixColorRange(Color)

        # -- Border Radius-- #
        if BorderRadius > 0 and Border_TopRight_Radius == 0 and Border_TopLeft_Radius == 0 and Border_BottomLeft_Radius == 0 and Border_BottomRight_Radius == 0:
            Border_TopRight_Radius = BorderRadius
            Border_TopLeft_Radius = BorderRadius
            Border_BottomRight_Radius = BorderRadius
            Border_BottomLeft_Radius = BorderRadius

        # -- Render the Rectangle -- #
        if not DrawLines:
            pygame.draw.rect(DISPLAY, Color, Rectangle, BorderWidth, BorderRadius, Border_TopLeft_Radius,
                             Border_TopRight_Radius, Border_BottomLeft_Radius, Border_BottomRight_Radius)
        else:
            gfxdraw.rectangle(DISPLAY, Rectangle, Color)

def Shape_Line(DISPLAY, Color, startX, startY, endX, endY, LineWidth, FoldLine=True):
    # -- Fix the Color Range -- #
    Color = utils.FixColorRange(Color)

    if FoldLine:
        if endX > DISPLAY.get_width():
            endX = DISPLAY.get_width()
        if endY > DISPLAY.get_height():
            endY = DISPLAY.get_height()

        if startX < 0:
            startX = 0
        if startY < 0:
            startY = 0

    pygame.draw.line(DISPLAY, Color, (startX, startY), (endX, endY), LineWidth)

def Shape_Pie(DISPLAY, X, Y, Radius, StartAngle, StopAngle, Color):
    if X + Radius >= DISPLAY.get_width() or X < Radius:
        Color = utils.FixColorRange(Color)

        gfxdraw.pie(DISPLAY, X, Y, Radius, StartAngle, StopAngle, Color)
