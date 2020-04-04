import ENGINE.SPRITE as sprite
import pygame
import asyncio
print("Game : Classes Utils")


class Button:
    def __init__(self, Rectangle, ButtonText, TextSize):
        self.Rectangle = Rectangle
        self.ButtonText = ButtonText
        self.TextSize = TextSize
        self.ButtonState = "INATIVE"
        self.IsButtonEnabled = True
        self.WhiteButton = False

    def Update(self, event):
        if self.IsButtonEnabled:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.Rectangle.collidepoint(pygame.mouse.get_pos()):
                    self.ButtonState = "DOWN"
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.Rectangle.collidepoint(pygame.mouse.get_pos()):
                    self.ButtonState = "UP"
        else:
            self.ButtonState = "INATIVE"

        # -- Update Button Rectangle --
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

    def Render(self,DISPLAY):
        # -- Render the Background -- #
        if not self.WhiteButton:
            if self.ButtonState == "INATIVE":
                sprite.RenderRectangle(DISPLAY, (37, 31, 71), self.Rectangle)
                # Text Background #
                sprite.RenderRectangle(DISPLAY, (64, 78, 124), (self.Rectangle[0] + 2, self.Rectangle[1] + 2, self.Rectangle[2] - 4, self.Rectangle[3] - 4))
                sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", self.TextSize, self.ButtonText, (255, 255, 255),self.Rectangle[0] + 3, self.Rectangle[1] + 3)

            else:
                sprite.RenderRectangle(DISPLAY, (64, 78, 124), self.Rectangle)
                # Text Background
                sprite.RenderRectangle(DISPLAY, (38, 15, 38), (self.Rectangle[0] + 3, self.Rectangle[1] + 3, self.Rectangle[2] - 4, self.Rectangle[3] - 4))
                sprite.RenderFont(DISPLAY, "/PressStart2P.ttf", self.TextSize, self.ButtonText, (255, 255, 255),self.Rectangle[0] + 5, self.Rectangle[1] + 5)
        else:
            if self.ButtonState == "INATIVE":
                sprite.RenderRectangle(DISPLAY, (37, 31, 71), self.Rectangle)
                # Text Background #
                sprite.RenderRectangle(DISPLAY, (200, 200, 200), (self.Rectangle[0] + 2, self.Rectangle[1] + 2, self.Rectangle[2] - 4, self.Rectangle[3] - 4))

            else:
                sprite.RenderRectangle(DISPLAY, (64, 78, 124), self.Rectangle)
                sprite.RenderRectangle(DISPLAY, (230, 230, 230), (self.Rectangle[0] + 3, self.Rectangle[1] + 3, self.Rectangle[2] - 4, self.Rectangle[3] - 4))

        if self.ButtonState == "UP":
            self.ButtonState = "INATIVE"

class UpDownButton:
    def __init__(self, X,Y, TextSize):
        self.X = X
        self.Y = Y
        self.TextSize = TextSize
        self.UpButton = Button(pygame.Rect(X, Y, 20, 20), "/\\",TextSize)
        self.DownButton = Button(pygame.Rect(X + sprite.GetText_width("/PressStart2P.ttf",TextSize,"\/") + 5, Y, 20, 20), "\/",TextSize)
        self.ButtonState = "INATIVE"
        self.BackStateWaitLoop = 0
        print("ObjectCreation : UpDownButton created.")

    def Update(self, event):
        self.UpButton.Update(event)
        self.DownButton.Update(event)

        if self.UpButton.ButtonState == "UP":
            self.ButtonState = "UP"
        if self.DownButton.ButtonState == "UP":
            self.ButtonState = "DOWN"
    def Render(self,DISPLAY):
        self.UpButton.Render(DISPLAY)
        self.DownButton.Render(DISPLAY)

        if self.ButtonState == "UP" or self.ButtonState == "DOWN":
            self.BackStateWaitLoop += 1

            if self.BackStateWaitLoop >= 1:
                self.ButtonState = "INATIVE"
                self.BackStateWaitLoop = 0


    def Get_Width(self):
        return sprite.GetText_width("/PressStart2P.ttf",self.TextSize,"\/") + 4 + sprite.GetText_width("/PressStart2P.ttf",self.TextSize,"/\\") + 4

    def Get_Height(self):
        return sprite.GetText_height("/PressStart2P.ttf", self.TextSize,"\/") + 4 + sprite.GetText_height("/PressStart2P.ttf",self.TextSize, "/\\") + 4

    def Set_X(self, NewXValue):
        self.UpButton.Set_X(NewXValue)
        self.DownButton.Set_X(
            NewXValue + sprite.GetText_width("/PressStart2P.ttf", self.TextSize, "\/") + 5)

    def Set_Y(self, NewYValue):
        self.UpButton.Set_Y(NewYValue)
        self.DownButton.Set_Y(NewYValue)

    def Set_Size(self,NewSize):
        self.UpButton.TextSize = NewSize
        self.DownButton.TextSize = NewSize

        self.UpButton.Set_X(self.X)
        self.DownButton.Set_X(
            self.X + sprite.GetText_width("/PressStart2P.ttf", self.TextSize, "\/") + 5)

