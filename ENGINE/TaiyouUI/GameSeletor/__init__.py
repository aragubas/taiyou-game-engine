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
RestartList_Button = gtk.Button
SelectGame_Button = gtk.Button

# -- Lists -- #
InstalledGameList = gtk.HorizontalItemsView
GameAtibutesList = gtk.VerticalListWithDescription

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
UIOpacityAnim_ListLoaded = False
UIOpacity_EnableDelay = 0
UIOpacity_StartDelay = 5
UIOpacity_NextScreen = -1
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
    global UIOpacity_StartDelay
    global RestartList_Button
    global GameAtibutesList
    Exit_Button = gtk.Button(pygame.Rect(0,0,5,5), gtk.GetLangText("options_button", "seletor"), 20)
    SelectGame_Button = gtk.Button(pygame.Rect(0,0,5,5), gtk.GetLangText("select_button", "seletor"), 20)
    InstalledGameList = gtk.HorizontalItemsView(pygame.Rect(20, 50, 760, 200))
    RestartList_Button = gtk.Button(pygame.Rect(0,0,5,5), gtk.GetLangText("restart_button", "seletor"), 20)
    SeletorLoadingSquare = gtk.LoadingSquare(5,5)
    GameAtibutesList = gtk.VerticalListWithDescription(pygame.Rect(5, 600 - 305, 370, 300))

    GameAtibutesList.AddItem("Title Information", "Title, ID, Version...")
    GameAtibutesList.AddItem("Local Information", "Size, Files...")
    GameAtibutesList.AddItem("Online Information", "is Registred Game, Online Version, Patch Notes")

    UIOpacity_StartDelay = reg.ReadKey_int("TaiyouSystem/CONF/start_delay")



    LoadGameList()

def LoadGameList():
    print("TaiyouUI.LoadGameList : Started")
    ValidGameFolders.clear()
    InstalledGameList.ClearItems()
    ListInstalledGames()

    for game in ValidGameFolders:
        InstalledGameList.AddItem(game)
    print("TaiyouUI.LoadGameList : Game List has been reloaded.")

def UnloadGameList():
    print("TaiyouUI.UnloadGameList : Started")
    ValidGameFolders.clear()
    InstalledGameList.ClearItems()
    print("TaiyouUI.UnloadGameList : Game List has been unloaded.")

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
    global RestartList_Button
    global GameAtibutesList

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
        RestartList_Button.Render(DisplaySurface)

        # -- Render the Game List -- #
        InstalledGameList.Render(DisplaySurface)

        RenderGameInfos(DisplaySurface)


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
    global RestartList_Button
    global UIOpacity_EnableDelay

    AnimationNumb = UIOpacity - 255 + UIOpacityAnimSpeed

    UpdateGameInfos()


    if UIOpacityAnimEnabled and UIOpacityAnimState == 0:
        if DisplaySurfaceInited:
            SeletorLoadingSquare.X = DisplaySurface.get_width() - 38
            SeletorLoadingSquare.Y = DisplaySurface.get_height() - 38

        SeletorLoadingSquare.Update()
        SeletorLoadingSquare.Opacity = UIOpacity_EnableDelay + 50 - UIOpacity

    # -- Refresh Button -- #
    if RestartList_Button.ButtonState == "UP":
        UIOpacity_AnimExitToOpenGame = False
        UIOpacityAnimEnabled = True

    # -- Update Bar's Positions -- #
    if DisplaySurfaceInited:
        TopPanel_Rect = pygame.Rect(0, AnimationNumb * 1.5, DisplaySurface.get_width(), 35)

        Exit_Button.Set_X(TopPanel_Rect[2] - Exit_Button.Rectangle[2] - 5)

        InstalledGameList.SurfaceOpacity = AnimationNumb * 2.5 + 255
        InstalledGameList.Set_X(AnimationNumb * 1.5 + 20)
        SelectGame_Button.Set_X(InstalledGameList.Rectangle[0])
        SelectGame_Button.Set_Y(InstalledGameList.Rectangle[1] + InstalledGameList.Rectangle[3] + 5)

        RestartList_Button.Set_X(Exit_Button.Rectangle[0] - RestartList_Button.Rectangle[2] - 5)
        RestartList_Button.Set_Y(Exit_Button.Rectangle[1])

        if SelectGame_Button.ButtonState == "UP":
            if not InstalledGameList.SelectedItemIndex == -1:
                UIOpacityAnimEnabled = True
                UIOpacity_AnimExitToOpenGame = True

        # -- Update Objects Position -- #
        Exit_Button.Set_Y(AnimationNumb + 5)

    # -- Update the In/Out Animation -- #
    UpdateOpacityAnim()


