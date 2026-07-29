import pygame

pygame.init()

# --- Hex grid geometry ---
hexSize = 40                                   # radius/size of a single hex tile
defaultRings = 2                               # starting number of rings in the hex map
numberOfRings = defaultRings                   # current number of rings (mutable copy)
hexWidthRatio, hexHeightRatio = 3/2, 3**(1/2)/2  # width/height multipliers for hex layout math

# --- Camera / view controls ---
gameScale = 1.0                                # current zoom level
zoomFactor = 1.15                              # multiplier applied per zoom step
minZoom, maxZoom = 0.05, 15                    # zoom bounds
panSpeed = 450                                 # camera pan speed (units/sec)

# --- App / performance settings ---
fpsLimit = 60                                  # maximum frames per second

# --- UI colors ---
selectorColor, selectorAlpha = (255, 255, 255), 85  # tile selection highlight (color, transparency)
numberTileColor = (212, 205, 142)              # background color for number tokens

# --- Resource/tile colors ---
desert = (181, 174, 112)
sheep = (131, 187, 8)
ore = (141, 129, 182)
wheat = (251, 194, 51)
wood = (8, 100, 23)
brick = (255, 106, 42)
goldMine = (180, 144, 14)
sea = (17, 99, 176)
colorList = [sheep, ore, wheat, wood, brick, goldMine]  # resource tiles (excludes desert and sea)

# --- Number tokens / text ---
textSize = 20                                  # base font size for number tokens
numberList = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]  # standard Catan number token distribution
numberSize = pygame.font.Font('assets/fonts/MinionPro-BoldCn.otf', int(textSize * gameScale))  # font object, scaled to current zoom