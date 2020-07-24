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
import pygame, os, sys, shutil
from ENGINE import SPRITE as sprite
from ENGINE import SOUND as sound
from ENGINE.TaiyouUI import UIGTK as gtk
from ENGINE import TaiyouUI as taiyouUI
import ENGINE as tge
from ENGINE.TaiyouUI.GameOverlay import SystemVolumeSlider as volumeSlider
from ENGINE import utils
from ENGINE import SPRITE as sprite
from ENGINE import SOUND as sound
from ENGINE import REGISTRY as reg
from ENGINE.TaiyouUI import loadingScreen as loadingScreen
from ENGINE.TaiyouUI import OverlayDialog as ovelDiag
from ENGINE.TaiyouUI.GameSeletor import GameInfos
from ENGINE import DEBUGGING as debug

# -- Buttons -- #
RestartList_Button = gtk.Button
SelectApplication_Button = gtk.Button

# -- Lists -- #
InstalledGameList = gtk.InstalledApplicationList

# -- Rects -- #
TopPanel_Rect = pygame.Rect(0,0,30,30)

# -- Animation Fields -- #
SeletorLoadingSquare = gtk.LoadingSquare

# -- Animation Controllers -- #
GlobalAnimation_Controller = utils.AnimationController

# -- UI Animation -- #
UIOpacity = 0
UIOpacityAnim_InSoundPlayed = False
UIOpacityAnim_OutSoundPlayed = False
UIOpacity_AnimExitToOpenApplication = False
UIOpacityAnim_ListLoaded = False
UIOpacity_EnableDelay = 0
UIOpacity_EnableDelayEnabled = True
BackgroundR = 0
BackgroundG = 0
BackgroundB = 0

# -- UI Loading Animation -- #
UIOpacity_StartDelay = 10
UIOpacity_NextScreen = -1
AnimationNumb = 0

# -- UI Surface -- #
DisplaySurface = pygame.Surface((0,0))
DisplaySurfaceInited = False

# -- List of all valid game folders -- #
ValidGameFolders = list()

# -- Loading Task -- #
ItemsUnloadedAffterExiting = False
DownloadersCreated = False
DownloaderObj = utils.Downloader
LoadingPauseMessage = "NULL"

SelectedGameInfo = ("nul", "nul", "nul", "nul", sprite.DefaultSprite) # 0 == Game ID; 1 == Game Name; 2 == Game Version; 3 == Game Folder


def ListInstalledGames():
    ValidGameFolders = list()
    print("ListInstalledGames : Init")
    Dirs = [ f.path for f in os.scandir(".") if f.is_dir() ]

    for D in Dirs:
        print("ListInstalledGames : Analising Directory[" + D + "]")

        if os.path.isfile(D + "/meta.data"):
            print("ListInstalledGames : Directory is a Application Directory")
            ValidGameFolders.append(D)
        else:
            print("ListInstalledGames : Directory is invalid.")
    return ValidGameFolders

def Initialize():
    global InstalledGameList
    global ValidGameFolders
    global SelectApplication_Button
    global SeletorLoadingSquare
    global UIOpacity_StartDelay
    global RestartList_Button
    global DownloaderObj
    global GlobalAnimation_Controller

    SelectApplication_Button = gtk.Button(pygame.Rect(0, 0, 5, 5), gtk.GetLangText("select_button", "seletor"), 20)
    InstalledGameList = gtk.InstalledApplicationList(pygame.Rect(20, 50, 760, 200))
    RestartList_Button = gtk.Button(pygame.Rect(0,0,5,5), gtk.GetLangText("restart_button", "seletor"), 20)
    SeletorLoadingSquare = gtk.LoadingSquare(5,5)
    DownloaderObj = utils.Downloader()

    UIOpacity_StartDelay = reg.ReadKey_int("/TaiyouSystem/CONF/start_delay", True)

    ovelDiag.Initialize()
    GameInfos.Initialize()

    # -- Initialize Volume Slider -- #
    volumeSlider.Initialize()

    # -- Set Animation Controllers -- #
    GlobalAnimation_Controller = utils.AnimationController()


def LoadGameList():
    global ValidGameFolders
    print("TaiyouUI.LoadGameList : Started")
    UnloadGameList()

    ValidGameFolders = ListInstalledGames()

    for game in ValidGameFolders:
        InstalledGameList.AddItem(game)

    print("TaiyouUI.LoadGameList : Game List has been reloaded.")


def UnloadGameList():
    global ValidGameFolders
    global InstalledGameList

    print("TaiyouUI.UnloadGameList : Started")
    ValidGameFolders.clear()
    InstalledGameList.ClearItems()

    utils.GarbageCollector_Collect()
    del InstalledGameList
    utils.GarbageCollector_Collect()

    InstalledGameList = gtk.InstalledApplicationList(pygame.Rect(20, 50, 760, 200))

    print("TaiyouUI.UnloadGameList : Game List has been unloaded.")


