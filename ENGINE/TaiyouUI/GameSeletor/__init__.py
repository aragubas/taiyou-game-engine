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
from ENGINE.TaiyouUI import loadingScreen as loadingScreen

# -- Buttons -- #
Exit_Button = gtk.Button
SelectGame_Button = gtk.Button

# -- Lists -- #
InstalledGameList = gtk.HorizontalItemsView

# -- Rects -- #
TopPanel_Rect = pygame.Rect(0,0,30,30)

# -- Animation Fields -- #
SeletorLoadingSquare = gtk.LoadingSquare

UIOpacity = 0
UIOpacityAnimSpeed = 15
UIOpacityAnimEnabled = True
UIOpacityAnimState = 0
UIOpacityAnim_InSoundPlayed = False
UIOpacityAnim_OutSoundPlayed = False
UIOpacity_AnimExitToOpenGame = False
UIOpacity_EnableDelay = 0
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
    global Exit_Button
    global InstalledGameList
    global ValidGameFolders
    global SelectGame_Button
    global SeletorLoadingSquare
    Exit_Button = gtk.Button(pygame.Rect(0,0,5,5), gtk.GetLangText("exit_button", "seletor"), 20)
    SelectGame_Button = gtk.Button(pygame.Rect(0,0,5,5), gtk.GetLangText("select_button", "seletor"), 20)
    InstalledGameList = gtk.HorizontalItemsView(pygame.Rect(20, 50, 760, 200))
    SeletorLoadingSquare = gtk.LoadingSquare(5,5)


    LoadGameList()

def LoadGameList():
    ValidGameFolders.clear()
    InstalledGameList.ClearItems()
    ListInstalledGames()

    for game in ValidGameFolders:
        InstalledGameList.AddItem(game)


BackgroundR = 0
BackgroundG = 0
BackgroundB = 0

def Draw(Display):
    global Exit_Button
    global DisplaySurfaceInited
    global DisplaySurface
    global TopPanel_Rect
    global UIOpacity
    global InstalledGameList
    global SelectGame_Button
    global AnimationNumb
    global SeletorLoadingSquare
    Display.fill((0, 0, 0))
    if UIOpacityAnimEnabled and UIOpacityAnimState == 0:
        SeletorLoadingSquare.Render(Display)

    if DisplaySurfaceInited:
        DisplaySurface.fill((BackgroundR, BackgroundG, BackgroundB))
        DisplaySurface.set_alpha(UIOpacity)

        gtk.Draw_Panel(DisplaySurface, TopPanel_Rect, "DOWN")

        # -- Draw the Username -- #
        sprite.RenderFont(DisplaySurface, "/UbuntuMono_Bold.ttf",24,tge.UserName, (240,240,240), 5, AnimationNumb + 5)

        # -- Render Buttons -- #
        Exit_Button.Render(DisplaySurface)
        SelectGame_Button.Render(DisplaySurface)

        # -- Render the Game List -- #
        InstalledGameList.Render(DisplaySurface)


    Display.blit(DisplaySurface, (0,0))

    # -- Set the Display Inited Variable -- #
    if not DisplaySurfaceInited:
        DisplaySurface = pygame.Surface((800,600))
        DisplaySurfaceInited = True

def Update():
    global Exit_Button
    global AnimationNumb
    global TopPanel_Rect
    global DisplaySurface
    global DisplaySurfaceInited
    global SelectGame_Button
    global InstalledGameList
    global UIOpacity_AnimExitToOpenGame
    global UIOpacityAnimEnabled
    global SeletorLoadingSquare
    AnimationNumb = UIOpacity - 255 + UIOpacityAnimSpeed

    if UIOpacityAnimEnabled and UIOpacityAnimState == 0:
        if DisplaySurfaceInited:
            SeletorLoadingSquare.X = DisplaySurface.get_width() - 38
            SeletorLoadingSquare.Y = DisplaySurface.get_height() - 38

        SeletorLoadingSquare.Update()
        SeletorLoadingSquare.Opacity = UIOpacity_EnableDelay + 50 - UIOpacity

    # -- Update Bar's Positions -- #
    if DisplaySurfaceInited:
        TopPanel_Rect = pygame.Rect(0, AnimationNumb * 1.5, DisplaySurface.get_width(), 35)

        Exit_Button.Set_X(TopPanel_Rect[2] - Exit_Button.Rectangle[2] - 5)

    InstalledGameList.SurfaceOpacity = AnimationNumb * 2.5 + 255
    InstalledGameList.Set_X(AnimationNumb * 1.5 + 20)
    SelectGame_Button.Set_X(InstalledGameList.Rectangle[0])
    SelectGame_Button.Set_Y(InstalledGameList.Rectangle[1] + InstalledGameList.Rectangle[3] + 5)

    if SelectGame_Button.ButtonState == "UP":
        if not InstalledGameList.SelectedItemIndex == -1:
            UIOpacityAnimEnabled = True
            UIOpacity_AnimExitToOpenGame = True

    # -- Update Objects Position -- #
    Exit_Button.Set_Y(AnimationNumb + 5)

    # -- Update the In/Out Animation -- #
    UpdateOpacityAnim()

def EventUpdate(event):
    global Exit_Button
    global InstalledGameList
    global SelectGame_Button
    global UIOpacityAnimEnabled
    global UIOpacity_AnimExitToOpenGame

    Exit_Button.Update(event)
    InstalledGameList.Update(event)
    SelectGame_Button.Update(event)

    if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
        if not InstalledGameList.SelectedItemIndex == -1:
            UIOpacityAnimEnabled = True
            UIOpacity_AnimExitToOpenGame = True


ItemsUnloadedAffterExiting = False
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
    global UIOpacity_EnableDelay
    UIOpacity_EnableDelay += 1

    if UIOpacityAnimEnabled and UIOpacity_EnableDelay >= reg.ReadKey_int("TaiyouSystem/CONF/start_delay"):
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
                sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/In"))
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
                sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Out"))
                UIOpacityAnim_OutSoundPlayed = True

            if UIOpacity <= 0:  # <- Triggers Animation End
                UIOpacity = 0
                UIOpacityAnimEnabled = True
                UIOpacityAnimState = 0

                if UIOpacity_AnimExitToOpenGame:
                    loadingScreen.GameFolderToOpen = InstalledGameList.SelectedGameFolderName.rstrip()
                    taiyouUI.CurrentMenuScreen = 4

                LoadGameList() # -- Re-Load the Game List -- #
                print("Taiyou.SystemUI.AnimationTrigger : Animation End.")
