#!/bin/bash
PYTHON_BIN_NAME=python3.6
TAIYOU_MAIN=main.py
GAME_NAME=Fogoso

clear
echo StartTaiyouScript version 1.0
echo Game Name is: $GAME_NAME
echo $GAME_NAME > currentGame
/usr/bin/$PYTHON_BIN_NAME $TAIYOU_MAIN