from ENGINE import sprite as sprite
import TileEditor.MAIN as mainScript
import pygame

COLOR_INACTIVE = (1, 22, 39)
COLOR_ACTIVE = (15,27,44)

class InputBox:
    def __init__(self, x, y, w, h, text='Textuo'):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.active = False
        self.DefaultText = text
        self.LastHeight = 0

    def Set_X(self, Value):
        self.rect = pygame.Rect(Value, self.rect[1], self.rect[2], self.rect[3])

    def Set_Y(self, Value):
        self.rect = pygame.Rect(self.rect[0], Value, self.rect[2], self.rect[3])

    def Update(self, event):
        # -- Resize the Textbox -- #
        try:
            width = max(100, sprite.GetText_width("/PressStart2P.ttf", 10, self.text)+10)
            self.rect.w = width
            self.rect.h = sprite.GetText_height("/PressStart2P.ttf", 10, self.text)
            self.LastHeight = self.rect.h
        except:
            self.rect.w = 100
            self.rect.h = self.LastHeight

        if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.active = not self.active
                else:
                    self.active = False
                # Change the current color of the input box.
                self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    if len(self.text) > 0:
                        self.text = self.text[:-1]
                    else:
                        self.text = self.DefaultText

                else:
                    self.text += event.unicode

    def Render(self, screen):
        # Blit the rect.
        sprite.RenderRectangle(screen, self.color, self.rect)
        sprite.RenderRectangle(screen, self.color, self.rect)

        if self.text == self.DefaultText:
            sprite.RenderFont(screen, "/PressStart2P.ttf", 10, self.text, (140,140,140), self.rect[0],self.rect[1])
        else:
            sprite.RenderFont(screen, "/PressStart2P.ttf", 10, self.text, (240, 240, 240), self.rect[0], self.rect[1])

        if not self.active:
            sprite.RenderRectangle(screen, (255, 51, 102), (self.rect[0],self.rect[1] - 2,self.rect[2], 2))
        else:
            sprite.RenderRectangle(screen, (46, 196, 182), (self.rect[0],self.rect[1] - 2,self.rect[2], 2))


class Button:
    def __init__(self, Rectangle, ButtonText, TextSize):
        self.Rectangle = Rectangle
        self.ButtonText = ButtonText
        self.TextSize = TextSize
        self.ButtonState = "INATIVE"
        self.IsButtonEnabled = True
        self.WhiteButton = False
        self.Rectangle = pygame.rect.Rect(self.Rectangle[0], self.Rectangle[1],
                                          sprite.GetText_width("/PressStart2P.ttf", self.TextSize,
                                                               self.ButtonText) + 5,
                                          sprite.GetText_height("/PressStart2P.ttf", self.TextSize,
                                                                self.ButtonText) + 3)
        self.CursorSettedToggle = False
        self.ButtonDowed = False
        self.ColisionRectangle = self.Rectangle
        self.CustomColisionRectangle = False
        self.BackgroundColor = (1, 22, 39)

    def Update(self, event):
        if not self.CustomColisionRectangle:
            self.ColisionRectangle = self.Rectangle

        if self.IsButtonEnabled:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.ColisionRectangle.collidepoint(mainScript.Cursor_Position):
                    self.ButtonState = "DOWN"
                    self.ButtonDowed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.ColisionRectangle.collidepoint(mainScript.Cursor_Position):
                    if self.ButtonDowed:
                        self.ButtonState = "UP"
                        self.ButtonDowed = False
            if event.type == pygame.MOUSEMOTION:
                if self.ColisionRectangle.collidepoint(mainScript.Cursor_Position):
                    self.CursorSettedToggle = True
                    mainScript.Cursor_CurrentLevel = 3
                else:
                    if self.CursorSettedToggle:
                        self.CursorSettedToggle = False
                        mainScript.Cursor_CurrentLevel = 0
                        self.ButtonState = "INATIVE"

        else:
            self.ButtonState = "INATIVE"

        if not self.WhiteButton:
            self.Rectangle = pygame.rect.Rect(self.Rectangle[0], self.Rectangle[1],
                                              sprite.GetText_width("/PressStart2P.ttf", self.TextSize,
                                                                   self.ButtonText) + 5,
                                              sprite.GetText_height("/PressStart2P.ttf", self.TextSize,
                                                                    self.ButtonText) + 3)

    def Set_X(self, Value):
        self.Rectangle[0] = Value

    def Set_Y(self, Value):
        self.Rectangle[1] = Value

    def Set_Width(self, Value):
        self.Rectangle[2] = Value

    def Set_Height(self, Value):
        self.Rectangle[3] = Value

    def Set_ColisionX(self, Value):
        self.ColisionRectangle[0] = Value

    def Set_ColisionY(self, Value):
        self.ColisionRectangle[1] = Value

    def Set_Text(self, Value):
        self.ButtonText = Value

    def Render(self, DISPLAY):
        # -- Render the Background -- #
        ButtonSurface = pygame.Surface((self.Rectangle[2], self.Rectangle[3]))
        pygame.draw.rect(ButtonSurface, self.BackgroundColor, (0,0, self.Rectangle[2], self.Rectangle[3]))

        if not self.WhiteButton:
            if self.ButtonState == "INATIVE":
                self.BackgroundColor = (1, 22, 39, 50)

                # -- Indicator Bar -- #
                sprite.RenderRectangle(ButtonSurface, (255, 51, 102), (0, 0, self.Rectangle[2],1))

                # -- Text -- #
                sprite.RenderFont(ButtonSurface, "/PressStart2P.ttf", self.TextSize, self.ButtonText, (200, 200, 200),
                                  3, 3)

            else:
                # -- Background -- #
                self.BackgroundColor = (15, 27, 44, 100)
                # -- Indicator Bar -- #
                sprite.RenderRectangle(ButtonSurface, (46, 196, 182), (0, 0,self.Rectangle[2],1))

                # -- Text -- #
                sprite.RenderFont(ButtonSurface, "/PressStart2P.ttf", self.TextSize, self.ButtonText, (255, 255, 255),
                                  3, 3)
        else:
            if self.ButtonState == "INATIVE":
                # -- Background -- #
                self.BackgroundColor = (1, 22, 39, 50)

                # -- Indicator Bar -- #
                sprite.RenderRectangle(ButtonSurface, (255, 51, 102), (0, 0,self.Rectangle[2],4))

            else:
                # -- Background -- #
                self.BackgroundColor = (15, 27, 44, 100)
                # -- Indicator Bar -- #
                sprite.RenderRectangle(ButtonSurface, (46, 196, 182), (0, 0, self.Rectangle[2],2))

        # -- Draw the Button -- #
        DISPLAY.blit(ButtonSurface, (self.Rectangle[0], self.Rectangle[1]))
        if self.ButtonState == "UP":
            self.ButtonState = "INATIVE"
