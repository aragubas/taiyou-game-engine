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

# -- Imports -- #
from ENGINE import REGISTRY as reg
from Fogoso.MAIN import ClassesUtils as gameObjs
from Fogoso.MAIN.Screens import Settings as ScreenSettings
from Fogoso import MAIN as gameMain
from Fogoso.MAIN.Window import StoreWindow as storeWindow
from Fogoso.MAIN.Window import ExperienceStore as expStoreWindow
from Fogoso.MAIN.Window import InfosWindow as infosWindow
from ENGINE import SPRITE as sprite
from Fogoso.MAIN import GameVariables as save
from Fogoso.MAIN.Screens.Game import IncomingLog
import pygame

# -- Objects Definition -- #
GrindButton = gameObjs.Button
GameOptionsButton = gameObjs.Button
SaveButton = gameObjs.Button
BackToMainMenuButton = gameObjs.Button
OpenStoreButton = gameObjs.Button
OpenInfosWindowButton = gameObjs.Button
OpenExperienceWindowButton = gameObjs.Button

# -- Game Items View -- #
ItemsView = gameObjs.HorizontalItemsView

# -- Store Window -- #
StoreWindow_Enabled = True

# -- Infos Window -- #
InfosWindow_Enabled = False

# -- Experience Store Windows -- #
ExperienceStore_Enabled = False

# -- Unload -- #
UnloadRequested = False
UnloadDelay = 0

# -- Saving Screen Variables -- #
IsControlsEnabled = True
SavingScreenEnabled = False

Current_Maintenance = 0.0


# -- Load/Save Functions -- #
def LoadGame():
    global ItemsView
    print("LoadGame : Init")
    gameMain.FadeEffectState = True
    gameMain.FadeEffectCurrentState = 0
    gameMain.FadeEffectValue = 255

    save.LoadSaveData()

    save.LoadItems()

    gameMain.FadeEffectState = True
    print("LoadGame : Game Loaded Sucefully")

def SaveGame():
    global SavingScreenEnabled
    global IsControlsEnabled
    global BackgroundAnim_Type
    global BackgroundAnim_Enabled
    global BackgroundAnim_Numb

    save.SaveData()
    save.SaveItems()

    BackgroundAnim_Type = 1
    BackgroundAnim_Enabled = True

BackgroundAnim_Type = 0
BackgroundAnim_Enabled = True
BackgroundAnim_Numb = 1.0
def UpdateSavingScreen(DISPLAY):
    global SavingScreenEnabled
    global IsControlsEnabled
    global BackgroundAnim_Type
    global BackgroundAnim_Enabled
    global BackgroundAnim_Numb

    if BackgroundAnim_Enabled:
        if BackgroundAnim_Type == 0:
            BackgroundAnim_Numb += 0.5
            if BackgroundAnim_Numb >= 30.5:

                BackgroundAnim_Enabled = False
                BackgroundAnim_Type = 1
                BackgroundAnim_Numb = 30.5

                SaveGame()
        if BackgroundAnim_Type == 1:
            BackgroundAnim_Numb -= 0.5
            if BackgroundAnim_Numb <= 1.1:
                BackgroundAnim_Numb = 1.0
                BackgroundAnim_Enabled = True
                BackgroundAnim_Type = 0

                SavingScreenEnabled = False
                IsControlsEnabled = True

    SavingSurfaceBackground = pygame.Surface((DISPLAY.get_width(), DISPLAY.get_height()))
    SavingSurfaceBackground.blit(sprite.Surface_Blur(DISPLAY, BackgroundAnim_Numb), (0,0))
    DISPLAY.blit(SavingSurfaceBackground, (0, 0))

    TextsSurface = pygame.Surface((DISPLAY.get_width(), DISPLAY.get_height()), pygame.SRCCOLORKEY)
    TextsSurface.fill((255,0,255))
    TextsSurface.set_colorkey((255,0,255))
    TextsSurface.set_alpha(BackgroundAnim_Numb * 8.5)

    SavingText = reg.ReadKey("/strings/game/save_screen/title")
    SavingStatusText = reg.ReadKey("/strings/game/save_screen/message")
    TextSavingX = DISPLAY.get_width() / 2 - sprite.GetText_width("/PressStart2P.ttf", 50, SavingText) / 2
    TextSavingY = DISPLAY.get_height() / 2 - sprite.GetText_height("/PressStart2P.ttf", 50, SavingText) / 2 - 100
    sprite.RenderFont(TextsSurface, "/PressStart2P.ttf", 50, SavingText, (250,250,255),TextSavingX, TextSavingY, False)
    sprite.RenderFont(TextsSurface, "/PressStart2P.ttf", 35, SavingStatusText, (250,250,255),DISPLAY.get_width() / 2 - sprite.GetText_width("/PressStart2P.ttf", 35, SavingStatusText) / 2, TextSavingY + 100, False)

    DISPLAY.blit(TextsSurface, (0,0))

