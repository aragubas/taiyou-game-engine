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

    WindowObject = gtk.Window(pygame.Rect(50,50,550, 350), "Developer Console", True)
    WindowObject.Resiziable = False
    TextEnter = gtk.InputBox(0,0,200,20,"help")
    TextEnter.CustomColision = True
    TextEnter.CustomWidth = True

def Update():
    global WindowObject
    global TextEnter
    global TerminalBuffer
    global TextScrollWhenInitialized
    global WindowInitialized
    if not WindowObject.WindowMinimized:
        TextEnter.colisionRect = pygame.Rect(WindowObject.WindowSurface_Dest[0], WindowObject.WindowSurface_Dest[1] + WindowObject.WindowSurface.get_height() - 11, WindowObject.WindowSurface.get_width(), 11)
        TextEnter.rect[1] = WindowObject.WindowSurface.get_height() - 11

        TextEnter.width = WindowObject.WindowSurface.get_width()

        while sprite.GetText_height("/PressStart2P.ttf", 9, TerminalBuffer) >= WindowObject.WindowSurface.get_height() - 10:
            TerminalBuffer = TerminalBuffer.split("\n", 1)[1]


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

TerminalBuffer = "Initial Message"

def PrintToTerminalBuffer(text):
    global TerminalBuffer
    global WindowObject
    global WindowInitialized

    TerminalBuffer += "\n" + str(text)

def Draw(DISPLAY):
    global TextEnter
    global WindowInitialized

    if not WindowObject.WindowMinimized:
        WindowObject.WindowSurface.fill((0,0,0))

        # -- Draw the Terminal Buffer -- #
        if WindowInitialized:
            sprite.RenderFont(WindowObject.WindowSurface, "/PressStart2P.ttf", 8, TerminalBuffer, (240,240,240), 0, 0)
        else:
            sprite.RenderFont(WindowObject.WindowSurface, "/PressStart2P.ttf", 8, "Initializing the console, please wait...", (240, 240, 240), 0, 0)

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
            PrintToTerminalBuffer("kill{kil} - Kill the current game")
            PrintToTerminalBuffer("reload{rel} [REGISTRY,SPRITE/FONT,SOUND] - Reload")
            PrintToTerminalBuffer("unload{unl} [REGISTRY,SPRITE/FONT,SOUND] - Unload")
            PrintToTerminalBuffer("clear{cls} - Clear the Screen")
            PrintToTerminalBuffer("continue{cnt} - Continue game execution")
            PrintToTerminalBuffer("versions{ver} - Print all Taiyou Game Engine components versions")
            PrintToTerminalBuffer("gameData{gmd} - Print loaded game data")
            PrintToTerminalBuffer("overlayLevel{oll} - Set the overlay level")

        # -- Reload Command -- #
        if SplitedComma[0] == "kill" or SplitedComma[0] == "kil":
            CommandWasValid = True
            taiyouUI.Messages.append("KILL")
            PrintToTerminalBuffer("Goodbye...")

        if SplitedComma[0] == "overlayLevel" or SplitedComma[0] == "oll":
            CommandWasValid = True
            try:
                int(SplitedComma[1])

                taiyouUI.Messages.append("OVERLAY_LEVEL:" + str(SplitedComma[1]))

                PrintToTerminalBuffer("OverlayLevel was set to:\n " + str(SplitedComma[1]) + ".")

            except:
                PrintToTerminalBuffer("ERROR!\n The value[" + str(SplitedComma[1]) + "] is not a valid Integer.")




        if SplitedComma[0] == "gameData" or SplitedComma[0] == "gmd":
            CommandWasValid = True
            PrintToTerminalBuffer("==============================================")
            PrintToTerminalBuffer("GameTitle: " + tge.Get_GameTitle())
            PrintToTerminalBuffer("SourceFolder: " + tge.Get_GameSourceFolder())
            PrintToTerminalBuffer("GameID: " + tge.Get_GameID())
            PrintToTerminalBuffer("GameVersion: " + tge.Get_GameVersion())
            PrintToTerminalBuffer("==============================================")

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

        if SplitedComma[0] == "unload" or SplitedComma[0] == "unl":
            CommandWasValid = True
            PrintToTerminalBuffer("Unload")

            if SplitedComma[1] == "REGISTRY":
                PrintToTerminalBuffer("Unloading Registry...")
                reg.Unload()
                PrintToTerminalBuffer("Done!")
            elif SplitedComma[1] == "SPRITE":
                PrintToTerminalBuffer("Unloading Sprites...")
                sprite.Unload()
                PrintToTerminalBuffer("Done!")

            elif SplitedComma[1] == "SOUND":
                PrintToTerminalBuffer("Unloading Sound...")
                sound.Unload()
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
