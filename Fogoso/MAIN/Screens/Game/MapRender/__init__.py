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
from ENGINE import UTILS as utils
import ENGINE as tge
from ENGINE import SOUND as sound
from Fogoso.MAIN import ClassesUtils as gameObjs
from Fogoso.MAIN.Screens import Settings as ScreenSettings
from Fogoso import MAIN as gameMain
from Fogoso.MAIN.Window import StoreWindow as storeWindow
from Fogoso.MAIN.Window import ExperienceStore as expStoreWindow
from Fogoso.MAIN.Window import InfosWindow as infosWindow
from ENGINE import SPRITE as sprite
from random import randint
from Fogoso.MAIN import Items as items
import pygame, os
import importlib
import time
from math import *

MapData = list()
MapTileset = 0
MapSizeW = 0
MapSizeH = 0
MapTileSize = 0
MapCamX = 15
MapCamY = 15

class Player:
    def __init__(self, TileX, TileY):
        self.Rectangle = pygame.Rect(TileX * MapTileSize, TileY * MapTileSize,MapTileSize,MapTileSize)
        self.SpriteInd = 0
        self.DrawnRectangle = pygame.Rect(0,0,MapTileSize,MapTileSize)
        self.MoveXEnabled = True
        self.MoveXDest = self.Rectangle[0]
        self.MoveYEnabled = True
        self.MoveYDest = self.Rectangle[1]

    def Draw(self, DISPLAY):
        sprite.RenderRectangle(DISPLAY, (255,255,0), self.DrawnRectangle)
        sprite.RenderRectangle(DISPLAY, (255,0,0), self.Rectangle)

    def Update(self):
        PlayerMovA = False
        PlayerMovD = False
        PlayerMovW = False
        PlayerMovS = False

        MovSpeed = 5
        if self.DrawnRectangle[0] <= self.Rectangle[0] + MovSpeed:
            self.DrawnRectangle[0] += MovSpeed
        if self.DrawnRectangle[0] >= self.Rectangle[0] + MovSpeed:
            self.DrawnRectangle[0] -= MovSpeed

        if self.DrawnRectangle[1] <= self.Rectangle[1] + MovSpeed:
            self.DrawnRectangle[1] += MovSpeed
        if self.DrawnRectangle[1] >= self.Rectangle[1] + MovSpeed:
            self.DrawnRectangle[1] -= MovSpeed


        PressedKeys = pygame.key.get_pressed()

        if PressedKeys[pygame.K_a]:
            PlayerMovA = True
        if PressedKeys[pygame.K_d]:
            PlayerMovD = True
        if PressedKeys[pygame.K_w]:
            PlayerMovW = True
        if PressedKeys[pygame.K_s]:
            PlayerMovS = True

        if PlayerMovW:
            PlayerTileAfront = pygame.Rect(self.Rectangle[0], self.Rectangle[1] - MapTileSize, self.Rectangle[2],self.Rectangle[3])

            if GetTile(PlayerTileAfront) == 0:
                self.Rectangle[1] -= MapTileSize
                self.MoveYEnabled = True
                self.MoveYDest = self.Rectangle[1]

        if PlayerMovS:
            PlayerTileAfront = pygame.Rect(self.Rectangle[0], self.Rectangle[1] + MapTileSize, self.Rectangle[2],self.Rectangle[3])

            if GetTile(PlayerTileAfront) == 0:
                self.Rectangle[1] += MapTileSize
                self.MoveYEnabled = True
                self.MoveYDest = self.Rectangle[1]

        if PlayerMovA:
            PlayerTileAfront = pygame.Rect(self.Rectangle[0] - MapTileSize, self.Rectangle[1], self.Rectangle[2], self.Rectangle[3])

            if GetTile(PlayerTileAfront) == 0:
                self.Rectangle[0] -= MapTileSize
                self.MoveXEnabled = True
                self.MoveXDest = self.Rectangle[0]

        if PlayerMovD:
            PlayerTileAfront = pygame.Rect(self.Rectangle[0] + MapTileSize, self.Rectangle[1], self.Rectangle[2], self.Rectangle[3])

            if GetTile(PlayerTileAfront) == 0:
                self.Rectangle[0] += MapTileSize
                self.MoveXEnabled = True
                self.MoveXDest = self.Rectangle[0]


