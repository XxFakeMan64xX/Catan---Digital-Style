# Main UI Layout

## Top Bar

- Player turn indicator (whose turn it is)
- Dice roll display (showing last roll)
- Game round/turn counter
- Menu button (settings, quit, stats)

## Bottom Panel (collapsible)

- Resource cards display (wood, brick, sheep, wheat, ore, gold)
- Building costs reference
- Current player's victory points

## Side Panel (right or left, toggleable)

- Player stats (VPs, resources, longest road, largest army)
- Development cards held
- Trade interface
- Build menu (roads, settlements, cities)

# Contextual UI Elements

## Hover Over Hex

- Show terrain type and number
- If has building: show owner and building type

## Hover Over Edge

- Show if road can be built there
- Show cost and owner if already built

## Hover Over Vertex

- Show if settlement/city can be built
- Show owner and building type if occupied

## Robber UI

- When robber is moved: highlight valid hexes
- Show player selection for stealing

# Controls

## Build Mode

- Click to select building type (road/settlement/city)
- Highlight valid placement locations in green
- Invalid locations in red
- Show resource cost overlay

## Trade Interface

- Resource selection (click to add to trade)
- Player selection (who to trade with)
- Bank trade rates (4:1 default, 3:1 with ports, 2:1 with specific ports)

## Development Cards

- Click to reveal/play card
- Show card type (Knight, Monopoly, Road Building, Year of Plenty, Victory Point)

# Visual Style

- Semi-transparent overlays so hex grid remains visible
- Color-coded by player (red, blue, white, orange)
- Clean, minimal design matching your current aesthetic
- Resource icons matching terrain colors
- Animated dice roll
- Victory point progress bars

# Recommended Structure

## New file: ui.py

UI element classes (Button, Panel, Overlay)
UI state management (current panel visibility, hover states)
UI rendering functions
UI event handling (clicks, hovers)

## Modify: game.py

Import and initialize UI system
Pass UI events to UI handler
Call UI render after hex grid rendering

## Modify: config.py

Add UI-specific constants (colors, sizes, positions)

## Starting Approach

Start simple - Create a basic UI class that can draw rectangles and text
Add one element at a time - Start with a simple resource counter or turn indicator
Build incrementally - Don't try to implement everything at once

## First Step

I'd suggest starting with a simple top bar showing:

Current player turn
Basic resource count