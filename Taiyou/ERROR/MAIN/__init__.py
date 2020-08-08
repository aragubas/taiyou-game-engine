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
import datetime
import traceback
import sys

DefaultContents = cntMng.ContentManager
ExcpWritten = False
FlashBorderDelta = 0
FlashBorderValue = 1
TracebackText = "null"
SysTxt = "null"
ModulesTxt = "null"
TracebackViewerMode = False
FontSize = 8
TextPanX = 0
TextPanY = 0

def Initialize(DISPLAY):
    global DefaultContents
    tge.RunInFullScreen = False

    MAIN.ReceiveCommand(0, 15)
    MAIN.ReceiveCommand(1, "800x600")
    MAIN.ReceiveCommand(5, "Taiyou Game Engine has CRASHED!")
    MAIN.ReceiveCommand(6, True)

    DefaultContents = cntMng.ContentManager()
    tge.CurrentGame_Folder = "Taiyou{0}ERROR{0}".format(tge.TaiyouPath_CorrectSlash)
    DefaultContents.SetFontPath("Data{0}FONT".format(tge.TaiyouPath_CorrectSlash))

    print("Taiyou.CrashScreen : Initialized")
    WriteLog()
    UpdateErrorTexts()

    # -- Set the Key Repeat -- #
    pygame.key.set_repeat(1, 10)

    # -- Print the Exception -- #
    print(traceback.format_exc())

def UpdateErrorTexts():
    global SysTxt
    global ModulesTxt

    SysTxt = "                       Taiyou Game Engine has Failed!               \n\n\n" \
             "If you are seeing this screen, the current application don't have an\n" \
             "Exception Handling System. Take a Screenshot of this screen and send\n" \
             "to the developer of the Application.\n\n" \
             "#-- APPLICATION METADATA -- #\n" \
             "Folder Name: {0}\n" \
             "\n\n#-- Exception 'Nickname' -- #\n" \
             "Excp(\n\n{1}\n\n)\n" \
             "\n\n" \
             "All details of the Exception has been written on\n" \
             "(.{2}LastExc.txt).\n" \
             "Press (ESC) key to exit"

    try:
        SysTxt = SysTxt.format(tge.CurrentGame_Folder, tge.LastException, tge.TaiyouPath_CorrectSlash)

    except Exception as ex:
        print("Taiyou.CrashScreen : Error while parsing the string:\n" + str(ex))

    ModulesTxt = "#-- Modules Version --#\n\nRuntime: {0}\n\nAppData: {1}\n\nContentManager: {2}\n\nFx: {3}\n\nMain: {4}\n\nShape: {5}\n\nUtils: {6}\n\nGeneral: {7}"

    try:
        ModulesTxt = ModulesTxt.format(str(tge.Get_Version()), str(tge.Get_AppDataVersion()), str(tge.Get_ContentManagerVersion()), str(tge.Get_FXVersion()), str(tge.Get_TaiyouMainVersion()), str(tge.Get_ShapeVersion()), str(tge.Get_UtilsVersion()), str(tge.TaiyouGeneralVersion))

    except Exception as ex:
        print("Taiyou.CrashScreen : Error while parsing the string:\n" + str(ex))


def WriteLog():
    global TracebackText

    LogFile = open("LastExc.txt", "w")
    # -- Write the File Header -- #
    LogFile.write("-- Taiyou Crash File--\nThis log file has been written on:\n{0}\n\n".format(datetime.datetime.now()))
    LogFile.write("Application Name: {0}\n".format(tge.CurrentGame_Folder))
    LogFile.write("Traceback:\n{0}\n".format(traceback.format_exc()))
    LogFile.write("\nModules Version:\n")

    ModulesTxt = "Runtime: {0}\n\nAppData: {1}\n\nContentManager: {2}\n\nFx: {3}\n\nMain: {4}\n\nShape: {5}\n\nUtils: {6}"

    try:
        ModulesTxt = ModulesTxt.format(str(tge.Get_Version()), str(tge.Get_AppDataVersion()), str(tge.Get_ContentManagerVersion()), str(tge.Get_FXVersion()), str(tge.Get_TaiyouMainVersion()), str(tge.Get_ShapeVersion()), str(tge.Get_UtilsVersion()))

        LogFile.write(ModulesTxt)

    except Exception as ex:
        print("Taiyou.CrashScreen : Error while parsing the string:\n" + str(ex))
        LogFile.write("ERROR WHILE PARSING THE STRING.")

    LogFile.close()
    TracebackText = traceback.format_exc()

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

    shape.Shape_Rectangle(DISPLAY, (135, 20, 55), (5, 5, 790, 255), FlashBorderValue)

    RenderSysTxt(DISPLAY)

    RenderModuleVersions(DISPLAY)


def RenderSysTxt(DISPLAY):
    global DefaultContents
    global SysTxt

    DefaultContents.FontRender(DISPLAY, "/PressStart2P.ttf", 10, SysTxt, (135, 55, 32), 15, 15, backgroundColor=(0, 0, 0))

def RenderModuleVersions(DISPLAY):
    global DefaultContents
    global FontSize
    global TextPanX
    global TextPanY
    global ModulesTxt
    global TracebackViewerMode

    if not TracebackViewerMode:
        DefaultContents.FontRender(DISPLAY, "/PressStart2P.ttf", FontSize, ModulesTxt, (32, 55, 135), 15 + TextPanX, 275 + TextPanY, backgroundColor=(0, 0, 0))
    else:
        DefaultContents.FontRender(DISPLAY, "/PressStart2P.ttf", FontSize, TracebackText, (255, 255, 255), 15 + TextPanX, 275 + TextPanY, backgroundColor=(0, 0, 0))


def EventUpdate(event):
    global TracebackViewerMode
    global FontSize
    global TextPanX
    global TextPanY

    if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
        MAIN.Destroy()

    # -- Enable Traceback Viewer -- #
    if event.type == pygame.KEYUP and event.key == pygame.K_t:
        if not TracebackViewerMode:
            TracebackViewerMode = True
        else:
            TracebackViewerMode = False
        TextPanX = 0
        TextPanY = 0

    # -- Traceback Viwer Controls -- #
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_m:
            if FontSize < 30:
                FontSize += 1

        # -- Decrease Font Size -- #
        if event.key == pygame.K_n:
            if FontSize > 6:
                FontSize -= 1

        # -- Increase Font Size -- #
        if event.key == pygame.K_w:
            TextPanY -= 5

        # -- Move Text -- #
        if event.key == pygame.K_s:
            TextPanY += 5

        # -- Move Text -- #
        if event.key == pygame.K_a:
            TextPanX -= 5

        # -- Move Text -- #
        if event.key == pygame.K_d:
            TextPanX += 5

        # -- Restart Values -- #
        if event.key == pygame.K_r:
            TextPanX = 0
            TextPanY = 0
            FontSize = 8

