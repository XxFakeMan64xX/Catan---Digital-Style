# Catan - Digital Style

A Python-based hexagonal grid visualization inspired by the board game Catan. Built with Pygame, this project renders a procedurally generated hex map with terrain types, number tokens, and interactive camera controls.

## Features

- **Procedural hex grid generation** using ring-based spiral algorithm
- **Random terrain assignment** with proper Catan resource distribution (sheep, ore, wheat, wood, brick, gold mine, desert)
- **Number token placement** with standard Catan dice roll distribution
- **Interactive camera controls**:
  - Pan with WASD or arrow keys
  - Zoom with mouse wheel (centered on cursor)
  - Drag to pan with mouse
  - Hold Shift for faster panning
- **Mouse hover highlighting** shows the hex under the cursor
- **Fullscreen toggle** with F11
- **Map regeneration** with R key
- **Pause system** with ESC (includes quit button)
- **View culling** for performance (only draws visible hexes)

## Requirements

- Python 3.x
- Pygame

## Installation

1. Clone the repository:
```bash
git clone https://github.com/XxFakeMan64xX/Catan---Digital-Style.git
cd Catan---Digital-Style
```

2. Install Pygame:
```bash
pip install pygame
```

3. Run the game:
```bash
python game.py
```

## Controls

| Key/Mouse | Action |
|-----------|--------|
| W / ↑ | Pan up |
| S / ↓ | Pan down |
| A / ← | Pan left |
| D / → | Pan right |
| Shift | Hold to pan faster |
| Mouse wheel | Zoom in/out |
| Left-click drag | Pan camera |
| R | Regenerate random map |
| F11 | Toggle fullscreen |
| Escape | Toggle pause / Quit from pause menu |

## Project Structure

- `game.py` - Main game loop and event handling
- `config.py` - Configuration constants (colors, zoom settings, hex geometry, UI settings)
- `hex_grid.py` - Hex grid generation algorithms (ring-based, terrain/number assignment)
- `coordinates.py` - Hex coordinate system conversions (pixel ↔ hex, rounding)
- `ui.py` - UI components (uiRect class for scalable UI elements, hex class for tile rendering)
- `assets/fonts/` - Font files for number tokens

## Technical Details

- **Coordinate system**: Uses doubled hex coordinates for grid logic, converts to axial for mouse interaction
- **Rendering**: Flat-topped hexagons with proper aspect ratio (3:2 width, √3/2 height)
- **Performance**: Implements view culling to avoid drawing off-screen hexes
- **Frame-rate independence**: Movement uses delta time for consistent speed across framerates

Disclaimer: Ive used AI to write the comments (and this readme), but all of the code comes from me :3