def Draw(Display):
    global DisplaySurfaceInited
    global DisplaySurface
    global TopPanel_Rect
    global UIOpacity
    global InstalledGameList
    global SelectApplication_Button
    global AnimationNumb
    global SeletorLoadingSquare
    global RestartList_Button
    global UIOpacity_EnableDelayEnabled
    Display.fill((0, 0, 0))

    if GlobalAnimation_Controller.Enabled and GlobalAnimation_Controller.CurrentMode:
        SeletorLoadingSquare.Render(Display)

        if not UIOpacity_EnableDelayEnabled and UIOpacity_EnableDelay <= UIOpacity_StartDelay:
            sprite.FontRender(Display, "/Ubuntu_Bold.ttf", 18, LoadingPauseMessage, (240, 240, 240), 5, 600 - 23)

    if DisplaySurfaceInited:
        DisplaySurface.fill((BackgroundR, BackgroundG, BackgroundB))
        DisplaySurface.set_alpha(UIOpacity)

        gtk.Draw_Panel(DisplaySurface, TopPanel_Rect, "DOWN")

        # -- Draw the Username -- #
        sprite.FontRender(DisplaySurface, "/UbuntuMono_Bold.ttf", 24, tge.UserName, (240, 240, 240), 5, AnimationNumb + 5)

        # -- Render Buttons -- #
        SelectApplication_Button.Render(DisplaySurface)
        RestartList_Button.Render(DisplaySurface)

        # -- Render the Game List -- #
        InstalledGameList.Render(DisplaySurface)

        if not InstalledGameList.SelectedItemIndex == -1:
            GameInfos.Draw(DisplaySurface)

        # -- Render Volume Slider -- #
        volumeSlider.Draw(DisplaySurface)

    Display.blit(DisplaySurface, (0,0))

    # -- Set the Display Inited Variable -- #
    if not DisplaySurfaceInited:
        DisplaySurface = pygame.Surface((800,600))
        DisplaySurfaceInited = True

def Update():
    global AnimationNumb
    global TopPanel_Rect
    global DisplaySurface
    global DisplaySurfaceInited
    global SelectApplication_Button
    global InstalledGameList
    global UIOpacity_AnimExitToOpenApplication
    global UIOpacityAnimEnabled
    global SeletorLoadingSquare
    global RestartList_Button
    global UIOpacity_EnableDelay
    global SelectedGameInfo

    # -- Set the Animation Numb -- #
    AnimationNumb = UIOpacity - 253

    # -- Update Game Infos -- #
    if not InstalledGameList.SelectedItemIndex == -1:
        GameInfos.Update()

    # -- Set Correct Subscreen -- #
    ovelDiag.Subscreen = 1

    # -- Update Loading Square -- #
    if GlobalAnimation_Controller.Enabled and GlobalAnimation_Controller.CurrentMode:
        if DisplaySurfaceInited:
            SeletorLoadingSquare.X = DisplaySurface.get_width() - 38
            SeletorLoadingSquare.Y = DisplaySurface.get_height() - 38

        SeletorLoadingSquare.Update()
        SeletorLoadingSquare.Opacity = UIOpacity_EnableDelay + 50 - UIOpacity

    # -- Update Bar's Positions -- #
    if DisplaySurfaceInited:
        TopPanel_Rect = pygame.Rect(0, AnimationNumb, DisplaySurface.get_width(), 35)

        InstalledGameList.SurfaceOpacity = AnimationNumb * 2.5 + 255
        InstalledGameList.Set_X(AnimationNumb * 1.5 + 20)
        SelectApplication_Button.Set_X(InstalledGameList.Rectangle[0])
        SelectApplication_Button.Set_Y(InstalledGameList.Rectangle[1] + InstalledGameList.Rectangle[3] + 5)

        RestartList_Button.Set_X(TopPanel_Rect[2] - RestartList_Button.Rectangle[2] - 37)
        RestartList_Button.Set_Y(AnimationNumb + 3)

        volumeSlider.ObjX = DisplaySurface.get_width() - 35
        volumeSlider.ObjY = RestartList_Button.Rectangle[1]
        volumeSlider.Update()

        # -- Update Selected Game Infos List -- #
        if not InstalledGameList.SelectedApplicationID == -1:
            SelectedGameInfo = (InstalledGameList.SelectedApplicationID.rstrip(), InstalledGameList.SelectedItem.rstrip(), InstalledGameList.SelectedApplicationVersion.rstrip(), InstalledGameList.SelectedApplicationFolderName.rstrip(), InstalledGameList.SelectedApplicationIcon)

        # -- Refresh Button -- #
        if RestartList_Button.ButtonState == 2:
            UIOpacity_AnimExitToOpenApplication = False
            GlobalAnimation_Controller.Enabled = True

        if SelectApplication_Button.ButtonState == 2:
            if not InstalledGameList.SelectedApplicationID == -1:
                UIOpacity_AnimExitToOpenApplication = True
                GlobalAnimation_Controller.Enabled = True

    # -- Update the In/Out Animation -- #
    UpdateOpacityAnim()

