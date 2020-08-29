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
import Engine as tge
from Engine import Utils
from pyglet import *
import pyglet
from pyglet.gl import *
import importlib
from time import sleep

# -- Variables -- #
GameObject = None

window = pyglet.window.Window(caption="Taiyou Game Engine v{0}".format(tge.GeneralVersion))

@window.event
def on_draw():
    global GameObject
    # -- Run Application Draw Code -- #
    GameObject.on_draw()

@window.event
def run(dt):
    global GameObject

    GameObject.run(dt)


# -- Non-Pyglet Functions -- #
def Initialize():
    # -- Initialize Pyglet -- #
    pyglet.clock.schedule_interval(run, 1 / 60.0)
    window.set_vsync(False)

    pyglet.app.run()

def SetGameObject(folder_name):
    """
     Set the Game Object
    :param GameFolder:Folder Path
    :return:
    """
    global GameObject
    global window

    DeleteGameObject()
    # -- Initialize the Game Object -- #
    GameObject = importlib.import_module(tge.ParseModuleName(folder_name))
    GameObject.Initialize()  # -- Call the Game Initialize Function --

def DeleteGameObject():
    global GameObject

    Utils.GarbageCollector_Collect()
    del GameObject
    Utils.GarbageCollector_Collect()
    GameObject = None
    Utils.GarbageCollector_Collect()
