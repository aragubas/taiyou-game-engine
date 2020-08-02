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
import os, shutil, requests, string, random, threading, zipfile, urllib.request, gc, psutil
from pathlib import Path
from urllib.error import HTTPError
import binascii
import struct
from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
import glob

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

def FormatNumber(num, precision=2, suffixes=['', 'K', 'M', 'G', 'T', 'P']):
    m = sum([abs(num/1000.0**x) >= 1 for x in range(1, len(suffixes))])
    return f'{num/1000.0**m:.{precision}f}{suffixes[m]}'

def GetImage_DominantColor(Surface, Number_Clusters=5):
    strFormat = 'RGBA'
    raw_str = pygame.image.tostring(Surface, strFormat)
    ConvertedImage = Image.frombytes(strFormat, Surface.get_size(), raw_str)

    ConvertedImage = ConvertedImage.resize((100, 100))  # optional, to reduce time
    ar = np.asarray(ConvertedImage)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

    codes, dist = scipy.cluster.vq.kmeans(ar, Number_Clusters)

    vecs, dist = scipy.cluster.vq.vq(ar, codes)  # assign codes
    counts, bins = scipy.histogram(vecs, len(codes))  # count occurrences

    index_max = scipy.argmax(counts)  # find most frequent
    peak = codes[index_max]
    return peak


def FixColorRange(ColorArguments):
    """
    Fix the Color Range (0 - 255)
    :param ColorArguments: Input
    :return: Output
    """
    ColorArguments = list(ColorArguments)

    if len(ColorArguments) < 4:  # -- Add the Alpha Argument
        ColorArguments.append(255)

    # -- Limit the Color Range -- #
    if int(ColorArguments[0]) < 0:  # -- R
        ColorArguments[0] = 0
    if int(ColorArguments[1]) < 0:  # -- G
        ColorArguments[1] = 0
    if int(ColorArguments[2]) < 0:  # -- B
        ColorArguments[2] = 0
    if int(ColorArguments[3]) < 0:  # -- A
        ColorArguments[3] = 0

    if int(ColorArguments[0]) > 255:  # -- R
        ColorArguments[0] = 255
    if int(ColorArguments[1]) > 255:  # -- G
        ColorArguments[1] = 255
    if int(ColorArguments[2]) > 255:  # -- B
        ColorArguments[2] = 255
    if int(ColorArguments[3]) > 255:  # -- A
        ColorArguments[3] = 255

    return ColorArguments


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
        self.DownloadMetaData.append("0")  # -- Index 0 is File Size
        self.DownloadMetaData.append("0")  # -- Index 1 is Download Progress

        # -- Create the Path for Download -- #
        Directory_MakeDir(Get_DirectoryOfFilePath(self.InstanceFileName))

        # -- Create the Download Thread -- #
        self.DownloadThread = threading.Thread(target=self.Update)
        self.DownloadThread.daemon = True
        self.DownloadThread.start()

def GarbageCollector_Collect():
    return
    gc.collect()
    print("Taiyou.Utils.GC_COLLECT : Function Called")

def GarbageCollector_GetInfos():

    InfosString = "Count: {0}".format(gc.get_count())

    return InfosString

def Get_MemoryUsage():
    return psutil.Process(os.getpid()).memory_full_info()[0]

class AnimationController:
    def __init__(self, multiplierSpeed=1.0, maxValue=255, minValue=0, multiplierRestart=False):
        self.Enabled = True
        self.CurrentMode = True
        self.Value = 0
        self.ValueMultiplier = 0
        self.ValueMultiplierSpeed = multiplierSpeed
        self.MaxValue = maxValue
        self.MinValue = minValue
        self.DisableSignal = False
        self.RestartMultiplier = multiplierRestart

    def Update(self):
        if self.DisableSignal:
            # -- Animation TRUE end -- #
            if self.Value >= self.MaxValue:
                self.Value = self.MaxValue
                self.Enabled = False
                self.CurrentMode = False
                if self.RestartMultiplier:
                    self.ValueMultiplier = 0

            elif self.Value <= self.MinValue:  # -- Animation FALSE end -- #
                self.Value = self.MinValue
                self.Enabled = False
                self.ValueMultiplier = 0
                self.CurrentMode = True

            self.DisableSignal = False

        if self.Enabled:
            # -- Increase the Multiplier -- #
            self.ValueMultiplier += self.ValueMultiplierSpeed

            if self.CurrentMode:
                self.Value += self.ValueMultiplier

                if self.Value >= self.MaxValue:
                    self.DisableSignal = True

            else:
                self.Value -= self.ValueMultiplier

                if self.Value <= self.MinValue:
                    self.DisableSignal = True
