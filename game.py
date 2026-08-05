import pygame
from config import fpsLimit
from screens.mainMenu import MainMenu
from screens.GameScreen import GameScreen
# from screens.gameScreen import GameScreen  # when you create it

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
pygame.init()

screenWidth, screenHeight = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# ---------------------------------------------------------------------------
# Screen manager
# ---------------------------------------------------------------------------
class ScreenManager:
    def __init__(self):
        self.current_screen = None
    
    def switch_screen(self, screen_name):
        if screen_name == "main_menu":
            self.current_screen = MainMenu(self, screen)
            self.current_screen.OnEnter()
        elif screen_name == "continue":
            self.current_screen = GameScreen(self, screen)
            self.current_screen.OnEnter()
        elif screen_name == "quit":
            return False  # Signal to quit
        return True

screenManager = ScreenManager()
screenManager.switch_screen("main_menu")

# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
running = True
fullscreen = True
while running:
    dt = clock.tick(fpsLimit) / 1000
    
    # Update current screen and handle screen switching
    result = screenManager.current_screen.Update(dt)
    if result == "fullscreen":
        # Toggle fullscreen <-> windowed
        if fullscreen:
            screen = pygame.display.set_mode((1280, 720))
            fullscreen = False
        else:
            screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN)
            fullscreen = True
        screenManager.current_screen.OnEnter()
    elif result:
        running = screenManager.switch_screen(result)
    
    # Draw current screen
    screenManager.current_screen.Draw(screen)
    
    pygame.display.flip()

pygame.quit()