def Update():
    global GameOptionsButton
    global BackToMainMenuButton
    global OpenStoreButton
    global StoreWindow_Enabled
    global ItemsView
    global UnloadDelay
    global UnloadRequested
    global IsControlsEnabled
    global SavingScreenEnabled
    global ExperienceStore_Enabled
    global InfosWindow_Enabled

    if IsControlsEnabled:
        # -- Update Save -- #
        save.Update()

        ItemsView.Set_X(5)
        ItemsView.Set_Y(gameMain.DefaultDisplay.get_height() - 130)

        # -- Update General Maintenance -- #
        MaintenanceCost()

        # -- Update Buttons Click -- #
        if GrindButton.ButtonState == "UP":
            GrindClick()
        if GameOptionsButton.ButtonState == "UP":
            gameMain.FadeEffectValue = 255
            gameMain.FadeEffectCurrentState = 0
            gameMain.FadeEffectState = True
            ScreenSettings.ScreenToReturn = gameMain.CurrentScreen
            ScreenSettings.Initialize()
            storeWindow.RestartAnimation()
            gameMain.CurrentScreen += 1

        if SaveButton.ButtonState == "UP":
            SavingScreenEnabled = True
            IsControlsEnabled = False

        if BackToMainMenuButton.ButtonState == "UP":
            gameMain.FadeEffectState = 0
            gameMain.FadeEffectValue = 255
            gameMain.FadeEffectState = True
            UnloadRequested = True

        if UnloadRequested:
            UnloadDelay += 1

            if UnloadDelay >= 5:
                Unload()
                gameMain.CurrentScreen -= 1

        if OpenStoreButton.ButtonState == "UP":
            if StoreWindow_Enabled:
                StoreWindow_Enabled = False
                storeWindow.RestartAnimation()
            else:
                StoreWindow_Enabled = True
                InfosWindow_Enabled = False
                ExperienceStore_Enabled = False

        if OpenInfosWindowButton.ButtonState == "UP":
            if InfosWindow_Enabled:
                InfosWindow_Enabled = False
                storeWindow.RestartAnimation()
            else:
                InfosWindow_Enabled = True
                StoreWindow_Enabled = False
                ExperienceStore_Enabled = False

        if OpenExperienceWindowButton.ButtonState == "UP" and save.GameItems_TotalIndx_NegativeOne == 1:
            if ExperienceStore_Enabled:
                ExperienceStore_Enabled = False
                storeWindow.RestartAnimation()
            else:
                ExperienceStore_Enabled = True
                StoreWindow_Enabled = False
                InfosWindow_Enabled = False


        GameOptionsButton.Set_X(gameMain.DefaultDisplay.get_width() - 120)
        SaveButton.Set_X(gameMain.DefaultDisplay.get_width() - 120)
        BackToMainMenuButton.Set_X(gameMain.DefaultDisplay.get_width() - 120)
        GrindButton.Rectangle[2] = 130
        GrindButton.Rectangle[3] = 150
        OpenStoreButton.Set_X(5)
        OpenStoreButton.Set_Y(gameMain.DefaultDisplay.get_height() - OpenStoreButton.Rectangle[3] - 5)
        OpenInfosWindowButton.Set_X(OpenStoreButton.Rectangle[0] + OpenStoreButton.Rectangle[2] + 5)
        OpenInfosWindowButton.Set_Y(OpenStoreButton.Rectangle[1])
        if save.GameItems_TotalIndx_NegativeOne == 1:
            OpenExperienceWindowButton.Set_X(OpenInfosWindowButton.Rectangle[0] + OpenInfosWindowButton.Rectangle[2] + 5)
            OpenExperienceWindowButton.Set_Y(OpenInfosWindowButton.Rectangle[1])


        IncomingLog.Update()

