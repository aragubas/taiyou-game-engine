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
import os, time
print("TaiyouRegistryManager version " + tge.Get_RegistryVersion())


# Variables
reg_keys = ()
reg_contents = ()
SystemReg_keys = ()
SystemReg_contents = ()


def Initialize(reg_dir, LoadOnSystemReg=False):
    """
    Load all keys on Specified Folder
    :param reg_dir:Specified Folder
    :return:
    """
    global reg_keys
    global reg_contents
    global SystemReg_keys
    global SystemReg_contents

    start_time = time.time()
    # -- Unload the Registry -- #
    Unload(LoadOnSystemReg)

    if not LoadOnSystemReg:
        print("Taiyou.RegistryManager.Initialize : Loading Application Registry")
    else:
        print("Taiyou.RegistryManager.Initialize : Loading System Registry")

    reg_dir = reg_dir + "Data/REG"
    temp_reg_keys = utils.Directory_FilesList(reg_dir)
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

        if not LoadOnSystemReg:
            reg_keys += (CorrectKeyName,)
            reg_contents += (AllData,)

        else:
            SystemReg_keys += (CorrectKeyName,)
            SystemReg_contents += (AllData,)

        print("Taiyou.RegistryManager.Initialize : KeyLoaded[" + CorrectKeyName + "]")

    if not LoadOnSystemReg:
        print("Taiyou.RegistryManager.Initialize : Total of {0} registry keys loaded. In {1} seconds.".format(str(len(reg_keys)), utils.FormatNumber(time.time() - start_time, 4)))
    else:
        print("Taiyou.RegistryManager.Initialize : Total of {0} System Registry keys loaded. In {1} seconds".format(str(len(SystemReg_keys)), utils.FormatNumber(time.time() - start_time, 4)))

    utils.GarbageCollector_Collect()



def Reload(ReloadSystemReg=False):
    """
    Reload all Registry Keys
    :return:
    """
    CurrentGameFolder = tge.Get_GameFolder() + "/"

    if not ReloadSystemReg:
        print("Taiyou.RegistryManager.ReloadRegistry : Reloading Application Registry...")
        Unload()
        Initialize(CurrentGameFolder)

    else:
        print("Taiyou.RegistryManager.ReloadRegistry : Reloading System Registry...")
        Unload(True)
        Initialize("Taiyou/SYSTEM/", True)

    utils.GarbageCollector_Collect()

def Unload(UnloadSystemReg=False):
    """
    Unload all registry keys
    :return:
    """
    global reg_keys
    global reg_contents
    global SystemReg_keys
    global SystemReg_contents

    # -- Clear the Registry -- #
    if not UnloadSystemReg:
        print("Taiyou.RegistryManager.UnloadRegistry : Unloading Application Registry")
        reg_keys = ()
        reg_contents = ()

    else:
        print("Taiyou.RegistryManager.UnloadRegistry : Unloading System Registry")
        SystemReg_keys = ()
        SystemReg_contents = ()

    utils.GarbageCollector_Collect()

# -- Read Keys -- #
def CorrectKeyName(keyEntred):
    if not keyEntred.startswith("/"):
        return "/" + keyEntred
    else:
        return keyEntred

def ReadKey(keyName, SystemReg=False):
    """
    Returns a String Key
    :param keyName:Name of Key [starting with /]
    :return:KeyData
    """
    global reg_contents
    global SystemReg_contents
    global SystemReg_keys
    global reg_keys

    try:
        if not SystemReg:
            return reg_contents[reg_keys.index(CorrectKeyName(keyName))]
        else:
            return SystemReg_contents[SystemReg_keys.index(CorrectKeyName(keyName))]
    except ValueError:
        if SystemReg:
            raise FileNotFoundError("Taiyou.Registry Error!\nCannot find the Registry Key [{0}] in System Registry.".format(str(keyName)))
        else:
            raise FileNotFoundError("Taiyou.Registry Error!\nCannot find the Registry Key [{0}].".format(str(keyName)))

