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
# -- Import All Commands -- #
import ENGINE.TaiyouUI.DeveloperConsole.commands.help as c_help
import ENGINE.TaiyouUI.DeveloperConsole.commands.kill as c_kill
import ENGINE.TaiyouUI.DeveloperConsole.commands.overlayLevel as c_overlayLevel
import ENGINE.TaiyouUI.DeveloperConsole.commands.gameData as c_gameData
import ENGINE.TaiyouUI.DeveloperConsole.commands.reload as c_reload
import ENGINE.TaiyouUI.DeveloperConsole.commands.clear as c_clear
import ENGINE.TaiyouUI.DeveloperConsole.commands.unload as c_unload
import ENGINE.TaiyouUI.DeveloperConsole.commands.versions as c_versions
import ENGINE.TaiyouUI.DeveloperConsole.commands.send as c_send
from ENGINE import *
import ENGINE.TaiyouUI.UIGTK as gtk

def GetCommandObject_byID(commandObjName):
    '''
    Return Command Command, all commands Entry needs to go here
    :param commandObjName:Name of Command
    :return:Command Module
    '''
    # -- Help Command -- #
    if commandObjName == "help" or commandObjName == "hlp":
        return c_help

    # -- Reload Command -- #
    if commandObjName == "kill" or commandObjName == "kil":
        return c_kill

    # -- Overlay Level Command -- #
    if commandObjName == "overlayLevel" or commandObjName == "oll":
        return c_overlayLevel

    # -- Game Data Command -- #
    if commandObjName == "gameData" or commandObjName == "gmd":
        return c_gameData

    # -- Reload Command -- #
    if commandObjName == "reload" or commandObjName == "rel":
        return c_reload

    # -- Unload Command -- #
    if commandObjName == "unload" or commandObjName == "unl":
        return c_unload

    # -- Clear Command -- #
    if commandObjName == "clear" or commandObjName == "cls":
        return c_clear

    # -- Versions Command -- #
    if commandObjName == "versions" or commandObjName == "ver":
        return c_versions

    # -- Send Message Command -- #
    if commandObjName == "send" or commandObjName == "snd":
        return c_send

    return None # -- If command was not found

def processCommand(SplitedComma):
    commandObj = GetCommandObject_byID(SplitedComma[0])

    if not commandObj is None:
        SplitedComma = SplitedComma.pop(0)

        commandObj.Run(SplitedComma)

        # -- Play Click Sound -- #
        sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Click"))
    else:
        raise TypeError(gtk.GetLangText("error/invalid_command", "developer_console"))
