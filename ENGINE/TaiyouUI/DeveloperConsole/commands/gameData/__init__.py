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
import ENGINE.TaiyouUI.DeveloperConsole as devel
from ENGINE.TaiyouUI.DeveloperConsole import PrintToTerminalBuffer
from ENGINE.TaiyouUI import UIGTK as gtk
import ENGINE as tge

def Run(SplitedComma):
    PrintToTerminalBuffer(gtk.GetLangText("comma:gameData", "developer_console").format(
        tge.Get_GameTitle(),
        tge.Get_GameSourceFolder(),
        tge.Get_GameID(),
        tge.Get_GameVersion()
    ))
