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
import pygame
from ENGINE import SOUND as sound
from ENGINE import SPRITE as sprite
from ENGINE import REGISTRY as reg
from ENGINE.TaiyouUI import UIGTK as gtk
from ENGINE import TaiyouUI as UiHandler
from ENGINE import UTILS as utils
from ENGINE.TaiyouUI import OverlayDialog as ovlDiag
import ENGINE as tge
from ENGINE import TaiyouMain as taiyouMain
import os, datetime, dis

# -- Animation -- #
UIOpacity = 0
UIOpacityAnimSpeed = 15
UIOpacityAnimEnabled = True
UIOpacityAnimState = 0
UIOpacityPauseGame = True
UIOpacityAnim_InSoundPlayed = False
UIOpacityAnim_OutSoundPlayed = False
UIOpacityAnim_InGameErrorSoundPlayed = False
AnimationNumb = 0
UpdateSaveLists = False


# -- Copy of Screen -- #
CopyOfScreen_Last = False
CopyOfScreen_Result = pygame.Surface
CopyOfScreen_BlurAmount = 0

# -- Surfaces -- #
UIObjectsSurfaceUpdated = False
DISPLAYObject = pygame.Surface
UIObjectsSurface = pygame.Surface

# -- Controls -- #
SelectFolderButton = gtk.Button
VerticalList = gtk.VerticalListWithDescription
ControlsPanel = pygame.Rect(0, 0, 550, 35)
CreateFolderButton = gtk.Button
DeleteFolderButton = gtk.Button
RenameFolderButton = gtk.Button

# -- etc -- #
PendingOperation = "null" """Pending Operation on Save Folder\n0 - Delete\n1 - Create\n2 - Rename"""

def Initialize():
    global SelectFolderButton
    global VerticalList
    global CreateFolderButton
    global DeleteFolderButton
    global RenameFolderButton

    VerticalList = gtk.VerticalListWithDescription(pygame.Rect(0, 0, 550, 250))
    SelectFolderButton = gtk.Button((3, 1, 5, 5), gtk.GetLangText("button_select_folder", "save_fs"), 18)
    CreateFolderButton = gtk.Button((3, 1, 5, 5), gtk.GetLangText("button_create_folder", "save_fs"), 18)
    DeleteFolderButton = gtk.Button((3, 1, 5, 5), gtk.GetLangText("button_delete_folder", "save_fs"), 18)
    RenameFolderButton = gtk.Button((3, 1, 5, 5), gtk.GetLangText("button_rename_folder", "save_fs"), 18)

def ReloadSaveList():
    global VerticalList

    print("Taiyou.SaveFolderSelect.ReloadSaveList : Listings Directories")

    VerticalList.ClearList()

    SaveName = "null"
    SaveDescription = ""

    for dir in [x[0] for x in os.walk(tge.Get_GlobalAppDataFolder())]:
        print("Taiyou.SaveFolderSelect.ReloadSavesList : CurrentScan[" + dir + "]")

        if utils.File_Exists(dir + "/.save_fs"):  # -- Check if directory is a valid Save Folder
            SaveMetadataFile = dir + "/.save_fs"
            print("Taiyou.SaveFolderSelect.ReloadSavesList : CurrentScan is a valid Save Folder, reading Metadata...")

            Data = open(SaveMetadataFile, "r")  # -- Read Meta Data File

            for line in Data:  # -- Get Information on that data file
                line = line.rstrip()
                SplitedThing = line.split(';')

                if SplitedThing[0] == "Name":
                    SaveName = SplitedThing[1]
                    print("Taiyou.SaveFolderSelect.ReloadSavesList : SaveName is [{0}].".format(SplitedThing[1]))

                if SplitedThing[0] == "Description":
                    SaveDescription = SplitedThing[1]
                    print("Taiyou.SaveFolderSelect.ReloadSavesList : SaveDescription is [{0}].".format(SplitedThing[1]))

            VerticalList.AddItem(SaveName, SaveDescription)  # -- And finally, add to the list

