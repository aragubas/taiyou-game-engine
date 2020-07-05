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
from ENGINE.TaiyouUI import OverlayDialog as Handler

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
IsMetadataUpdate = False
DownloadError = False

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
    global DwObj

    # -- Render Status Message when Updating -- #
    if not UpdateCompleted and not VersionChecking and not DownloadError:
        if not IsMetadataUpdate:
            sprite.FontRender(Display, "/Ubuntu_Bold.ttf", 18, gtk.GetLangText("update_progress_text", "update_diag").format(str(UpdateStep), "6"), (240, 240, 240), 5, 25)
        else:
            sprite.FontRender(Display, "/Ubuntu_Bold.ttf", 18, gtk.GetLangText("metaupdate_progress_text", "update_diag").format(str(UpdateStep), "6"), (240, 240, 240), 5, 25)

        # -- Render the Steps -- #
        if not IsMetadataUpdate:
            sprite.FontRender(Display, "/Ubuntu_Bold.ttf", 12, gtk.GetLangText("update_steps", "update_diag"), (240, 240, 240), 5, 50)
        else:
            sprite.FontRender(Display, "/Ubuntu_Bold.ttf", 12, gtk.GetLangText("metadata_steps", "update_diag"), (240, 240, 240), 5, 50)

    elif VersionChecking and not UpdateCompleted and not DownloadError:
        sprite.FontRender(Display, "/Ubuntu_Bold.ttf", 18, gtk.GetLangText("version_checking", "update_diag").format(str(UpdateStep), "6"), (240, 240, 240), 5, 25)

    # -- Render the Downloading Progress Bar -- #
    if DownloaderEnabled and not UpdateCompleted:
        sprite.FontRender(Display, "/Ubuntu_Bold.ttf", 14, UpdateProgressStatus.format(str(UpdateProgress)), (240, 240, 240), 3, UpdateProgressBar_Rectangle[1] - 18)

        LoadingAnimSquare.Render(Display)
        sprite.Shape_Rectangle(Display, (240, 240, 240), UpdateProgressBar_Rectangle)

    # -- Render the Update Complete Message -- #
    if UpdateCompleted or DownloadError:
        sprite.FontRender(Display, "/Ubuntu_Bold.ttf", 14, gtk.GetLangText(UpdateCompletedMessage, "update_diag").format(DwObj.DownloadState.replace("ERROR_", "")), (240, 240, 240), 5, 25)

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
    global IsMetadataUpdate
    global DownloadError

    # -- Set the Title -- #
    if not Handler.DialogOpctAnim_AnimEnabled:
        if not IsMetadataUpdate:
            if not VersionChecking:
                Handler.MessageTitle = gtk.GetLangText("update_in_progress_title", "update_diag")
            else:
                if not UpdateCompleted:
                    Handler.MessageTitle = gtk.GetLangText("version_checking_title", "update_diag")
                else:
                    Handler.MessageTitle = gtk.GetLangText("update_complete_title", "update_diag")
        else:
            if not UpdateCompleted:
                Handler.MessageTitle = gtk.GetLangText("metadw_downloading", "update_diag")
            else:
                Handler.MessageTitle = gtk.GetLangText("metadw_download_complete", "update_diag")

        # -- Update the Steps -- #
        if not UpdateCompleted:
            if not IsMetadataUpdate:
                Update_Steps()
            else:
                Update_MetaSteps()

        else:
            # -- Update OK Button -- #
            OK_Button.Set_ColisionX(Handler.CommonDisplayScreenPos[0] + OK_Button.Rectangle[0])
            OK_Button.Set_ColisionY(Handler.CommonDisplayScreenPos[1] + OK_Button.Rectangle[1])
            OK_Button.Set_X(5)
            OK_Button.Set_Y(Handler.CommonDisplay.get_height() - OK_Button.Rectangle[3] - 5)

            if OK_Button.ButtonState == "UP":
                Handler.DialogOpctAnim_AnimEnabled = True

                sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Confirm", True))
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
                IsMetadataUpdate = False
                DownloadError = False
                OK_Button.ButtonState = "INACTIVE"

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
    global UpdateCompletedMessage
    global UpdateCompleted

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

    if DwObj.DownloadState.startswith("ERROR"):
        UpdateProgress = 0
        UpdateStepCanAdd = False

        DownloaderDownloadStarted = False
        DownloaderDownloadURL = "NULL"
        DownloaderDownloadFilePath = "Taiyou/HOME/Webcache/NULL"
        DownloaderEnabled = False
        UpdateCompleted = True
        UpdateCompletedMessage = "download_error_message"
        print("TaiyouUI.ApplicationUpdateDiag.UpdateDownloader : Downloader Task has given an error. Error {0}".format(DwObj.DownloadState.replace("ERROR_", "")))


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

        print("TaiyouUI.ApplicationUpdateDiag : Update Step; " + str(UpdateStep))

        if UpdateStep == 0: # -- Download Current Version Data -- #
            TaskUrl = reg.ReadKey("/TaiyouSystem/TaiyouOnlineGameIDPath", True) + Handler.ApplicationID + "/version"
            SetDownloadTask(TaskUrl, "Taiyou/HOME/Webcache/UPDATER/" + Handler.ApplicationID + "/version")

        if UpdateStep == 1: # -- Compare Versions -- #
            if float(open("Taiyou/HOME/Webcache/UPDATER/" + Handler.ApplicationID + "/version").read()) == Handler.ApplicationVersion:
                UpdateCompletedMessage = "version_already_updated"
                UpdateCompleted = True
                UpdateStepCanAdd = False
                VersionChecking = False

        if UpdateStep == 2: # -- Download the Update File -- #
            VersionChecking = False
            TaskUrl = reg.ReadKey("TaiyouSystem/TaiyouOnlineGameIDPath", True) + Handler.ApplicationID + "/updateFile.zip"
            SetDownloadTask(TaskUrl, "Taiyou/HOME/Webcache/UPDATER/" + Handler.ApplicationID + "/updateFile.zip")

        if UpdateStep == 3: # -- Copy Updated Files -- #
            UpdateStepCanAdd = False
            UpdateFileZipPath = "Taiyou/HOME/Webcache/UPDATER/" + Handler.ApplicationID + "/updateFile.zip"

            utils.FileCopy(UpdateFileZipPath, Handler.ApplicationFolder + "/updateFile.zip")

            UpdateStepCanAdd = True

        if UpdateStep == 4: # -- Unzip File  -- #
            UpdateStepCanAdd = False
            print("Unzip File")

            ZipFilePath = Handler.ApplicationFolder + "/updateFile.zip"

            utils.Unzip_File(ZipFilePath, Handler.ApplicationFolder + "/")

            UpdateStepCanAdd = True

        if UpdateStep == 5: # -- Download Patch Notes -- #
            TaskUrl = reg.ReadKey("/TaiyouSystem/TaiyouOnlineGameIDPath", True) + Handler.ApplicationID + "/patchNotes"
            SetDownloadTask(TaskUrl, "Taiyou/HOME/Webcache/UPDATER/" + Handler.ApplicationID + "/patchNotes")

        if UpdateStep == 6: # -- Write some Registry Keys -- #
            # -- Write Current Version
            reg.WriteKey("/TaiyouSystem/UPDATER/" + Handler.ApplicationID + "/CurrentVersion", open("Taiyou/HOME/Webcache/UPDATER/" + Handler.ApplicationID + "/version", "r").read().rstrip())
            reg.WriteKey("/TaiyouSystem/UPDATER/" + Handler.ApplicationID + "/PatchNotes", open("Taiyou/HOME/Webcache/UPDATER/" + Handler.ApplicationID + "/patchNotes", "r").read().rstrip())

            reg.WriteKey("/TaiyouSystem/UPDATER/" + Handler.ApplicationID + "/ApplicationDataHasBeenDownloaded", "True")

        if UpdateStep == 7: # -- Delete Temporary Files -- #
            UpdateStepCanAdd = False

            utils.Directory_Remove("Taiyou/HOME/Webcache/UPDATER/" + Handler.ApplicationID) # Delete All downloaded files
            utils.File_Delete(Handler.ApplicationFolder + "/updateFile.zip")

            UpdateStepCanAdd = True
            UpdateCompleted = True
            UpdateCompletedMessage = "update_completed"
            VersionChecking = True