def EventUpdate(event):
    global InstalledGameList
    global SelectApplication_Button
    global UIOpacity_AnimExitToOpenApplication
    global RestartList_Button

    # -- Update Buttons -- #
    SelectApplication_Button.Update(event)
    RestartList_Button.Update(event)

    # -- Update Lists -- #
    InstalledGameList.Update(event)

    if not InstalledGameList.SelectedApplicationID == -1:
        GameInfos.EventUpdate(event)

    if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
        if not InstalledGameList.SelectedApplicationID == -1:
            GlobalAnimation_Controller.Enabled = True
            UIOpacity_AnimExitToOpenApplication = True

    volumeSlider.EventUpdate(event)



def LoadingTasks():
    global UIOpacityAnim_ListLoaded
    global UIOpacity_EnableDelay
    global UIOpacity_EnableDelayEnabled

    if UIOpacity_EnableDelay == 2:  # -- Loading Task 1
        UIOpacityAnim_ListLoaded = True
        LoadGameList()

def UpdateOpacityAnim():
    global UIOpacity
    global UIOpacityAnim_InSoundPlayed
    global UIOpacityAnim_OutSoundPlayed
    global BackgroundR
    global BackgroundG
    global BackgroundB
    global UIOpacity_EnableDelay
    global UIOpacity_StartDelay
    global UIOpacityAnim_ListLoaded
    global GlobalAnimation_Controller

    if UIOpacity_EnableDelayEnabled:
        UIOpacity_EnableDelay += 1

    LoadingTasks()

    if UIOpacity_EnableDelay >= UIOpacity_StartDelay:
        GlobalAnimation_Controller.Update()

        if GlobalAnimation_Controller.Enabled and GlobalAnimation_Controller.CurrentMode:  # <- Enter Animation
            UIOpacity = GlobalAnimation_Controller.Value

            if BackgroundR < gtk.GameSeletor_BackgroundColor[0]:
                BackgroundR += 1
            else:
                BackgroundR = gtk.GameSeletor_BackgroundColor[0]

            if BackgroundG < gtk.GameSeletor_BackgroundColor[1]:
                BackgroundG += 1
            else:
                BackgroundR = gtk.GameSeletor_BackgroundColor[1]

            if BackgroundB < gtk.GameSeletor_BackgroundColor[2]:
                BackgroundB += 1
            else:
                BackgroundR = gtk.GameSeletor_BackgroundColor[2]

            # -- Play the In Sound -- #
            if not UIOpacityAnim_InSoundPlayed:
                sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/In", True))
                UIOpacityAnim_InSoundPlayed = True

            if GlobalAnimation_Controller.Value >= 255:  # <- Triggers Animation End
                UIOpacity = 255
                UIOpacityAnim_InSoundPlayed = True
                UIOpacityAnim_OutSoundPlayed = True

        elif GlobalAnimation_Controller.Enabled and not GlobalAnimation_Controller.CurrentMode:  # <- Exit Animation
            UIOpacity = GlobalAnimation_Controller.Value

            if BackgroundR > 0:
                BackgroundR -= 1
            if BackgroundG > 0:
                BackgroundG -= 1
            if BackgroundB > 0:
                BackgroundB -= 1

            # -- Play the Out Sound -- #
            if not UIOpacityAnim_OutSoundPlayed:
                sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Out", True))
                UIOpacityAnim_OutSoundPlayed = True

        if GlobalAnimation_Controller.Value <= 0 and not GlobalAnimation_Controller.Enabled and GlobalAnimation_Controller.CurrentMode:  # <- Triggers Animation End
            UIOpacityAnim_ListLoaded = False
            UIOpacity_EnableDelay = 0

            # -- Open the Selected Game -- #
            if UIOpacity_AnimExitToOpenApplication:
                loadingScreen.GameFolderToOpen = InstalledGameList.SelectedApplicationFolderName.rstrip()
                loadingScreen.GameIcon = SelectedGameInfo[4]
                taiyouUI.CurrentMenuScreen = 4

            # -- Re-Load the Game List -- #
            UnloadGameList()

            # -- Set to Another Screen -- #
            if not UIOpacity_NextScreen == -1:
                taiyouUI.CurrentMenuScreen = UIOpacity_NextScreen

            GlobalAnimation_Controller.Enabled = True
