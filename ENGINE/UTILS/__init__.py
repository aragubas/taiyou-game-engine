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
import os, shutil, requests, string, random, threading, zipfile, urllib.request, gc
from pathlib import Path
from urllib.error import HTTPError

print("TaiyouGameEngineUtils version " + tge.Get_UtilsVersion())


def Directory_FilesList(dirName):
    # -- Create a list with all files in Directory -- #
    listOfFile = os.listdir(dirName)
    allFiles = list()

    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + Directory_FilesList(fullPath)
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

def Directory_MakeDir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def Unzip_File(path, destination):
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(destination)

def FileCopy(path, destinationPath):
    shutil.copy(path, destinationPath)

def Calculate_FolderSize(path):
    total_size = 0
    start_path = path  # To get size of current directory
    for path, dirs, files in os.walk(start_path):
        for f in files:
            fp = os.path.join(path, f)
            total_size += os.path.getsize(fp)
    return total_size

def Get_DirectoryOfFilePath(file_path):
    p = Path(file_path)
    return p.parent


def Get_DirectoryTotalOfFiles(path):
    try:
        list = Directory_FilesList(path)  # dir is your directory path
        number_files = len(list)
        return number_files
    except:
        return 0

def Random_String(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def Online_LinkExists(url):
    try:
        conn = urllib.request.urlopen(url)
        return conn.getcode()
    except HTTPError as e:
        return e.code
    except:
        return 404

def Get_Percentage(Percentage, Max, MaxPercentage):
    return (Percentage * Max) / MaxPercentage

def File_Delete(filePath):
    os.remove(filePath)

def Directory_Remove(path):
    shutil.rmtree(path, True)

def Directory_Rename(sourcePath, newName):
    os.rename(sourcePath, newName)

# -- Class Downloader -- #
class Downloader:
    def __init__(self):
        self.Url = ""
        self.DownloadState = "STOPPED"
        self.InstanceFileName = "Taiyou/HOME/Webcache/" + Random_String(20) + ".temp"
        self.DownloadThread = threading.Thread
        self.DownloadMetaData = list()

    def Update(self):
        self.DownloadState = "STARTING"

        Response = Online_LinkExists(self.Url)
        DownloadError = False
        if not Response == 200:
            self.DownloadState = "ERROR_" + str(Response)
            DownloadError = True

        if not DownloadError:
            with open(self.InstanceFileName, "wb") as f:
                response = requests.get(self.Url, stream=True)
                total_length = response.headers.get('content-length')
                self.DownloadMetaData[0] = total_length
                self.DownloadState = "DOWNLOADING"

                if total_length is None:  # no content length header
                    f.write(response.content)
                else:
                    dl = 0
                    total_length = int(total_length)
                    for data in response.iter_content(chunk_size=1024):
                        dl += len(data)
                        f.write(data)
                        done = int(100 * dl / total_length)
                        self.DownloadMetaData[1] = done

            self.DownloadState = "FINISHED"

    def StartDownload(self, Url, FileLocation="default"):
        if FileLocation == "default":
            self.InstanceFileName = "Taiyou/HOME/Webcache/" + Random_String(50) + ".temp"
        else:
            self.InstanceFileName = FileLocation
        # -- Set Download State -- #
        self.DownloadState = "STOPPED"
        # -- Set the Url -- #
        self.Url = Url
        # -- Restart some Variables -- #
        self.DownloadMetaData.clear()
        self.DownloadMetaData.append("0") # -- Index 0 is File Size
        self.DownloadMetaData.append("0") # -- Index 1 is Download Progress

        # -- Create the Path for Download -- #
        Directory_MakeDir(Get_DirectoryOfFilePath(self.InstanceFileName))

        # -- Create the Download Thread -- #
        self.DownloadThread = threading.Thread(target=self.Update)
        self.DownloadThread.daemon = True
        self.DownloadThread.start()

def GarbageCollector_Collect():
    gc.collect()
    print("Taiyou.Utils.GC_COLLECT : Function Called")

def GarbageCollector_GetInfos():
    InfosString = "Count: {0}\nStats: {1}\nDebug: {2}\nThreshold: {3}".format(gc.get_count(), gc.get_stats(), gc.get_debug(), gc.get_threshold())
    return InfosString
