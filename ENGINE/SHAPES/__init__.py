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
from pygame import gfxdraw
from ENGINE import UTILS as utils
from ENGINE import CONTENT_MANAGER as cntMng
import ENGINE as tge

print("Taiyou SHAPE version: " + tge.Get_ShapeVersion())


def Shape_Rectangle(DISPLAY, Color, Rectangle, BorderWidth=0, BorderRadius=0, Border_TopLeft_Radius=0, Border_TopRight_Radius=0, Border_BottomLeft_Radius=0, Border_BottomRight_Radius=0, DrawLines=False):
    """
    Draw a Rectangle
    :param DISPLAY:Surface to be drawn
    :param Color:Color (RGB)
    :param Rectangle:Rectangle Rectangle
    :param BorderWidth:Border Width
    :param BorderRadius:Border Radius
    :param Border_TopLeft_Radius:Only apply border to TopLeft
    :param Border_TopRight_Radius:Only apply border to TopRight
    :param Border_BottomLeft_Radius:Only apply border to BottomLeft
    :param Border_BottomRight_Radius:Only apply border to BottomRight
    :param DrawLines:Draw only rectangle line
    :return:
    """
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
    """
    Draw a Line
    :param DISPLAY:Surface to be drawn
    :param Color:Color (RGB)
    :param startX:Line StartX
    :param startY:Line StartY
    :param endX:Line EndX
    :param endY:Line EndY
    :param LineWidth:Line Width
    :param FoldLine:Fold the line when getting offscreen
    :return:
    """
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


def Shape_Circle(DISPLAY, X, Y, Radius, Color, Width=0, draw_top_right=False, draw_top_left=False, draw_bottom_left=False, draw_bottom_right=False):
    """
    Draw a Circle
    :param DISPLAY:Surface to draw
    :param X:Circle X
    :param Y:Circle Y
    :param Radius:Circle Radius
    :param Color:Color (RGB)
    :param Width:Circle Width
    :param draw_top_right:Draw top right
    :param draw_top_left:Draw top left
    :param draw_bottom_left:Draw bottom left
    :param draw_bottom_right:Draw bottom right
    :return:
    """
    if X - Radius < DISPLAY.get_width() and Y - Radius < DISPLAY.get_height() and X > -Radius and Y > -Radius and Radius > 1:
        Color = utils.FixColorRange(Color)

        pygame.draw.circle(DISPLAY, Color, (X, Y), Radius, Width, draw_top_right, draw_top_left, draw_bottom_left, draw_bottom_right)