MaintenanceCost_Delta = 0
def MaintenanceCost():
    global MaintenanceCost_Delta
    global Current_Maintenance
    global GameItemsList

    MaintenanceCost_Delta += 1

    if MaintenanceCost_Delta >= reg.ReadKey_float("/Save/general_maintenance_delta"):
        TotalItemsMaintenance = 0

        for item in save.GameItemsList:
            TotalItemsMaintenance = TotalItemsMaintenance + item.maintenance_cost

        MaintenanceGeral = reg.ReadKey_float("/Save/general_maintenance") + TotalItemsMaintenance
        IncomingLog.AddMessageText(reg.ReadKey("/strings/game/GeneralMaintenance") , True, (250, 150, 150, ), -MaintenanceGeral)
        MaintenanceCost_Delta = 0
        Current_Maintenance = MaintenanceGeral

def GameDraw(DISPLAY):
    global BackToMainMenuButton
    global OpenStoreButton
    global OpenInfosWindowButton
    global OpenExperienceWindowButton
    global StoreWindow_Enabled
    global ItemsView
    global SavingScreenEnabled
    global Current_MoneyFormated
    global Current_MoneyPerSecoundFormatted
    global GameItems_TotalIndx_NegativeOne
    # -- Draw the Grind Text -- #
    IncomingLog.DrawGrindText(DISPLAY)
    # -- Draw the Grind Button -- #
    GrindButton.Render(DISPLAY)
    # -- Draw the Options Button -- #
    GameOptionsButton.Render(DISPLAY)
    # -- Draw the Save Button -- #
    SaveButton.Render(DISPLAY)
    # -- Draw the BackToMenu button -- #
    BackToMainMenuButton.Render(DISPLAY)
    # -- Draw the Store Button -- #
    OpenStoreButton.Render(DISPLAY)
    # -- Draw the Items View -- #
    ItemsView.Render(DISPLAY)
    # -- Draw the OpenInfosWindow -- #
    OpenInfosWindowButton.Render(DISPLAY)
    # -- Draw the OpenExperience -- #
    if save.GameItems_TotalIndx_NegativeOne == 1:
        OpenExperienceWindowButton.Render(DISPLAY)

    # -- Render Money Text -- #
    MoneyColor = (250,250,255)
    PerSecoundColor = (220, 220, 220)
    if save.Current_Money > 0.1:
        MoneyColor = (120, 220, 120)
    elif save.Current_Money <= 0:
        MoneyColor = (220, 10, 10)
    if save.Current_MoneyPerSecound > 0.1:
        PerSecoundColor = (50, 200, 50)
    elif save.Current_MoneyPerSecound <= 0:
        PerSecoundColor = (120, 10, 10)

    # -- Render Current Money, at Top -- #
    sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 18, reg.ReadKey("/strings/game/money") + save.Current_MoneyFormated, MoneyColor, 10, 20)
    # -- Render Money per Secound -- #
    sprite.RenderFont(DISPLAY,"/PressStart2P.ttf", 18, reg.ReadKey("/strings/game/money_per_secound") + save.Current_MoneyPerSecoundFormatted, PerSecoundColor, 10,50)
    # -- Render Experience -- #
    sprite.RenderFont(DISPLAY,"/PressStart2P.ttf", 18, reg.ReadKey("/strings/game/experience") + str(save.CUrrent_ExperienceFormated) + "/" + str(save.Current_TotalClicks - save.Current_TotalClicksNext) + "=" + str(save.Current_ExperiencePerEach), (140, 130, 120) , 10, 80)


    # -- Draw the Store Window -- #
    if StoreWindow_Enabled:
        storeWindow.Render(DISPLAY)

    # -- Draw the Infos Window -- #
    if InfosWindow_Enabled:
        infosWindow.Render(DISPLAY)

    # -- Draw the Exp Store Window -- #
    if ExperienceStore_Enabled and save.GameItems_TotalIndx_NegativeOne == 1:
        expStoreWindow.Render(DISPLAY)

    # -- Draw the Saving Screen -- #
    if SavingScreenEnabled:
        UpdateSavingScreen(DISPLAY)

