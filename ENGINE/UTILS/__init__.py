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
import ENGINE as tge
import shutil
import os

print("TaiyouGameEngineUtils version " + tge.Get_UtilsVersion())


def GetFileInDir(dirName):
    # -- Create a list with all files in Directory -- #
    listOfFile = os.listdir(dirName)
    allFiles = list()

    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + GetFileInDir(fullPath)
        else:
            allFiles.append(fullPath)
            
    return allFiles

def GetCurrentSourceFolder():
    return tge.Get_GameSourceFolder()

def FormatNumber(num, precision=2, suffixes=['', 'K', 'M', 'G', 'T', 'P']):
    m = sum([abs(num/1000.0**x) >= 1 for x in range(1, len(suffixes))])
    return f'{num/1000.0**m:.{precision}f}{suffixes[m]}'

def File_Exists(path):
    return os.path.isfile(path)

def Directory_Exists(path):
    return os.path.exists(path)

def FileCopy(path, destinationPath):
    shutil.copy(path, destinationPath)