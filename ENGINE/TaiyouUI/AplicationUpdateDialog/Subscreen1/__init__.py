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
from ENGINE.TaiyouUI import GameSeletor as seletorScreen
from ENGINE.TaiyouUI import AplicationUpdateDialog as Handler

UpdateProgressBar_Rectangle = pygame.Rect
LoadingAnimSquare = gtk.LoadingSquare
UpdateProgress = 0
UpdateStep = -1
UpdateStepCanAdd = True
UpdateCompleted = False
VersionChecking = True
UpdateCompletedMessage = "update_completed"
UpdateProgressStatus = "Stopped."
FileIsDownloading = False
OK_Button = gtk.Button

def Initialize():
    global UpdateProgressBar_Rectangle
    global LoadingAnimSquare
    global OK_Button
    LoadingAnimSquare = gtk.LoadingSquare(5,5)
    UpdateProgressBar_Rectangle = pygame.Rect(5, 200, 300, 50)
    OK_Button = gtk.Button(pygame.Rect(0,0,0,0), gtk.GetLangText("ok_button"), 18)
    OK_Button.CustomColisionRectangle = True

def Draw(Display):
    global UpdateProgressBar_Rectangle
    global LoadingAnimSquare
    global DownloaderEnabled
    global UpdateCompletedMessage
    global OK_Button

    # -- Render Status Message when Updating -- #
    if not UpdateCompleted and not VersionChecking:
        sprite.RenderFont(Display, "/Ubuntu_Bold.ttf", 18, gtk.GetLangText("update_progress_text", "update_diag").format(str(UpdateStep), "6"), (240,240,240), 5, 25)

        sprite.RenderFont(Display, "/Ubuntu_Bold.ttf", 12, gtk.GetLangText("update_steps", "update_diag"), (240,240,240), 5, 50)

    elif VersionChecking and not UpdateCompleted:
        sprite.RenderFont(Display, "/Ubuntu_Bold.ttf", 18, gtk.GetLangText("version_checking", "update_diag").format(str(UpdateStep), "6"), (240,240,240), 5, 25)

    # -- Render the Downloading Progress Bar -- #
    if DownloaderEnabled and not UpdateCompleted:
        sprite.RenderFont(Display, "/Ubuntu_Bold.ttf", 14, UpdateProgressStatus.format(str(UpdateProgress)), (240,240,240), 3, UpdateProgressBar_Rectangle[1] - 18)

        LoadingAnimSquare.Render(Display)
        sprite.RenderRectangle(Display, (240,240,240), UpdateProgressBar_Rectangle)

    # -- Render the Update Complete Message -- #
    if UpdateCompleted:
        sprite.RenderFont(Display, "/Ubuntu_Bold.ttf", 14, gtk.GetLangText(UpdateCompletedMessage, "update_diag"), (240,240,240), 5, 25)

        OK_Button.Render(Display)




def Update():
    global UpdateProgressBar_Rectangle
    global UpdateProgress
    global LoadingAnimSquare
    global OK_Button
    global DownloaderEnabled
    global UpdateStep
    global UpdateStepCanAdd
    global UpdateCompleted
    global VersionChecking
    global UpdateCompletedMessage
    global UpdateProgressStatus
    global FileIsDownloading
    
    # -- Set the Title -- #
    if not VersionChecking:
        Handler.MessageTitle = gtk.GetLangText("update_in_progress_title", "update_diag")
    else:
        Handler.MessageTitle = gtk.GetLangText("version_checking_title", "update_diag")

    if not UpdateCompleted:
        Update_Steps()
    else:
        # -- Update OK Button -- #
        OK_Button.Set_ColisionX(Handler.CommonDisplayScreenPos[0] + OK_Button.Rectangle[0])
        OK_Button.Set_ColisionY(Handler.CommonDisplayScreenPos[1] + OK_Button.Rectangle[1])
        OK_Button.Set_X(5)
        OK_Button.Set_Y(Handler.CommonDisplay.get_height() - OK_Button.Rectangle[3] - 5)

        if OK_Button.ButtonState == "UP":
            OK_Button.ButtonState = "INACTIVE"

            Handler.DialogOpctAnim_AnimEnabled = True

            # -- Reset Variables -- #
            DownloaderEnabled = False
            UpdateProgress = 0
            UpdateStep = -1
            UpdateStepCanAdd = True
            UpdateCompleted = False
            VersionChecking = True
            UpdateCompletedMessage = "update_completed"
            UpdateProgressStatus = "Stopped."
            FileIsDownloading = False

    if DownloaderEnabled:
        LoadingAnimSquare.Set_Y(Handler.CommonDisplay.get_height() - 38)
        LoadingAnimSquare.Set_X(Handler.CommonDisplay.get_width() - 38)
        LoadingAnimSquare.Update()

        UpdateDownloader()


    # -- Set Progress -- #
    UpdateProgressBar_Rectangle = pygame.Rect(5, Handler.DialogRectangle[3] - 20, (Handler.DialogRectangle[2] - 44) * UpdateProgress / 100, 15)

