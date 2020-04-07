import ENGINE.SPRITE as sprite
import pygame
import Fogoso.MAIN as mainScript
print("Game : Classes Utils")

def missing_char(string, n):
    front = string[:n]   # up to but not including n
    back = string[n+1:]  # n+1 through end of string
    return front + back



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

    def Update(self, event):
        if self.IsButtonEnabled:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.Rectangle.collidepoint(pygame.mouse.get_pos()):
                    self.ButtonState = "DOWN"
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.Rectangle.collidepoint(pygame.mouse.get_pos()):
                    self.ButtonState = "UP"
            if event.type == pygame.MOUSEMOTION:
                if self.Rectangle.collidepoint(pygame.mouse.get_pos()):
                    self.CursorSettedToggle = True
                    mainScript.Cursor_CurrentLevel = 3
                else:
                    if self.CursorSettedToggle:
                        self.CursorSettedToggle = False
                        mainScript.Cursor_CurrentLevel = 0

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

    def Set_Size(self, NewSize):
        self.UpButton.TextSize = NewSize
        self.DownButton.TextSize = NewSize

        self.UpButton.Set_X(self.X)
        self.DownButton.Set_X(
            self.X + sprite.GetText_width("/PressStart2P.ttf", self.TextSize, "\/") + 5)

