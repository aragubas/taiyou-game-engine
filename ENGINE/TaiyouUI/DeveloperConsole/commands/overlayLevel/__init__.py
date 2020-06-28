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
from ENGINE import TaiyouUI as taiyouUI
import ENGINE as tge

def Run(SplitedComma):
    # -- Convert the Value to string -- #
    Value = int(SplitedComma[0])

    # -- Send the Message -- #
    taiyouUI.Messages.append("OVERLAY_LEVEL:" + str(Value))

    # -- Print to Termianl Buffer -- #
    PrintToTerminalBuffer(gtk.GetLangText("comma:overlayLevel", "developer_console").format(str(SplitedComma[0])))
