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
def Get_Version():
    return "1.1"

def Get_ContentManager():
    return "1.1"

def Get_UtilsVersion():
    return "1.1"

def Get_AppDataVersion():
    return "1.1"

GeneralVersion = float(Get_Version()) + float(Get_ContentManager()) + float(Get_UtilsVersion()) + float(Get_AppDataVersion()) + 20

print("Taiyou General Version\n{0}".format(GeneralVersion))

CorrectSlash = "/"
AppDataFolder = ""
SystemFolder = "Taiyou{0}".format(CorrectSlash)
ConfigurationFile = ""
IPLloaderName = ""

Current_ApplicationFolder = ""

from Engine import Utils
from Engine.Utils import Convert
from Engine import Main
from Engine import AppData
import Engine.ContentManager as Content

import os, platform


def init_engine():
    global ConfigurationFile
    global CorrectSlash
    global SystemFolder
    print("### Initialize Taiyou Game Engine ###\nSet SystemSlash")

    # -- Set the Correct Slash Directory -- #
    if platform.system() == "Linux":
        CorrectSlash = "/"
        SystemFolder = "Taiyou/"
        ConfigurationFile = SystemFolder + "Taiyou.config"

    elif platform.system() == "Windows":
        CorrectSlash = "\\"
        SystemFolder = "Taiyou\\"
        ConfigurationFile = SystemFolder + "Taiyou.config"

    LoadConfFile()

    print("Initialize IPL")
    Loader(IPLloaderName)
    print("Initialization Steps Completed!")


def Loader(source_folder):
    global CorrectSlash
    global Current_ApplicationFolder
    global AppDataFolder

    Current_ApplicationFolder = source_folder
    AppDataFolder = ''.join(("AppData", CorrectSlash, source_folder.replace("/", "."), "/"))
    print("Taiyou.Loader : Loading Module {0}...".format(Current_ApplicationFolder))

    Main.SetGameObject(source_folder)

    print("Taiyou.Loader : Module loaded sucefully!")


def LoadConfFile():
    global IPLloaderName
    global ConfigurationFile
    global CorrectSlash

    print("Loading Configuration File...")
    conf_file = open(ConfigurationFile)

    for line in conf_file:
        try:
            line = line.rstrip()
            SplitedParms = line.split(":")

            if SplitedParms[0] == "IPL":
                IPLloaderName = SplitedParms[1].rstrip().replace("/", CorrectSlash)

        except Exception as ex:
            raise ex

    print("Done.")

def ParseModuleName(input):
    global CorrectSlash

    return "{0}{1}".format(input.replace(CorrectSlash, "."), ".MAIN")

def CloseApplicationFolder():
    global Current_ApplicationFolder
    Current_ApplicationFolder = ""
    Main.DeleteGameObject()
