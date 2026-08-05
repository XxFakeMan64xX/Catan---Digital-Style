from config import (
    numberOfRings, hexSize, gameScale, hexWidthRatio, hexHeightRatio,
    selectorColor, selectorAlpha, zoomFactor, maxZoom, minZoom, textSize,
    numberSize, pauseAlpha, panSpeed
)
from screens import Screen
from ui import uiRect, hex
from hex_grid import newTiles
from coordinates import hexRound, pixelToFractionalHex
import pygame

class GameScreen(Screen):
    def __init__(self, screenManager, screen): # Assets, fonts, static button positions, things that never change
        super().__init__(screenManager, screen)
        # Only setup things that don't depend on screen size here
        # Generate the initial hex map (a spiral/ring-based board of `numberOfRings` rings)
        self.tileList = newTiles(numberOfRings)

    def OnEnter(self): # Reset game state, start animations, recalculate responsive positions
        super().OnEnter()
        self.paused = False
        self.dragging = False
        self.gamePos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.mouse_down_pos = None
        self.offset_x = 0
        self.offset_y = 0
        self.gameScale = gameScale
        self.numberSize = numberSize
        # Recalculate buttons with current screen size
        self.continueButton = uiRect(self.screen.get_width()/2 - self.buttonWidth/2, self.screen.get_height()*3/8 - self.buttonHeight/2, self.buttonWidth, self.buttonHeight, self.buttonColor, "Continue Game", self.fontSize, (True, "center"), borderRadius=10)
        self.mainMenuButton = uiRect(self.screen.get_width()/2 - self.buttonWidth/2, self.screen.get_height()*4/8 - self.buttonHeight/2, self.buttonWidth, self.buttonHeight, self.buttonColor, "Main Menu", self.fontSize, (True, "center"), borderRadius=10)
        self.quitButton = uiRect(self.screen.get_width()/2 - self.buttonWidth/2, self.screen.get_height()*5/8 - self.buttonHeight/2, self.buttonWidth, self.buttonHeight, self.buttonColor, "Quit Game", self.fontSize, (True, "center"), borderRadius=10)

    def OnExit(self):
        pass # Likely nothing here

    def Update(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                elif event.key == pygame.K_F11:
                    return "fullscreen"

            # When the game is running (not paused)
            if not self.paused:
                if event.type == pygame.MOUSEWHEEL:
                    # Zoom in/out, keeping the point under the mouse cursor fixed in place.
                    mousePos = pygame.Vector2(pygame.mouse.get_pos())

                    # Where in "world space" the mouse currently points, before the zoom changes.
                    worldPos = (mousePos - self.gamePos) / self.gameScale

                    if event.y > 0:
                        self.gameScale *= zoomFactor
                        if self.gameScale > maxZoom:
                            self.gameScale = maxZoom
                    else:
                        self.gameScale /= zoomFactor
                        if self.gameScale < minZoom:
                            self.gameScale = minZoom

                    # Re-anchor gamePos so the same world point stays under the mouse after zooming.
                    self.gamePos = mousePos - worldPos * self.gameScale

                    # Number tokens are drawn from a font, so their size must be regenerated
                    # whenever zoom level changes.
                    self.numberSize = pygame.font.Font('assets/fonts/MinionPro-BoldCn.otf', round(textSize * self.gameScale))

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Start a drag: remember the offset between the mouse and gamePos
                        self.mouse_down_pos = event.pos
                        self.offset_x = self.gamePos.x - self.mouse_down_pos[0]
                        self.offset_y = self.gamePos.y - self.mouse_down_pos[1]
                        self.dragging = True
                        
                elif event.type == pygame.MOUSEMOTION:
                    if self.mouse_down_pos is not None and not self.dragging:
                        mouse_x, mouse_y = event.pos
                    if self.dragging:
                        mouse_x, mouse_y = event.pos
                        self.gamePos.x = mouse_x + self.offset_x
                        self.gamePos.y = mouse_y + self.offset_y

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.dragging = False
                        self.mouse_down_pos = None

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Regenerate a fresh random map
                        self.tileList = newTiles(numberOfRings)
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        mouse_pos = pygame.mouse.get_pos()
                        if self.continueButton.isClicked(mouse_pos):
                            self.paused = False
                        elif self.mainMenuButton.isClicked(mouse_pos):
                            return "main_menu"
                        elif self.quitButton.isClicked(mouse_pos):
                            return "quit"
        
        if not self.paused:
            keys = pygame.key.get_pressed()

            # Hold shift to pan faster.
            if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
                speed = panSpeed * 2
            else:
                speed = panSpeed

            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.gamePos.y += speed * dt
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.gamePos.y -= speed * dt
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.gamePos.x += speed * dt
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.gamePos.x -= speed * dt

    def Draw(self, screen):
        screen.fill(self.background)
        gameWidth, gameHeight = screen.get_size()
        shapeSize = hexSize * self.gameScale
        buffer = shapeSize  # extra margin so hexes just off-screen still get drawn (avoids pop-in)
        
        # Visible world-space bounds, used to cull hexes that are off-screen.
        min_x = -self.gamePos.x - buffer
        max_x = -self.gamePos.x + gameWidth + buffer
        min_y = -self.gamePos.y - buffer
        max_y = -self.gamePos.y + gameHeight + buffer

        for tile in self.tileList:
            tile_x = tile.x * shapeSize * hexWidthRatio
            tile_y = tile.y * shapeSize * hexHeightRatio

            # Only draw hexes that are within (or near) the visible screen area.
            if min_x <= tile_x <= max_x and min_y <= tile_y <= max_y:
                tile.draw(screen, self.gamePos, self.gameScale, self.numberSize)

        # uiBase = uiRect(0, screen.get_height()*5/6, screen.get_width(), screen.get_height()/6, (255, 255, 255), scalable=(True, "bottom"))
        # uiBase.draw(screen)
        if not self.paused:
            # Highlight the hex currently under the mouse cursor.
            hoveredHexCoords = hexRound(pixelToFractionalHex(self.gamePos, pygame.mouse.get_pos(), hexSize * self.gameScale))
            hoveredHex = hex(hoveredHexCoords[0], hoveredHexCoords[1], selectorColor)
            hoveredHex.draw(screen, self.gamePos, self.gameScale, alpha=selectorAlpha)
        else:
            # Draw pause overlay
            pauseRect = uiRect(0, 0, screen.get_width(), screen.get_height(), (0, 0, 0), scalable=(False, None), alpha=pauseAlpha)
            pauseRect.draw(screen)

            # Draw quit button and text
            self.continueButton.draw(screen)
            self.mainMenuButton.draw(screen)
            self.quitButton.draw(screen)