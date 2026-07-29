# Example file showing a circle moving on screen
import pygame
import random as ran

# pygame setup
pygame.init()
screenWidth, screenHeight = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN)
clock = pygame.time.Clock()

running = True
dragging = False
fullscreen = True
dt = 0
hexSize = 40
defaultRings = 2
numberOfRings = defaultRings
zoomFactor = 1.15
minZoom, maxZoom = 0.05, 15
gamePos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
gameScale = 1.0
panSpeed = 450
hexWidthRatio, hexHeightRatio = 3/2, 3**(1/2)/2
fpsLimit = 60

selectorColor, selectorAlpha = (255, 255, 255), 85
numberTileColor = (212, 205, 142)
desert = (181, 174, 112)
sheep = (131,187,8)
ore = (141,129,182)
wheat = (251, 194, 51)
wood = (8, 100, 23)
brick = (255, 106, 42)
goldMine = (180, 144, 14)
sea = (17, 99, 176)
colorList = [sheep, ore, wheat, wood, brick, goldMine]

textSize = 20
numberList = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
numberSize = pygame.font.Font('assets/fonts/MinionPro-BoldCn.otf', int(textSize*gameScale))


def newTiles(rings):
    
    tileList = []
    
    for tile in hexGrid((0, 0), rings):
        if tile != (0, 0):
            tileList.append((tile, ran.choice(colorList), ran.choice(numberList)))
        else:
            tileList.append((tile, desert, None))
    
    return tileList

def drawHexagon(coord, color, alpha=None):
    shapeSize = hexSize * gameScale
    alphaSurfaceSize = shapeSize * 2
    x = coord[0] * shapeSize * hexWidthRatio
    y = shapeSize * hexHeightRatio * coord[1]
    
    if alpha is None:
        pygame.draw.polygon(screen, color, [
            (shapeSize + x, 0 + y) + gamePos, 
            (0.5 * shapeSize + x, hexHeightRatio * shapeSize + y) + gamePos, 
            (-0.5 * shapeSize + x, hexHeightRatio * shapeSize + y) + gamePos, 
            (-1 * shapeSize + x, 0 + y) + gamePos, 
            (-0.5 * shapeSize + x, -hexHeightRatio * shapeSize + y) + gamePos, 
            (0.5 * shapeSize + x, -hexHeightRatio * shapeSize + y) + gamePos
        ])
    else:
        alphaSurface = pygame.Surface((alphaSurfaceSize, alphaSurfaceSize), pygame.SRCALPHA)
        pygame.draw.polygon(alphaSurface, color + (alpha,), [
            (alphaSurfaceSize, alphaSurfaceSize/2), 
            (hexWidthRatio * shapeSize, hexHeightRatio * shapeSize + alphaSurfaceSize/2), 
            (0.5 * shapeSize, hexHeightRatio * shapeSize + alphaSurfaceSize/2), 
            (0, alphaSurfaceSize/2), 
            (0.5 * shapeSize, -hexHeightRatio * shapeSize + shapeSize), 
            (hexWidthRatio * shapeSize, -hexHeightRatio * shapeSize + shapeSize)
        ])
        screen.blit(alphaSurface, (gamePos.x + x - shapeSize, gamePos.y + y - shapeSize))

def drawNumberToken(coord, number):
    shapeSize = hexSize * gameScale
    x = coord[0] * shapeSize * hexWidthRatio
    y = shapeSize * hexHeightRatio * coord[1]
    pygame.draw.circle(screen, numberTileColor, (gamePos.x + x, gamePos.y + y), shapeSize/3)

    if number in [6, 8]:
        tokenNumber = numberSize.render(str(number), True, "red")
    elif 2 <= number <= 12 and number != 7:
        tokenNumber = numberSize.render(str(number), True, "black")
    else:
        tokenNumber = numberSize.render(str(number), True, "blue")
    numberRect = tokenNumber.get_rect(center=(gamePos.x + x, gamePos.y + y))
    screen.blit(tokenNumber, numberRect)

def hexGrid(center, numRings):
    """Return all tile coords from the center out to numRings."""
    tiles = [center]
    for r in range(1, numRings + 1):
        tiles.extend(hexRing(center, r))
    return tiles

