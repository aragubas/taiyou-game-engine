#!/usr/bin/python3.6
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
import pygame, os, sys
from ENGINE import SPRITE as sprite
from ENGINE import SOUND as sound
from ENGINE.TaiyouUI import UIGTK as gtk
from ENGINE import TaiyouUI as taiyouUI
import ENGINE as tge
from ENGINE import utils
from ENGINE import SPRITE as sprite
from ENGINE import SOUND as sound
from ENGINE import REGISTRY as reg

# -- Buttons -- #
LogOut_Button = gtk.Button
SelectGame_Button = gtk.Button

# -- Lists -- #
InstalledGameList = gtk.HorizontalItemsView

# -- Rects -- #
TopPanel_Rect = pygame.Rect(0,0,30,30)

# -- Animation Fields -- #
UIOpacity = 0
UIOpacityAnimSpeed = 15
UIOpacityAnimEnabled = True
UIOpacityAnimState = 0
UIOpacityAnim_InSoundPlayed = False
UIOpacityAnim_OutSoundPlayed = False
UIOpacity_AnimExitToOpenGame = False
AnimationNumb = 0

DisplaySurface = pygame.Surface((0,0))
DisplaySurfaceInited = False

ValidGameFolders = list()

def ListInstalledGames():
    print("ListInstalledGames : Init")
    Dirs = [ f.path for f in os.scandir(".") if f.is_dir() ]

    for D in Dirs:
        print("ListInstalledGames : Analising Directory[" + D + "]")

        if os.path.isfile(D + "/meta.data"):
            print("ListInstalledGames : Directory is a Game Directory!")
            ValidGameFolders.append(D)
        else:
            print("ListInstalledGames : Directory is invalid.")


def Initialize():
    global LogOut_Button
    global InstalledGameList
    global ValidGameFolders
    global SelectGame_Button
    LogOut_Button = gtk.Button(pygame.Rect(0,0,5,5), "Log Out", 14)
    SelectGame_Button = gtk.Button(pygame.Rect(0,0,5,5), "Select Game", 14)
    InstalledGameList = gtk.HorizontalItemsView(pygame.Rect(20, 50, 760, 190))


    ListInstalledGames()

    for game in ValidGameFolders:
        InstalledGameList.AddItem(game)

BackgroundR = 0
BackgroundG = 0
BackgroundB = 0

def Draw(Display):
    global LogOut_Button
    global DisplaySurfaceInited
    global DisplaySurface
    global TopPanel_Rect
    global UIOpacity
    global InstalledGameList
    global SelectGame_Button
    DisplaySurface = Display
    Display.fill((BackgroundR,BackgroundG,BackgroundB))

    if DisplaySurfaceInited:
        gtk.Draw_Panel(Display, TopPanel_Rect, "DOWN")

    # -- Render Buttons -- #
    LogOut_Button.Render(Display)
    SelectGame_Button.Render(Display)

    # -- Render the Game List -- #
    InstalledGameList.Render(Display)

    # -- Set the Display Inited Variable -- #
    if not DisplaySurfaceInited:
        DisplaySurfaceInited = True

def Update():
    global LogOut_Button
    global AnimationNumb
    global TopPanel_Rect
    global DisplaySurface
    global DisplaySurfaceInited
    global SelectGame_Button
    global InstalledGameList
    global UIOpacity_AnimExitToOpenGame
    global UIOpacityAnimEnabled
    AnimationNumb = UIOpacity - 255 + UIOpacityAnimSpeed

    # -- Update Bar's Positions -- #
    if DisplaySurfaceInited:
        TopPanel_Rect = pygame.Rect(0, AnimationNumb * 1.5, DisplaySurface.get_width(), 35)

        LogOut_Button.Set_X(TopPanel_Rect[2] - LogOut_Button.Rectangle[2] - 5)

    InstalledGameList.SurfaceOpacity = AnimationNumb * 2.5 + 255
    InstalledGameList.Set_X(AnimationNumb * 1.5 + 20)
    SelectGame_Button.Set_X(InstalledGameList.Rectangle[0])
    SelectGame_Button.Set_Y(InstalledGameList.Rectangle[1] + InstalledGameList.Rectangle[3] + 5)

    if SelectGame_Button.ButtonState == "UP":
        UIOpacityAnimEnabled = True
        UIOpacity_AnimExitToOpenGame = True
    # -- Update Objects Position -- #
    LogOut_Button.Set_Y(AnimationNumb + 5)

    # -- Update the In/Out Animation -- #
    UpdateOpacityAnim()

def OpenGame(GameFolderName):
    GameFolderName = GameFolderName.rstrip()
    global UIOpacityAnimEnabled
    print("TaiyouUI.OpenGame : Folder Name[" + str(GameFolderName) + "]")

    tge.OpenGameFolder(GameFolderName)
    taiyouUI.Messages.append("OPEN_GAME:" + GameFolderName)
    taiyouUI.Messages.append("TOGGLE_GAME_START")
    taiyouUI.Messages.append("GAME_UPDATE:True")

    UIOpacityAnimEnabled = True
    taiyouUI.CurrentMenuScreen = 0

def EventUpdate(event):
    global LogOut_Button
    global InstalledGameList
    global SelectGame_Button

    LogOut_Button.Update(event)
    InstalledGameList.Update(event)
    SelectGame_Button.Update(event)

def UpdateOpacityAnim():
    global UIOpacityAnimState
    global UIOpacity
    global UIOpacityAnimEnabled
    global UIOpacityAnimSpeed
    global UIOpacityAnim_InSoundPlayed
    global UIOpacityAnim_OutSoundPlayed
    global BackgroundR
    global BackgroundG
    global BackgroundB

    if UIOpacityAnimEnabled:
        if UIOpacityAnimState == 0:  # <- Enter Animation
            UIOpacity += UIOpacityAnimSpeed

            if BackgroundR < 0:
                BackgroundR += 1
            if BackgroundG < 1:
                BackgroundG += 1
            if BackgroundB < 12:
                BackgroundB += 1

            # -- Play the In Sound -- #
            if not UIOpacityAnim_InSoundPlayed:
                sound.PlaySound("/TAIYOU_UI/HUD_In.wav")
                UIOpacityAnim_InSoundPlayed = True

            if UIOpacity >= 255:  # <- Triggers Animation End
                UIOpacity = 255
                UIOpacityAnimEnabled = False
                UIOpacityAnimState = 1
                UIOpacityAnim_InSoundPlayed = True
                UIOpacityAnim_OutSoundPlayed = True
                print("Taiyou.SystemUI.AnimationTrigger : Animation Start.")

        if UIOpacityAnimState == 1:  # <- Exit Animation
            UIOpacity -= UIOpacityAnimSpeed

            if BackgroundR > 0:
                BackgroundR -= 1
            if BackgroundG > 0:
                BackgroundG -= 1
            if BackgroundB > 0:
                BackgroundB -= 1


            # -- Play the Out Sound -- #
            if not UIOpacityAnim_OutSoundPlayed:
                sound.PlaySound("/TAIYOU_UI/HUD_Out.wav")
                UIOpacityAnim_OutSoundPlayed = True

            if UIOpacity <= 0:  # <- Triggers Animation End
                UIOpacity = 0
                UIOpacityAnimEnabled = False
                UIOpacityAnimState = 0

                if UIOpacity_AnimExitToOpenGame:
                    OpenGame(InstalledGameList.SelectedGameFolderName)


                print("Taiyou.SystemUI.AnimationTrigger : Animation End.")
