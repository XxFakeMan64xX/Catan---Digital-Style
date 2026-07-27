# Example file showing a circle moving on screen
import pygame
import random as ran

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dragging = False
dt = 0
gameSize = 40
numberOfRings = -1

gamePos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
gameScale = 1.0

def newTiles(rings):

    # desert (219, 196, 138)
    # sheep (126, 237, 71)
    # ore (87, 71, 196)
    # wheat (247, 220, 10)
    # wood (4, 110, 24)
    # brick (168, 66, 22)
    # gold mine (212, 176, 56)
    # sea (42, 126, 235)

    colors = [(126, 237, 71), (87, 71, 196), (247, 220, 10), (4, 110, 24), (168, 66, 22), (212, 176, 56), (42, 126, 235)]
    
    tileList = []
    
    for tile in hex_grid((0, 0), rings):
        if tile != (0, 0):
            tileList.append((tile, ran.choice(colors)))
        else:
            tileList.append((tile, (219, 196, 138)))
    
    return tileList

def drawHexagon(coord, color):
    shapeSize = gameSize * gameScale
    x = coord[0] * shapeSize * 3/2
    y = coord[1] * shapeSize * 3**(1/2)/2
    pygame.draw.polygon(screen, color, [
        (shapeSize + x, 0 + y) + gamePos, 
        (0.5 * shapeSize + x, 3**(1/2)/2 * shapeSize + y) + gamePos, 
        (-0.5 * shapeSize + x, 3**(1/2)/2 * shapeSize + y) + gamePos, 
        (-1 * shapeSize + x, 0 + y) + gamePos, 
        (-0.5 * shapeSize + x, -3**(1/2)/2 * shapeSize + y) + gamePos, 
        (0.5 * shapeSize + x, -3**(1/2)/2 * shapeSize + y) + gamePos
    ])

def hex_ring(center, radius):
    # The 6 directions between adjacent hexes
    DIRECTIONS = [(1, 1), (1, -1), (0, -2), (-1, -1), (-1, 1), (0, 2)]
    #Return all tile coords in the ring at the given radius from center
    if radius == 0:
        return
    
    cx, cy = center
    # Start at the corner of the ring reached by going DIRECTIONS[0] * radius steps
    x = cx + DIRECTIONS[0][0] * radius
    y = cy + DIRECTIONS[0][1] * radius

    # Walk order starts two directions ahead of the start direction
    walk_dirs = DIRECTIONS[2:] + DIRECTIONS[:2]

    results = []
    for dx, dy in walk_dirs:
        for _ in range(radius):
            results.append((x, y))
            x += dx
            y += dy
    return results

def hex_grid(center, num_rings):
    """Return all tile coords from the center out to num_rings."""
    tiles = [center]
    for r in range(1, num_rings + 1):
        tiles.extend(hex_ring(center, r))
    return tiles

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
                gameScale *= 1.15
            else:
                # Zoom out
                gameScale /= 1.15
            
            gamePos = mousePos - worldPos * gameScale

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


    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill((42, 126, 235))


    for i in tileList:
        drawHexagon(i[0], i[1])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        gamePos.y += speed * dt
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        gamePos.y -= speed * dt
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        gamePos.x += speed * dt
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        gamePos.x -= speed * dt
    if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
        speed = 800
    else:
        speed = 400
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()