DownloaderDownloadURL = "NULL"
DownloaderDownloadFilePath = "Taiyou/HOME/Webcache/NULL"
DownloaderDownloadStarted = False
DownloaderEnabled = False
DwObj = utils.Downloader
def UpdateDownloader():
    global DwObj
    global DownloaderDownloadURL
    global DownloaderDownloadStarted
    global DownloaderDownloadFilePath
    global UpdateProgressStatus
    global UpdateProgress
    global UpdateStepCanAdd
    global DownloaderEnabled

    if not DownloaderDownloadStarted:
        DwObj = utils.Downloader()
        DwObj.StartDownload(DownloaderDownloadURL, DownloaderDownloadFilePath)
        DownloaderDownloadStarted = True
        print("TaiyouUI.ApplicationUpdateDiag.UpdateDownloader : Downloader Started:\nUrl[" + DownloaderDownloadURL + "]\nPath:[" + DownloaderDownloadFilePath + "]")

    if DwObj.DownloadState == "STARTING":
        UpdateProgressStatus = gtk.GetLangText("download_status_starting", "update_diag")
        UpdateStepCanAdd = False

    if DwObj.DownloadState == "DOWNLOADING":
        UpdateProgressStatus = gtk.GetLangText("download_status_downloading", "update_diag")
        UpdateProgress = int(DwObj.DownloadMetaData[1])
        UpdateStepCanAdd = False

    if DwObj.DownloadState == "FINISHED":
        UpdateProgressStatus = gtk.GetLangText("download_status_finished", "update_diag")
        UpdateProgress = 0
        UpdateStepCanAdd = True


        DownloaderDownloadStarted = False
        DownloaderDownloadURL = "NULL"
        DownloaderDownloadFilePath = "Taiyou/HOME/Webcache/NULL"
        DownloaderEnabled = False
        print("TaiyouUI.ApplicationUpdateDiag.UpdateDownloader : Downloader Task has been finished.")

def SetDownloadTask(Url, FilePath):
    global DownloaderDownloadURL
    global DownloaderDownloadStarted
    global DownloaderDownloadFilePath
    global UpdateProgressStatus
    global UpdateProgress
    global UpdateStepCanAdd
    global DownloaderEnabled
    global UpdateStepCanAdd

    DownloaderDownloadURL = Url
    DownloaderDownloadFilePath = FilePath
    DownloaderEnabled = True
    DownloaderDownloadStarted = False

    UpdateStepCanAdd = False

def Update_Steps():
    global UpdateStep
    global UpdateStepCanAdd
    global UpdateCompleted
    global UpdateCompletedMessage
    global VersionChecking

    if UpdateStepCanAdd:
        UpdateStep += 1

        if UpdateStep == 0: # -- Download Current Version Data -- #
            print("TaiyouUI.ApplicationUpdateDiag : Update Step; 0")
            TaskUrl = reg.ReadKey("/TaiyouSystem/TaiyouOnlineGameIDPath") + Handler.ApplicationID + "/version"
            SetDownloadTask(TaskUrl, "Taiyou/HOME/Webcache/UPDATER/" + Handler.ApplicationID + "/version.data")

        if UpdateStep == 1: # -- Compare Versions -- #
            print("TaiyouUI.ApplicationUpdateDiag : Update Step; 1")
            if float(open("Taiyou/HOME/Webcache/UPDATER/" + Handler.ApplicationID + "/version.data").read()) == Handler.ApplicationVersion:
                UpdateCompletedMessage = "version_already_updated"
                UpdateCompleted = True
                UpdateStepCanAdd = False
                VersionChecking = False

        if UpdateStep == 2: # -- Download the new Meta Data File -- #
            print("TaiyouUI.ApplicationUpdateDiag : Update Step; 2")
            VersionChecking = False
            TaskUrl = reg.ReadKey("/TaiyouSystem/TaiyouOnlineGameIDPath") + Handler.ApplicationID + "/metaData"
            SetDownloadTask(TaskUrl, "Taiyou/HOME/Webcache/UPDATER/" + Handler.ApplicationID + "/meta.data")

        if UpdateStep == 3: # -- Download the Update File -- #
            print("TaiyouUI.ApplicationUpdateDiag : Update Step; 3")
            TaskUrl = reg.ReadKey("/TaiyouSystem/TaiyouOnlineGameIDPath") + Handler.ApplicationID + "/updateFile.zip"
            SetDownloadTask(TaskUrl, "Taiyou/HOME/Webcache/UPDATER/" + Handler.ApplicationID + "/updateFile.zip")

        if UpdateStep == 4: # -- Copy Updated Files -- #
            print("TaiyouUI.ApplicationUpdateDiag : Update Step; 4")
            UpdateStepCanAdd = False
            UpdateFileZipPath = "Taiyou/HOME/Webcache/UPDATER/" + Handler.ApplicationID + "/updateFile.zip"
            MetadataFile = "Taiyou/HOME/Webcache/UPDATER/" + Handler.ApplicationID + "/meta.data"

            print("Copy Update Zip to Game Folder")
            utils.FileCopy(UpdateFileZipPath, Handler.ApplicationFolder + "/updateFile.zip")
            utils.FileCopy(MetadataFile, Handler.ApplicationFolder + "/meta.data")

            UpdateStepCanAdd = True

        if UpdateStep == 5: # -- Unzip File  -- #
            print("TaiyouUI.ApplicationUpdateDiag : Update Step; 5")
            UpdateStepCanAdd = False
            print("Unzip File")

            ZipFilePath = Handler.ApplicationFolder + "/updateFile.zip"

            utils.Unzip_File(ZipFilePath, Handler.ApplicationFolder + "/")

            UpdateStepCanAdd = True

        if UpdateStep == 6: # -- Delete Temporary Files -- #
            print("TaiyouUI.ApplicationUpdateDiag : Update Step; 6")
            UpdateStepCanAdd = False

            utils.Directory_Remove("Taiyou/HOME/Webcache/UPDATER/" + Handler.ApplicationID) # Delete All downloaded files
            utils.File_Delete(Handler.ApplicationFolder + "/updateFile.zip")

            UpdateStepCanAdd = True
            UpdateCompleted = True
            UpdateCompletedMessage = "update_completed"
            VersionChecking = True


def EventUpdate(event):
    global OK_Button
    global UpdateCompleted

    if UpdateCompleted:
        OK_Button.Update(event)