GameInfosRectBox = pygame.Rect(0,0, 300,200)
InformationLoaded_Last = "null"
InformationLoaded = False
SelectedGameInfosList = list()
def UpdateGameInfos():
    global GameAtibutesList
    global GameInfosRectBox
    global InformationLoaded
    global InformationLoaded_Last

    if not InformationLoaded_Last == InstalledGameList.SelectedItem:
        # -- Get Selected Game Infos List -- #
        SelectedGameInfosList.clear()

        # -- Title Informations -- #
        SelectedGameInfosList.append(InstalledGameList.SelectedItem)
        SelectedGameInfosList.append(InstalledGameList.SelectedGameVersion)
        SelectedGameInfosList.append(InstalledGameList.SelectedGameID)
        SelectedGameInfosList.append(InstalledGameList.SelectedGameFolderName)


        # -- Local Informations -- #

        SelectedGameInfosList.append(tge.utils.FormatNumber(tge.utils.Calculate_FolderSize(InstalledGameList.SelectedGameFolderName.rstrip()), 2, ['B', 'Kb', 'MB', 'GB', 'TB']))
        SelectedGameInfosList.append(tge.utils.Get_DirectoryTotalOfFiles(InstalledGameList.SelectedGameFolderName.rstrip()))

        InformationLoaded_Last = InstalledGameList.SelectedItem



    GameInfosRectBox = pygame.Rect(GameAtibutesList.Rectangle[0] + GameAtibutesList.Rectangle[2] + 5, GameAtibutesList.Rectangle[1], GameAtibutesList.Rectangle[2] + 20, GameAtibutesList.Rectangle[3])

def RenderGameInfos(Display):
    global GameInfosRectBox
    # -- Render Games Info List -- #
    GameAtibutesList.Render(Display)

    # -- Render Infos Box -- #
    gtk.Draw_Panel(Display, GameInfosRectBox, "BORDER")


    if GameAtibutesList.LastItemClicked == "Title Information":
        RenderTitleInformation(Display)

    if GameAtibutesList.LastItemClicked == "Local Information":
        RenderLocalInformation(Display)

    if GameAtibutesList.LastItemClicked == "Online Information":
        RenderOnlineInformation(Display)

def RenderTitleInformation(Display):
    global SelectedGameInfosList
    Text = "Title: {0}\n" \
           "Version: {1}\n" \
           "ID: {2}\n" \
           "Game Folder: {3}".format(SelectedGameInfosList[0], SelectedGameInfosList[1], SelectedGameInfosList[2], SelectedGameInfosList[3])

    sprite.RenderFont(Display, "/Ubuntu_Bold.ttf", 14, Text, (230,230,230), GameInfosRectBox[0] + 5, GameInfosRectBox[1] + 25, True)


def RenderLocalInformation(Display):
    Text = "Folder Size: {0}\n" \
           "Number of Files: {1}".format(SelectedGameInfosList[4], SelectedGameInfosList[5])

    sprite.RenderFont(Display, "/Ubuntu_Bold.ttf", 14, Text, (230,230,230), GameInfosRectBox[0] + 5, GameInfosRectBox[1] + 25, True)


def RenderOnlineInformation(Display):
    sprite.Render(Display, "/TAIYOU_UI/Cursor/1.png", 5, 5, 20, 20)


def EventGameInfos(event):
    # -- Render Games Info List -- #
    GameAtibutesList.Update(event)





def EventUpdate(event):
    global Exit_Button
    global InstalledGameList
    global SelectGame_Button
    global UIOpacityAnimEnabled
    global UIOpacity_AnimExitToOpenGame
    global RestartList_Button
    global GameAtibutesList

    # -- Update Buttons -- #
    Exit_Button.Update(event)
    SelectGame_Button.Update(event)
    RestartList_Button.Update(event)

    # -- Update Lists -- #
    InstalledGameList.Update(event)

    EventGameInfos(event)

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
    global UIOpacity_StartDelay
    global UIOpacityAnim_ListLoaded
    UIOpacity_EnableDelay += 1

    if not UIOpacityAnim_ListLoaded and UIOpacity_EnableDelay == 20:
        UIOpacityAnim_ListLoaded = True
        LoadGameList()

    if UIOpacityAnimEnabled and UIOpacity_EnableDelay >= UIOpacity_StartDelay:
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
                UIOpacityAnim_ListLoaded = False
                UIOpacity_EnableDelay = 0

                if UIOpacity_AnimExitToOpenGame:
                    loadingScreen.GameFolderToOpen = InstalledGameList.SelectedGameFolderName.rstrip()
                    taiyouUI.CurrentMenuScreen = 4

                UnloadGameList() # -- Re-Load the Game List -- #
                if not UIOpacity_NextScreen == -1:
                    taiyouUI.CurrentMenuScreen = UIOpacity_NextScreen

                print("Taiyou.SystemUI.AnimationTrigger : Animation End.")
