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

# -- Imports --
import glob
from ENGINE import UTILS as utils
import ENGINE as tge
import os
print("TaiyouRegistryManager version " + tge.Get_RegistryVersion())


# Variables
reg_keys = list()
reg_contents = list()


def Initialize(reg_dir):
    """
    Load all keys on Specified Folder
    :param reg_dir:Specified Folder
    :return:
    """
    print("\nTaiyou.RegistryManager.Initialize : Loading Registry...")

    temp_reg_keys = utils.GetFileInDir(reg_dir)
    index = -1

    for x in temp_reg_keys:
        index += 1

        CorrectKeyName = x.replace(reg_dir,"").replace(".data","")
        file = open(x,"r")

        CurrentLine = file.read().splitlines()
        AllData = ""
        for x in CurrentLine:
            if not x.startswith("#"):
                AllData += x + "\n"

        # -- Format the Text -- #
        AllData = AllData.rstrip().replace("%n", "\n").replace("%t","\t").replace("%s"," ")

        reg_contents.append(AllData)
        reg_keys.append(CorrectKeyName)
        print("Taiyou.RegistryManager.Initialize : KeyLoaded[" + CorrectKeyName + "]")

    print("Taiyou.RegistryManager.Initialize : Operation Completed.")
    print("Taiyou.RegistryManager.Initialize : Total of {0} registry keys loaded.".format(str(len(reg_keys))))

def Reload():
    """
    Reload all Registry Keys
    :return:
    """
    print("Taiyou.RegistryManager.ReloadRegistry : Re-Loading Game Registry...")
    CurrentGameFolder = tge.Get_GameSourceFolder() + "/REG"

    Unload()
    Initialize(CurrentGameFolder)
    print("Taiyou.RegistryManager.UnloadRegistry : Re-Loading System Registry...")

    Initialize("Taiyou/SYSTEM/SOURCE/REG")

    print("Taiyou.RegistryManager.UnloadRegistry : Operation Completed.")

def Unload():
    """
    Unload all registry keys
    :return:
    """
    print("Taiyou.RegistryManager.UnloadRegistry : Unloading Registry...")

    # -- Clear the Registry -- #
    reg_keys.clear()
    reg_contents.clear()

    print("Taiyou.RegistryManager.UnloadRegistry : Re-Loading System Registry...")

    Initialize("Taiyou/SYSTEM/SOURCE/REG")

    print("Taiyou.RegistryManager.UnloadRegistry : Operation Completed.")


# -- Game Keys -- #
def CorrectKeyName(keyEntred):
    if not keyEntred.startswith("/"):
        return "/" + keyEntred
    else:
        return keyEntred

def ReadKey(keyName):
    """
    Returns a String Key
    :param keyName:Name of Key [starting with /]
    :return:KeyData
    """
    return reg_contents[reg_keys.index(CorrectKeyName(keyName))]

def ReadKey_int(keyName):
    """
    Returns a Integer Key
    :param keyName:Name of Key [starting with /]
    :return:KeyData
    """
    return int(reg_contents[reg_keys.index(CorrectKeyName(keyName))])

def ReadKey_float(keyName):
    """
    Returns a Float Key
    :param keyName:Name of Key [starting with /]
    :return:KeyData
    """
    return float(reg_contents[reg_keys.index(CorrectKeyName(keyName))])

def ReadKey_bool(keyName):
    """
    Returns a Boolean Key
    :param keyName:Name of Key [starting with /]
    :return:KeyData
    """
    if reg_contents[reg_keys.index(CorrectKeyName(keyName))] == "True":
        return True
    else:
        return False

