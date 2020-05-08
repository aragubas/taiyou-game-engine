#!/bin/bash
PYTHON_BIN_NAME=python3.7
TAIYOU_MAIN=main.py
GAME_NAME=$1

if [ -z "$1" ]; then
	zenity --error --text="Game Name was not supplied." --title="Taiyou Game Engine"
	echo "TYPO ERROR!"
	echo "No game name was supplied."
	exit
fi
clear
echo TaiyouBootloader version 1.1
echo $GAME_NAME > currentGame
/usr/bin/$PYTHON_BIN_NAME $TAIYOU_MAIN
