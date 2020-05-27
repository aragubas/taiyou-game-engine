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
from ENGINE import utils
from ENGINE import SPRITE as sprite
from ENGINE import SOUND as sound
from ENGINE import REGISTRY as reg
from ENGINE.TaiyouUI import loadingScreen as loadingScreen
from ENGINE.TaiyouUI import AplicationUpdateDialog as UpdateDiag

# -- Buttons -- #
Exit_Button = gtk.Button
RestartList_Button = gtk.Button
SelectGame_Button = gtk.Button
RunUpdater_Button = gtk.Button

# -- Lists -- #
InstalledGameList = gtk.HorizontalItemsView
GameAtibutesList = gtk.VerticalListWithDescription

# -- Rects -- #
TopPanel_Rect = pygame.Rect(0,0,30,30)

# -- Animation Fields -- #
SeletorLoadingSquare = gtk.LoadingSquare

# -- UI Animation -- #
UIOpacity = 0
UIOpacityAnimSpeed = 15
UIOpacityAnimEnabled = True
UIOpacityAnimState = 0
UIOpacityAnim_InSoundPlayed = False
UIOpacityAnim_OutSoundPlayed = False
UIOpacity_AnimExitToOpenGame = False
UIOpacityAnim_ListLoaded = False
UIOpacity_EnableDelay = 0
UIOpacity_EnableDelayEnabled = True
BackgroundR = 0
BackgroundG = 0
BackgroundB = 0

# -- UI Loading Animation -- #
UIOpacity_StartDelay = 5
UIOpacity_NextScreen = -1
AnimationNumb = 0

# -- UI Surface -- #
DisplaySurface = pygame.Surface((0,0))
DisplaySurfaceInited = False

# -- Game Infos -- #
GameInfosAnim_Opacity = 0
GameInfosAnim_Enabled = False
GameInfosAnim_Mode = 0
GameInfosAnim_Numb = 0
GameInfosAnim_Last = "null"
GameInfosSurface = pygame.Surface
GameInfosSurface_Dest = (5,5)
GameInfosRectBox = pygame.Rect(0,0, 300,200)
SelectedGameInfosList = list()
InformationLoaded_Last = "null"
InformationLoaded = False

# -- Application Update Dialog -- #
ApplicationUpdateDialogEnabled = False

# -- List of all valid game folders -- #
ValidGameFolders = list()

# -- Loading Task -- #
ItemsUnloadedAffterExiting = False
DownloadersCreated = False
DownloaderObj = utils.Downloader
LoadingPauseMessage = "0%"




def GameInfosAnimUpdate():
    global GameInfosAnim_Enabled
    global GameInfosAnim_Mode
    global GameInfosAnim_Opacity
    global GameInfosAnim_Numb

    if GameInfosAnim_Enabled:
        GameInfosAnim_Numb = GameInfosAnim_Opacity - 255 + 15

        if GameInfosAnim_Mode == 0:
            GameInfosAnim_Opacity += 15

            if GameInfosAnim_Opacity >= 255:
                GameInfosAnim_Numb = 0
                GameInfosAnim_Opacity = 255
                GameInfosAnim_Enabled = False
                GameInfosAnim_Mode = 1

        if GameInfosAnim_Mode == 1:
            GameInfosAnim_Opacity -= 15

            if GameInfosAnim_Opacity <= 0:
                GameInfosAnim_Numb = 0
                GameInfosAnim_Opacity = 0
                GameInfosAnim_Enabled = True
                GameInfosAnim_Mode = 0




def ListInstalledGames():
    ValidGameFolders = list()
    print("ListInstalledGames : Init")
    Dirs = [ f.path for f in os.scandir(".") if f.is_dir() ]

    for D in Dirs:
        print("ListInstalledGames : Analising Directory[" + D + "]")

        if os.path.isfile(D + "/meta.data"):
            print("ListInstalledGames : Directory is a Game Directory!")
            ValidGameFolders.append(D)
        else:
            print("ListInstalledGames : Directory is invalid.")
    return ValidGameFolders




