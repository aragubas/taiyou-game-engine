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
import pygame
from ENGINE import SPRITE as sprite
from ENGINE.TaiyouUI import UIGTK as gtk
import ENGINE as tge
from ENGINE import utils
from ENGINE import SPRITE as sprite
from ENGINE import SOUND as sound
from ENGINE import REGISTRY as reg

WindowObject = gtk.Window
TextEnter = gtk.InputBox
TextEnter_LastCommand = ""
TextEnter_LastCurrentCommand = ""

def Initialize():
    global WindowObject
    global TextEnter

    WindowObject = gtk.Window(pygame.Rect(50,50,550, 350), "Developer Console", True)
    WindowObject.Resiziable = False
    TextEnter = gtk.InputBox(5,5,200,20,"help")
    TextEnter.CustomColision = True
    TextEnter.CustomWidth = True

def Update():
    global WindowObject
    global TextEnter

    TextEnter.colisionRect = pygame.Rect(WindowObject.WindowSurface_Dest[0], WindowObject.WindowSurface_Dest[1] + WindowObject.WindowSurface.get_height() - 24, WindowObject.WindowSurface.get_width(), 24)
    TextEnter.rect[1] = WindowObject.WindowSurface.get_height() - 20

    TextEnter.width = WindowObject.WindowSurface.get_width()

def EventUpdate(event):
    global WindowObject
    global TextEnter
    global TextEnter_LastCommand
    global TextEnter_LastCurrentCommand

    WindowObject.EventUpdate(event)
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



TerminalBuffer = "Type Command then press [ENTER]"

def PrintToTerminalBuffer(text):
    global TerminalBuffer
    global WindowObject

    # -- "Scroll" the text -- #
    while sprite.GetText_height("/PressStart2P.ttf", 9, TerminalBuffer) >= WindowObject.WindowSurface.get_height() - 5:
        TerminalBuffer = TerminalBuffer.split("\n", 1)[1]

    TerminalBuffer += "\n" + str(text)

def Draw(DISPLAY):
    global TextEnter
    global TerminalTextY
    WindowObject.WindowSurface.fill((0,0,0))

    # -- Draw the Terminal Buffer -- #
    sprite.RenderFont(WindowObject.WindowSurface, "/PressStart2P.ttf", 8, TerminalBuffer, (240,240,240), 0, 0)

    # -- Draw the Text Box -- #
    TextEnter.Render(WindowObject.WindowSurface)

    # -- Draw the Window Frame -- #
    WindowObject.Render(DISPLAY)

    # -- Draw the Window Content -- #
    DISPLAY.blit(WindowObject.WindowSurface, WindowObject.WindowSurface_Dest)

def ReadCommand(Input):
    global TerminalBuffer

    CurrentInput = str(Input)
    CommandWasValid = False
    SplitedComma = CurrentInput.split(' ')

    try:
        # -- Help Command -- #
        if SplitedComma[0] == "help" or SplitedComma[0] == "hlp":
            CommandWasValid = True
            PrintToTerminalBuffer("Taiyou DC [Developer Console] version " + tge.Get_DeveloperConsole())
            PrintToTerminalBuffer("RuntimeVersion: " + tge.Get_Version())
            PrintToTerminalBuffer("Template: [Command][ShortName] [ARGUMENTS] - [Description]")
            PrintToTerminalBuffer("\n\n")
            PrintToTerminalBuffer("help{hlp} - This list of commands")
            PrintToTerminalBuffer("destroy{des} - Kill the current game")
            PrintToTerminalBuffer("reload{rel} [REGISTRY,SPRITE/FONT,SOUND] - Reload")
            PrintToTerminalBuffer("clear{cls} - Clear the Screen")
            PrintToTerminalBuffer("continue{cnt} - Continue game execution")
            PrintToTerminalBuffer("versions{ver} - Print all Taiyou Game Engine components versions")
            PrintToTerminalBuffer("gameData{gmd} - Print loaded game data")

        # -- Reload Command -- #
        if SplitedComma[0] == "reload" or SplitedComma[0] == "rel":
            CommandWasValid = True
            PrintToTerminalBuffer("Reload")

            if SplitedComma[1] == "REGISTRY":
                PrintToTerminalBuffer("Reloading Registry...")
                reg.Reload()
                PrintToTerminalBuffer("Done!")
            elif SplitedComma[1] == "SPRITE":
                PrintToTerminalBuffer("Reloading Sprites...")
                sprite.Reload()
                PrintToTerminalBuffer("Done!")

            elif SplitedComma[1] == "SOUND":
                PrintToTerminalBuffer("Reloading Sound...")
                sound.Reload()
                PrintToTerminalBuffer("Done!")

            else:
                raise TypeError("[" + SplitedComma[1] + "] is not a valid argument.")

        # -- Clear Command -- #
        if SplitedComma[0] == "clear" or SplitedComma[0] == "cls":
            CommandWasValid = True
            TerminalBuffer = ""

        # -- Versions Command -- #
        if SplitedComma[0] == "versions" or SplitedComma[0] == "ver":
            CommandWasValid = True
            PrintToTerminalBuffer("Taiyou Developer Console [DC] Version " + tge.Get_DeveloperConsole())
            PrintToTerminalBuffer("Taiyou Runtime Version " + tge.Get_Version())
            PrintToTerminalBuffer("Taiyou Sprite/Font Version " + tge.Get_SpriteVersion())
            PrintToTerminalBuffer("Taiyou Sound System Version " + tge.Get_SoundVersion())
            PrintToTerminalBuffer("Taiyou Registry Version " + tge.Get_RegistryVersion())
            PrintToTerminalBuffer("Taiyou Game Object Version " + tge.Get_GameObjVersion())
            PrintToTerminalBuffer("General Taiyou Version " + utils.FormatNumber(tge.TaiyouGeneralVersion))

        if not CommandWasValid:
            raise TypeError("Command was not valid\nWrite 'help' to see the list of commands.")
    except IndexError:
        PrintToTerminalBuffer("ARGUMENTS ERROR!\nThe command: [{0}] does not have the correct amount of arguments.".format(str(SplitedComma[0])))
    except TypeError as ex:
        PrintToTerminalBuffer("TYPO ERROR!\n" + str(ex) + "\n in [" + SplitedComma[0] + "]")
