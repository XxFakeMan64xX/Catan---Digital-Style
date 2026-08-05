from config import deepSea
import pygame

class Screen:
    def __init__(self, screenManager, screen):
        self.screenManager = screenManager
        self.screen = screen
        self.background = deepSea
    
    def OnEnter(self):
        # Common UI setup for all screens
        self.buttonWidth = self.screen.get_width() / 2.5
        self.buttonHeight = self.screen.get_height() / 10
        self.buttonColor = (255, 255, 255)
        self.fontSize = self.screen.get_height() / 20
    
    def OnExit(self):
        pass
    
    def Update(self, dt):
        pass
    
    def Draw(self):
        pass