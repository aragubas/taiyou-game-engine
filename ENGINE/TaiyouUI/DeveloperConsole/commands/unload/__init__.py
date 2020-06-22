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

from ENGINE.TaiyouUI.DeveloperConsole import PrintToTerminalBuffer
from ENGINE.TaiyouUI import UIGTK as gtk
import ENGINE as tge

def Run(SplitedCommand):
    PrintToTerminalBuffer("Unload")

    if SplitedComma[1] == "REGISTRY":  # -- Unload Registry -- #
        PrintToTerminalBuffer(gtk.GetLangText("comma:unload_1", "developer_console"))
        reg.Unload()

    elif SplitedComma[1] == "SPRITE":  # -- Unload Sprites -- #
        PrintToTerminalBuffer(gtk.GetLangText("comma:unload_2", "developer_console"))
        sprite.Unload()

    elif SplitedComma[1] == "SOUND":  # -- Unload Sounds -- #
        PrintToTerminalBuffer(gtk.GetLangText("comma:unload_3", "developer_console"))
        sound.Unload()

    else:
        raise TypeError(gtk.GetLangText("error/unload", "developer_console"))
