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
TextToDisplay = "/error_text"
TracebackText = "null"
ErrorSoundPlayed = False
FormatedTrackback = ""
ErrorDescription = "null"
ErrorDescriptionX = 0
ErrorDescriptionY = 0


def Initialize(DISPLAY):
    global DefaultContents
    global TracebackText
    global FormatedTrackback

    tge.RunInFullScreen = False

    MAIN.ReceiveCommand(0, 60)
    MAIN.ReceiveCommand(1, "800x600")
    MAIN.ReceiveCommand(5, "Taiyou Game Engine has CRASHED!")
    MAIN.ReceiveCommand(6, False)

    DefaultContents = cntMng.ContentManager()
    tge.CurrentGame_Folder = "Taiyou{0}ERROR{0}".format(tge.TaiyouPath_CorrectSlash)
    DefaultContents.SetFontPath("Data{0}FONT".format(tge.TaiyouPath_CorrectSlash))
    DefaultContents.LoadSpritesInFolder("Data/SPRITE")
    DefaultContents.LoadRegKeysInFolder("Data/REG")
    DefaultContents.LoadSoundsInFolder("Data/SOUND")

    print("Taiyou.CrashScreen : Initialized")
    WriteLog()

    # -- Print the Exception -- #
    print(traceback.format_exc())

    FormatedTrackback = list(TracebackText)

    AllText = ""
    SplitedLines = TracebackText.splitlines()

    for line in SplitedLines:
        LineList = list(line)

        while len(LineList) >= 100:
            LineList = ''.join(LineList)[:-1]

        AllChars = ""

        for char in LineList:
            AllChars += char

        AllText += "\n{0}".format(AllChars)

    FormatedTrackback = AllText

def WriteLog():
    global TracebackText

    LogFile = open("LastExc.txt", "w")
    # -- Write the File Header -- #
    LogFile.write("-- Taiyou Crash File--\nThis log file has been written on:\n{0}\n\n".format(datetime.datetime.now()))
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
    global ErrorDescription
    global ErrorDescriptionX
    global ErrorDescriptionY
    global TracebackText
    global ErrorSoundPlayed
    global FormatedTrackback

    if not ErrorSoundPlayed:
        ErrorSoundPlayed = True
        DefaultContents.PlaySound("/notify.wav")

    ErrorDescription = DefaultContents.Get_RegKey(TextToDisplay).format(FormatedTrackback)
    ErrorDescriptionX = 800 / 2 - DefaultContents.GetFont_width("/Ubuntu_Bold.ttf", 14, ErrorDescription) / 2
    ErrorDescriptionY = 60 + DefaultContents.GetImage_height("/warning.png")

def GameDraw(DISPLAY):
    global DefaultContents
    global TextToDisplay
    global ErrorDescription
    global ErrorDescriptionX
    global ErrorDescriptionY
    DISPLAY.fill((0, 0, 0))

    # -- Render Background -- #
    DefaultContents.ImageRender(DISPLAY, "/background.png", 0, 0)

    # -- Render the Taiyou Logo -- #
    DefaultContents.ImageRender(DISPLAY, "/warning.png", 800 / 2 - DefaultContents.GetImage_width("/warning.png") / 2, 50)


    # -- Render the Text -- #
    DefaultContents.ImageRender(DISPLAY, "/bar.png", ErrorDescriptionX, ErrorDescriptionY, DefaultContents.GetFont_width("/Ubuntu_Bold.ttf", 14, ErrorDescription), DefaultContents.GetFont_height("/Ubuntu_Bold.ttf", 14, ErrorDescription))
    DefaultContents.FontRender(DISPLAY, "/Ubuntu_Bold.ttf", 14, ErrorDescription, (255, 255, 255), ErrorDescriptionX, ErrorDescriptionY)

    # -- Render Cursor -- #
    DefaultContents.ImageRender(DISPLAY, "/cursor.png", pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

def EventUpdate(event):
    global TracebackViewerMode
    global FontSize
    global TextPanX
    global TextPanY

    if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
        MAIN.Destroy()
