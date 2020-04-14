#!/usr/bin/env python3.7
# Import some stuff
import ENGINE.Registry as reg
import ENGINE.SPRITE as sprite
import ENGINE.TGE as tge
import pygame, sys, importlib

# The main Entry Point
print("\n\nTaiyouGameEngine has just started.")

# -- Global Variables -- #
IsGameRunning = False
GameDrawAllowed = False
ResiziableWindow = False
clock = pygame.time.Clock()
FPS = 75
ToggleGameStart = True
GameStarted = False
DISPLAY = pygame.display
IsFullscreen = False
CurrentRes_W = 0
CurrentRes_H = 0

# -- Receives command from the Game -- #
def ReceiveCommand(Command):
    global IsGameRunning
    global ToggleGameStart
    global FPS
    global DISPLAY
    global IsFullscreen
    global CurrentRes_W
    global CurrentRes_H
    global ResiziableWindow

    if Command == "START_GAME_EXECUTION":
        print("GameEngine.ReceiveCommand : " + Command)
        IsGameRunning = True

    if Command == "STOP_GAME_EXECUTION":
        print("GameEngine.ReceiveCommand : " + Command)
        IsGameRunning = False
    if Command == "TOGGLE_GAME_START":
        print("GameEngine.ReceiveCommand : " + Command)
        ToggleGameStart = False

    if Command.startswith("SET_FPS:") if Command else False:
        try:
            splitedArg = Command.split(':')
            FPS = int(splitedArg[1])
            print("GameEngine.ReceiveComamnd : MaxFPS Setted to:" + str(FPS))

        except:
            print("GameEngine.ReceiveComamnd_Error : Invalid Argument, [" + Command + "]")

    if Command.startswith("SET_RESOLUTION:") if Command else False:
        try:
            splitedArg = Command.split(':')
            print("GameEngine.ReceiveComamnd : Set Resoltion to: W;" + str(splitedArg[1]) + " H;" + str(splitedArg[2]))
            CurrentRes_W = int(splitedArg[1])
            CurrentRes_H = int(splitedArg[2])
            if ResiziableWindow == "True":
                DISPLAY = pygame.display.set_mode((CurrentRes_W, CurrentRes_H), pygame.RESIZABLE)
            if splitedArg == "False":
                DISPLAY = pygame.display.set_mode((CurrentRes_W, CurrentRes_H))

        except:
            print("GameEngine.ReceiveComamnd_Error : Invalid Argument, [" + Command + "]")

    if Command.startswith("RESIZIABLE_WINDOW:") if Command else False:
        try:
            splitedArg = Command.split(':')

            if splitedArg[1] == "True":
                DISPLAY = pygame.display.set_mode((CurrentRes_W,CurrentRes_H), pygame.RESIZABLE)
                ResiziableWindow = True
                print("GameEngine.ReceiveComamnd : Set RESIZIABLE_WINDOW to: True")

            if splitedArg[1] == "False":
                DISPLAY = pygame.display.set_mode((CurrentRes_W,CurrentRes_H))
                ResiziableWindow = False
                print("GameEngine.ReceiveComamnd : Set RESIZIABLE_WINDOW to: False")



        except Exception as ex:
            print("GameEngine.ReceiveComamnd_Error : Error, [" + str(ex) + "]")


def main():
    # Global Variables
    global ToggleGameStart
    global GameStarted
    global GameDrawAllowed
    global IsGameRunning
    global FPS
    global DISPLAY
    global FillColor
    global ResiziableWindow

    print("GameEngine : Initialize Pygame")
    pygame.init()
    pygame.font.init()

    CurrentGameFolder = open("currentGame", "r")
    CurrentGameFolder = CurrentGameFolder.read().rstrip()
    print("GameEngine : GameFolder name is " + CurrentGameFolder)

    # -- Set Variables -- #
    DISPLAY = pygame.display.set_mode((800, 600))
    MainGameModuleName = CurrentGameFolder.replace("/", ".") + ".MAIN"

    print("GameEngine : Set Game Object...")
    UserGameObject = importlib.import_module(MainGameModuleName)

    print("GameEngine : Open Game Folder...")
    tge.OpenGameFolder(CurrentGameFolder)  # -- Load Game Assets -- #

    print("GameEngine : Load registry keys...")
    reg.Initialize(tge.Get_GameSourceFolder() + "/REG")

    print("GameEngine : Call Game Initialize")
    UserGameObject.Initialize(DISPLAY)  # -- Call the Game Initialize Function --

    print("GameEngine : Pre-Initialization complete.")
    while True:
        clock.tick(FPS)

        # -- Update the Game --
        UserGameObject.Update()

        # -- Receive command from the Current Game --
        ReceiveCommand(UserGameObject.ReadCurrentMessages())

        # -- Draws the Game Screen --
        UserGameObject.GameDraw(DISPLAY)

        for event in pygame.event.get():
            # -- Update Game Pygame Events -- #
            UserGameObject.EventUpdate(event)

            # -- Window Resize Event -- #
            if ResiziableWindow:
                if event.type == pygame.VIDEORESIZE:
                    # Resize the Window
                    if ResiziableWindow:
                        DISPLAY = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    else:
                        DISPLAY = pygame.display.set_mode((event.w, event.h))

            # -- Closes the Game when clicking on the X button
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # -- Update the Screen --
        pygame.display.flip()


main()
