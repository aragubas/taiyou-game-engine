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

import pygame, threading, asyncio
from ENGINE import SPRITE as sprite
from ENGINE import SOUND as sound
from ENGINE.TaiyouUI import UIGTK as gtk
from ENGINE import TaiyouUI as taiyouUI
import ENGINE as tge
from ENGINE import utils
from ENGINE import SPRITE as sprite
from ENGINE import SOUND as sound
from ENGINE import REGISTRY as reg

WindowObject = gtk.Window
TextEnter = gtk.InputBox
TextEnter_LastCommand = ""
TextEnter_LastCurrentCommand = ""
WindowInitialized = False
TextScrollWhenInitialized = False

def Initialize():
    global WindowObject
    global TextEnter
    global TerminalBuffer

    WindowObject = gtk.Window(pygame.Rect(50,50,620, 350), gtk.GetLangText("title", "developer_console/window"), True)

    TextEnter = gtk.InputBox(0,0,200,20,"help")
    TextEnter.CustomColision = True
    TextEnter.CustomWidth = True

    ScrollConsole()

def ScrollConsole():
    global TerminalBuffer
    global WindowObject

    if sprite.GetFont_height("/PressStart2P.ttf", 8, TerminalBuffer) >= WindowObject.WindowSurface.get_height() - 10:
        try:
            RemoveAmount = 4
            TerminalBuffer = TerminalBuffer.split("\n", RemoveAmount)[RemoveAmount]
        except:
            print("Taiyou.DeveloperConsole : Oops, cannot clear more than this.")


def Update():
    global WindowObject
    global TextEnter
    global TerminalBuffer
    global TextScrollWhenInitialized
    global WindowInitialized
    if not WindowObject.WindowMinimized:
        TextEnter.colisionRect = pygame.Rect(WindowObject.WindowSurface_Dest[0], WindowObject.WindowSurface_Dest[1] + WindowObject.WindowSurface.get_height() - 18, WindowObject.WindowSurface.get_width(), 18)
        TextEnter.rect[1] = WindowObject.WindowSurface.get_height() - TextEnter.rect[3]

        TextEnter.width = WindowObject.WindowSurface.get_width()

        ScrollConsole()

def EventUpdate(event):
    global WindowObject
    global TextEnter
    global TextEnter_LastCommand
    global TextEnter_LastCurrentCommand

    WindowObject.EventUpdate(event)

    if not WindowObject.WindowMinimized:

        TextEnter.Update(event)

        if event.type == pygame.KEYUP and event.key == pygame.K_RETURN and TextEnter.active:
            PrintToTerminalBuffer("\n$:" + TextEnter.text)
            ReadCommand(TextEnter.text)
            TextEnter_LastCommand = TextEnter.text
            TextEnter.text = ""

        if event.type == pygame.KEYUP and event.key == pygame.K_UP and TextEnter.active:
            TextEnter_LastCurrentCommand = TextEnter.text
            TextEnter.text = TextEnter_LastCommand

        if event.type == pygame.KEYUP and event.key == pygame.K_DOWN and TextEnter.active:
            TextEnter.text = TextEnter_LastCurrentCommand
        # - Set the default text
        TextEnter.DefaultText = TextEnter_LastCommand


TerminalBuffer = "Taiyou Developer Console v" + tge.Get_DeveloperConsoleVersion()
def PrintToTerminalBuffer(text):
    global TerminalBuffer
    global WindowObject
    global WindowInitialized

    if TerminalBuffer == "":
        TerminalBuffer += str(text)
    else:
        TerminalBuffer += "\n" + str(text)


def Draw(DISPLAY):
    global TextEnter
    global WindowInitialized

    if not WindowObject.WindowMinimized:
        WindowObject.WindowSurface.fill((0,0,0))

        # -- Draw the Terminal Buffer -- #
        if WindowInitialized:
            sprite.FontRender(WindowObject.WindowSurface, "/PressStart2P.ttf", 8, TerminalBuffer, (240, 240, 240), 0, 0)
        else:
            sprite.FontRender(WindowObject.WindowSurface, "/PressStart2P.ttf", 8, gtk.GetLangText("initial", "developer_console"), (240, 240, 240), 0, 0)

        # -- Draw the Text Box -- #
        TextEnter.Render(WindowObject.WindowSurface)

    # -- Draw the Window Frame -- #
    WindowObject.Render(DISPLAY)

    # -- Draw the Window Content -- #
    if not WindowObject.WindowMinimized:
        DISPLAY.blit(WindowObject.WindowSurface, WindowObject.WindowSurface_Dest)

    WindowInitialized = True


def ReadCommand(Input):
    global TerminalBuffer

    CurrentInput = str(Input)  # -- Convert INPUT to String -- #
    SplitedComma = CurrentInput.split(' ')

    try:
        # -- Process Command on Other Module -- #
        commands.processCommand(SplitedComma)

    except IndexError:
        PrintToTerminalBuffer(gtk.GetLangText("error/arguments_error", "developer_console").format(str(SplitedComma[0])))
        # -- Play Sound Error -- #
        sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Notify"))

    except TypeError as ex:
        PrintToTerminalBuffer("TYPO ERROR!\n" + str(ex) + "\n in [" + SplitedComma[0] + "]")
        # -- Play Notify Sound -- #
        sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Notify"))

    except Exception as ex:
        try:
            PrintToTerminalBuffer("EXCEPTION!\n" + str(ex) + "\n in [" + SplitedComma[0] + "]")
        except IndexError:
            PrintToTerminalBuffer("EXCEPTION!\n" + str(ex) + "\n in [ERROR_OBTAINING_MODULE_NAME]")

        # -- Play Error Sound -- #
        sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Error"))

# -- When module was fully initialized, import Commands Module -- #
from ENGINE.TaiyouUI.DeveloperConsole import commands as commands
