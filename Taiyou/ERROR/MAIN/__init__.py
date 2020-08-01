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
from ENGINE import appData
from ENGINE import cntMng
from ENGINE import shape
from ENGINE import MAIN
import ENGINE as tge
import pygame

DefaultContents = cntMng.ContentManager
ExcpWritten = False
FlashBorderDelta = 0
FlashBorderValue = 1

def Initialize(DISPLAY):
    global DefaultContents
    tge.RunInFullScreen = False

    MAIN.ReceiveCommand(0, 5)
    MAIN.ReceiveCommand(1, "800x600")
    MAIN.ReceiveCommand(5, "Taiyou Game Engine has CRASHED!")

    DefaultContents = cntMng.ContentManager()
    DefaultContents.LoadFonts("Taiyou{0}ERROR{0}".format(tge.TaiyouPath_CorrectSlash))

    print("Taiyou.CrashScreen : Initialized")

def Update():
    global FlashBorderDelta
    global FlashBorderValue

    FlashBorderDelta += 1

    if FlashBorderDelta == 5:
        FlashBorderValue = 1

    if FlashBorderDelta >= 10:
        FlashBorderDelta = 1

    if FlashBorderDelta == 1:
        FlashBorderValue = 4

def GameDraw(DISPLAY):
    global DefaultContents
    global FlashBorderValue
    DISPLAY.fill((0, 0, 0))

    shape.Shape_Rectangle(DISPLAY, (255, 0, 0), (5, 5, 790, 255), FlashBorderValue, 2)

    RenderSysTxt(DISPLAY)

    RenderModuleVersions(DISPLAY)

def RenderSysTxt(DISPLAY):
    global DefaultContents
    SysTxt = "                       Taiyou Game Engine has Failed!               \n\n\n" \
             "If you are seeing this screen, the current application don't have an\n" \
             "Exception Handling System. Take a Screenshot of this screen and send\n" \
             "to the developer of the Application.\n\n" \
             "#-- APPLICATION METADATA -- #\n" \
             "Folder Name: {0}\n" \
             "\n\n#-- EXCEPTION DETAILS -- #\n" \
             "Excp(\n\n{1}\n\n)\n" \
             "\n\n" \
             "All details of the Exception has been written on\n" \
             "(.{2}LastExc.txt)."

    try:
        SysTxt = SysTxt.format(tge.CurrentGame_Folder, tge.LastException, tge.TaiyouPath_CorrectSlash)

    except Exception as ex:
        print("Taiyou.CrashScreen : Error while parsing the string:\n" + str(ex))

    DefaultContents.FontRender(DISPLAY, "/PressStart2P.ttf", 10, SysTxt, (230, 0, 20), 15, 15, False)

def RenderModuleVersions(DISPLAY):
    global DefaultContents

    ModulesTxt = "Runtime: {0}\n\nAppData: {1}\n\nContentManager: {2}\n\nFx: {3}\n\nMain: {4}\n\nShape: {5}\n\nUtils: {6}"

    try:
        ModulesTxt = ModulesTxt.format(str(tge.Get_Version()), str(tge.Get_AppDataVersion()), str(tge.Get_ContentManagerVersion()), str(tge.Get_FXVersion()), str(tge.Get_TaiyouMainVersion()), str(tge.Get_ShapeVersion()), str(tge.Get_UtilsVersion()))

    except Exception as ex:
        print("Taiyou.CrashScreen : Error while parsing the string:\n" + str(ex))

    DefaultContents.FontRender(DISPLAY, "/PressStart2P.ttf", 10, ModulesTxt, (230, 0, 20), 15, 275, False)

def EventUpdate(event):
    pass