def ReadKey_int(keyName, SystemReg=False):
    """
    Returns a Integer Key
    :param keyName:Name of Key [starting with /]
    :return:KeyData
    """
    global reg_contents
    global SystemReg_contents
    global SystemReg_keys
    global reg_keys
    try:
        if not SystemReg:
            return int(reg_contents[reg_keys.index(CorrectKeyName(keyName))])
        else:
            return int(SystemReg_contents[SystemReg_keys.index(CorrectKeyName(keyName))])
    except ValueError:
        if SystemReg:
            raise FileNotFoundError("Taiyou.Registry Error!\nCannot find the Registry Key [{0}] in System Registry.".format(str(keyName)))
        else:
            raise FileNotFoundError("Taiyou.Registry Error!\nCannot find the Registry Key [{0}].".format(str(keyName)))

def ReadKey_float(keyName, SystemReg=False):
    """
    Returns a Float Key
    :param keyName:Name of Key [starting with /]
    :return:KeyData
    """
    global reg_contents
    global SystemReg_contents
    global SystemReg_keys
    global reg_keys

    try:
        if not SystemReg:
            return float(reg_contents[reg_keys.index(CorrectKeyName(keyName))])
        else:
            return float(SystemReg_contents[SystemReg_keys.index(CorrectKeyName(keyName))])
    except ValueError:
        if SystemReg:
            raise FileNotFoundError("Taiyou.Registry Error!\nCannot find the Registry Key [{0}] in System Registry.".format(str(keyName)))
        else:
            raise FileNotFoundError("Taiyou.Registry Error!\nCannot find the Registry Key [{0}].".format(str(keyName)))

def ReadKey_bool(keyName, SystemReg=False):
    """
    Returns a Boolean Key
    :param keyName:Name of Key [starting with /]
    :return:KeyData
    """
    global reg_contents
    global SystemReg_contents
    global SystemReg_keys
    global reg_keys

    try:
        if not SystemReg:
            if reg_contents[reg_keys.index(CorrectKeyName(keyName))] == "True":
                return True
            else:
                return False
        else:
            if SystemReg_contents[SystemReg_keys.index(CorrectKeyName(keyName))] == "True":
                return True
            else:
                return False
    except ValueError:
        if SystemReg:
            raise FileNotFoundError("Taiyou.Registry Error!\nCannot find the Registry Key [{0}] in System Registry.".format(str(keyName)))
        else:
            raise FileNotFoundError("Taiyou.Registry Error!\nCannot find the Registry Key [{0}].".format(str(keyName)))



def WriteKey(keyName, keyValue, WriteOnSystemReg=False):
    """
    Write data to a Key
    :param keyName:Name of Key [starting with /]
    :param keyValue:Key Value
    :return:
    """
    global reg_contents
    global SystemReg_contents
    global SystemReg_keys
    global reg_keys

    keyName = CorrectKeyName(keyName)
    if not WriteOnSystemReg:
        FileLocation = tge.Get_GameSourceFolder() + "/REG" + keyName + ".data"
    else:
        FileLocation = "Taiyou/SYSTEM/Data/REG" + keyName + ".data"

    # -- Create the directory -- #
    os.makedirs(os.path.dirname(FileLocation), exist_ok=True)

    print("Taiyou.RegistryManager.WriteKey : Registry File Location;" + FileLocation)

    # -- Write the Actual Registry Key -- #
    f = open(FileLocation, "w+")
    f.write(keyValue)
    f.close()

    Reload(WriteOnSystemReg)

    print("Taiyou.RegistryManager.WriteKey : Registry File Writed.")


def KeyExists(keyName):
    """
    Returns True if the Specified Key Exists
    :param keyName: Specified Key [starting with /]
    :return: Value to Return
    """
    global reg_contents
    global SystemReg_contents
    global SystemReg_keys
    global reg_keys

    try:
        Test = reg_contents[reg_keys.index(CorrectKeyName(keyName))]
        return True
    except ValueError:
        return False