def WriteKey(keyName, keyValue, WriteOnSystemReg=False):
    """
    Write data to a Key
    :param keyName:Name of Key [starting with /]
    :param keyValue:Key Value
    :return:
    """
    keyName = CorrectKeyName(keyName)
    if not WriteOnSystemReg:
        FileLocation = tge.Get_GameSourceFolder() + "/REG" + keyName + ".data"
    else:
        FileLocation = "Taiyou/SYSTEM/SOURCE/REG" + keyName + ".data"

    # -- Create the directory if not exists -- #
    os.makedirs(os.path.dirname(FileLocation), exist_ok=True)

    print("Taiyou.RegistryManager.WriteKey : Registry File Location;" + FileLocation)

    f = open(FileLocation, "w+")
    f.write(keyValue)
    f.close()

    try:
        RegIndex = reg_keys.index(keyName)
        reg_contents[RegIndex] = keyValue

    except:
        reg_keys.append(keyName)
        reg_contents.append(keyValue)

    print("Taiyou.RegistryManager.WriteKey : Registry File Writed.")


def KeyExists(keyName):
    """
    Returns True if the Specified Key Exists
    :param keyName: Specified Key [starting with /]
    :return: Value to Return
    """
    try:
        Test = reg_contents[reg_keys.index(CorrectKeyName(keyName))]
        return True
    except:
        return False


# -- Read key with Try -- #
def ReadKeyWithTry(keyName,defaultValue):
    """
    Tries to Read a Key, if there is a error, Return Default Value [String]
    :param keyName:Name of Key [starting with /]
    :param defaultValue:Default Value to Return
    :return:KeyData
    """
    try:
        return reg_contents[reg_keys.index(CorrectKeyName(keyName))]
    except:
        WriteKey(CorrectKeyName(keyName),defaultValue)
        return defaultValue

def ReadKeyWithTry_int(keyName,defaultValue):
    """
    Tries to Read a Key, if there is a error, Return Default Value [Integer]
    :param keyName:Name of Key [starting with /]
    :param defaultValue:Default Value to Return
    :return:KeyData
    """
    try:
        return int(reg_contents[reg_keys.index(CorrectKeyName(keyName))])
    except:
        WriteKey(CorrectKeyName(keyName),str(defaultValue))
        return int(defaultValue)

def ReadKeyWithTry_float(keyName,defaultValue):
    """
    Tries to Read a Key, if there is a error, Return Default Value [Float]
    :param keyName:Name of Key [starting with /]
    :param defaultValue:Default Value to Return
    :return:KeyData
    """
    try:
        return float(reg_contents[reg_keys.index(CorrectKeyName(keyName))])
    except:
        WriteKey(CorrectKeyName(keyName),str(defaultValue))
        return float(defaultValue)

def ReadKeyWithTry_bool(keyName,defaultValue):
    """
    Tries to Read a Key, if there is a error, Return Default Value [Boolean]
    :param keyName:Name of Key [starting with /]
    :param defaultValue:Default Value to Return
    :return:KeyData
    """
    try:
        if reg_contents[reg_keys.index(CorrectKeyName(keyName))] == "True":
            return True
        else:
            return False

    except:
        WriteKey(keyName,str(defaultValue))
        if reg_contents[reg_keys.index(CorrectKeyName(keyName))] == "True":
            return True
        else:
            return False

# -- Read App Data Functions -- #

def ReadAppData(FileName, DataType=str):
    FileLocation = tge.Get_GlobalAppDataFolder() + "/" + FileName + ".data"
    file = open(FileLocation, "r")

    ReadData = file.read().rstrip()

    if DataType == str:
        return ReadData
    if DataType == float:
        return float(ReadData)
    if DataType == int:
        return int(ReadData)
    if DataType == bool:
        if ReadData == "True":
            return True
        else:
            return False

    print("Taiyou.Registry.ReadAppData : File[{0}] has been read.".format(FileName))


def ReadAppData_WithTry(FileName, DataType, DefaultValue):
    try:
        return ReadAppData(FileName, DataType)
    except:
        WriteAppData(FileName, DefaultValue)
        return ReadAppData(FileName, DataType)

def WriteAppData(FileName, Data):
    FileLocation = tge.Get_GlobalAppDataFolder() + "/" + FileName + ".data"
    os.makedirs(os.path.dirname(FileLocation), exist_ok=True)

    f = open(FileLocation, "w+")
    f.write(str(Data))
    f.close()

    print("Taiyou.Registry.WriteAppData : File[{0}] has been written.".format(FileName))
