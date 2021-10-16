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