def WriteSaveFS(name):
    FilePath = tge.Get_GlobalAppDataFolder() + name + "/.save_fs"

    # -- Write File -- #
    Day = str(datetime.datetime.today().day)
    Month = str(datetime.datetime.today().month)
    Year = str(datetime.datetime.today().year)
    Hour = str(datetime.datetime.today().hour)
    Minutes = str(datetime.datetime.today().minute)
    Secound = str(datetime.datetime.today().second)

    f = open(FilePath, "w+")
    f.write("Name;" + str(name))
    f.write("\nDescription;{0}".format(gtk.GetLangText("savefs_created_at", "save_fs").format(Day, Month, Year, Hour, Minutes, Secound)))
    f.close()


def CreateSaveFolder(name):
    # -- Create Directory -- #
    utils.Directory_MakeDir(tge.Get_GlobalAppDataFolder() + name)

    # -- Write the save_fs File  -- #
    WriteSaveFS(name)

    ReloadSaveList()

def DeleteSaveFolder(name):
    FilePath = tge.Get_GlobalAppDataFolder() + name
    print("Taiyou.SaveFolderSelect.DeleteSaveFolder : Requested Path[" + FilePath + "]")

    utils.Directory_Remove(FilePath)

    ReloadSaveList()

def RenameSaveFolder(source, new_name):
    FilePath = tge.Get_GlobalAppDataFolder()

    # -- Rename Actual Directory -- #
    utils.Directory_Rename(FilePath + source, FilePath + new_name)

    # -- Write the save_fs File  -- #
    WriteSaveFS(new_name)

    # -- Reload the List -- #
    ReloadSaveList()


def Draw(Display):
    global UIOpacity
    global UIOpacityAnimEnabled
    global UIOpacityAnimState
    global AnimationNumb
    global UIObjectsSurfaceUpdated
    global CopyOfScreen_BlurAmount
    global UIObjectsSurfaceUpdated
    global DISPLAYObject
    global UIObjectsSurface
    global SelectFolderButton
    global AnimationNumb
    global VerticalList
    global ControlsPanel
    global CreateFolderButton
    global DeleteFolderButton
    global RenameFolderButton

    DISPLAYObject = Display

    # -- Draw the Screenshot of Screen -- #
    Draw_ScreenshotOfGameScreen(Display)

    # -- Initialize the UIObjectSurface -- #
    UIObjectsSurfaceUpdated = True
    UIObjectsSurface = pygame.Surface((Display.get_width(), Display.get_height()), pygame.SRCALPHA)

    # -- Set Surface Alpha -- #
    UIObjectsSurface.set_alpha(UIOpacity)

    # -- Draw the Title -- #
    sprite.FontRender(UIObjectsSurface, "/Ubuntu_Bold.ttf", 24, gtk.GetLangText("title", "save_fs"), (230, 230, 230), 15, AnimationNumb + 15)

    # -- Draw Buttons -- #
    SelectFolderButton.Render(UIObjectsSurface)

    # -- Render Buttons Background -- #
    gtk.Draw_Panel(UIObjectsSurface, ControlsPanel)

    # -- Render Tools Button -- #
    CreateFolderButton.Render(UIObjectsSurface)
    DeleteFolderButton.Render(UIObjectsSurface)
    RenameFolderButton.Render(UIObjectsSurface)

    # -- Render List -- #
    VerticalList.Render(UIObjectsSurface)

    Display.blit(UIObjectsSurface, (0, 0))