# -- Read key with Try -- #
def ReadKeyWithTry(keyName,defaultValue):
    """
    Tries to Read a Key, if there is a error, Return Default Value [String]
    :param keyName:Name of Key [starting with /]
    :param defaultValue:Default Value to Return
    :return:KeyData
    """
    global reg_contents
    global SystemReg_contents
    global SystemReg_keys
    global reg_keys

    try:
        return reg_contents[reg_keys.index(CorrectKeyName(keyName))]
    except ValueError:
        WriteKey(CorrectKeyName(keyName),defaultValue)
        return defaultValue

def ReadKeyWithTry_int(keyName,defaultValue):
    """
    Tries to Read a Key, if there is a error, Return Default Value [Integer]
    :param keyName:Name of Key [starting with /]
    :param defaultValue:Default Value to Return
    :return:KeyData
    """
    global reg_contents
    global SystemReg_contents
    global SystemReg_keys
    global reg_keys

    try:
        return int(reg_contents[reg_keys.index(CorrectKeyName(keyName))])
    except ValueError:
        WriteKey(CorrectKeyName(keyName),str(defaultValue))
        return int(defaultValue)

def ReadKeyWithTry_float(keyName,defaultValue):
    """
    Tries to Read a Key, if there is a error, Return Default Value [Float]
    :param keyName:Name of Key [starting with /]
    :param defaultValue:Default Value to Return
    :return:KeyData
    """
    global reg_contents
    global SystemReg_contents
    global SystemReg_keys
    global reg_keys

    try:
        return float(reg_contents[reg_keys.index(CorrectKeyName(keyName))])
    except ValueError:
        WriteKey(CorrectKeyName(keyName),str(defaultValue))
        return float(defaultValue)

def ReadKeyWithTry_bool(keyName,defaultValue):
    """
    Tries to Read a Key, if there is a error, Return Default Value [Boolean]
    :param keyName:Name of Key [starting with /]
    :param defaultValue:Default Value to Return
    :return:KeyData
    """
    global reg_contents
    global SystemReg_contents
    global SystemReg_keys
    global reg_keys

    try:
        if reg_contents[reg_keys.index(CorrectKeyName(keyName))] == "True":
            return True
        else:
            return False

    except ValueError:
        WriteKey(keyName,str(defaultValue))
        if reg_contents[reg_keys.index(CorrectKeyName(keyName))] == "True":
            return True
        else:
            return False

# -- Read App Data Functions -- #

def ReadAppData(FileName, DataType=str):
    """
    Read a file on the App Data Folder, raises ValueError if Save Folder was not initialized
    :param FileName:File Name
    :param DataType:Data Type
    :return:Data
    """
    if tge.Get_SaveFolderInitialized():
        FileLocation = tge.Get_GlobalAppDataFolder() + tge.Get_SaveFolder() + FileName + ".data"
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
    else:
        raise ValueError("Taiyou.Registry.ReadAppData.Exception! : Save Folder was not initialized.")

def ReadAppData_WithTry(FileName, DataType, DefaultValue):
    """
    Runs ReadAppData but if data does not exist, it writes it
    :param FileName:File Name
    :param DataType:Data Type
    :param DefaultValue:Default Value to be written
    :return:Data
    """
    try:
        return ReadAppData(FileName, DataType)
    except FileNotFoundError:
        WriteAppData(FileName, DefaultValue)
        return ReadAppData(FileName, DataType)

def WriteAppData(FileName, Data):
    """
    Write Data to the AppData Folder, raises ValueError if Save Folder was not initialized.
    :param FileName:File Name
    :param DataType:Data Type
    :param DefaultValue:Default Value to be written
    :return:Data
    """
    if tge.Get_SaveFolderInitialized():
        FileLocation = tge.Get_GlobalAppDataFolder() + tge.Get_SaveFolder() + FileName + ".data"
        os.makedirs(os.path.dirname(FileLocation), exist_ok=True)

        f = open(FileLocation, "w+")
        f.write(str(Data))
        f.close()

        print("Taiyou.Registry.WriteAppData : File[{0}] has been written.".format(FileLocation))
    else:
        raise ValueError("Taiyou.Registry.WriteAppData.Exception! : Save Folder was not initialized.")