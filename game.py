import pygame
from hex_grid import newTiles
from config import (
    numberOfRings, sea, hexSize, gameScale, hexWidthRatio, hexHeightRatio,
    selectorColor, selectorAlpha, panSpeed, fpsLimit, zoomFactor,
    maxZoom, minZoom, textSize, numberSize
)
from drawing import drawHexagon, drawNumberToken
from coordinates import hexRound, pixelToFractionalHex

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
pygame.init()

screenWidth, screenHeight = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# gamePos is the on-screen pixel position that corresponds to world (0, 0).
# Panning/zooming just moves this point and changes gameScale.
gamePos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# --- State flags ---
running = True
dragging = False
fullscreen = True
dt = 0            # seconds elapsed since last frame, used to make movement frame-rate independent
speed = panSpeed   # current pan speed (doubles when shift is held)

# Generate the initial hex map (a spiral/ring-based board of `numberOfRings` rings)
tileList = newTiles(numberOfRings)

# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
while running:

    # -----------------------------------------------------------------
    # Event handling (things that happen once, not continuous key holds)
    # -----------------------------------------------------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEWHEEL:
            # Zoom in/out, keeping the point under the mouse cursor fixed in place.
            mousePos = pygame.Vector2(pygame.mouse.get_pos())

            # Where in "world space" the mouse currently points, before the zoom changes.
            worldPos = (mousePos - gamePos) / gameScale

            if event.y > 0:
                gameScale *= zoomFactor
                if gameScale > maxZoom:
                    gameScale = maxZoom
            else:
                gameScale /= zoomFactor
                if gameScale < minZoom:
                    gameScale = minZoom

            # Re-anchor gamePos so the same world point stays under the mouse after zooming.
            gamePos = mousePos - worldPos * gameScale

            # Number tokens are drawn from a font, so their size must be regenerated
            # whenever zoom level changes.
            numberSize = pygame.font.Font('assets/fonts/MinionPro-BoldCn.otf', int(textSize * gameScale))

        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = event.pos
                gamePos.x = mouse_x + offset_x
                gamePos.y = mouse_y + offset_y

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Start a drag: remember the offset between the mouse and gamePos
                # so we can keep that offset constant while dragging.
                mouse_x, mouse_y = event.pos
                dragging = True
                offset_x = gamePos.x - mouse_x
                offset_y = gamePos.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Regenerate a fresh random map
                tileList = newTiles(numberOfRings)

            if event.key == pygame.K_F11:
                # Toggle fullscreen <-> windowed
                if fullscreen:
                    screen = pygame.display.set_mode((1280, 720))
                    fullscreen = False
                else:
                    screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN)
                    fullscreen = True

    # -----------------------------------------------------------------
    # Drawing
    # -----------------------------------------------------------------
    screen.fill(sea)

    gameWidth, gameHeight = screen.get_size()
    shapeSize = hexSize * gameScale
    buffer = shapeSize  # extra margin so hexes just off-screen still get drawn (avoids pop-in)

    # Visible world-space bounds, used to cull hexes that are off-screen.
    min_x = -gamePos.x - buffer
    max_x = -gamePos.x + gameWidth + buffer
    min_y = -gamePos.y - buffer
    max_y = -gamePos.y + gameHeight + buffer

    for coord, terrain, number in tileList:
        hex_x = coord[0] * shapeSize * hexWidthRatio
        hex_y = coord[1] * shapeSize * hexHeightRatio

        # Only draw hexes that are within (or near) the visible screen area.
        if min_x <= hex_x <= max_x and min_y <= hex_y <= max_y:
            drawHexagon(screen, gamePos, gameScale, coord, terrain)
            if number is not None:
                drawNumberToken(screen, gamePos, gameScale, numberSize, coord, number)

    # Highlight the hex currently under the mouse cursor.
    hoveredHex = hexRound(pixelToFractionalHex(gamePos, pygame.mouse.get_pos(), hexSize * gameScale))
    drawHexagon(screen, gamePos, gameScale, hoveredHex, selectorColor, selectorAlpha)

    # -----------------------------------------------------------------
    # Continuous input (keys held down every frame)
    # -----------------------------------------------------------------
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        running = False

    # Hold shift to pan faster. Must be computed *before* using `speed` below.
    if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
        speed = panSpeed * 2
    else:
        speed = panSpeed

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        gamePos.y += speed * dt
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        gamePos.y -= speed * dt
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        gamePos.x += speed * dt
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        gamePos.x -= speed * dt

    # -----------------------------------------------------------------
    # Frame finalization
    # -----------------------------------------------------------------
    pygame.display.flip()
    dt = clock.tick(fpsLimit) / 1000  # convert ms -> seconds for frame-independent movement

pygame.quit()