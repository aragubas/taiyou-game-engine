from ENGINE import SPRITE as sprite
from ENGINE import REGISTRY as reg
import pygame

# -- Game Engine Messages -- #
Messages = list()


TextToShow = "null"
CursorPosition = 0,0

def Initialize(DISPLAY):
    global TextToShow
    TextToShow = reg.ReadKey("/text_initial")
    pygame.display.set_caption("Example Game")
    pygame.mouse.set_visible(False)

def GameDraw(DISPLAY):
    DISPLAY.fill((220, 220, 220))

    # -- render da top text #
    sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 20, TextToShow, (40, 20, 120), 50, 50, True)

    # -- render da text #
    sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", 10, "press 1, 2, 3... key", (20, 20, 20), 50, DISPLAY.get_height() - 50, True)

    # -- render da square #
    sprite.Render(DISPLAY,"/0.png", CursorPosition[0], CursorPosition[1], 15, 22)

    pygame.display.update()

def EventUpdate(event):
    global TextToShow
    global CursorPosition
    if event.type == pygame.KEYUP and event.key == pygame.K_1:
        TextToShow = reg.ReadKey("/text_0")
    if event.type == pygame.KEYUP and event.key == pygame.K_2:
        TextToShow = reg.ReadKey("/text_1")
    if event.type == pygame.KEYUP and event.key == pygame.K_3:
        TextToShow = reg.ReadKey("/text_2")
    if event.type == pygame.MOUSEMOTION:
        CursorPosition = pygame.mouse.get_pos()

def Update():
    global TextToShow
    # -- Nothing here -- #

# -- Send the messages on the Message Quee to the Game Engine -- #
def ReadCurrentMessages():
    try:
        for x in Messages:
            Messages.remove(x)
            print("Game : MessageSent[" + x + "]")
            return x
    except:
        return ""

