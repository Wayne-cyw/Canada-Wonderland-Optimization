# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A terminal-based optimizer for visiting Canada's Wonderland. Given a set of rides the user wants to visit and a time window, it finds the optimal route using A* search accounting for walk times between rides.

## Running

```bash
# Activate venv first
source .venv/bin/activate

# Run the program (must be run from a full-screen terminal — curses UI requires sufficient terminal dimensions)
python main.py
```

**Important:** The curses UI will raise an error if the terminal window is too small. Always run in a full-screen or maximized terminal.

## Dependencies

Only one external dependency:
```bash
pip install pick
```

## Architecture

The program flows linearly through `main.py`:
1. Load `rides.json` → list of zone lists
2. Show curses splash screen (`ascii_art`)
3. User selects rides via multi-column curses UI (`select_rides_2`)
4. User picks start/end time via `pick` menus (`ask_budget`)
5. A* search finds the optimal route (`astar.astar`)
6. Print the result

### Key files

**`main.py`** — Entry point. Wires together interface and algorithm. Calls `astar.astar(selected_rides, (start_time, end_time, budget_time))`.

**`interface.py`** — All terminal UI. Two libraries are used:
- `curses` for the ride selector (`select_rides_2`) and splash screen (`ascii_art`)
- `pick` for the time picker (`ask_budget`)

`ask_budget()` returns a tuple `(start_time, end_time, budget_time)` where all values are **minutes from midnight** (e.g. `10:00` → `600`).

**`rides.json`** — List of 8 zone lists. Each inner list: `[zone_name, ride1, ride2, ...]`. Zones in order: Grande World Expo, Action Zone, Alpenfest, Frontier Canada, Planet Snoopy, Kidzville, Medieval Faire, Splash Works.

**`travel_time.json`** — Adjacency map of walking times in minutes between every ride and the `"Entrance"`. Used by A* as the edge weights for the ride graph.

**`astar.py`** — A* search implementation (not yet implemented). Expected signature: `astar(selected_rides: list, time_budget: tuple) -> list`.

### `select_rides_2` layout

Columns wrap into rows of at most 4. `COL_WIDTH` is computed dynamically from terminal width divided by 4. Each band's vertical offset (`y_starts`) is precomputed based on the tallest column in the previous band.
