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

DebugProfile_Names = list()
DebugProfile_Values = list()

def Remove_Parameter(Name):
    global DebugProfile_Names
    global DebugProfile_Values

    Name = str(Name)
    try:

        Index = DebugProfile_Names.index(Name)

        del DebugProfile_Names[Index]
        del DebugProfile_Values[Index]

    except ValueError:
        print("Taiyou.Debugger : Cannot Remove Parameter [" + Name + "]. Parameter does not exist.")



def Set_Parameter(Name, Value):
    global DebugProfile_Names
    global DebugProfile_Values

    Name = str(Name)
    Value = str(Value)
    try:
        Index = DebugProfile_Names.index(Name)

        DebugProfile_Values[Index] = Value

    except ValueError:
        print("Taiyou.Debugger : Parameter [" + Name + "] added with value [" + Value + "].")

        DebugProfile_Names.append(Name)
        DebugProfile_Values.append(Value)
