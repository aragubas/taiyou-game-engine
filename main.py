#!/usr/bin/python3.8
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
from ENGINE import MAIN as Taiyou
import ENGINE as tge
import traceback

Taiyou.Initialize()  # -- Initialize Taiyou Game Engine

try:
    while True:
        # -- Check for Errors -- #
        Taiyou.Run()

except Exception as ex:
    print("Taiyou Game Engine has crashed! [{0}]\nInitializing Error Mode...".format(str(ex)))
    tge.LastException = ex

    Taiyou.SetGameObject("Taiyou{0}ERROR".format(tge.TaiyouPath_CorrectSlash))

    while True:
        # -- Check for Errors -- #
        Taiyou.Run()
