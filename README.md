# Sokoban Solver

Sokoban solver is an application for solving Sokoban game using Breadth-first search (BFS) and Greedy Best-first search (GBS) algorithm.

## Usage
Before running the application, make sure to create folder `log/` in the root directory.\
To run the application:
```
python run.py
```

## Statistics
Before running, make sure to create folder `stat/` in the root directory.\
Run:
```
python stat.py
```
Then input the start index and end index of the map interval to generate statistics. The index of a map is the position of the map's file in `map/` folder.

### Configuration
- `max_time_bfs` and `max_time_gbs`: Maximum time for each test case.
- `filename_bfs` and `filename_gbs`: File name (no extension) of statistics file.
- `header`: header of the columns.

## Input new map
Run:
```
python make_game.py
```
Then input the number of rows and columns of the map.\
This console application having 2 modes, pen up and pen down. To switch between the modes, press `space`.\
When in pen-up mode, you can use the arrow keys to move freely. When in pen-down mode, moving will make the 'color' spread. The 'color' of the pen is controlled by the number key from `0` to `6`:
- `0`: ground or nothing
- `1`: wall
- `2`: box
- `3`: goal
- `4`: box on goal
- `5`: player
- `6`: player on goal

After finishing inputting the map, press `Enter` to save the map and exit.

## Screenshot
![Sokoban solver screenshot](image/screenshot.png?raw=true)