#!/usr/bin/python3
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
import ENGINE.Utils as utils
import ENGINE.TGE as tge
import os
print("RegistryManager version 1.0")

# Variables
system_reg_keys = list()
system_reg_contents = list()
reg_keys = list()
reg_contents = list()


def Initialize(reg_dir):
    print("\nRegistry : Initializing the Keys...")
    temp_reg_keys = utils.GetFileInDir(reg_dir)
    index = -1

    for x in temp_reg_keys:
        index += 1

        CorrectKeyName = x.replace(reg_dir,"").replace(".data","")
        file = open(x,"r")
        reg_contents.append(file.read().rstrip().replace("%n", "\n").replace("%t","\t"))
        reg_keys.append(CorrectKeyName)
        print("Registry : KeyLoaded[" + CorrectKeyName + "]")

    print("Registry : Load Complete.\n")

# -- Game Keys -- #
def ReadKey(keyName):
    return reg_contents[reg_keys.index(keyName)]

def ReadKey_int(keyName):
    return int(reg_contents[reg_keys.index(keyName)])

def ReadKey_float(keyName):
    return float(reg_contents[reg_keys.index(keyName)])

def ReadKey_bool(keyName):
    return eval(reg_contents[reg_keys.index(keyName)])

def WriteKey(keyName, keyValue):
    FileLocation = tge.Get_GameSourceFolder() + "/REG" + keyName + ".data"
    BarraSplit = keyName.split('/')
    CorrectDir = tge.Get_GameSourceFolder() + "/REG/" + BarraSplit[len(BarraSplit) - 2]
    if not os.path.exists(CorrectDir):
        os.makedirs(CorrectDir)
        print("WriteKey : Directory[" + CorrectDir + "]created.")

    print("WriteKey : Registry File Location;" + FileLocation)

    f = open(FileLocation, "w+")
    f.write(keyValue)
    f.close()

    try:
        RegIndex = reg_keys.index(keyName)
        reg_contents[RegIndex] = keyValue

    except:
        reg_keys.append(keyName)
        reg_contents.append(keyValue)

    print("WriteKey : Registry File Writed.")

def KeyExists(keyName):
    try:
        Test = reg_contents[reg_keys.index(keyName)]
        return True
    except:
        return False


# -- Read key with Try -- #
def ReadKeyWithTry(keyName,defaultValue):
    try:
        return reg_contents[reg_keys.index(keyName)]
    except:
        WriteKey(keyName,defaultValue)
        return defaultValue

def ReadKeyWithTry_int(keyName,defaultValue):
    try:
        return int(reg_contents[reg_keys.index(keyName)])
    except:
        WriteKey(keyName,str(defaultValue))
        return int(defaultValue)

def ReadKeyWithTry_float(keyName,defaultValue):
    try:
        return float(reg_contents[reg_keys.index(keyName)])
    except:
        WriteKey(keyName,str(defaultValue))
        return float(defaultValue)

def ReadKeyWithTry_bool(keyName,defaultValue):
    try:
        return bool(reg_contents[reg_keys.index(keyName)])
    except:
        WriteKey(keyName,str(defaultValue))
        return bool(defaultValue)

