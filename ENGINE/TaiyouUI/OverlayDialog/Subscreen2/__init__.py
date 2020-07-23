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
import pygame, os, sys, shutil
from ENGINE import SPRITE as sprite
from ENGINE import SOUND as sound
from ENGINE.TaiyouUI import UIGTK as gtk
from ENGINE import TaiyouUI as taiyouUI
import ENGINE as tge
from ENGINE import utils
from ENGINE import SPRITE as sprite
from ENGINE import SOUND as sound
from ENGINE import REGISTRY as reg
from ENGINE.TaiyouUI import OverlayDialog as Handler

MessageTitle = "null"
Message = "null"
Yes_Button = gtk.Button
No_Button = gtk.Button
InputBox = gtk.InputBox
OK_Button = gtk.Button

ResponseTrigger = False
Response = "null"
ResponseType = "INPUT"

def Initialize():
    global Yes_Button
    global No_Button
    global InputBox
    global OK_Button

    Yes_Button = gtk.Button(pygame.Rect(0,0,0,0), gtk.GetLangText("yes_button"), 18)
    Yes_Button.CustomColisionRectangle = True

    No_Button = gtk.Button(pygame.Rect(0,0,0,0), gtk.GetLangText("no_button"), 18)
    No_Button.CustomColisionRectangle = True

    OK_Button = gtk.Button(pygame.Rect(0, 0, 0, 0), gtk.GetLangText("ok_button"), 18)
    OK_Button.CustomColisionRectangle = True

    InputBox = gtk.InputBox(0, 0, 0, 0, "Default", 20)

    InputBox.CustomColision = True


def Draw(DISPLAY):
    global Message
    global Yes_Button
    global No_Button
    global ResponseType
    global InputBox
    global OK_Button

    # -- Render Buttons -- #
    if ResponseType == "YESNO":
        No_Button.Render(DISPLAY)
        Yes_Button.Render(DISPLAY)

    elif ResponseType == "INPUT":
        InputBox.Render(DISPLAY)

    elif ResponseType == "OK":
        OK_Button.Render(DISPLAY)

    # -- Render Message -- #
    sprite.FontRender(DISPLAY, "/Ubuntu_Bold.ttf", 18, Message, (230, 230, 230), 5, 26)

def Update():
    global MessageTitle
    global Yes_Button
    global No_Button
    global ResponseTrigger
    global Response
    global InputBox
    global OK_Button

    if ResponseType == "YESNO":
        # -- Update Yes Button -- #
        Yes_Button.Set_ColisionX(Handler.CommonDisplayScreenPos[0] + Yes_Button.Rectangle[0])
        Yes_Button.Set_ColisionY(Handler.CommonDisplayScreenPos[1] + Yes_Button.Rectangle[1])
        Yes_Button.Set_X(5)
        Yes_Button.Set_Y(Handler.CommonDisplay.get_height() - Yes_Button.Rectangle[3] - 5)

        # -- Update No Button -- #
        No_Button.Set_ColisionX(Handler.CommonDisplayScreenPos[0] + No_Button.Rectangle[0])
        No_Button.Set_ColisionY(Handler.CommonDisplayScreenPos[1] + No_Button.Rectangle[1])
        No_Button.Set_X(Yes_Button.Rectangle[0] + Yes_Button.Rectangle[2] + 3)
        No_Button.Set_Y(Handler.CommonDisplay.get_height() - No_Button.Rectangle[3] - 5)

        if Yes_Button.ButtonState == 2:
            Response = "YES"
            ResponseTrigger = True
            Handler.DialogOpctAnim_AnimEnabled = True

        if No_Button.ButtonState == 2:
            Response = "NO"
            ResponseTrigger = True
            Handler.DialogOpctAnim_AnimEnabled = True

    elif ResponseType == "INPUT":
        # -- Update Input Button -- #
        InputBox.Set_X(5)
        InputBox.Set_Y(Handler.CommonDisplay.get_height() - InputBox.rect[3] - 5)

        InputBox.colisionRect = pygame.Rect(Handler.CommonDisplayScreenPos[0] + InputBox.rect[0], Handler.CommonDisplayScreenPos[1] + InputBox.rect[1], InputBox.rect[2], InputBox.rect[3])
        InputBox.active = True

    elif ResponseType == "OK":
        # -- Update OK Button -- #
        OK_Button.Set_ColisionX(Handler.CommonDisplayScreenPos[0] + OK_Button.Rectangle[0])
        OK_Button.Set_ColisionY(Handler.CommonDisplayScreenPos[1] + OK_Button.Rectangle[1])
        OK_Button.Set_X(5)
        OK_Button.Set_Y(Handler.CommonDisplay.get_height() - OK_Button.Rectangle[3] - 5)

        if OK_Button.ButtonState == 2:
            Handler.DialogOpctAnim_AnimEnabled = True
            ResponseTrigger = True
            Response = "OK"

    Handler.MessageTitle = MessageTitle

def SetMessage(title, message):
    global MessageTitle
    global Message
    taiyouUI.OverlayDialogEnabled = True

    MessageTitle = title.rstrip()
    Message = message.rstrip()


def EventUpdate(event):
    global Yes_Button
    global No_Button
    global InputBox
    global ResponseType
    global ResponseTrigger
    global Response
    global OK_Button

    if ResponseType == "YESNO":
        No_Button.Update(event)
        Yes_Button.Update(event)

    elif ResponseType == "INPUT":
        InputBox.Update(event)

        if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
            Handler.DialogOpctAnim_AnimEnabled = True
            ResponseTrigger = True
            Response = InputBox.text
            InputBox.active = False

    elif ResponseType == "OK":
        OK_Button.Update(event)