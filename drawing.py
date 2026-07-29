import pygame
from config import hexSize, hexWidthRatio, hexHeightRatio, numberTileColor

def drawHexagon(screen, gamePos, gameScale, coord, color, alpha=None):
    """
    Draw a single flat-topped/pointy-topped hexagon tile onto the
    given screen at a given hex-grid coordinate, either fully opaque
    or with a specified transparency.

    Relies on the following names being defined elsewhere in scope:
        pygame (module): The pygame library, used for drawing and
            surface creation.
        hexSize (float): Base size of a hexagon before scaling.
        hexWidthRatio (float): Ratio used to convert hex-grid x
            coordinates into pixel offsets (horizontal spacing between
            hex centers).
        hexHeightRatio (float): Ratio used to convert hex-grid y
            coordinates into pixel offsets, and to position the
            slanted top/bottom vertices of the hexagon.

    Args:
        screen (pygame.Surface): The display surface to draw the
            opaque hexagon onto.
        gamePos (pygame.Vector2 or similar): Pixel offset of the
            game board's origin on screen, added to every vertex so
            the whole board can be panned.
        gameScale (float): Global scale factor applied to hex size.
        coord (tuple[float, float]): The (x, y) hex-grid coordinate of
            the tile to draw (in the same doubled-coordinate style
            used elsewhere, i.e. not raw pixel coordinates).
        color (tuple[int, int, int]): RGB color to fill the hexagon
            with.
        alpha (int, optional): Opacity value (0-255) for the hexagon.
            If None (default), the hexagon is drawn fully opaque
            directly onto `screen`. If provided, the hexagon is drawn
            onto a temporary per-pixel-alpha surface and blitted onto
            `screen`, allowing transparency.

    Returns:
        None. Draws directly onto `screen` as a side effect.
    """
    # Compute the on-screen size of a hex tile after applying global
    # scaling, and the size of the temporary surface used for
    # transparent drawing (generously oversized to fit the hexagon).
    shapeSize = hexSize * gameScale
    alphaSurfaceSize = shapeSize * 2

    # Convert the hex-grid coordinate into a pixel offset from the
    # board's origin.
    x = coord[0] * shapeSize * hexWidthRatio
    y = shapeSize * hexHeightRatio * coord[1]

    if alpha is None:
        # Opaque path: draw the hexagon's 6 vertices directly onto the
        # given screen, offset by both the tile's position (x, y) and
        # the board's overall pan offset (gamePos). Vertices go
        # clockwise starting from the rightmost point.
        pygame.draw.polygon(screen, color, [
            (shapeSize + x, 0 + y) + gamePos, 
            (0.5 * shapeSize + x, hexHeightRatio * shapeSize + y) + gamePos, 
            (-0.5 * shapeSize + x, hexHeightRatio * shapeSize + y) + gamePos, 
            (-1 * shapeSize + x, 0 + y) + gamePos, 
            (-0.5 * shapeSize + x, -hexHeightRatio * shapeSize + y) + gamePos, 
            (0.5 * shapeSize + x, -hexHeightRatio * shapeSize + y) + gamePos
        ])
    else:
        # Transparent path: draw onto a separate per-pixel-alpha
        # surface first (since pygame.draw doesn't support alpha
        # blending directly onto the main screen), then blit that
        # surface onto the given screen at the correct position.
        alphaSurface = pygame.Surface((alphaSurfaceSize, alphaSurfaceSize), pygame.SRCALPHA)

        # Vertices here are expressed relative to the small alpha
        # surface itself (not the main screen/gamePos), roughly
        # centered within it.
        pygame.draw.polygon(alphaSurface, color + (alpha,), [
            (alphaSurfaceSize, alphaSurfaceSize/2), 
            (hexWidthRatio * shapeSize, hexHeightRatio * shapeSize + alphaSurfaceSize/2), 
            (0.5 * shapeSize, hexHeightRatio * shapeSize + alphaSurfaceSize/2), 
            (0, alphaSurfaceSize/2), 
            (0.5 * shapeSize, -hexHeightRatio * shapeSize + shapeSize), 
            (hexWidthRatio * shapeSize, -hexHeightRatio * shapeSize + shapeSize)
        ])

        # Blit the alpha surface onto the given screen, positioned so
        # the hexagon drawn on it lines up with (x, y) plus the
        # board's pan offset, accounting for the surface being
        # centered on the tile (hence the `- shapeSize` correction).
        screen.blit(alphaSurface, (gamePos.x + x - shapeSize, gamePos.y + y - shapeSize))
    
def drawNumberToken(screen, gamePos, gameScale, numberSize, coord, number):
    """
    Draw a circular number token (e.g. a resource-production number
    for a hex tile) onto the given screen at a given hex-grid
    coordinate, with the number's text color indicating its relative
    importance/probability.

    Relies on the following names being defined elsewhere in scope:
        pygame (module): The pygame library, used for drawing.
        hexSize (float): Base size of a hexagon before scaling.
        hexWidthRatio (float): Ratio used to convert hex-grid x
            coordinates into pixel offsets (horizontal spacing between
            hex centers).
        hexHeightRatio (float): Ratio used to convert hex-grid y
            coordinates into pixel offsets.
        numberTileColor (Color-like): Fill color for the circular
            token background.
        numberSize (pygame.font.Font): Font used to render the
            number's text.

    Args:
        screen (pygame.Surface): The display surface to draw the
            token onto.
        gamePos (pygame.Vector2 or similar): Pixel offset of the
            game board's origin on screen, added to the tile's
            position so the whole board can be panned.
        gameScale (float): Global scale factor applied to hex size.
        coord (tuple[float, float]): The (x, y) hex-grid coordinate of
            the tile the token belongs to (in the same doubled-
            coordinate style used elsewhere, i.e. not raw pixel
            coordinates).
        number (int): The number to display on the token (typically a
            dice-roll value, e.g. 2-12).

    Returns:
        None. Draws directly onto `screen` as a side effect.
    """
    # Compute the on-screen size of a hex tile after applying global
    # scaling, and convert the hex-grid coordinate into a pixel offset
    # from the board's origin.
    shapeSize = hexSize * gameScale
    x = coord[0] * shapeSize * hexWidthRatio
    y = shapeSize * hexHeightRatio * coord[1]

    # Draw the token's circular background, centered on the tile.
    pygame.draw.circle(screen, numberTileColor, (gamePos.x + x, gamePos.y + y), shapeSize/3)

    # Color the number text based on how "hot" the roll is: 6 and 8
    # are the most probable non-7 rolls on two dice, so they're
    # highlighted in red; other valid production numbers (2-12,
    # excluding 7, which triggers the robber rather than production)
    # are black; anything else (e.g. a placeholder/invalid value)
    # falls back to blue.
    if number in [6, 8]:
        tokenNumber = numberSize.render(str(number), True, "red")
    elif 2 <= number <= 12 and number != 7:
        tokenNumber = numberSize.render(str(number), True, "black")
    else:
        tokenNumber = numberSize.render(str(number), True, "blue")

    # Center the rendered text on the tile and draw it on top of the
    # circular background.
    numberRect = tokenNumber.get_rect(center=(gamePos.x + x, gamePos.y + y))
    screen.blit(tokenNumber, numberRect)