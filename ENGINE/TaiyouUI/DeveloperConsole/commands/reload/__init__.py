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

def Run(SplitedComma):
    if SplitedComma[1] == "REGISTRY":  # -- Reload Registry -- #
        PrintToTerminalBuffer(gtk.GetLangText("comma:reload_1", "developer_console"))
        reg.Reload()

    elif SplitedComma[1] == "SPRITE":  # -- Reload Sprite -- #
        PrintToTerminalBuffer(gtk.GetLangText("comma:reload_2", "developer_console"))
        sprite.Reload()

    elif SplitedComma[1] == "SOUND":  # -- Reload Sound System -- #
        PrintToTerminalBuffer(gtk.GetLangText("comma:reload_3", "developer_console"))
        sound.Reload()

    elif SplitedComma[1] == "SYS_OPTS":  # -- Reload Taiyou Optiuns -- #
        PrintToTerminalBuffer(gtk.GetLangText("comma:reload_4", "developer_console"))
        tge.InitEngine()

    elif SplitedComma[1] == "ALL":  # -- Reload Everthing -- #
        # -- Reload Registry -- #
        PrintToTerminalBuffer(gtk.GetLangText("comma:reload_1", "developer_console"))
        reg.Reload()

        # -- Reload Sprites -- #
        PrintToTerminalBuffer(gtk.GetLangText("comma:reload_2", "developer_console"))
        sprite.Reload()

        # -- Reload Sound System -- #
        PrintToTerminalBuffer(gtk.GetLangText("comma:reload_3", "developer_console"))
        sound.Reload()

        # -- Reload Taiyou Options -- #
        PrintToTerminalBuffer(gtk.GetLangText("comma:reload_4", "developer_console"))
        tge.InitEngine()

        PrintToTerminalBuffer(gtk.GetLangText("comma:reload_done", "developer_console"))

    else:
        raise TypeError(gtk.GetLangText("error/reload", "developer_console"))