def Draw_ScreenshotOfGameScreen(Display):
    global CopyOfScreen_Result
    global CopyOfScreen_Last
    global CopyOfScreen_BlurAmount

    # -- Blur Amount Value -- #
    if not CopyOfScreen_Last:
        CopyOfScreen_BlurAmount = max(1.0, UIOpacity / reg.ReadKey_int("/TaiyouSystem/CONF/blur_amount", True)) * 32

    if UIOpacityAnimEnabled:  # -- Draw the Animation -- #
        CopyOfScreen_Last = False
        if reg.ReadKey_bool("/TaiyouSystem/CONF/blur_enabled", True):
            # -- Pixalizate if Overlay Pixalizate is True -- #
            if not reg.ReadKey_bool("/TaiyouSystem/CONF/overlay_pixelizate", True):
                # -- Blur the Copy of Screen -- #
                Display.blit(sprite.Surface_Blur(CopyOfTheScreen, CopyOfScreen_BlurAmount), (0, 0))
            else:
                # -- Pixalizate Copy of Screen -- #
                Display.blit(sprite.Surface_Blur(CopyOfTheScreen, CopyOfScreen_BlurAmount, True), (0, 0))

        else:
            Display.blit(CopyOfTheScreen, (0, 0))

    # -- Draw the Last Frame -- #
    if not CopyOfScreen_Last and not UIOpacityAnimEnabled:
        CopyOfScreen_Result = sprite.Surface_Blur(CopyOfTheScreen, CopyOfScreen_BlurAmount)
        CopyOfScreen_Last = True

    # -- Render the Last Frame -- #
    if CopyOfScreen_Last and not UIOpacityAnimEnabled:  # -- Render the last frame of animation -- #
        Display.blit(CopyOfScreen_Result, (0, 0))

def Update():
    global SelectFolderButton
    global UIObjectsSurfaceUpdated
    global UIObjectsSurface
    global AnimationNumb
    global UIOpacityAnimEnabled
    global VerticalList
    global ControlsPanel
    global CreateFolderButton
    global UpdateSaveLists
    global DeleteFolderButton
    global PendingOperation
    global RenameFolderButton

    if not UpdateSaveLists:
        ReloadSaveList()
        UpdateSaveLists = True

    UpdateOpacityAnim()

    # -- Set the Correct Subscreen for Overlay Dialog -- #
    ovlDiag.Subscreen = 2
    if not PendingOperation == "null":
        # -- Do Pending Operation -- #
        try:
            if PendingOperation == 0:
                if ovlDiag.subscreen2.Response == "YES":
                    DeleteSaveFolder(VerticalList.Selected_Name)

            elif PendingOperation == 1:
                CreateSaveFolder(ovlDiag.subscreen2.Response)

            elif PendingOperation == 2:
                RenameSaveFolder(VerticalList.Selected_Name, ovlDiag.subscreen2.Response)

        except Exception as ex:
            print("Taiyou.SaveFolderSelect : Error while processing the operation[" + PendingOperation + "]\nError: " + str(ex))

            ovlDiag.subscreen2.ResponseType = "OK"
            ovlDiag.subscreen2.ResponseTrigger = False
            ovlDiag.DialogOpctAnim_Enabled = True
            ovlDiag.DialogOpctAnim_AnimMode = 0
            ovlDiag.subscreen2.SetMessage(gtk.GetLangText("diag_error_title", "save_fs"), gtk.GetLangText("diag_error_text", "save_fs").format(PendingOperation))

        PendingOperation = "null"
        ovlDiag.subscreen2.Response = "null"
        ovlDiag.subscreen2.ResponseTrigger = False

    if UIObjectsSurfaceUpdated:
        # -- Update Animation Numb -- #
        AnimationNumb = UIOpacity - 255 + UIOpacityAnimSpeed

        # -- Update Select Folder Button -- #
        SelectFolderButton.Set_X(15)
        SelectFolderButton.Set_Y(UIObjectsSurface.get_height() - SelectFolderButton.Rectangle[3] - AnimationNumb - 15)

        # -- Update Locations -- #
        VerticalList.Set_X(UIObjectsSurface.get_width() / 2 - VerticalList.Rectangle[2] / 2)
        VerticalList.Set_Y(AnimationNumb + UIObjectsSurface.get_height() / 2 - VerticalList.Rectangle[3] / 1.5)

        # -- Update Panel Location -- #
        ControlsPanel[0] = VerticalList.Rectangle[0]
        ControlsPanel[1] = VerticalList.Rectangle[1] + VerticalList.Rectangle[3]

        DeleteFolderButton.Set_Y(ControlsPanel[1] + 5)
        DeleteFolderButton.Set_X(ControlsPanel[0] + 3)

        CreateFolderButton.Set_Y(DeleteFolderButton.Rectangle[1])
        CreateFolderButton.Set_X(DeleteFolderButton.Rectangle[0] + DeleteFolderButton.Rectangle[2] + 3)

        RenameFolderButton.Set_Y(CreateFolderButton.Rectangle[1])
        RenameFolderButton.Set_X(CreateFolderButton.Rectangle[0] + CreateFolderButton.Rectangle[2] + 3)

        # -- Select Folder -- #
        if SelectFolderButton .ButtonState == 2 and not VerticalList.Selected_Name == "null":
            tge.Set_SaveFolder(VerticalList.Selected_Name + "/")

            UIOpacityAnimEnabled = True

        # -- Create Folder -- #
        if CreateFolderButton .ButtonState == 2:
            taiyouMain.SystemUI.OverlayDialogEnabled = True
            PendingOperation = 1
            ovlDiag.subscreen2.InputBox.CharacterLimit = 14
            ovlDiag.subscreen2.ResponseType = "INPUT"

            ovlDiag.subscreen2.SetMessage(gtk.GetLangText("diag_create_title", "save_fs"), gtk.GetLangText("diag_create_text", "save_fs"))

        # -- Delete Folder -- #
        if DeleteFolderButton .ButtonState == 2 and not VerticalList.Selected_Name == "null":
            taiyouMain.SystemUI.OverlayDialogEnabled = True
            PendingOperation = 0
            ovlDiag.subscreen2.ResponseType = "YESNO"

            ovlDiag.subscreen2.SetMessage(gtk.GetLangText("diag_delete_title", "save_fs"), gtk.GetLangText("diag_delete_text", "save_fs").format(VerticalList.Selected_Name))

        # -- Rename Folder -- #
        if RenameFolderButton .ButtonState == 2 and not VerticalList.Selected_Name == "null":
            taiyouMain.SystemUI.OverlayDialogEnabled = True

            PendingOperation = 2
            ovlDiag.subscreen2.ResponseType = "INPUT"
            ovlDiag.subscreen2.InputBox.CharacterLimit = 14
            ovlDiag.subscreen2.InputBox.text = VerticalList.Selected_Name

            ovlDiag.subscreen2.SetMessage(gtk.GetLangText("diag_rename_title", "save_fs"), gtk.GetLangText("diag_rename_text", "save_fs").format(VerticalList.Selected_Name))