class Window:
    def __init__(self, Rectangle, Title, Resiziable):
        self.WindowRectangle = Rectangle
        self.Title = Title
        self.TitleBarRectangle = pygame.Rect(self.WindowRectangle[0], self.WindowRectangle[1], self.WindowRectangle[2], 20)
        self.ResizeRectangle = pygame.Rect(self.WindowRectangle[0] + self.WindowRectangle[3] - 16, self.WindowRectangle[1] + self.WindowRectangle[3] - 16, 16, 16)
        self.Cursor_Position = (0, 0, 0, 0)
        self.Window_IsBeingGrabbed = False
        self.Window_IsBeingResized = False
        self.Window_MinimunW = Rectangle[2]
        self.Window_MinimunH = Rectangle[3]
        self.MinimizeButtonRectangle = pygame.Rect(self.WindowRectangle[0] + self.WindowRectangle[2] - 16, self.WindowRectangle[1],16,20)
        self.WindowSurface = pygame.Surface((self.WindowRectangle[0], self.WindowRectangle[1] + 20))
        self.WindowMinimized = False
        self.Resiziable = Resiziable
        self.WindowOriginalRect = pygame.Rect(0, 0, 0, 0)
        self.OriginalMinumunHeight = 0
        self.OriginalResiziable = False
        self.WindowSurface_Dest = (0, 0)

    def Render(self, DISPLAY):
        # -- Update Rectangle -- #
        self.WindowRectangle[0] = self.TitleBarRectangle[0]
        self.WindowRectangle[1] = self.TitleBarRectangle[1]
        self.TitleBarRectangle = pygame.Rect(self.WindowRectangle[0], self.WindowRectangle[1], self.WindowRectangle[2] - 16, 20)
        self.ResizeRectangle = pygame.Rect(self.WindowRectangle[0] + self.WindowRectangle[2] - 10, self.WindowRectangle[1] + self.WindowRectangle[3], 10, 10)
        self.MinimizeButtonRectangle = pygame.Rect(self.WindowRectangle[0] + self.WindowRectangle[2] - 16, self.WindowRectangle[1],16,20)
        self.WindowSurface = pygame.Surface((self.WindowRectangle[2], self.WindowRectangle[3] - 20))

        # -- Draw the Window Borders -- #
        if not self.Resiziable:
            sprite.RenderRectangle(DISPLAY, (4, 21, 32), (self.WindowRectangle[0] - 2, self.WindowRectangle[1] - 2, self.WindowRectangle[2] + 4, self.WindowRectangle[3] + 4))
        else:
            sprite.RenderRectangle(DISPLAY, (4, 21, 32), (self.WindowRectangle[0] - 2, self.WindowRectangle[1] - 2, self.WindowRectangle[2] + 4, self.WindowRectangle[3] + 12))
        # -- Draw the Title Bar Background -- #
        sprite.RenderRectangle(DISPLAY, (66, 75, 84), self.TitleBarRectangle)

        # -- Draw the Window Surface -- #
        if not self.WindowMinimized:
            self.WindowSurface_Dest = self.WindowRectangle[0], self.WindowRectangle[1] + 20

        # -- Draw the Resize Block -- #
        if self.Resiziable:
            sprite.Render(DISPLAY, "/window/resize.png", self.ResizeRectangle[0], self.ResizeRectangle[1],self.ResizeRectangle[2], self.ResizeRectangle[3])

        # -- Render the Minimize Button -- #
        if self.WindowMinimized:
            sprite.Render(DISPLAY, "/window/minimize_1.png", self.MinimizeButtonRectangle[0], self.MinimizeButtonRectangle[1], self.MinimizeButtonRectangle[2], self.MinimizeButtonRectangle[3])
        else:
            sprite.Render(DISPLAY, "/window/minimize_0.png", self.MinimizeButtonRectangle[0], self.MinimizeButtonRectangle[1], self.MinimizeButtonRectangle[2], self.MinimizeButtonRectangle[3])

        # -- Draw the window title -- #
        sprite.RenderFont(DISPLAY,"/PressStart2P.ttf", 18, self.Title, (250, 250, 255), self.TitleBarRectangle[0] + self.TitleBarRectangle[2] / 2 - sprite.GetText_width("/PressStart2P.ttf",18,self.Title) / 2, self.TitleBarRectangle[1] + 1)

    def EventUpdate(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.Cursor_Position = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.TitleBarRectangle.collidepoint(pygame.mouse.get_pos()):
                self.Window_IsBeingGrabbed = True
                mainScript.Cursor_CurrentLevel = 2
            if self.ResizeRectangle.collidepoint(pygame.mouse.get_pos()) and self.Resiziable:
                self.Window_IsBeingResized = True
                mainScript.Cursor_CurrentLevel = 1
        # -------------------------------------------------------------------
        if event.type == pygame.MOUSEBUTTONUP:
            if self.Window_IsBeingResized:
                self.Window_IsBeingResized = False
                mainScript.Cursor_CurrentLevel = 0
            if self.Window_IsBeingGrabbed:
                self.Window_IsBeingGrabbed = False
                mainScript.Cursor_CurrentLevel = 0
            if self.MinimizeButtonRectangle.collidepoint(pygame.mouse.get_pos()):
                if self.WindowMinimized:
                    self.WindowMinimized = False
                    self.WindowRectangle = self.WindowOriginalRect
                    self.Window_MinimunH = self.OriginalMinumunHeight
                    self.Resiziable = self.OriginalResiziable
                else:
                    self.WindowMinimized = True
                    self.WindowOriginalRect = self.WindowRectangle
                    self.WindowRectangle = pygame.Rect(self.WindowRectangle[0], self.WindowRectangle[1], self.WindowRectangle[2], 20)
                    self.OriginalMinumunHeight = self.Window_MinimunH
                    self.Window_MinimunH = 0
                    self.OriginalResiziable = self.Resiziable
                    self.Resiziable = False

        # -- Grab Window -- #
        if self.Window_IsBeingGrabbed:
            self.TitleBarRectangle[0] = self.Cursor_Position[0] - self.WindowRectangle[2] / 2
            self.TitleBarRectangle[1] = self.Cursor_Position[1] - self.TitleBarRectangle[3] / 2
        # -- Resize Window -- #
        if self.Window_IsBeingResized and self.Resiziable:
            if self.WindowRectangle[2] >= self.Window_MinimunW:
                self.WindowRectangle[2] = self.Cursor_Position[0] - self.WindowRectangle[0]

            if self.WindowRectangle[3] >= self.Window_MinimunH:
                self.WindowRectangle[3] = self.Cursor_Position[1] - self.WindowRectangle[1]

        if self.WindowRectangle[2] <= self.Window_MinimunW:
            self.WindowRectangle[2] = self.Window_MinimunW
        # -------------------------------------------------
        if self.WindowRectangle[3] <= self.Window_MinimunH:
            self.WindowRectangle[3] = self.Window_MinimunH



