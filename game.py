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

gamePos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
gameScale = 1.0

def newTiles():

    colors = [(126, 237, 71), (81, 120, 207), (247, 220, 10), (4, 110, 24), (168, 66, 22), (212, 176, 56)]

    list = [
    (0,0, (219, 196, 138)), 
    (1, 1, ran.choice(colors)), 
    (1, -1, ran.choice(colors)),
    (0, -2, ran.choice(colors)),
    (-1, -1, ran.choice(colors)), 
    (-1, 1, ran.choice(colors)), 
    (0, 2, ran.choice(colors)), 
    (2, 2, ran.choice(colors)),
    (2, 0, ran.choice(colors)),
    (2, -2, ran.choice(colors)),
    (1, -3, ran.choice(colors)),
    (0, -4, ran.choice(colors)),
    (-1, -3, ran.choice(colors)),
    (-2, -2, ran.choice(colors)),
    (-2, 0, ran.choice(colors)),
    (-2, 2, ran.choice(colors)),
    (-1, 3, ran.choice(colors)),
    (0, 4, ran.choice(colors)),
    (1, 3, ran.choice(colors))
]
    return list

def drawHexagon(x, y, color):
    shapeSize = gameSize * gameScale
    x = x * shapeSize * 3/2
    y = y * shapeSize * 3**(1/2)/2
    pygame.draw.polygon(screen, color, [
        (shapeSize + x, 0 + y) + gamePos, 
        (0.5 * shapeSize + x, 3**(1/2)/2 * shapeSize + y) + gamePos, 
        (-0.5 * shapeSize + x, 3**(1/2)/2 * shapeSize + y) + gamePos, 
        (-1 * shapeSize + x, 0 + y) + gamePos, 
        (-0.5 * shapeSize + x, -3**(1/2)/2 * shapeSize + y) + gamePos, 
        (0.5 * shapeSize + x, -3**(1/2)/2 * shapeSize + y) + gamePos
    ])


tileList = newTiles()
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

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            dragging = True
            offset_x = gamePos.x - mouse_x
            offset_y = gamePos.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = event.pos
                gamePos.x = mouse_x + offset_x
                gamePos.y = mouse_y + offset_y
    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill((20, 190, 224))


    for i in tileList:
        drawHexagon(i[0], i[1], i[2])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
            gamePos.y += 1200 * dt
        else:
            gamePos.y += 600 * dt
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
            gamePos.y -= 1200 * dt
        else:
            gamePos.y -= 600 * dt
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
            gamePos.x += 1200 * dt
        else:
            gamePos.x += 600 * dt
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
            gamePos.x -= 1200 * dt
        else:
            gamePos.x -= 600 * dt
    if keys[pygame.K_r]:
        tileList = newTiles()
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()