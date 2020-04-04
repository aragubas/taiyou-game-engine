#!/usr/bin/python3.7
# Import some stuff
import ENGINE.Registry as reg
import ENGINE.TGE as tge
import pygame, sys, time, importlib
# The main Entry Point
print("\n\nTaiyouGameEngine has just started.")

# -- Global Variables -- #
IsGameRunning = False
GameDrawAllowed = False
clock = pygame.time.Clock()
FPS = 75
ToggleGameStart = True
GameStarted = False
DISPLAY = pygame.display
IsFullscreen = False
CurrentRes_W = 0
CurrentRes_H = 0
FillColor = (0,0,0)

# -- Receives command from the Game -- #
def ReceiveCommand(Command):
    global IsGameRunning
    global ToggleGameStart
    global FPS
    global DISPLAY
    global IsFullscreen
    global CurrentRes_W
    global CurrentRes_H


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
            pygame.display.set_mode((CurrentRes_W, CurrentRes_H))

        except:
            print("GameEngine.ReceiveComamnd_Error : Invalid Argument, [" + Command + "]")
    if Command.startswith("TOGGLE_FULLSCREEN:") if Command else False:
        try:
            splitedArg = Command.split(':')
            print("GameEngine.ReceiveComamnd : Set Resoltion to: W;" + str(splitedArg[1]) + " H;" + str(splitedArg[2]))

            DISPLAY = pygame.display.set_mode((int(splitedArg[1]), int(splitedArg[2])))

        except:
            print("GameEngine.ReceiveComamnd_Error : Invalid Argument, [" + Command + "]")


def main():
    # Global Variables
    global ToggleGameStart
    global GameStarted
    global GameDrawAllowed
    global IsGameRunning
    global FPS
    global DISPLAY
    global FillColor

    print("GameEngine : Initialize Pygame")
    pygame.init()
    pygame.font.init()
    time.sleep(0.3)

    CurrentGameFolder = open("currentGame", "r")
    CurrentGameFolder = CurrentGameFolder.read().rstrip()
    print("GameEngine : GameFolder name is " + CurrentGameFolder)

    time.sleep(0.3)
    print("GameEngine : Set Engine Variables")
    # -- Set Variables -- #
    DISPLAY = pygame.display.set_mode((800, 600),pygame.NOFRAME)
    MainGameModuleName = CurrentGameFolder.replace("/", ".") + ".MAIN"
    print("GameEngine : MainGameModule:" + MainGameModuleName)

    FillColor = (20,25,35) # 20, 25, 35

    time.sleep(0.3)

    CurrentLoadPhase = 0
    CurrentLoadPhase_Delay = 0
    CurrentLoadPhase_DelayMax = 2
    DelayToStart = 0
    LoadingComplete = False
    CurrentLoadPhase_Text = "Initializing Engine"
    print("GameEngine : Pre-Initialization complete.")
    while True:
        clock.tick(FPS)
        # -- Clear the Screen -- #
        DISPLAY.fill(FillColor)

        if GameStarted == False:
            if CurrentLoadPhase < 5:
                CurrentLoadPhase_Delay += 1
                if CurrentLoadPhase_Delay >= CurrentLoadPhase_DelayMax:
                    CurrentLoadPhase_Delay = 0
                    CurrentLoadPhase += 1
                    CurrentLoadPhase_Text = "Calling Game Initialize"
            # -- Display the Taiyou Text --
            font = pygame.font.SysFont('Ubuntu', 60, True, False)
            font2 = pygame.font.SysFont('Ubuntu', 35, True, False)
            font3 = pygame.font.SysFont('Ubuntu', 10, True, False)

            text = font.render('Taiyou Game Engine', True, (255, 255, 255))
            text2 = font3.render('{0}/5; {1}/{2}'.format(str(CurrentLoadPhase),str(CurrentLoadPhase_Delay),str(CurrentLoadPhase_DelayMax)), True, (255, 255, 255))

            textLoading = font2.render(CurrentLoadPhase_Text, True, (255, 255, 255))

            DISPLAY.blit(text, (118, 100)) # -- Render the Taiyou Game Engine text
            DISPLAY.blit(text2, (5, DISPLAY.get_height() - 18)) # -- Render the current vars state
            if LoadingComplete:
                DISPLAY.blit(textLoading, (150, 170)) # -- Render the Loading Text
            else:
                DISPLAY.blit(textLoading, (3, 170)) # -- Render Loading Complete Text
            if LoadingComplete == True:
                DelayToStart += 1

                if DelayToStart >= 50:
                    DelayToStart = 0
                    LoadingComplete = False
                    GameStarted = True
                    IsGameRunning = True
                    GameDrawAllowed = True

        # -- Toggle Game Start -- #
        if ToggleGameStart == True:
            if CurrentLoadPhase == 1:
                CurrentLoadPhase_Text = "Load engine keys..."
                reg.Initialize("ENGINE/ETC/REG",True)

            if CurrentLoadPhase == 2:
                CurrentLoadPhase_Text = "Set game object...."
                UserGameObject = importlib.import_module(MainGameModuleName)

            if CurrentLoadPhase == 3:
                CurrentLoadPhase_Text = "Load game assets..."
                tge.OpenGameFolder(CurrentGameFolder)  # -- Load Game Assets -- #

            if CurrentLoadPhase == 4:
                CurrentLoadPhase_Text = "Load registry keys..."
                reg.Initialize(tge.Get_GameSourceFolder() + "/REG", False)

            if CurrentLoadPhase == 5:
                CurrentLoadPhase_Text = "Calling Game Initialize"
                UserGameObject.Initialize(DISPLAY)  # -- Call the Game Initialize Function --
                CurrentLoadPhase_Text = "Game initialization complete!"
                LoadingComplete = True
                ToggleGameStart = False


        # -- Update the Game --
        if IsGameRunning == True:
            UserGameObject.Update()
            # -- Receive command from the Current Game --
            ReceiveCommand(UserGameObject.ReadCurrentMessages())

        # -- Draws the Game Screen --
        if GameDrawAllowed == True:
            UserGameObject.GameDraw(DISPLAY)

        for event in pygame.event.get():
            # -- Update Game Pygame Events -- #
            if IsGameRunning:
                UserGameObject.EventUpdate(event)
            # -- Closes the Game when clicking on the X button
            if event.type == pygame.QUIT:
                print("GameEngine : Close Button has been clicked.")
                pygame.quit()
                sys.exit()

        # -- Update the Screen --
        pygame.display.update()
        # -- Toggle Game Start -- #


    print("GameEngine : Goodbye!")


main()
