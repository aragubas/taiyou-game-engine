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
import ENGINE as tge


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
WriteDirectoryInputBox = gtk.InputBox

def Initialize():
    global SelectFolderButton
    global VerticalList
    global CreateFolderButton
    global WriteDirectoryInputBox

    VerticalList = gtk.VerticalListWithDescription(pygame.Rect(0, 0, 550, 250))
    SelectFolderButton = gtk.Button((3, 1, 5, 5), gtk.GetLangText("button_select_folder", "save_fs"), 18)
    CreateFolderButton = gtk.Button((3, 1, 5, 5), gtk.GetLangText("button_create_folder", "save_fs"), 18)
    WriteDirectoryInputBox = gtk.InputBox(0, 0, 120, 18, "Default", 18)

    WriteDirectoryInputBox.CharacterLimit = 14

def ReloadSaveList():
    global VerticalList

    print("Taiyou.SaveFolderSelect.ReloadSaveList")

    VerticalList.ClearList()

    Dir = utils.Directory_FilesList(tge.Get_GlobalAppDataFolder())

    SaveName = "null"
    SaveIcon = "null"

    for Directoryes in Dir:
        if utils.File_Exists(str(utils.Get_DirectoryOfFilePath(Directoryes)) + "/.save_fs"):  # -- Check if directory is a valid Save Folder
            SaveMetadataFile = Directoryes

            Data = open(SaveMetadataFile, "r")  # -- Read Meta Data File

            for line in Data:  # -- Get Information on that data file
                line = line.rstrip()
                SplitedThing = line.split(':')

                if SplitedThing[0] == "Name":
                    SaveName = SplitedThing[1]

                if SplitedThing[0] == "Icon":
                    SaveIcon = SplitedThing[1]

            VerticalList.AddItem(SaveName, "" , SaveIcon)  # -- And finally, add to the list


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
    global WriteDirectoryInputBox

    DISPLAYObject = Display

    # -- Initialize the UIObjectSurface -- #
    if not UIObjectsSurfaceUpdated:
        UIObjectsSurface = pygame.Surface((Display.get_width(), Display.get_height()), pygame.SRCALPHA)
        print("Surface Created")
        UIObjectsSurfaceUpdated = True

    # -- Set Surface Alpha -- #
    UIObjectsSurface.set_alpha(UIOpacity)


    # -- Draw the Screenshot of Screen -- #
    Draw_ScreenshotOfGameScreen(UIObjectsSurface)

    # -- Draw the Title -- #
    sprite.FontRender(UIObjectsSurface, "/Ubuntu_Bold.ttf", 24, gtk.GetLangText("title", "save_fs"), (230, 230, 230), 15, AnimationNumb + 15)

    # -- Draw Buttons -- #
    SelectFolderButton.Render(UIObjectsSurface)

    # -- Render Buttons Background -- #
    gtk.Draw_Panel(UIObjectsSurface, ControlsPanel)

    # -- Render Tools Button -- #
    CreateFolderButton.Render(UIObjectsSurface)
    WriteDirectoryInputBox.Render(UIObjectsSurface)

    # -- Render List -- #
    VerticalList.Render(UIObjectsSurface)


    Display.blit(UIObjectsSurface, (0, 0))


def Draw_ScreenshotOfGameScreen(Display):
    global CopyOfScreen_Result
    global CopyOfScreen_Last
    global CopyOfScreen_BlurAmount

    # -- Blur Amount Value -- #
    if not CopyOfScreen_Last:
        CopyOfScreen_BlurAmount = max(1.0, UIOpacity - reg.ReadKey_int("/TaiyouSystem/CONF/blur_amount"))

    if UIOpacityAnimEnabled:  # -- Draw the Animation -- #
        CopyOfScreen_Last = False
        if reg.ReadKey_bool("/TaiyouSystem/CONF/blur_enabled"):
            # -- Pixalizate if Overlay Pixalizate is True -- #
            if not reg.ReadKey_bool("/TaiyouSystem/CONF/overlay_pixelizate"):
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
    global WriteDirectoryInputBox
    global UpdateSaveLists

    if not UpdateSaveLists:
        ReloadSaveList()
        UpdateSaveLists = True

    if UIObjectsSurfaceUpdated:
        UpdateOpacityAnim()

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

        CreateFolderButton.Set_Y(ControlsPanel[1] + 5)
        CreateFolderButton.Set_X(ControlsPanel[0] + 3)

        WriteDirectoryInputBox.Set_Y(CreateFolderButton.Rectangle[1] + 3)
        WriteDirectoryInputBox.Set_X(CreateFolderButton.Rectangle[0] + CreateFolderButton.Rectangle[2] + 3)

        # -- Test -- #
        if SelectFolderButton.ButtonState == "UP":
            tge.Set_SaveFolder(VerticalList.LastItemClicked + "/")

            UIOpacityAnimEnabled = True


def UpdateOpacityAnim():
    global UIOpacityAnimState
    global UIOpacity
    global UIOpacityAnimEnabled
    global UIOpacityAnimSpeed
    global CopyOfTheScreen
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

            # -- Play the Out Sound -- #
            if not UIOpacityAnim_OutSoundPlayed:
                sound.PlaySound(reg.ReadKey("/TaiyouSystem/SND/Out"))
                UIOpacityAnim_OutSoundPlayed = True

            if UIOpacity <= 0:  # <- Triggers Animation End
                UIOpacity = 0
                UIOpacityAnimEnabled = False
                UIOpacityAnimState = 0
                UiHandler.Messages.append("GAME_UPDATE:True")
                # -- Unload the Surfaces -- #
                CopyOfTheScreen = pygame.Surface((0, 0), pygame.SRCALPHA)
                UIObjectsSurface = pygame.Surface((0, 0), pygame.SRCALPHA)
                UIOpacityPauseGame = False
                UIObjectsSurfaceUpdated = False
                CopyOfScreen_Last = False

                UIOpacityAnim_InSoundPlayed = False
                UIOpacityAnim_OutSoundPlayed = False
                UiHandler.Messages.append("SET_GAME_MODE")
                UIOpacityAnim_InGameErrorSoundPlayed = False
                UiHandler.SystemMenuEnabled = False
                UpdateSaveLists = False

def EventUpdate(event):
    global SelectFolderButton
    global VerticalList
    global CreateFolderButton
    global WriteDirectoryInputBox

    SelectFolderButton.Update(event)
    VerticalList.Update(event)
    CreateFolderButton.Update(event)
    WriteDirectoryInputBox.Update(event)