def UpdateOpacityAnim():
    global UIOpacityAnimState
    global UIOpacity
    global UIOpacityAnimEnabled
    global UIOpacityAnimSpeed
    global UIObjectsSurface
    global UIObjectsSurfaceUpdated
    global UIOpacityAnim_InSoundPlayed
    global UIOpacityAnim_OutSoundPlayed
    global UIOpacityAnim_InGameErrorSoundPlayed
    global CopyOfScreen_Last
    global UIOpacityPauseGame

    if UIOpacityAnimEnabled:
        if UIOpacityAnimState == 0:  # <- Enter Animation
            UIOpacity += UIOpacityAnimSpeed

            # -- Play the In Sound -- #
            if not UIOpacityAnim_InSoundPlayed:
                sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/In", True))
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

            # -- Play the Out Sound -- #
            if not UIOpacityAnim_OutSoundPlayed:
                sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Out", True))
                UIOpacityAnim_OutSoundPlayed = True

            if UIOpacity <= 0:  # <- Triggers Animation End
                UIOpacity = 0
                UIOpacityAnimEnabled = False
                UIOpacityAnimState = 0
                # -- Unload the Surfaces -- #
                UIObjectsSurface = pygame.Surface((0, 0), pygame.SRCALPHA)
                UIOpacityPauseGame = False
                UIObjectsSurfaceUpdated = False
                CopyOfScreen_Last = False

                UIOpacityAnim_InSoundPlayed = False
                UIOpacityAnim_OutSoundPlayed = False
                taiyouMain.ReceiveCommand(5)
                UIOpacityAnim_InGameErrorSoundPlayed = False
                UiHandler.SystemMenuEnabled = False

def EventUpdate(event):
    global SelectFolderButton
    global VerticalList
    global CreateFolderButton
    global DeleteFolderButton
    global RenameFolderButton

    SelectFolderButton.Update(event)
    VerticalList.Update(event)
    CreateFolderButton.Update(event)
    DeleteFolderButton.Update(event)
    RenameFolderButton.Update(event)
