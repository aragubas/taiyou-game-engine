# -- Imports -- #
import ENGINE.TGE as tge
import os

print("TGEUtils version 1.0")


def GetFileInDir(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + GetFileInDir(fullPath)
        else:
            allFiles.append(fullPath)
            
    return allFiles

def GetCurrentSourceFolder():
    return tge.Get_GameSourceFolder()