def Initialize(DISPLAY):
    # -- Set Buttons -- #
    global SaveButton
    global GameOptionsButton
    global GrindButton
    global BackToMainMenuButton
    global OpenStoreButton
    global ItemsView
    global OpenInfosWindowButton
    global OpenExperienceWindowButton
    # -- Initialize Buttons -- #
    GrindButton = gameObjs.Button(pygame.rect.Rect(15, 115, 130, 150), "Loremk ipsum dolor sit amet...", 18)
    GrindButton.WhiteButton = True
    GameOptionsButton = gameObjs.Button(pygame.rect.Rect(DISPLAY.get_width() - 120, 5, 0, 0), reg.ReadKey("/strings/button/game/options"), 12)
    SaveButton = gameObjs.Button(pygame.rect.Rect(DISPLAY.get_width() - 120, 20, 0, 0), reg.ReadKey("/strings/button/game/save"), 12)
    BackToMainMenuButton = gameObjs.Button(pygame.Rect(DISPLAY.get_width() - 120,35,0,0),reg.ReadKey("/strings/button/game/main_menu"),12)
    OpenStoreButton = gameObjs.Button(pygame.Rect(5,DISPLAY.get_height() - 25,0,0),reg.ReadKey("/strings/button/game/store"),14)
    OpenInfosWindowButton = gameObjs.Button(pygame.Rect(0, 0, 0, 0), reg.ReadKey("/strings/button/game/infos"), 14)
    OpenExperienceWindowButton = gameObjs.Button(pygame.Rect(0,0,0,0), reg.ReadKey("/strings/button/game/experience_store"), 14)
    ItemsView = gameObjs.HorizontalItemsView(pygame.Rect(5, 500, 430, 100))

    IncomingLog.Initialize()

    # -- Load Saved Values -- #
    LoadGame()
    print("GameScreen : All objects initialized.")

    # -- Initialize Objects -- #
    storeWindow.Initialize()
    expStoreWindow.Initialize()
    infosWindow.Initialize()
    gameMain.ClearColor = (5, 20, 14)

def Unload():
    global StoreWindow_Enabled
    global UnloadDelay
    global UnloadRequested
    save.Unload()

    # -- Clear Game Items -- #
    save.GameItemsList.clear()
    StoreWindow_Enabled = False

    IncomingLog.Unload()

    print("GameScreen : Restart storeWindow")
    storeWindow.RestartAnimation()

    print("GameScreen : Restart Unload Variables")
    UnloadRequested = False
    UnloadDelay = 0

def EventUpdate(event):
    # -- Update all buttons -- #
    global GrindButton
    global GameOptionsButton
    global SaveButton
    global BackToMainMenuButton
    global OpenStoreButton
    global StoreWindow_Enabled
    global ItemsView
    global IsControlsEnabled
    global OpenExperienceWindowButton
    global OpenInfosWindowButton

    if IsControlsEnabled:
        GrindButton.Update(event)
        GameOptionsButton.Update(event)
        SaveButton.Update(event)
        BackToMainMenuButton.Update(event)
        OpenStoreButton.Update(event)
        ItemsView.Update(event)
        IncomingLog.EventUpdate(event)
        OpenInfosWindowButton.Update(event)
        if save.GameItems_TotalIndx_NegativeOne == 1:
            OpenExperienceWindowButton.Update(event)

        # -- Update store Window -- #
        if StoreWindow_Enabled:
            storeWindow.EventUpdate(event)

        # -- Update Infos Window -- #
        if InfosWindow_Enabled:
            infosWindow.EventUpdate(event)

        if ExperienceStore_Enabled:
            expStoreWindow.EventUpdate(event)

    if event.type == pygame.KEYUP and event.key == pygame.K_z:
        GrindClick()

    if event.type == pygame.KEYUP and event.key == pygame.K_m:
        GrindClick()



def GrindClick():
    save.Current_TotalClicks += 1

    if save.Current_TotalClicks == save.Current_TotalClicksNext:
        save.Current_TotalClicksNext = save.Current_TotalClicks + save.Current_TotalClicksForEach
        save.CUrrent_Experience += save.Current_ExperiencePerEach
        IncomingLog.AddMessageText("€+" + str(save.Current_ExperiencePerEach), False, (150,150,150))

    IncomingLog.AddMessageText("$+" + str(save.Current_MoneyValuePerClick), True, (20, 150, 25), save.Current_MoneyValuePerClick)