def Initialize():
    global Exit_Button
    global InstalledGameList
    global ValidGameFolders
    global SelectGame_Button
    global SeletorLoadingSquare
    global UIOpacity_StartDelay
    global RestartList_Button
    global GameAtibutesList
    global DownloaderObj
    global RunUpdater_Button
    global GameInfosSurface
    global GameInfosRectBox
    Exit_Button = gtk.Button(pygame.Rect(0,0,5,5), gtk.GetLangText("options_button", "seletor"), 20)
    SelectGame_Button = gtk.Button(pygame.Rect(0,0,5,5), gtk.GetLangText("select_button", "seletor"), 20)
    InstalledGameList = gtk.HorizontalItemsView(pygame.Rect(20, 50, 760, 200))
    RestartList_Button = gtk.Button(pygame.Rect(0,0,5,5), gtk.GetLangText("restart_button", "seletor"), 20)
    SeletorLoadingSquare = gtk.LoadingSquare(5,5)
    GameAtibutesList = gtk.VerticalListWithDescription(pygame.Rect(0, 0, 370, 300))
    RunUpdater_Button = gtk.Button(pygame.Rect(5,5,5,5), gtk.GetLangText("updater_button", "seletor"), 20)
    RunUpdater_Button.CustomColisionRectangle = True
    DownloaderObj = utils.Downloader()

    GameInfosSurface = pygame.Surface((GameAtibutesList.Rectangle[2] + GameInfosRectBox[2], GameAtibutesList.Rectangle[3]))

    GameAtibutesList.AddItem(gtk.GetLangText("title_info", "seletor/atribute_list/title"), gtk.GetLangText("title_desc", "seletor/atribute_list"))
    GameAtibutesList.AddItem(gtk.GetLangText("local_info", "seletor/atribute_list/title"), gtk.GetLangText("local_desc", "seletor/atribute_list"))
    GameAtibutesList.AddItem(gtk.GetLangText("online_info", "seletor/atribute_list/title"), gtk.GetLangText("online_desc", "seletor/atribute_list"))

    UIOpacity_StartDelay = reg.ReadKey_int("TaiyouSystem/CONF/start_delay")

    UpdateDiag.Initialize()

    LoadGameList()




def LoadGameList():
    global ValidGameFolders
    print("TaiyouUI.LoadGameList : Started")
    ValidGameFolders.clear()
    InstalledGameList.ClearItems()
    ValidGameFolders = ListInstalledGames()

    for game in ValidGameFolders:
        InstalledGameList.AddItem(game)
    print("TaiyouUI.LoadGameList : Game List has been reloaded.")




def UnloadGameList():
    print("TaiyouUI.UnloadGameList : Started")
    ValidGameFolders.clear()
    InstalledGameList.ClearItems()
    print("TaiyouUI.UnloadGameList : Game List has been unloaded.")




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
    global RunUpdater_Button
    global UIOpacity_EnableDelayEnabled
    global ApplicationUpdateDialogEnabled
    Display.fill((0, 0, 0, 0))

    if UIOpacityAnimEnabled and UIOpacityAnimState == 0:
        SeletorLoadingSquare.Render(Display)

        if not UIOpacity_EnableDelayEnabled and UIOpacity_EnableDelay <= UIOpacity_StartDelay:
            sprite.RenderFont(Display, "/Ubuntu_Bold.ttf", 18, LoadingPauseMessage, (240,240,240), 5, 600 - 23)

    if DisplaySurfaceInited and not ApplicationUpdateDialogEnabled:
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

        if not InstalledGameList.SelectedItemIndex == -1:
            RenderGameInfos(DisplaySurface)
    Display.blit(DisplaySurface, (0,0))

    if ApplicationUpdateDialogEnabled:
        UpdateDiag.Draw(Display)

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
    global ApplicationUpdateDialogEnabled
    global RunUpdater_Button

    AnimationNumb = UIOpacity - 255 + UIOpacityAnimSpeed

    UpdateGameInfos()

    if ApplicationUpdateDialogEnabled:
        UpdateDiag.Update()

    if UIOpacityAnimEnabled and UIOpacityAnimState == 0:
        if DisplaySurfaceInited:
            SeletorLoadingSquare.X = DisplaySurface.get_width() - 38
            SeletorLoadingSquare.Y = DisplaySurface.get_height() - 38

        SeletorLoadingSquare.Update()
        SeletorLoadingSquare.Opacity = UIOpacity_EnableDelay + 50 - UIOpacity

    # -- Update Bar's Positions -- #
    if DisplaySurfaceInited and not ApplicationUpdateDialogEnabled:
        TopPanel_Rect = pygame.Rect(0, AnimationNumb, DisplaySurface.get_width(), 35)

        Exit_Button.Set_X(TopPanel_Rect[2] - Exit_Button.Rectangle[2] - 5)

        InstalledGameList.SurfaceOpacity = AnimationNumb * 2.5 + 255
        InstalledGameList.Set_X(AnimationNumb * 1.5 + 20)
        SelectGame_Button.Set_X(InstalledGameList.Rectangle[0])
        SelectGame_Button.Set_Y(InstalledGameList.Rectangle[1] + InstalledGameList.Rectangle[3] + 5)

        RestartList_Button.Set_X(Exit_Button.Rectangle[0] - RestartList_Button.Rectangle[2] - 5)
        RestartList_Button.Set_Y(Exit_Button.Rectangle[1])

        # -- Refresh Button -- #
        if RestartList_Button.ButtonState == "UP":
            UIOpacity_AnimExitToOpenGame = False
            UIOpacityAnimEnabled = True

        if SelectGame_Button.ButtonState == "UP":
            if not InstalledGameList.SelectedItemIndex == -1:
                UIOpacityAnimEnabled = True
                UIOpacity_AnimExitToOpenGame = True

        # -- Update Objects Position -- #
        Exit_Button.Set_Y(AnimationNumb + 5)

    # -- Update the In/Out Animation -- #
    UpdateOpacityAnim()
    GameInfosAnimUpdate()