def Update_MetaSteps():
    global UpdateStep
    global UpdateStepCanAdd
    global UpdateCompleted
    global UpdateCompletedMessage
    global VersionChecking
    global IsMetadataUpdate

    if UpdateStepCanAdd:
        UpdateStep += 1

        if UpdateStep == 0:
            TaskUrl = reg.ReadKey("/TaiyouSystem/TaiyouOnlineGameIDPath", True) + Handler.ApplicationID + "/version"
            SetDownloadTask(TaskUrl, "Taiyou/HOME/Webcache/UPDATER/" + Handler.ApplicationID + "/version")

        if UpdateStep == 1:
            TaskUrl = reg.ReadKey("/TaiyouSystem/TaiyouOnlineGameIDPath", True) + Handler.ApplicationID + "/patchNotes"
            SetDownloadTask(TaskUrl, "Taiyou/HOME/Webcache/UPDATER/" + Handler.ApplicationID + "/patchNotes")

        if UpdateStep == 2:
            reg.WriteKey("/TaiyouSystem/UPDATER/" + Handler.ApplicationID + "/CurrentVersion", open("Taiyou/HOME/Webcache/UPDATER/" + Handler.ApplicationID + "/version", "r").read().rstrip())
            reg.WriteKey("/TaiyouSystem/UPDATER/" + Handler.ApplicationID + "/PatchNotes", open("Taiyou/HOME/Webcache/UPDATER/" + Handler.ApplicationID + "/patchNotes", "r").read().rstrip())

            reg.WriteKey("/TaiyouSystem/UPDATER/" + Handler.ApplicationID + "/ApplicationDataHasBeenDownloaded", "True")

            UpdateCompleted = True
            UpdateCompletedMessage = "metadw_download_completests"



def EventUpdate(event):
    global OK_Button
    global UpdateCompleted

    if UpdateCompleted:
        OK_Button.Update(event)