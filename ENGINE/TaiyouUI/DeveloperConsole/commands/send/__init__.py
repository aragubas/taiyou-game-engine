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
import ENGINE.TaiyouUI as taiyouUI
from ENGINE.TaiyouUI import UIGTK as gtk
import ENGINE as tge
from ENGINE import TaiyouMain as taiyouMain

def Run(SplitedCommand):
    AllLine = ""
    for i in range(0, len(SplitedCommand)):
        if i <= 0:
            AllLine += SplitedCommand[i]
        else:
            AllLine += " " + SplitedCommand[i]

    PrintToTerminalBuffer(gtk.GetLangText("comma:send_1", "developer_console").format(AllLine))

    taiyouMain.ReceiveCommand(AllLine)
