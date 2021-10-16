from run import bfs_solver, gbs_solver
import re
import os
import csv

if __name__ == "__main__":
    ## Configuration
    max_time_bfs = 900 # Maximum time for each BFS test case
    max_time_gbs = 600 # Maximum time for each GBS test case
    map_start = 0
    map_end = 1
    filename_bfs = os.path.join("stat", "all_bfs.csv")
    filename_aStar = os.path.join("stat", "all_gbs.csv")
    header = ("Map", "Time", "Solution Length", "Generated States", "Traversed States", "Solution")
    # Pattern to extract information from log
    pattern = re.compile("Time: (.*) seconds\nSolution Length: (.*)\nGenerated States: (.*)\nTraversed States: (.*)\nSolution: (.*)")
    ## End configuration

    if map_start > map_end or map_start < 0:
        print("Configuration error")
        exit()

    # Get list of map names
    choices_map = [os.path.splitext(file)[0] for file in os.listdir('map') if os.path.isfile(os.path.join("map", file))]
    if map_start > len(choices_map) - 1:
        print("Configuration error")
        exit()
    if map_end > len(choices_map) - 1: # Adjust map_end if needed
        map_end = len(choices_map) - 1

    f_bfs = open(filename_bfs, "w", encoding="UTF8", newline="")
    f_gbs = open(filename_gbs, "w", encoding="UTF8", newline="")
    writer_bfs = csv.writer(f_bfs)
    writer_gbs = csv.writer(f_gbs)

    # Write header
    writer_bfs.writerow(header)
    writer_gbs.writerow(header)

    for map_id in range(map_start, map_end + 1):
        _, log = bfs_solver(os.path.join("map", choices_map[map_id] + ".txt"), max_time_bfs)
        writer_bfs.writerow([choices_map[map_id], *pattern.findall(log)[0]])
        _, log = gbs_solver(os.path.join("map", choices_map[map_id] + ".txt"), max_time_gbs)
        writer_gbs.writerow([choices_map[map_id], *pattern.findall(log)[0]])
    
    f_bfs.close()
    f_gbs.close()