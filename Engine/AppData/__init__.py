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
from Engine import Utils
import Engine as tge
import os, time
print("Taiyou AppData version " + tge.Get_AppDataVersion())

# -- Read App Data Functions -- #
def CorrectFileName(Input):
    """
    Returns the Path to the correct AppData Folder
    :param Input: File Name
    :return:Returns the Path
    """
    if not Input.startswith("/"):
        Input = "/" + Input
    Input = tge.TaiyouPath_AppDataFolder + Input + ".sav"

    if not tge.TaiyouPath_CorrectSlash == "/":
        Input.replace("/", tge.TaiyouPath_CorrectSlash)

    return Input


def ReadAppData(FileName, DataType=str):
    """
    Read a file on the App Data Folder, raises ValueError if Save Folder was not initialized
    :param FileName:File Name
    :param DataType:Data Type
    :return:Data
    """
    FileLocation = CorrectFileName(FileName)

    file = open(FileLocation, "r")

    ReadData = file.read().rstrip()

    if DataType == str:
        return ReadData
    if DataType == float:
        return float(ReadData)
    if DataType == int:
        return int(ReadData)
    if DataType == bool:
        return ReadData.lower() in ("true", "yes", "t", "1")

    print("Taiyou.Registry.ReadAppData : File[{0}] has been read.".format(FileName))

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

def GetAppDataPathIO(FileName):
    """
    Write Data to the AppData Folder, File Name MUST Start with [/].
    :param FileName:File Name
    :return:Data to be written
    """
    FileLocation = ''.join((tge.AppDataFolder, FileName))

    # -- Make the Directory if does not exist -- #
    os.makedirs(os.path.dirname(FileLocation), exist_ok=True)

    return open(FileLocation, "w+")

def WriteAppData(FileName, Data):
    """
    Write String Data to AppData Folder
    :param FileName:File Name
    :return:Data to be written
    """

    FileLocation = ''.join((tge.AppDataFolder, FileName))

    os.makedirs(os.path.dirname(FileLocation), exist_ok=True)

    f = open(FileLocation, "w+")
    f.write(str(Data))
    f.close()