def hexRing(center, radius):
    # The 6 directions between adjacent hexes
    HEX_DIRECTIONS = [(1, 1), (1, -1), (0, -2), (-1, -1), (-1, 1), (0, 2)]
    #Return all tile coords in the ring at the given radius from center
    if radius == 0:
        return []
    
    cx, cy = center
    # Start at the corner of the ring reached by going DIRECTIONS[0] * radius steps
    x = cx + HEX_DIRECTIONS[0][0] * radius
    y = cy + HEX_DIRECTIONS[0][1] * radius

    # Walk order starts two directions ahead of the start direction
    walkDirs = HEX_DIRECTIONS[2:] + HEX_DIRECTIONS[:2]

    results = []
    for dx, dy in walkDirs:
        for _ in range(radius):
            results.append((x, y))
            x += dx
            y += dy
    return results


def pixelToFractionalHex(coord, size):
    x, y = coord[0] - gamePos[0], coord[1] - gamePos[1]
    q = (2/3 * x) / size
    r = (-1/3 * x + (3)**(1/2)/3 * y) / size
    return (q, r)

def hexRound(coords):
    fracQ, fracR = coords
    # Calculate 3D cube coordinates
    fracS = -fracQ - fracR

    # Round each coordinate to the nearest integer
    q = round(fracQ)
    r = round(fracR)
    s = round(fracS)

    # Measure the difference between float and rounded integer
    q_diff = abs(q - fracQ)
    r_diff = abs(r - fracR)
    s_diff = abs(s - fracS)

    # Reset the coordinate with the largest difference to satisfy q + r + s = 0
    if (q_diff > r_diff and q_diff > s_diff):
        q = -r - s
    elif (r_diff > s_diff):
        r = -q - s
    else:
        s = -q - r

    return q, 2 * r + q

tileList = newTiles(numberOfRings)
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEWHEEL:
            mousePos = pygame.Vector2(pygame.mouse.get_pos())

            worldPos = (mousePos - gamePos) / gameScale
            
            if event.y > 0:
                # Zoom in
                gameScale *= zoomFactor
                if gameScale > maxZoom:
                    gameScale = maxZoom
            else:
                # Zoom out
                gameScale /= zoomFactor
                if gameScale < minZoom:
                    gameScale = minZoom
            
            gamePos = mousePos - worldPos * gameScale

            numberSize = pygame.font.Font('assets/fonts/MinionPro-BoldCn.otf', int(textSize*gameScale))

        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = event.pos
                gamePos.x = mouse_x + offset_x
                gamePos.y = mouse_y + offset_y

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                dragging = True
                offset_x = gamePos.x - mouse_x
                offset_y = gamePos.y - mouse_y
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                tileList = newTiles(numberOfRings)
            if event.key == pygame.K_F11:
                if fullscreen:
                    screen = pygame.display.set_mode((1280, 720))
                    fullscreen = False
                else:
                    screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN)
                    fullscreen = True


    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill(sea)

    # Calculate screen bounds in world coordinates
    gameWidth, gameHeight = screen.get_size()
    shapeSize = hexSize * gameScale
    buffer = shapeSize  # Extra margin to prevent popping
    
    # Convert screen corners to world coordinates
    min_x = -gamePos.x - buffer
    max_x = -gamePos.x + gameWidth + buffer
    min_y = -gamePos.y - buffer  
    max_y = -gamePos.y + gameHeight + buffer

    for i in tileList:
        coord = i[0]
        # Calculate hex position in world coordinates
        hex_x = coord[0] * shapeSize * hexWidthRatio
        hex_y = coord[1] * shapeSize * hexHeightRatio
        
        # Check if hex is within screen bounds
        if (min_x <= hex_x <= max_x and min_y <= hex_y <= max_y):
            drawHexagon(i[0], i[1])
            if i[2] is not None:
                drawNumberToken(i[0], i[2])
    
    hex = hexRound(pixelToFractionalHex(pygame.mouse.get_pos(), hexSize * gameScale))
    drawHexagon(hex, selectorColor, selectorAlpha)

    #text_surface = my_font.render('CATAN 0123456789', True, (255, 255, 255))
    #screen.blit(text_surface, (50, 50))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        gamePos.y += speed * dt
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        gamePos.y -= speed * dt
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        gamePos.x += speed * dt
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        gamePos.x -= speed * dt
    if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
        speed = panSpeed * 2
    else:
        speed = panSpeed
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to the limit (default 60)
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(fpsLimit) / 1000

pygame.quit()