def UpdateGameInfos():
    global GameAtibutesList
    global GameInfosRectBox
    global InformationLoaded
    global InformationLoaded_Last
    global GameInfosSurface
    global ApplicationUpdateDialogEnabled
    global RunUpdater_Button
    global GameInfosAnim_Numb
    global GameInfosSurface_Dest

    GameInfosSurface_Dest = (GameInfosAnim_Numb + 5, 600 - GameInfosRectBox[3] - 5)

    if not InformationLoaded_Last == InstalledGameList.SelectedItem:
        # -- Get Selected Game Infos List -- #
        SelectedGameInfosList.clear()

        # -- Title Informations -- #
        SelectedGameInfosList.append(InstalledGameList.SelectedItem.rstrip())
        SelectedGameInfosList.append(InstalledGameList.SelectedGameVersion.rstrip())
        SelectedGameInfosList.append(InstalledGameList.SelectedGameID.rstrip())
        SelectedGameInfosList.append(InstalledGameList.SelectedGameFolderName.rstrip())

        GameInfosRectBox = pygame.Rect(GameAtibutesList.Rectangle[2] + 5, GameAtibutesList.Rectangle[1], GameAtibutesList.Rectangle[2] + 20, GameAtibutesList.Rectangle[3])

        GameInfosSurface = pygame.Surface((GameAtibutesList.Rectangle[2] + GameInfosRectBox[2] - 10, GameAtibutesList.Rectangle[3]))

        GameAtibutesList.ColisionXOffset = 5
        GameAtibutesList.ColisionYOffset = 600 - GameInfosRectBox[3] - 5

    if GameAtibutesList.LastItemClicked == gtk.GetLangText("online_info", "seletor/atribute_list/title"):
        # -- Run Updater Button -- #
        RunUpdater_Button.Set_X(GameInfosRectBox[0] + 15)
        RunUpdater_Button.Set_Y(GameInfosRectBox[1] + GameInfosRectBox[3] - 32)

        RunUpdater_Button.Set_ColisionX(GameInfosSurface_Dest[0] + RunUpdater_Button.Rectangle[0])
        RunUpdater_Button.Set_ColisionY(GameInfosSurface_Dest[1] + RunUpdater_Button.Rectangle[1])

        # -- Update Button -- #
        if RunUpdater_Button.ButtonState == "UP":
            # -- Set Variables -- #
            ApplicationUpdateDialogEnabled = True
            UpdateDiag.ApplicationID = InstalledGameList.SelectedGameID.rstrip()
            UpdateDiag.ApplicationName = InstalledGameList.SelectedItem.rstrip()
            UpdateDiag.ApplicationVersion = float(InstalledGameList.SelectedGameVersion.rstrip())
            UpdateDiag.ApplicationFolder = InstalledGameList.SelectedGameFolderName.rstrip()
            RunUpdater_Button.ButtonState = "INACTIVE"




def RenderGameInfos(Display):
    global GameInfosRectBox
    global GameInfosAnim_Last
    global GameInfosAnim_Enabled
    global GameInfosSurface
    global GameInfosAnim_Numb
    global GameAtibutesList
    global GameInfosAnim_Opacity
    global GameInfosSurface_Dest

    if not GameInfosAnim_Last == InstalledGameList.SelectedItemIndex:
        GameInfosAnim_Last = InstalledGameList.SelectedItemIndex
        GameInfosAnim_Enabled = True

    # -- Clear the Surface -- #
    GameInfosSurface.fill((BackgroundR, BackgroundG, BackgroundB))
    GameInfosSurface.set_alpha(GameInfosAnim_Opacity)

    # -- Render Games Info List -- #
    GameAtibutesList.Render(GameInfosSurface)


    # -- Render Infos Box -- #
    gtk.Draw_Panel(GameInfosSurface, GameInfosRectBox, "BORDER")

    if GameAtibutesList.LastItemClicked == gtk.GetLangText("title_info", "seletor/atribute_list/title"):
        RenderTitleInformation(GameInfosSurface)

    if GameAtibutesList.LastItemClicked == gtk.GetLangText("local_info", "seletor/atribute_list/title"):
        RenderLocalInformation(GameInfosSurface)

    if GameAtibutesList.LastItemClicked == gtk.GetLangText("online_info", "seletor/atribute_list/title"):
        RenderOnlineInformation(GameInfosSurface)

    Display.blit(GameInfosSurface, GameInfosSurface_Dest)




