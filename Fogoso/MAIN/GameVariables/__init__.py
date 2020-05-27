#!/usr/bin/ python3.7
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
from ENGINE import REGISTRY as reg
from Fogoso.MAIN.Screens import Game as gameScr
from Fogoso.MAIN import ClassesUtils as gameObjs
from Fogoso.MAIN import Items as items
from ENGINE import UTILS as utils

print("Fogoso Save Management, version 1.3")

# -- Money -- #
Current_Money = 0.0
Current_MoneyValuePerClick = 0.2

# -- Experience -- #
CUrrent_Experience = 250
Current_TotalClicks = 0
Current_TotalClicksNext = 0
Current_TotalClicksForEach = 0
Current_ExperiencePerEach = 20

# -- Formated Money Strings -- #
Current_MoneyPerSecound = 0.0
Current_MoneyFormated = "0,00"
Current_MoneyPerSecoundFormatted = "0,00"
CUrrent_ExperienceFormated = "0"

# -- Game Items Variables -- #
GameItemsList = list()
GameItemsInitialized = False
GameItems_TotalIndx_0 = 0
GameItems_TotalIndx_NegativeOne = 0

# -- Money Per Secound -- #
MoneyPerSecound_Delta = 0
MoneyPerSecound_Last = 0.0

# -- Load Save Data -- #
def LoadSaveData():
    global GameItemsList
    global GameItems_TotalIndx_0
    global GameItems_TotalIndx_NegativeOne
    global Current_TotalClicks
    global Current_TotalClicksNext
    global Current_TotalClicksForEach
    global Current_ExperiencePerEach
    global CUrrent_Experience
    global Current_Money
    global Current_MoneyValuePerClick
    global GameItemsInitialized

    Current_Money = reg.ReadKeyWithTry_float("/Save/money", 0.05)
    Current_MoneyValuePerClick = reg.ReadKeyWithTry_float("/Save/money_per_click", 0.1)
    CUrrent_Experience = reg.ReadKeyWithTry_int("/Save/experience", 1500)
    Current_TotalClicks = reg.ReadKeyWithTry_int("/Save/total_clicks", 0.1)
    Current_TotalClicksForEach = reg.ReadKeyWithTry_int("/Save/total_clicks_each", 50)
    Current_ExperiencePerEach = reg.ReadKeyWithTry_int("/Save/total_experience_per_each", 20)

    Current_TotalClicksNext = Current_TotalClicks + Current_TotalClicksForEach


# -- Restart Items Data -- #
def RestartItems():
    global GameItemsInitialized
    global GameItemsList
    global GameItems_TotalIndx_0
    global GameItems_TotalIndx_NegativeOne
    print("RestartItems : Clear Item Data...")
    GameItemsInitialized = False
    GameItems_TotalIndx_0 = 0
    GameItems_TotalIndx_NegativeOne = 0
    GameItemsList.clear()

    LoadItems()

# -- Load Items Data -- #
def LoadItems():
    global GameItems_TotalIndx_NegativeOne
    global GameItems_TotalIndx_0
    global GameItemsList
    global GameItemsInitialized
    AllKeys = 0
    SavedItemsData = reg.ReadKey("/Save/item/items").splitlines()

    for i, x in enumerate(SavedItemsData):
        print("LoadItems ; Loading ItemID: " + x)

        gameScr.ItemsView.AddItem(x)

        if x == "0":
            GameItems_TotalIndx_0 += 1
            GameItemsList.append(gameObjs.Item_AutoClicker())
        if x == "-1":
            GameItems_TotalIndx_NegativeOne += 1
            GameItemsList.append(gameObjs.Item_ExperienceStore())
    GameItemsInitialized = True
    print("LoadItems ; AllItemsLoaded: " + str(AllKeys))
    if GameItems_TotalIndx_NegativeOne > 1:
        print(reg.ReadKey("/strings/game/save_reset"))
        RestartSaveData()

def RestartSaveData():
    print("RestartSave : Restarting save data...")

    ResetKeysString = reg.ReadKey("/Save/reset_keys").splitlines()
    DefaultValuesStrings = reg.ReadKey("/Save/reset_keys_default_values").splitlines()

    for x in range(0, len(ResetKeysString)):
        print("RestartSave : CurrentID{0}".format(x))
        reg.WriteKey(ResetKeysString[x], DefaultValuesStrings[x])

    print("RestartSave : Operation completed successfully.")
    reg.WriteKey("/Save/cheater", "True")
    LoadSaveData()
    LoadItems()

def SaveData():
    reg.WriteKey("/Save/money", str(Current_Money))
    reg.WriteKey("/Save/money_per_click", str(Current_MoneyValuePerClick))
    reg.WriteKey("/Save/total_clicks", str(Current_TotalClicks))
    reg.WriteKey("/Save/total_clicks_each", str(Current_TotalClicksForEach))
    reg.WriteKey("/Save/total_experience_per_each", str(Current_ExperiencePerEach))


# -- Save Items Data -- #
def SaveItems():
    global GameItemsList
    AllItemsData = ""
    for i in range(0,len(GameItemsList)):
        print("SaveItem : id:" + str(i))
        if i >= 1:
            AllItemsData += "\n" + str(GameItemsList[i].ItemID)
        else:
            AllItemsData += str(GameItemsList[i].ItemID)
        print("SaveItem : Item saved.")
    reg.WriteKey("/Save/item/items",AllItemsData)

def Unload():
    global Current_Money
    global Current_MoneyValuePerClick
    global CUrrent_Experience
    global GameItemsList
    global GameItemsInitialized
    global GameItems_TotalIndx_NegativeOne
    global GameItems_TotalIndx_0

def Update():
    global Current_Money
    global Current_MoneyValuePerClick
    global Current_MoneyPerSecound
    global GameItemsList
    global GameItemsInitialized
    global Current_MoneyFormated
    global Current_MoneyPerSecoundFormatted
    global MoneyPerSecound_Delta
    global MoneyPerSecound_Last
    global CUrrent_ExperienceFormated

    # -- Updated Formated Strings -- #
    Current_MoneyFormated = utils.FormatNumber(Current_Money,2)
    Current_MoneyPerSecoundFormatted = utils.FormatNumber(Current_MoneyPerSecound,2)
    CUrrent_ExperienceFormated = utils.FormatNumber(CUrrent_Experience,2)

    # -- Update Money Per Secound -- #
    MoneyPerSecound_Delta += 1
    if MoneyPerSecound_Delta == 1000:
        Current_MoneyPerSecound = Current_Money - MoneyPerSecound_Last
        MoneyPerSecound_Last = Current_Money
        MoneyPerSecound_Delta = 0

    # -- Update All Loaded Items -- #
    if GameItemsInitialized:
        for x in GameItemsList:
            x.Update()