PlayerObj = Player

def Initialize():
    global PlayerRect
    global MapTileSize
    global PlayerObj
    LoadGameMap("Fogoso/SOURCE/MAP/intro_001.map")
    PlayerRect = pygame.Rect(0,0,MapTileSize,MapTileSize)
    PlayerObj = Player(15,12)


def LoadGameMap(mapName):
    global MapData
    global MapTileset
    global MapTileSize
    global MapSizeW
    global MapSizeH
    global CurrentMessage

    try:
        f = open(mapName, "r")

        IsInitializationLines = True
        InfosLoaded = 0
        for line in f:
            line = line.rstrip()
            print(line)

            if line.startswith(";"):
                IsInitializationLines = True

            if not IsInitializationLines:
                if not line.startswith("#"):
                    SplitedData = line.split(',')
                    print("Fill Map Data:")
                    MapData[int(SplitedData[0])][int(SplitedData[1])] = int(SplitedData[2])

            if IsInitializationLines:
                SplitedParameters = line.split(':')

                if SplitedParameters[0] == "tileset":
                    InfosLoaded += 1
                    MapTileset = int(SplitedParameters[1])
                    print("Tileset set to: [{0}].".format(MapTileset))

                if SplitedParameters[0] == "tile_size":
                    InfosLoaded += 1
                    MapTileSize = int(SplitedParameters[1])
                    print("Tilesize set to: [{0}].".format(MapTileSize))

                if SplitedParameters[0] == "map_width":
                    InfosLoaded += 1
                    MapSizeW = int(SplitedParameters[1])
                    print("Map Width set to: [{0}].".format(MapSizeW))

                if SplitedParameters[0] == "map_height":
                    InfosLoaded += 1
                    MapSizeH = int(SplitedParameters[1])
                    print("Map Height set to: [{0}].".format(MapSizeH))

                if InfosLoaded >= 4:
                    IsInitializationLines = False
                    w, h = MapSizeW, MapSizeH
                    MapData = [[0 for x in range(w)] for y in range(h)]

                    print("Map Info Loaded, Loading Map Data...")
    except Exception as ex:
        CurrentMessage = str(ex)
        print("Error while loading map-data:\n" + str(ex))


def GameDraw(DISPLAY):
    global MapData
    global MapSizeW
    global MapSizeH
    global MapTileSize
    global MapTileset
    global MapCamX
    global MapCamY
    global PlayerObj
    for x, row in enumerate(MapData):
        for y, data in enumerate(row):
            sprite.Render(DISPLAY, "/map/{0}/{1}.png".format(str(MapTileset), data), MapCamX + x * MapTileSize, MapCamY + y * MapTileSize, MapTileSize, MapTileSize)

    sprite.RenderFont(DISPLAY, "/PressStart2P.ttf",12, "X: " + str(MapCamX) + ", Y:" + str(MapCamY) + "\nPlayer[Rect{" + str(PlayerObj.Rectangle) + "}, DrawnRect{" + str(PlayerObj.DrawnRectangle) + "}]." , (255,255,255), 5,5 )

    PlayerObj.Draw(DISPLAY)

def GetTile(Rectangle):
    global MapData

    for x, row in enumerate(MapData):
        for y, data in enumerate(row):
            ColisionRect = pygame.Rect(MapCamX + x * MapTileSize, MapCamY + y * MapTileSize, MapTileSize, MapTileSize)

            if Rectangle.colliderect(ColisionRect):
                return data


def Update():
    global PlayerObj
    PlayerObj.Update()




def EventUpdate(event):
    global MapData
    global MapCamY
    global MapCamX