def RenderTitleInformation(Display):
    global SelectedGameInfosList
    Text = gtk.GetLangText("title_info", "seletor/atribute_list/txt").format(SelectedGameInfosList[0], SelectedGameInfosList[1], SelectedGameInfosList[2], SelectedGameInfosList[3])

    sprite.RenderFont(Display, "/Ubuntu_Bold.ttf", 14, Text, (230,230,230), GameInfosRectBox[0] + 5, GameInfosRectBox[1] + 25, True)




def RenderLocalInformation(Display):
    Text = gtk.GetLangText("local_info", "seletor/atribute_list/txt").format(InstalledGameList.SelectedGameFolderInfos[0], InstalledGameList.SelectedGameFolderInfos[1])

    sprite.RenderFont(Display, "/Ubuntu_Bold.ttf", 14, Text, (230,230,230), GameInfosRectBox[0] + 5, GameInfosRectBox[1] + 25, True)




def RenderOnlineInformation(Display):
    global RunUpdater_Button
    RunUpdater_Button.Render(Display)




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
    global ApplicationUpdateDialogEnabled
    global RunUpdater_Button

    # -- Update Buttons -- #
    if not ApplicationUpdateDialogEnabled:
        Exit_Button.Update(event)
        SelectGame_Button.Update(event)
        RestartList_Button.Update(event)
        RunUpdater_Button.Update(event)

        # -- Update Lists -- #
        InstalledGameList.Update(event)

        EventGameInfos(event)

        if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
            if not InstalledGameList.SelectedItemIndex == -1:
                UIOpacityAnimEnabled = True
                UIOpacity_AnimExitToOpenGame = True

    # -- Event Application Update Ready Message -- #
    if ApplicationUpdateDialogEnabled:
        UpdateDiag.EventUpdate(event)





def LoadingTasks():
    global UIOpacityAnim_ListLoaded
    global UIOpacity_EnableDelay
    global UIOpacity_EnableDelayEnabled
    global DownloadersCreated
    global DownloaderObj
    if UIOpacity_EnableDelay == 20: # -- Loading Task 1
        UIOpacityAnim_ListLoaded = True
        LoadGameList()

def DownloadFileInLoading(Url, FilePath):
    global DownloadersCreated
    global UIOpacity_EnableDelayEnabled
    global LoadingPauseMessage

    UIOpacity_EnableDelayEnabled = False

    if not DownloadersCreated:
        DownloaderObj.StartDownload(reg.ReadKey("/TaiyouSystem/TaiyouOnlineServer") + Url, FilePath)
        DownloadersCreated = True

    if DownloaderObj.DownloadState == "DOWNLOADING":
        LoadingPauseMessage = str(DownloaderObj.DownloadMetaData[1]) + "%"
    if DownloaderObj.DownloadState == "STARTING":
        LoadingPauseMessage = "Starting download of: [" + Url + "]..."

    # -- Detect Download End -- #
    if DownloaderObj.DownloadMetaData[1] == 100:
        UIOpacity_EnableDelayEnabled = True
        DownloadersCreated = False


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
    global GameInfosAnim_Last
    global GameInfosAnim_Enabled
    global GameInfosAnim_Opacity
    global GameInfosAnim_Mode
    global GameInfosAnim_Numb

    if not ApplicationUpdateDialogEnabled:
        if UIOpacity_EnableDelayEnabled:
            UIOpacity_EnableDelay += 1

        LoadingTasks()

    if UIOpacityAnimEnabled and UIOpacity_EnableDelay >= UIOpacity_StartDelay and not ApplicationUpdateDialogEnabled:
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


                # -- Restart Atribute Error -- #
                GameInfosAnim_Last = -1
                GameInfosAnim_Opacity = 0
                GameInfosAnim_Mode = 0
                GameInfosAnim_Numb = 0
                GameInfosAnim_Enabled = True

                UnloadGameList() # -- Re-Load the Game List -- #
                if not UIOpacity_NextScreen == -1:
                    taiyouUI.CurrentMenuScreen = UIOpacity_NextScreen

                print("Taiyou.SystemUI.AnimationTrigger : Animation End.")
