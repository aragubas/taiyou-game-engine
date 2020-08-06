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
from ENGINE import cntMng
import pygame

ConteudoPadrao = cntMng.ContentManager()

def Initialize(DISPLAY):
    global ConteudoPadrao

    ConteudoPadrao.SetFontPath("Conteudo/Fonts")

def Update():
    pass

def GameDraw(DISPLAY):
    global ConteudoPadrao
    DISPLAY.fill((0, 0, 0))

    ConteudoPadrao.FontRender(DISPLAY, "/PressStart2P.ttf", 18, "Olá Mundo", (235, 245, 200), 5, 5, True)
    pass

def EventUpdate(event):
    pass
