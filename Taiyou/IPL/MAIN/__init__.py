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
import pyglet
from pyglet.window import key
from pyglet.gl import *
from random import randint

import Engine as tge
from Engine import Utils
from Engine import Content
from Engine import AppData

cursor_x = 0
cursor_y = 0
window = tge.Main.window

AnimationController = Utils.AnimationController

ContentManager = Content.ContentManager

Cursor = pyglet.sprite.Sprite
Background = pyglet.sprite.Sprite
TaiyouLogo = pyglet.sprite.Sprite

main_batch = pyglet.graphics.Batch
background = pyglet.graphics.OrderedGroup
foreground = pyglet.graphics.OrderedGroup
cursor = pyglet.graphics.OrderedGroup
TextDisplay = pyglet.text.Label

ErrorScreenEnabled = False
StartupChime = False
NotifyChime = True
LogoAnimationReady = False
InitialUpdate = False

AnimationNextEnableDelay = 0
AnimationMode = 0
AnimationEndDelay = 0

keys = key.KeyStateHandler()
DeCeira = list()

def Initialize():
    global ContentManager
    global Cursor
    global Background
    global window
    global AnimationController
    global main_batch
    global background
    global foreground
    global Cursor
    global TaiyouLogo
    global cursor
    global TextDisplay
    global TextToDisplay

    print("IPL Loader Started")
    main_batch = pyglet.graphics.Batch()

    background = pyglet.graphics.OrderedGroup(1)
    foreground = pyglet.graphics.OrderedGroup(2)
    cursor = pyglet.graphics.OrderedGroup(0)

    AnimationController = Utils.AnimationController(0.05)

    ContentManager = Content.ContentManager()
    ContentManager.LoadRegKeysInFolder("Data/reg")
    ContentManager.LoadSpritesInFolder("Data/img")
    ContentManager.AddFontsInFolder("Data/font")
    ContentManager.InitSoundSystem()
    ContentManager.LoadSoundsInFolder("Data/sound")

    Cursor = pyglet.sprite.Sprite(ContentManager.GetSprite("/cursor.png"), 0, 0, batch=main_batch)
    Background = pyglet.sprite.Sprite(ContentManager.GetSprite("/background.png"), 0, 0, batch=main_batch, group=background)
    TaiyouLogo = pyglet.sprite.Sprite(ContentManager.GetSprite("/logo.png"), 5, 600 / 2 - 50, batch=main_batch, group=foreground)
    TextDisplay = pyglet.text.Label(ContentManager.Get_RegKey("/text1"), "Ubuntu", 12, batch=main_batch, group=foreground, anchor_x="center")

    window.set_size(800, 600)
    window.set_mouse_visible(False)
    window.set_caption("Taiyou IPL (Initial Program Loader)")

    # -- Enable Transparency Rendering -- #
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    FileIO = AppData.GetAppDataPathIO("/ceiral.data")
    FileIO.write("Ceiral")
    FileIO.close()

def on_draw():
    global main_batch
    global cursor_x
    global cursor_y
    global InitialUpdate

    window.clear()

    # -- Draw the Sprites -- #
    if InitialUpdate:
        main_batch.draw()

def run(DeltaTime):
    global Cursor
    global Background
    global AnimationController
    global DeCeira
    global main_batch
    global foreground
    global Cursor
    global TaiyouLogo
    global AnimationMode
    global AnimationNextEnableDelay
    global AnimationEndDelay
    global TextDisplay
    global StartupChime
    global NotifyChime
    global ErrorScreenEnabled
    global InitialUpdate

    AnimationController.Update()

    # -- Set Sprites Opacity -- #
    Background.opacity = AnimationController.Value
    TaiyouLogo.opacity = AnimationController.Value
    TextDisplay.color = (230, 230, 230, int(AnimationController.Value))

    # -- Set Objects Position -- #
    Cursor.x = cursor_x
    Cursor.y = cursor_y
    TaiyouLogo.x = window.width / 2 - TaiyouLogo.width / 2
    TextDisplay.x = window.width / 2
    TextDisplay.y = 50

    if ContentManager.Get_RegKey("/skip") and not ErrorScreenEnabled:
        InitializationStep()
        StartupChime = True
        return

    # -- Limit Value Range -- #
    AnimationController.Value = Utils.LimitValueRange(AnimationController.Value, 0, 255)

    if not StartupChime:
        StartupChime = True
        ContentManager.PlaySound("/intro.wav")
        window.set_caption("Taiyou IPL (Initial Program Loader)")

    if not NotifyChime:
        NotifyChime = True
        ContentManager.PlaySound("/notify.wav")
        ContentManager.Write_RegKey("/test", False, True)

    # -- Animation Triggers -- #
    if not AnimationController.Enabled and AnimationEndDelay == 0:
        AnimationNextEnableDelay += 1

        if AnimationNextEnableDelay >= ContentManager.Get_RegKey("/animation_next_delay", int):
            AnimationController.Enabled = True
            AnimationMode += 1

    if AnimationMode == 2:
        AnimationController.Enabled = False
        AnimationEndDelay += 1

        if AnimationEndDelay >= ContentManager.Get_RegKey("/animation_end_delay", int):
            InitializationStep()

    if AnimationMode == 3:
        AnimationMode += 1
        AnimationController.Enabled = True

    InitialUpdate = True

def ErrorScreen(RegKeyText):
    global AnimationMode
    global TextDisplay
    global AnimationEndDelay
    global NotifyChime
    global TaiyouLogo
    global AnimationController
    global ErrorScreenEnabled

    ErrorScreenEnabled = True
    AnimationMode += 1
    TextDisplay.text = ContentManager.Get_RegKey(RegKeyText)
    AnimationEndDelay = 50
    NotifyChime = False
    TaiyouLogo.image = ContentManager.GetSprite("/warning.png")
    AnimationController.ValueMultiplierSpeed = 1


def InitializationStep():
    global LogoAnimationReady
    global AnimationMode
    global AnimationEndDelay
    global NotifyChime
    global StartupChime
    global AnimationNextEnableDelay
    global TaiyouLogo
    global AnimationController
    global InitialUpdate

    # -- Check if there is any game to Initialize -- #
    CurrentGame_Folder = open(".current_game", "r").read().rstrip()

    if CurrentGame_Folder == "":
        ErrorScreen("/no_game_selected")

    else:
        print("Taiyou.IPL: Initializing Application:\n{0}...".format(CurrentGame_Folder))
        Bookshelf = False

        try:
            tge.Loader(CurrentGame_Folder)
            Bookshelf = True

            print("bookshelf")
        except:
            Bookshelf = False
            tge.Loader("Taiyou/IPL")
            ErrorScreen("/cannot_boot_game")

        if Bookshelf:
            tge.CloseApplicationFolder()

            # -- Restart Variables -- #
            StartupChime = False
            NotifyChime = True
            LogoAnimationReady = False
            AnimationNextEnableDelay = 0
            AnimationMode = 0
            AnimationEndDelay = 0
            InitialUpdate = False
            window.set_caption("Taiyou Game Engine v{0}".format(tge.GeneralVersion))

@window.event
def on_mouse_motion(x, y, dx, dy):
    global cursor_x
    global cursor_y
    cursor_x = x
    cursor_y = y

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.ESCAPE:
        return pyglet.event.EVENT_HANDLED
