# Improvement Recommendations

A survey of the current codebase (`game.py`) with suggested improvements,
grouped by priority. The intent is to make the project easier to extend
toward a full digital Catan experience without collapsing under its own
weight later.

## 1. Correctness & Bugs

- **Uninitialized `speed` on first frame.** `speed` is only defined inside
  the shift-key branch of the main loop. On frame 1, before any key is
  pressed, `speed` is referenced by the WASD movement block and will raise
  `NameError` if a movement key is held before shift is evaluated. Define
  `speed = 450` alongside the other module-level constants.
- **`hex_ring(center, 0)` returns `None`** instead of an empty list, which
  would break any caller that iterates. `hex_grid` avoids this by starting
  at `r=1`, but the function itself should return `[]` for consistency.
- **`newTiles` places `DESERT` only at `(0, 0)`.** Real Catan boards have
  exactly one desert regardless of position, and it can appear anywhere.
  Consider generating a shuffled bag of tile types with fixed counts
  (see section 4).
- **Zoom clamp missing.** `gameScale` can shrink to ~0 or explode; add
  `gameScale = max(0.2, min(gameScale, 5.0))` after each wheel event.

## 2. Code Style & Consistency

- **Naming.** Mix of `camelCase` (`gameSize`, `newTiles`, `tileList`) and
  `snake_case` (`hex_ring`, `hex_grid`). Pick one — PEP 8 recommends
  `snake_case` for functions and variables, `PascalCase` for classes.
- **Magic numbers.** `1.15` (zoom step), `40` (tile size), `450`/`900`
  (pan speeds), `1280x720` (window) should be named constants at the top.
- **Stale header comment.** Line 1 still says "Example file showing a
  circle moving on screen".
- **Global state everywhere.** `gamePos`, `gameScale`, `tileList`, etc.
  are module globals mutated inside the main loop. This will not scale;
  wrap them in a `Game` / `Camera` / `Board` object (see section 3).

## 3. Architecture

Break `game.py` into modules. A reasonable initial layout:

```
game.py            # entry point, main loop only
board.py           # Board, hex_ring, hex_grid, newTiles
tiles.py           # TileType and definitions
camera.py          # gamePos, gameScale, world<->screen transforms
input.py           # event handling (drag, zoom, keys)
render.py          # drawHexagon and future rendering helpers
constants.py       # window size, colors, tuning knobs
```

Suggested classes:

- **`Camera`** — owns `pos`, `scale`, and `world_to_screen()` /
  `screen_to_world()`. Removes the ad-hoc math inline in the zoom
  handler.
- **`Board`** — owns the tile list, exposes `tiles_in_ring(r)`,
  `neighbors(coord)`, `at(coord)`, and generation methods.
- **`Tile`** (distinct from `TileType`) — instance data per hex:
  coordinate, `TileType`, dice number, robber flag, harvest state.
  Currently tiles are `(coord, TileType)` tuples, which will become
  awkward once numbers/robber/settlements are added.
- **`Game`** — top-level object holding `Camera`, `Board`, players,
  current turn, etc.

## 4. Gameplay Features (Catan roadmap)

To move from "colored hex map" toward Catan proper:

- **Number tokens (2–12)** on non-desert tiles.
- **Dice rolls** and resource distribution to adjacent settlements.
- **Vertices & edges** data structures for settlements/cities/roads.
  A hex has 6 vertices and 6 edges; store them as canonical
  `(coord, corner_index)` / `(coord, edge_index)` keys so each is unique
  regardless of which hex references it.
- **Players** with hands, victory points, and colors.
- **Turn state machine**: roll → trade → build → end.
- **Robber** placement and 7-roll handling.
- **Standard board layout**: 19 tiles (1 desert, 4 wheat, 4 sheep,
  4 wood, 3 brick, 3 ore) with the canonical number-token ring order.
  Use a shuffled bag instead of independent random picks.

## 5. Rendering & UX

- **Tile borders** — draw a dark polygon outline so adjacent tiles are
  visually separable.
- **Number tokens** — render the pip number in the center of each tile
  (larger font + red for 6/8).
- **Anti-aliased polygons** via `pygame.draw.aalines` around each hex.
- **HUD** — current player, resources, dice result, in a fixed
  screen-space overlay unaffected by camera transforms.
- **Screen resize** — handle `pygame.VIDEORESIZE` and rebuild
  `screen` so the window is not locked to 1280x720.
- **Hover highlight** — light-up the tile under the mouse; useful for
  debugging and required for placement UI.

## 6. Performance

Not urgent at ring counts <10, but worth knowing:

- `drawHexagon` recomputes six points per tile per frame. Cache the
  base hex shape once and translate it per tile.
- Consider drawing into a `Surface` when the board is static and only
  re-blitting on camera changes.

## 7. Tooling & Project Hygiene

- **`requirements.txt`** pinning `pygame`.
- **`README.md`** currently minimal — document controls (WASD/arrows,
  shift, wheel, R to regenerate) and how to run.
- **`.gitignore`** for `__pycache__/`, `.venv/`, editor files.
- **Type hints** on public functions (`def hex_ring(center: tuple[int,int], radius: int) -> list[tuple[int,int]]:`).
- **Unit tests** for the pure-logic pieces (`hex_ring`, `hex_grid`,
  future `Board.neighbors`) using `pytest`. These do not require
  pygame and catch regressions cheaply.
- **Linter/formatter**: `ruff` or `black` + `ruff check`.

## 8. Small, High-Value First Steps

If picking a few items to do first, I would prioritize:

1. Fix the `speed` initialization bug.
2. Rename to consistent `snake_case`; extract constants.
3. Introduce a `Tile` instance class (coord + type + number + robber).
4. Extract `Camera` and move zoom/pan math into it.
5. Add `requirements.txt` and expand `README.md` with controls.

Everything above section 4 can be done without changing gameplay, and
sets up a clean base for the Catan rules implementation.
