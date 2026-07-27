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
numberOfRings = 2

gamePos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
gameScale = 1.0

class TileType:
    """
    Defines a type of hex tile on the board.

    Attributes:
        name:        Human-readable identifier (e.g. "wheat").
        color:       RGB tuple used when rendering the tile.
        harvestable: Whether players can collect resources from this tile.
        spawn_weight: Relative probability of appearing during random board
                     generation. 0 means the type is never spawned randomly
                     (e.g. desert/sea are placed manually).
    """

    # Registry of every TileType created, keyed by name. Makes it easy to
    # look up types by name and iterate over all of them.
    registry = {}

    def __init__(self, name, color, harvestable=True, spawn_weight=1.0):
        self.name = name
        self.color = color
        self.harvestable = harvestable
        self.spawn_weight = spawn_weight
        TileType.registry[name] = self

    def __repr__(self):
        return f"TileType({self.name!r})"

    @classmethod
    def spawnable(cls):
        """Return all tile types eligible for random placement."""
        return [t for t in cls.registry.values() if t.spawn_weight > 0]

    @classmethod
    def random(cls, rng=ran):
        """Pick a random spawnable tile type, weighted by spawn_weight."""
        pool = cls.spawnable()
        weights = [t.spawn_weight for t in pool]
        return rng.choices(pool, weights=weights, k=1)[0]


# Tile type definitions ------------------------------------------------------
DESERT = TileType("desert",    (219, 196, 138), harvestable=False, spawn_weight=0)
SEA    = TileType("sea",       (42, 126, 235),  harvestable=False, spawn_weight=0)
SHEEP  = TileType("sheep",     (126, 237, 71))
ORE    = TileType("ore",       (87, 71, 196))
WHEAT  = TileType("wheat",     (247, 220, 10))
WOOD   = TileType("wood",      (4, 110, 24))
BRICK  = TileType("brick",     (168, 66, 22))
GOLD   = TileType("gold_mine", (212, 176, 56),  spawn_weight=0.25)


def newTiles(rings):
    tileList = []
    for coord in hex_grid((0, 0), rings):
        tile_type = DESERT if coord == (0, 0) else TileType.random()
        tileList.append((coord, tile_type))
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


    for coord, tile in tileList:
        drawHexagon(coord, tile.color)

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
        speed = 900
    else:
        speed = 450
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()